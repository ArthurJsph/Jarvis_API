"""
Sistema de pesquisa de documentação e cheatsheets
"""

import requests
from bs4 import BeautifulSoup
import json
import yaml
from typing import Dict, List, Optional
from pathlib import Path
import re
from urllib.parse import urljoin, quote

class DocumentationSearcher:
    """Pesquisador de documentação online"""
    
    def __init__(self, config_path: str = "jarvis.config.yml"):
        self.config = self._load_config(config_path)
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Jarvis CLI Documentation Searcher 2.1'
        })
        
        # Cache local
        self.cache_dir = Path("data/doc_cache")
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        
        # Cheatsheets embarcados
        self.embedded_cheatsheets = self._load_embedded_cheatsheets()
    
    def _load_config(self, config_path: str) -> Dict:
        """Carrega configuração"""
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            return self._get_default_config()
    
    def _get_default_config(self) -> Dict:
        """Configuração padrão"""
        return {
            'documentation': {
                'sources': [
                    {
                        'name': 'MDN',
                        'url': 'https://developer.mozilla.org',
                        'languages': ['html', 'css', 'javascript']
                    },
                    {
                        'name': 'Python Docs',
                        'url': 'https://docs.python.org',
                        'languages': ['python']
                    }
                ]
            }
        }
    
    def search_docs(self, query: str, language: str = None) -> Dict:
        """
        Pesquisa documentação
        
        Args:
            query: Termo de pesquisa
            language: Linguagem específica (opcional)
        
        Returns:
            Dict com resultados da pesquisa
        """
        try:
            # Determinar fontes baseadas na linguagem
            sources = self._get_sources_for_language(language)
            
            results = {
                'query': query,
                'language': language,
                'sources': []
            }
            
            for source in sources:
                source_results = self._search_source(query, source)
                if source_results:
                    results['sources'].append(source_results)
            
            # Se não encontrou nada específico, tentar busca geral
            if not results['sources']:
                general_results = self._search_general(query)
                if general_results:
                    results['sources'].append(general_results)
            
            return results
            
        except Exception as e:
            return {
                'error': str(e),
                'query': query,
                'language': language
            }
    
    def _get_sources_for_language(self, language: str) -> List[Dict]:
        """Retorna fontes de documentação para linguagem específica"""
        if not language:
            return self.config.get('documentation', {}).get('sources', [])
        
        relevant_sources = []
        for source in self.config.get('documentation', {}).get('sources', []):
            if language.lower() in [lang.lower() for lang in source.get('languages', [])]:
                relevant_sources.append(source)
        
        return relevant_sources
    
    def _search_source(self, query: str, source: Dict) -> Optional[Dict]:
        """Pesquisa em fonte específica"""
        try:
            source_name = source.get('name', 'Unknown')
            base_url = source.get('url', '')
            
            # Estratégias de busca específicas por fonte
            if 'developer.mozilla.org' in base_url:
                return self._search_mdn(query, source)
            elif 'docs.python.org' in base_url:
                return self._search_python_docs(query, source)
            elif 'react.dev' in base_url:
                return self._search_react_docs(query, source)
            else:
                return self._search_generic(query, source)
                
        except Exception as e:
            return {
                'source': source.get('name', 'Unknown'),
                'error': str(e)
            }
    
    def _search_mdn(self, query: str, source: Dict) -> Dict:
        """Pesquisa específica no MDN"""
        try:
            # URL de busca do MDN
            search_url = f"https://developer.mozilla.org/en-US/search?q={quote(query)}"
            
            response = self.session.get(search_url, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            results = []
            
            # Procurar resultados de busca
            search_results = soup.find_all('article', class_='result-item')
            
            for result in search_results[:5]:  # Primeiros 5 resultados
                title_elem = result.find('h3')
                desc_elem = result.find('p')
                link_elem = result.find('a')
                
                if title_elem and link_elem:
                    results.append({
                        'title': title_elem.get_text(strip=True),
                        'description': desc_elem.get_text(strip=True) if desc_elem else '',
                        'url': urljoin('https://developer.mozilla.org', link_elem.get('href', ''))
                    })
            
            return {
                'source': 'MDN Web Docs',
                'results': results,
                'search_url': search_url
            }
            
        except Exception as e:
            return {
                'source': 'MDN Web Docs',
                'error': f"Erro na busca: {str(e)}"
            }
    
    def _search_python_docs(self, query: str, source: Dict) -> Dict:
        """Pesquisa específica na documentação Python"""
        try:
            # Buscar na documentação Python
            search_url = f"https://docs.python.org/3/search.html?q={quote(query)}"
            
            # Para Python, também incluir busca por módulos comuns
            python_modules = {
                'os': 'https://docs.python.org/3/library/os.html',
                'sys': 'https://docs.python.org/3/library/sys.html',
                'json': 'https://docs.python.org/3/library/json.html',
                'requests': 'https://requests.readthedocs.io/',
                'pandas': 'https://pandas.pydata.org/docs/',
                'numpy': 'https://numpy.org/doc/',
                'datetime': 'https://docs.python.org/3/library/datetime.html',
                'pathlib': 'https://docs.python.org/3/library/pathlib.html'
            }
            
            results = []
            
            # Se a query corresponde a um módulo conhecido
            for module, url in python_modules.items():
                if module.lower() in query.lower():
                    results.append({
                        'title': f'Módulo {module}',
                        'description': f'Documentação oficial do módulo {module}',
                        'url': url
                    })
            
            # Adicionar link de busca geral
            results.append({
                'title': f'Buscar "{query}" na documentação Python',
                'description': 'Busca geral na documentação oficial',
                'url': search_url
            })
            
            return {
                'source': 'Python Documentation',
                'results': results,
                'search_url': search_url
            }
            
        except Exception as e:
            return {
                'source': 'Python Documentation',
                'error': f"Erro na busca: {str(e)}"
            }
    
    def _search_react_docs(self, query: str, source: Dict) -> Dict:
        """Pesquisa específica na documentação React"""
        try:
            # Conceitos comuns do React
            react_concepts = {
                'hook': 'https://react.dev/reference/react',
                'usestate': 'https://react.dev/reference/react/useState',
                'useeffect': 'https://react.dev/reference/react/useEffect',
                'component': 'https://react.dev/learn/your-first-component',
                'props': 'https://react.dev/learn/passing-props-to-a-component',
                'jsx': 'https://react.dev/learn/writing-markup-with-jsx',
                'router': 'https://reactrouter.com/docs'
            }
            
            results = []
            
            for concept, url in react_concepts.items():
                if concept.lower() in query.lower():
                    results.append({
                        'title': f'React {concept.title()}',
                        'description': f'Documentação sobre {concept} no React',
                        'url': url
                    })
            
            # Busca geral no React
            search_url = f"https://react.dev/?q={quote(query)}"
            results.append({
                'title': f'Buscar "{query}" na documentação React',
                'description': 'Busca na documentação oficial do React',
                'url': search_url
            })
            
            return {
                'source': 'React Documentation',
                'results': results,
                'search_url': search_url
            }
            
        except Exception as e:
            return {
                'source': 'React Documentation',
                'error': f"Erro na busca: {str(e)}"
            }
    
    def _search_generic(self, query: str, source: Dict) -> Dict:
        """Busca genérica em qualquer fonte"""
        try:
            base_url = source.get('url', '')
            search_url = f"{base_url}/search?q={quote(query)}"
            
            return {
                'source': source.get('name', 'Unknown'),
                'results': [{
                    'title': f'Buscar "{query}"',
                    'description': f'Busca em {source.get("name", "fonte desconhecida")}',
                    'url': search_url
                }],
                'search_url': search_url
            }
            
        except Exception as e:
            return {
                'source': source.get('name', 'Unknown'),
                'error': f"Erro na busca: {str(e)}"
            }
    
    def _search_general(self, query: str) -> Dict:
        """Busca geral quando não há fonte específica"""
        return {
            'source': 'Busca Geral',
            'results': [
                {
                    'title': f'Pesquisar "{query}" no Google',
                    'description': 'Busca geral na web',
                    'url': f'https://www.google.com/search?q={quote(query + " documentation")}'
                },
                {
                    'title': f'Pesquisar "{query}" no Stack Overflow',
                    'description': 'Busca na comunidade de desenvolvedores',
                    'url': f'https://stackoverflow.com/search?q={quote(query)}'
                },
                {
                    'title': f'Pesquisar "{query}" no GitHub',
                    'description': 'Busca em repositórios de código',
                    'url': f'https://github.com/search?q={quote(query)}&type=repositories'
                }
            ]
        }
    
    def get_cheatsheet(self, tool: str) -> Dict:
        """
        Retorna cheatsheet para ferramenta específica
        
        Args:
            tool: Nome da ferramenta (git, docker, regex, etc.)
        
        Returns:
            Dict com cheatsheet
        """
        try:
            tool = tool.lower()
            
            # Verificar se temos cheatsheet embarcado
            if tool in self.embedded_cheatsheets:
                return {
                    'tool': tool,
                    'type': 'embedded',
                    'content': self.embedded_cheatsheets[tool]
                }
            
            # URLs de cheatsheets externos
            cheatsheet_urls = {
                'git': 'https://education.github.com/git-cheat-sheet-education.pdf',
                'docker': 'https://dockerlabs.collabnix.com/docker/cheatsheet/',
                'regex': 'https://regexr.com/',
                'bash': 'https://devhints.io/bash',
                'vim': 'https://vim.rtorr.com/',
                'linux': 'https://www.linuxtrainingacademy.com/linux-commands-cheat-sheet/',
                'python': 'https://www.pythoncheatsheet.org/',
                'javascript': 'https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference',
                'css': 'https://developer.mozilla.org/en-US/docs/Web/CSS/Reference',
                'html': 'https://developer.mozilla.org/en-US/docs/Web/HTML/Element'
            }
            
            if tool in cheatsheet_urls:
                return {
                    'tool': tool,
                    'type': 'external',
                    'url': cheatsheet_urls[tool],
                    'description': f'Cheatsheet externo para {tool}'
                }
            
            return {
                'tool': tool,
                'error': f'Cheatsheet para {tool} não encontrado',
                'available': list(cheatsheet_urls.keys()) + list(self.embedded_cheatsheets.keys())
            }
            
        except Exception as e:
            return {
                'tool': tool,
                'error': str(e)
            }
    
    def _load_embedded_cheatsheets(self) -> Dict:
        """Carrega cheatsheets embarcados"""
        return {
            'git': {
                'Comandos Básicos': [
                    'git init - Inicializa repositório',
                    'git clone <url> - Clona repositório',
                    'git status - Mostra status',
                    'git add <arquivo> - Adiciona arquivo',
                    'git add . - Adiciona todos os arquivos',
                    'git commit -m "msg" - Faz commit',
                    'git push - Envia para remote',
                    'git pull - Baixa do remote'
                ],
                'Branches': [
                    'git branch - Lista branches',
                    'git branch <nome> - Cria branch',
                    'git checkout <branch> - Troca branch',
                    'git checkout -b <nome> - Cria e troca',
                    'git merge <branch> - Merge branch',
                    'git branch -d <nome> - Deleta branch'
                ],
                'Histórico': [
                    'git log - Mostra commits',
                    'git log --oneline - Log resumido',
                    'git diff - Mostra diferenças',
                    'git show <commit> - Mostra commit específico'
                ]
            },
            
            'python': {
                'Estruturas Básicas': [
                    '# Comentário',
                    'variable = value',
                    'if condition:',
                    'for item in lista:',
                    'while condition:',
                    'def function():',
                    'class MyClass:'
                ],
                'Tipos de Dados': [
                    'str = "texto"',
                    'int = 42',
                    'float = 3.14',
                    'bool = True/False',
                    'list = [1, 2, 3]',
                    'dict = {"key": "value"}',
                    'tuple = (1, 2, 3)',
                    'set = {1, 2, 3}'
                ],
                'Módulos Comuns': [
                    'import os',
                    'import sys',
                    'import json',
                    'import datetime',
                    'from pathlib import Path',
                    'import requests'
                ]
            },
            
            'javascript': {
                'Sintaxe Básica': [
                    '// Comentário',
                    'let variable = value;',
                    'const constant = value;',
                    'if (condition) {}',
                    'for (let i = 0; i < 10; i++) {}',
                    'function name() {}',
                    'const arrow = () => {}'
                ],
                'Arrays e Objetos': [
                    'const arr = [1, 2, 3];',
                    'const obj = {key: value};',
                    'arr.push(item);',
                    'arr.map(item => item * 2);',
                    'arr.filter(item => item > 5);',
                    'Object.keys(obj);',
                    'Object.values(obj);'
                ],
                'DOM': [
                    'document.getElementById("id");',
                    'document.querySelector(".class");',
                    'element.addEventListener("click", fn);',
                    'element.innerHTML = "html";',
                    'element.textContent = "text";'
                ]
            }
        }
    
    def list_available_cheatsheets(self) -> List[str]:
        """Lista cheatsheets disponíveis"""
        embedded = list(self.embedded_cheatsheets.keys())
        external = ['docker', 'regex', 'bash', 'vim', 'linux', 'css', 'html']
        return sorted(embedded + external)
    
    def format_search_results(self, results: Dict) -> str:
        """Formata resultados de busca para exibição"""
        if 'error' in results:
            return f"❌ Erro na busca: {results['error']}"
        
        lines = []
        lines.append(f"🔍 Resultados para: '{results['query']}'")
        
        if results.get('language'):
            lines.append(f"📝 Linguagem: {results['language']}")
        
        for source_result in results.get('sources', []):
            lines.append(f"\n📚 {source_result.get('source', 'Fonte desconhecida')}:")
            
            if 'error' in source_result:
                lines.append(f"   ❌ {source_result['error']}")
                continue
            
            for i, result in enumerate(source_result.get('results', []), 1):
                lines.append(f"   {i}. {result.get('title', 'Sem título')}")
                if result.get('description'):
                    lines.append(f"      {result['description']}")
                lines.append(f"      🔗 {result.get('url', 'Sem URL')}")
        
        if not results.get('sources'):
            lines.append("❌ Nenhum resultado encontrado")
            lines.append("💡 Tente termos mais específicos ou verifique a linguagem")
        
        return '\n'.join(lines)
    
    def format_cheatsheet(self, cheatsheet: Dict) -> str:
        """Formata cheatsheet para exibição"""
        if 'error' in cheatsheet:
            available = cheatsheet.get('available', [])
            lines = [
                f"❌ {cheatsheet['error']}",
                f"💡 Cheatsheets disponíveis: {', '.join(available)}"
            ]
            return '\n'.join(lines)
        
        tool = cheatsheet.get('tool', 'Unknown').title()
        
        if cheatsheet.get('type') == 'external':
            return f"""📋 {tool} Cheatsheet
🔗 {cheatsheet.get('url')}
💡 {cheatsheet.get('description', '')}"""
        
        # Cheatsheet embarcado
        lines = [f"📋 {tool} Cheatsheet\n"]
        
        content = cheatsheet.get('content', {})
        for section, items in content.items():
            lines.append(f"📌 {section}:")
            for item in items:
                lines.append(f"   • {item}")
            lines.append("")
        
        return '\n'.join(lines)
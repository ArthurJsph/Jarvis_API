"""
Sistema de gerenciamento e consulta de pacotes
"""

import requests
import json
import subprocess
import sys
from typing import Dict, List, Optional, Tuple
from pathlib import Path
import re

class PackageManager:
    """Gerenciador de pacotes para diferentes linguagens"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Jarvis CLI Package Manager 2.1'
        })
        
        # Registries e URLs
        self.registries = {
            'npm': 'https://registry.npmjs.org',
            'pypi': 'https://pypi.org/pypi',
            'github': 'https://api.github.com'
        }
    
    def search_package(self, package_name: str, registry: str = 'auto') -> Dict:
        """
        Busca informações sobre um pacote
        
        Args:
            package_name: Nome do pacote
            registry: Registry específico ou 'auto' para detectar
        
        Returns:
            Dict com informações do pacote
        """
        try:
            if registry == 'auto':
                registry = self._detect_registry()
            
            if registry == 'npm':
                return self._search_npm_package(package_name)
            elif registry == 'pypi':
                return self._search_pypi_package(package_name)
            else:
                return self._search_github_package(package_name)
                
        except Exception as e:
            return {
                'error': str(e),
                'package': package_name,
                'registry': registry
            }
    
    def _detect_registry(self) -> str:
        """Detecta o registry baseado no projeto atual"""
        current_dir = Path.cwd()
        
        # Verificar se é projeto Node.js
        if (current_dir / 'package.json').exists():
            return 'npm'
        
        # Verificar se é projeto Python
        if any((current_dir / file).exists() for file in ['requirements.txt', 'setup.py', 'pyproject.toml']):
            return 'pypi'
        
        # Default para npm se não detectar
        return 'npm'
    
    def _search_npm_package(self, package_name: str) -> Dict:
        """Busca pacote no NPM"""
        try:
            # Primeiro tentar buscar pacote específico
            url = f"{self.registries['npm']}/{package_name}"
            response = self.session.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                return self._format_npm_response(data)
            
            # Se não encontrar, fazer busca por texto
            search_url = f"https://api.npms.io/v2/search?q={package_name}&size=5"
            search_response = self.session.get(search_url, timeout=10)
            
            if search_response.status_code == 200:
                search_data = search_response.json()
                return self._format_npm_search_response(search_data, package_name)
            
            return {
                'error': f'Pacote {package_name} não encontrado no NPM',
                'package': package_name,
                'registry': 'npm'
            }
            
        except Exception as e:
            return {
                'error': f'Erro buscando no NPM: {str(e)}',
                'package': package_name,
                'registry': 'npm'
            }
    
    def _search_pypi_package(self, package_name: str) -> Dict:
        """Busca pacote no PyPI"""
        try:
            url = f"{self.registries['pypi']}/{package_name}/json"
            response = self.session.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                return self._format_pypi_response(data)
            
            return {
                'error': f'Pacote {package_name} não encontrado no PyPI',
                'package': package_name,
                'registry': 'pypi'
            }
            
        except Exception as e:
            return {
                'error': f'Erro buscando no PyPI: {str(e)}',
                'package': package_name,
                'registry': 'pypi'
            }
    
    def _search_github_package(self, package_name: str) -> Dict:
        """Busca pacote no GitHub"""
        try:
            # Buscar repositórios
            url = f"{self.registries['github']}/search/repositories"
            params = {
                'q': package_name,
                'sort': 'stars',
                'order': 'desc',
                'per_page': 5
            }
            
            response = self.session.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                return self._format_github_response(data, package_name)
            
            return {
                'error': f'Erro na busca do GitHub: {response.status_code}',
                'package': package_name,
                'registry': 'github'
            }
            
        except Exception as e:
            return {
                'error': f'Erro buscando no GitHub: {str(e)}',
                'package': package_name,
                'registry': 'github'
            }
    
    def _format_npm_response(self, data: Dict) -> Dict:
        """Formata resposta do NPM"""
        latest_version = data.get('dist-tags', {}).get('latest', 'N/A')
        latest_data = data.get('versions', {}).get(latest_version, {})
        
        return {
            'registry': 'npm',
            'name': data.get('name', 'N/A'),
            'version': latest_version,
            'description': data.get('description', 'Sem descrição'),
            'homepage': data.get('homepage', ''),
            'repository': data.get('repository', {}).get('url', ''),
            'keywords': data.get('keywords', []),
            'license': data.get('license', 'N/A'),
            'author': self._extract_author(data.get('author', {})),
            'dependencies': latest_data.get('dependencies', {}),
            'install_command': f"npm install {data.get('name', '')}",
            'npm_url': f"https://www.npmjs.com/package/{data.get('name', '')}",
            'weekly_downloads': self._get_npm_downloads(data.get('name', ''))
        }
    
    def _format_npm_search_response(self, data: Dict, query: str) -> Dict:
        """Formata resposta de busca do NPM"""
        results = []
        
        for result in data.get('results', [])[:5]:
            package = result.get('package', {})
            results.append({
                'name': package.get('name', 'N/A'),
                'version': package.get('version', 'N/A'),
                'description': package.get('description', 'Sem descrição'),
                'keywords': package.get('keywords', []),
                'npm_url': f"https://www.npmjs.com/package/{package.get('name', '')}"
            })
        
        return {
            'registry': 'npm',
            'query': query,
            'type': 'search_results',
            'results': results
        }
    
    def _format_pypi_response(self, data: Dict) -> Dict:
        """Formata resposta do PyPI"""
        info = data.get('info', {})
        
        return {
            'registry': 'pypi',
            'name': info.get('name', 'N/A'),
            'version': info.get('version', 'N/A'),
            'description': info.get('summary', 'Sem descrição'),
            'long_description': info.get('description', ''),
            'homepage': info.get('home_page', ''),
            'repository': info.get('project_url', ''),
            'keywords': info.get('keywords', '').split(',') if info.get('keywords') else [],
            'license': info.get('license', 'N/A'),
            'author': info.get('author', 'N/A'),
            'author_email': info.get('author_email', ''),
            'python_requires': info.get('requires_python', 'N/A'),
            'install_command': f"pip install {info.get('name', '')}",
            'pypi_url': f"https://pypi.org/project/{info.get('name', '')}/",
            'classifiers': info.get('classifiers', [])
        }
    
    def _format_github_response(self, data: Dict, query: str) -> Dict:
        """Formata resposta do GitHub"""
        results = []
        
        for repo in data.get('items', [])[:5]:
            results.append({
                'name': repo.get('name', 'N/A'),
                'full_name': repo.get('full_name', 'N/A'),
                'description': repo.get('description', 'Sem descrição'),
                'language': repo.get('language', 'N/A'),
                'stars': repo.get('stargazers_count', 0),
                'forks': repo.get('forks_count', 0),
                'issues': repo.get('open_issues_count', 0),
                'last_update': repo.get('updated_at', 'N/A'),
                'url': repo.get('html_url', ''),
                'clone_url': repo.get('clone_url', '')
            })
        
        return {
            'registry': 'github',
            'query': query,
            'type': 'search_results',
            'results': results
        }
    
    def _extract_author(self, author_data) -> str:
        """Extrai informação do autor"""
        if isinstance(author_data, str):
            return author_data
        elif isinstance(author_data, dict):
            return author_data.get('name', 'N/A')
        else:
            return 'N/A'
    
    def _get_npm_downloads(self, package_name: str) -> str:
        """Busca downloads do NPM (simplificado)"""
        try:
            url = f"https://api.npmjs.org/downloads/point/last-week/{package_name}"
            response = self.session.get(url, timeout=5)
            if response.status_code == 200:
                data = response.json()
                return f"{data.get('downloads', 0):,}"
        except:
            pass
        return 'N/A'
    
    def install_package(self, package_name: str, dev: bool = False, global_install: bool = False) -> Dict:
        """
        Instala um pacote
        
        Args:
            package_name: Nome do pacote
            dev: Se é dependência de desenvolvimento
            global_install: Se é instalação global
        
        Returns:
            Dict com resultado da instalação
        """
        try:
            registry = self._detect_registry()
            
            if registry == 'npm':
                return self._install_npm_package(package_name, dev, global_install)
            elif registry == 'pypi':
                return self._install_python_package(package_name)
            else:
                return {
                    'error': 'Não foi possível determinar o tipo de projeto',
                    'package': package_name
                }
                
        except Exception as e:
            return {
                'error': str(e),
                'package': package_name
            }
    
    def _install_npm_package(self, package_name: str, dev: bool, global_install: bool) -> Dict:
        """Instala pacote NPM"""
        try:
            cmd = ['npm', 'install']
            
            if global_install:
                cmd.append('-g')
            elif dev:
                cmd.append('--save-dev')
            
            cmd.append(package_name)
            
            result = subprocess.run(cmd, capture_output=True, text=True, cwd=Path.cwd())
            
            if result.returncode == 0:
                return {
                    'success': True,
                    'package': package_name,
                    'command': ' '.join(cmd),
                    'output': result.stdout
                }
            else:
                return {
                    'error': f'Erro na instalação: {result.stderr}',
                    'package': package_name,
                    'command': ' '.join(cmd)
                }
                
        except Exception as e:
            return {
                'error': f'Erro executando npm: {str(e)}',
                'package': package_name
            }
    
    def _install_python_package(self, package_name: str) -> Dict:
        """Instala pacote Python"""
        try:
            cmd = [sys.executable, '-m', 'pip', 'install', package_name]
            
            result = subprocess.run(cmd, capture_output=True, text=True, cwd=Path.cwd())
            
            if result.returncode == 0:
                return {
                    'success': True,
                    'package': package_name,
                    'command': ' '.join(cmd),
                    'output': result.stdout
                }
            else:
                return {
                    'error': f'Erro na instalação: {result.stderr}',
                    'package': package_name,
                    'command': ' '.join(cmd)
                }
                
        except Exception as e:
            return {
                'error': f'Erro executando pip: {str(e)}',
                'package': package_name
            }
    
    def list_installed_packages(self) -> Dict:
        """Lista pacotes instalados no projeto atual"""
        try:
            registry = self._detect_registry()
            
            if registry == 'npm':
                return self._list_npm_packages()
            elif registry == 'pypi':
                return self._list_python_packages()
            else:
                return {
                    'error': 'Não foi possível determinar o tipo de projeto'
                }
                
        except Exception as e:
            return {
                'error': str(e)
            }
    
    def _list_npm_packages(self) -> Dict:
        """Lista pacotes NPM instalados"""
        try:
            # Ler package.json
            package_json_path = Path.cwd() / 'package.json'
            if not package_json_path.exists():
                return {
                    'error': 'package.json não encontrado'
                }
            
            with open(package_json_path, 'r', encoding='utf-8') as f:
                package_data = json.load(f)
            
            dependencies = package_data.get('dependencies', {})
            dev_dependencies = package_data.get('devDependencies', {})
            
            return {
                'registry': 'npm',
                'dependencies': dependencies,
                'devDependencies': dev_dependencies,
                'total': len(dependencies) + len(dev_dependencies)
            }
            
        except Exception as e:
            return {
                'error': f'Erro listando pacotes NPM: {str(e)}'
            }
    
    def _list_python_packages(self) -> Dict:
        """Lista pacotes Python instalados"""
        try:
            # Usar pip list
            result = subprocess.run(
                [sys.executable, '-m', 'pip', 'list', '--format=json'],
                capture_output=True, text=True
            )
            
            if result.returncode == 0:
                packages = json.loads(result.stdout)
                return {
                    'registry': 'pypi',
                    'packages': {pkg['name']: pkg['version'] for pkg in packages},
                    'total': len(packages)
                }
            else:
                return {
                    'error': f'Erro executando pip list: {result.stderr}'
                }
                
        except Exception as e:
            return {
                'error': f'Erro listando pacotes Python: {str(e)}'
            }
    
    def check_outdated_packages(self) -> Dict:
        """Verifica pacotes desatualizados"""
        try:
            registry = self._detect_registry()
            
            if registry == 'npm':
                return self._check_npm_outdated()
            elif registry == 'pypi':
                return self._check_python_outdated()
            else:
                return {
                    'error': 'Não foi possível determinar o tipo de projeto'
                }
                
        except Exception as e:
            return {
                'error': str(e)
            }
    
    def _check_npm_outdated(self) -> Dict:
        """Verifica pacotes NPM desatualizados"""
        try:
            result = subprocess.run(
                ['npm', 'outdated', '--json'],
                capture_output=True, text=True, cwd=Path.cwd()
            )
            
            if result.stdout:
                outdated = json.loads(result.stdout)
                return {
                    'registry': 'npm',
                    'outdated': outdated,
                    'count': len(outdated)
                }
            else:
                return {
                    'registry': 'npm',
                    'outdated': {},
                    'count': 0,
                    'message': 'Todos os pacotes estão atualizados'
                }
                
        except Exception as e:
            return {
                'error': f'Erro verificando pacotes NPM: {str(e)}'
            }
    
    def _check_python_outdated(self) -> Dict:
        """Verifica pacotes Python desatualizados"""
        try:
            result = subprocess.run(
                [sys.executable, '-m', 'pip', 'list', '--outdated', '--format=json'],
                capture_output=True, text=True
            )
            
            if result.returncode == 0 and result.stdout:
                outdated = json.loads(result.stdout)
                return {
                    'registry': 'pypi',
                    'outdated': {pkg['name']: {
                        'current': pkg['version'],
                        'latest': pkg['latest_version']
                    } for pkg in outdated},
                    'count': len(outdated)
                }
            else:
                return {
                    'registry': 'pypi',
                    'outdated': {},
                    'count': 0,
                    'message': 'Todos os pacotes estão atualizados'
                }
                
        except Exception as e:
            return {
                'error': f'Erro verificando pacotes Python: {str(e)}'
            }
    
    def format_package_info(self, package_info: Dict) -> str:
        """Formata informações do pacote para exibição"""
        if 'error' in package_info:
            return f"❌ {package_info['error']}"
        
        registry = package_info.get('registry', 'unknown').upper()
        
        if package_info.get('type') == 'search_results':
            return self._format_search_results(package_info)
        
        lines = [f"📦 {package_info.get('name', 'N/A')} ({registry})"]
        
        # Informações básicas
        lines.append(f"🏷️  Versão: {package_info.get('version', 'N/A')}")
        lines.append(f"📝 Descrição: {package_info.get('description', 'Sem descrição')}")
        
        if package_info.get('author') and package_info['author'] != 'N/A':
            lines.append(f"👤 Autor: {package_info['author']}")
        
        if package_info.get('license') and package_info['license'] != 'N/A':
            lines.append(f"⚖️  Licença: {package_info['license']}")
        
        # Links
        if package_info.get('homepage'):
            lines.append(f"🏠 Homepage: {package_info['homepage']}")
        
        if package_info.get('repository'):
            lines.append(f"📂 Repositório: {package_info['repository']}")
        
        # Registry específico
        if registry == 'NPM':
            if package_info.get('npm_url'):
                lines.append(f"📦 NPM: {package_info['npm_url']}")
            if package_info.get('weekly_downloads') != 'N/A':
                lines.append(f"⬇️  Downloads/semana: {package_info['weekly_downloads']}")
        elif registry == 'PYPI':
            if package_info.get('pypi_url'):
                lines.append(f"🐍 PyPI: {package_info['pypi_url']}")
            if package_info.get('python_requires') != 'N/A':
                lines.append(f"🐍 Python: {package_info['python_requires']}")
        
        # Comandos de instalação
        if package_info.get('install_command'):
            lines.append(f"💾 Instalar: {package_info['install_command']}")
        
        # Keywords
        if package_info.get('keywords'):
            keywords = package_info['keywords'][:5]  # Primeiras 5
            lines.append(f"🏷️  Tags: {', '.join(keywords)}")
        
        return '\n'.join(lines)
    
    def _format_search_results(self, search_data: Dict) -> str:
        """Formata resultados de busca"""
        registry = search_data.get('registry', 'unknown').upper()
        query = search_data.get('query', 'N/A')
        
        lines = [f"🔍 Resultados para '{query}' no {registry}:\n"]
        
        for i, result in enumerate(search_data.get('results', []), 1):
            lines.append(f"{i}. {result.get('name', 'N/A')}")
            lines.append(f"   📝 {result.get('description', 'Sem descrição')}")
            
            if registry == 'GITHUB':
                lines.append(f"   ⭐ {result.get('stars', 0)} stars | 🍴 {result.get('forks', 0)} forks")
                lines.append(f"   💻 {result.get('language', 'N/A')}")
            elif registry == 'NPM':
                lines.append(f"   🏷️  v{result.get('version', 'N/A')}")
            
            lines.append(f"   🔗 {result.get('npm_url', result.get('url', 'N/A'))}")
            lines.append("")
        
        if not search_data.get('results'):
            lines.append("❌ Nenhum resultado encontrado")
        
        return '\n'.join(lines)
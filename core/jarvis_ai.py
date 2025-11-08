"""
Jarvis AI Core - Processamento de linguagem natural avançado
Sistema expandido com geração de código, Git, documentação e muito mais
"""

import re
import os
import json
import subprocess
from typing import Dict, List, Optional, Tuple
from datetime import datetime

class JarvisAI:
    """IA avançada do Jarvis com funcionalidades expandidas"""
    
    def __init__(self):
        self.commands_db = self._load_commands_database()
        self.context = {}
        
    def _load_commands_database(self) -> Dict:
        """Carrega base expandida de comandos"""
        return {
            # Comandos de arquivo/diretório
            'file_operations': {
                'patterns': [
                    r'(criar|gerar|fazer)\s+(arquivo|file)\s+(.+)',
                    r'(listar|mostrar|ver)\s+(arquivos|files|diretório|pasta)',
                    r'(abrir|editar)\s+(arquivo|file)\s+(.+)',
                    r'(deletar|remover|apagar)\s+(arquivo|file)\s+(.+)'
                ],
                'actions': ['create_file', 'list_files', 'edit_file', 'delete_file']
            },
            
            # Geração de código e projetos
            'code_generation': {
                'patterns': [
                    r'(criar|gerar)\s+(projeto|boilerplate)\s+(\w+)\s+(.+)',
                    r'(scaffold|criar)\s+(projeto)\s+(\w+)',
                    r'(gerar|criar)\s+(componente|component)\s+(\w+)\s+(.+)',
                    r'(snippet|código)\s+(\w+)\s+(.*)',
                    r'(template|modelo)\s+(.+)'
                ],
                'actions': ['create_project', 'scaffold_project', 'create_component', 'generate_snippet', 'create_template']
            },
            
            # Git avançado
            'git_operations': {
                'patterns': [
                    r'git\s+(status|log|diff|branch)',
                    r'(commit|commitar)\s+(.+)',
                    r'(push|empurrar|enviar)',
                    r'(pull|puxar|baixar)',
                    r'(clone|clonar)\s+(.+)',
                    r'(branch|ramo)\s+(.*)',
                    r'(merge|mesclar)\s+(.+)',
                    r'(stash|guardar)\s*(.*)',
                    r'git\s+(ahead|behind|sync)'
                ],
                'actions': ['git_status', 'git_commit', 'git_push', 'git_pull', 'git_clone', 
                           'git_branch', 'git_merge', 'git_stash', 'git_sync']
            },
            
            # Pesquisa de documentação
            'documentation': {
                'patterns': [
                    r'(docs|documentação|doc)\s+(.+)',
                    r'(pesquisar|buscar)\s+(docs|documentação)\s+(.+)',
                    r'(cheatsheet|cheat)\s+(.+)',
                    r'(help|ajuda)\s+(.+)',
                    r'(referência|reference)\s+(.+)'
                ],
                'actions': ['search_docs', 'search_documentation', 'show_cheatsheet', 'get_help', 'show_reference']
            },
            
            # Gerenciamento de pacotes
            'package_management': {
                'patterns': [
                    r'(package|pacote)\s+(info|informações)\s+(.+)',
                    r'(instalar|install)\s+(package|pacote)\s+(.+)',
                    r'(buscar|search)\s+(package|pacote)\s+(.+)',
                    r'(listar|list)\s+(packages|pacotes)',
                    r'(atualizar|update|upgrade)\s+(packages|pacotes)',
                    r'(npm|pip|yarn)\s+(.+)'
                ],
                'actions': ['package_info', 'install_package', 'search_package', 'list_packages', 'update_packages', 'package_command']
            },
            
            # Gerenciamento de tarefas
            'task_management': {
                'patterns': [
                    r'(tarefa|task|todo)\s+(criar|nova|add)\s+(.+)',
                    r'(listar|mostrar)\s+(tarefas|tasks|todos)',
                    r'(concluir|completar|done)\s+(tarefa|task)\s+(.+)',
                    r'(deletar|remover)\s+(tarefa|task)\s+(.+)',
                    r'(editar|modificar)\s+(tarefa|task)\s+(.+)',
                    r'(estatísticas|stats)\s+(tarefas|tasks)',
                    r'(buscar|search)\s+(tarefa|task)\s+(.+)'
                ],
                'actions': ['create_task', 'list_tasks', 'complete_task', 'delete_task', 'edit_task', 'task_stats', 'search_tasks']
            },
            
            # Manipulação de documentos
            'document_management': {
                'patterns': [
                    # Excel
                    r'(criar|gerar)\s+(excel|planilha)\s+(.+)',
                    r'(ler|abrir)\s+(excel|planilha)\s+(.+)',
                    r'(limpar|clean)\s+(excel|planilha)\s+(.+)',
                    r'(converter|convert)\s+(excel|csv)\s+(.+)',
                    r'(atualizar|update)\s+(excel|planilha)\s+(.+)',
                    r'(info|informações)\s+(excel|planilha)\s+(.+)',
                    
                    # Word
                    r'(criar|gerar)\s+(word|documento|doc)\s+(.+)',
                    r'(ler|abrir)\s+(word|documento|doc)\s+(.+)',
                    r'(extrair|extract)\s+(texto|text)\s+(.+)',
                    r'(substituir|replace)\s+(.+)\s+(por|with|by)\s+(.+)\s+(em|in)\s+(.+)',
                    r'(buscar|find)\s+(.+)\s+(em|in)\s+(.+)',
                    r'(template|modelo)\s+(word|doc)\s+(.+)',
                    
                    # PowerPoint
                    r'(criar|gerar)\s+(ppt|powerpoint|apresentação)\s+(.+)',
                    r'(adicionar|add)\s+(slide)\s+(.+)',
                    r'(gerar|criar)\s+(ppt|apresentação)\s+(do|from)\s+(excel|json)\s+(.+)',
                    r'(extrair|extract)\s+(texto|text)\s+(ppt|powerpoint)\s+(.+)',
                    r'(template|modelo)\s+(ppt|json)\s+(.+)',
                    
                    # Geral
                    r'(dados|data)\s+(exemplo|sample|teste)\s+(excel|planilha)'
                ],
                'actions': [
                    'create_excel', 'read_excel', 'clean_excel', 'convert_excel_csv', 
                    'update_excel', 'excel_info', 'create_word', 'read_word', 'extract_text',
                    'find_replace', 'search_in_doc', 'word_template', 'create_ppt', 
                    'add_slide', 'generate_ppt_from_data', 'extract_ppt_text', 'ppt_template',
                    'generate_sample_data'
                ]
            },
            
            # Scripts e automação
            'automation': {
                'patterns': [
                    r'(executar|run|rodar)\s+(script|comando)\s+(.+)',
                    r'(alias|atalho)\s+(.+)',
                    r'(watch|monitorar)\s+(.+)',
                    r'(build|compilar|construir)',
                    r'(test|testar|teste)',
                    r'(deploy|publicar)'
                ],
                'actions': ['run_script', 'create_alias', 'watch_files', 'build_project', 'run_tests', 'deploy_project']
            },
            
            # Geração de dados
            'data_generation': {
                'patterns': [
                    r'(gerar|criar)\s+(dados|data)\s+(falsos|fake|teste)',
                    r'(nome|names?)\s+(falsos?|fake)',
                    r'(email|emails?)\s+(falsos?|fake)',
                    r'(número|numbers?|telefone)\s+(falsos?|fake)',
                    r'(endereço|address)\s+(falsos?|fake)',
                    r'(empresa|company)\s+(falsos?|fake)',
                    r'(lorem|texto)\s+(ipsum|fake)',
                    r'(json|csv|xml)\s+(fake|falso)'
                ],
                'actions': ['generate_fake_data', 'generate_names', 'generate_emails', 'generate_phones', 
                           'generate_addresses', 'generate_companies', 'generate_lorem', 'generate_structured_data']
            },
            
            # Sistema
            'system_operations': {
                'patterns': [
                    r'(data|hora|time)',
                    r'(informações|info)\s+(sistema|system)',
                    r'(help|ajuda|comandos)',
                    r'(limpar|clear|cls)',
                    r'(configuração|config|settings)',
                    r'(versão|version)',
                    r'(status|estado)\s+(projeto|project)'
                ],
                'actions': ['show_datetime', 'system_info', 'show_help', 'clear_screen', 
                           'show_config', 'show_version', 'project_status']
            },
            
            # Análise de código
            'code_analysis': {
                'patterns': [
                    r'(analisar|análise)\s+(código|code)',
                    r'(lint|linter)\s+(.+)',
                    r'(format|formatar)\s+(código|code)',
                    r'(complexity|complexidade)',
                    r'(metrics|métricas)\s+(código|code)'
                ],
                'actions': ['analyze_code', 'lint_code', 'format_code', 'code_complexity', 'code_metrics']
            }
        }
    
    def process_input(self, user_input: str) -> Dict:
        """Processa entrada do usuário com análise avançada"""
        user_input = user_input.lower().strip()
        
        # Primeiro, tentar padrões específicos
        for category, data in self.commands_db.items():
            for i, pattern in enumerate(data['patterns']):
                match = re.search(pattern, user_input, re.IGNORECASE)
                if match:
                    return {
                        'category': category,
                        'action': data['actions'][min(i, len(data['actions'])-1)],
                        'matches': match.groups(),
                        'confidence': 0.9,
                        'original_input': user_input
                    }
        
        # Se não encontrou padrão específico, tentar interpretação contextual
        return self._interpret_contextual(user_input)
    
    def _interpret_contextual(self, text: str) -> Dict:
        """Interpretação contextual avançada"""
        
        # Análise de contexto baseada em palavras-chave ponderadas
        context_scores = {}
        
        # Palavras-chave com pesos para cada categoria
        keyword_weights = {
            'code_generation': {
                'projeto': 3, 'criar': 2, 'gerar': 2, 'boilerplate': 4, 'scaffold': 4,
                'componente': 3, 'template': 3, 'python': 2, 'react': 2, 'nodejs': 2
            },
            'git_operations': {
                'git': 4, 'commit': 3, 'push': 3, 'pull': 3, 'branch': 3, 'merge': 3,
                'repositório': 2, 'repo': 2, 'clone': 3, 'stash': 3
            },
            'documentation': {
                'docs': 4, 'documentação': 4, 'cheatsheet': 4, 'help': 2, 'ajuda': 2,
                'referência': 3, 'pesquisar': 2, 'buscar': 2
            },
            'package_management': {
                'pacote': 4, 'package': 4, 'npm': 4, 'pip': 4, 'instalar': 3,
                'install': 3, 'dependência': 3, 'biblioteca': 2
            },
            'task_management': {
                'tarefa': 4, 'task': 4, 'todo': 4, 'fazer': 2, 'lista': 2,
                'completar': 3, 'concluir': 3, 'pendente': 2
            },
            'file_operations': {
                'arquivo': 3, 'file': 3, 'pasta': 2, 'diretório': 2, 'criar': 2,
                'listar': 2, 'abrir': 2, 'editar': 2
            },
            'data_generation': {
                'dados': 3, 'fake': 4, 'falso': 4, 'gerar': 2, 'nome': 2,
                'email': 2, 'telefone': 2, 'teste': 2
            }
        }
        
        # Calcular scores para cada categoria
        for category, keywords in keyword_weights.items():
            score = 0
            for keyword, weight in keywords.items():
                if keyword in text:
                    score += weight
            context_scores[category] = score
        
        # Encontrar categoria com maior score
        if context_scores:
            best_category = max(context_scores, key=context_scores.get)
            best_score = context_scores[best_category]
            
            if best_score > 0:
                return {
                    'category': best_category,
                    'action': 'contextual_action',
                    'matches': [text],
                    'confidence': min(best_score / 10, 0.8),  # Normalizar score
                    'original_input': text,
                    'context_scores': context_scores
                }
        
        # Fallback para comando desconhecido
        return {
            'category': 'unknown',
            'action': 'unknown_command',
            'matches': [text],
            'confidence': 0.1,
            'original_input': text
        }
    
    def generate_response(self, processed_input: Dict) -> str:
        """Gera resposta avançada baseada no input processado"""
        
        action = processed_input['action']
        matches = processed_input['matches']
        category = processed_input['category']
        
        # Respostas específicas por categoria e ação
        responses = {
            # File operations
            'create_file': f"Vou criar o arquivo {matches[2] if len(matches) > 2 else 'especificado'}",
            'list_files': "Listando arquivos do diretório atual:",
            
            # Code generation
            'create_project': f"Criando projeto {matches[2] if len(matches) > 2 else 'especificado'}",
            'create_component': f"Criando componente {matches[1] if len(matches) > 1 else 'especificado'}",
            'generate_snippet': f"Gerando snippet de código {matches[1] if len(matches) > 1 else 'solicitado'}",
            
            # Git operations
            'git_status': "Verificando status do Git:",
            'git_commit': f"Fazendo commit: {matches[1] if len(matches) > 1 else 'mudanças atuais'}",
            'git_push': "Enviando alterações para o repositório remoto:",
            'git_pull': "Baixando alterações do repositório remoto:",
            'git_branch': "Gerenciando branches:",
            
            # Documentation
            'search_docs': f"Pesquisando documentação para: {matches[1] if len(matches) > 1 else 'termo especificado'}",
            'show_cheatsheet': f"Mostrando cheatsheet para: {matches[1] if len(matches) > 1 else 'ferramenta especificada'}",
            
            # Package management
            'package_info': f"Buscando informações do pacote: {matches[2] if len(matches) > 2 else 'especificado'}",
            'install_package': f"Instalando pacote: {matches[2] if len(matches) > 2 else 'especificado'}",
            'search_package': f"Buscando pacotes: {matches[2] if len(matches) > 2 else 'especificado'}",
            
            # Task management
            'create_task': f"Criando nova tarefa: {matches[2] if len(matches) > 2 else 'especificada'}",
            'list_tasks': "Listando tarefas:",
            'complete_task': f"Concluindo tarefa: {matches[2] if len(matches) > 2 else 'especificada'}",
            
            # Data generation
            'generate_fake_data': "Gerando dados falsos para teste:",
            'generate_names': "Gerando nomes falsos:",
            'generate_emails': "Gerando emails falsos:",
            
            # System
            'show_help': "Aqui estão os comandos disponíveis:",
            'show_datetime': "Mostrando data e hora atual:",
            'system_info': "Informações do sistema:",
            
            # Contextual action
            'contextual_action': f"Entendi que você quer trabalhar com {category.replace('_', ' ')}. Processando...",
            
            # Unknown
            'unknown_command': f"Não entendi completamente '{processed_input['original_input']}'. Posso ajudar com código, Git, documentação, pacotes, tarefas e muito mais!"
        }
        
        return responses.get(action, "Processando sua solicitação...")
        
    def get_suggestions(self, partial_input: str) -> List[str]:
        """Sugere comandos avançados baseado em entrada parcial"""
        
        # Sugestões categorizadas
        all_suggestions = {
            'Geração de Código': [
                "criar projeto python meu_projeto",
                "criar projeto react minha_app", 
                "criar projeto nodejs meu_servidor",
                "criar componente Button react",
                "gerar snippet python for_loop"
            ],
            'Git': [
                "git status",
                "commit 'mensagem do commit'",
                "git push",
                "git pull", 
                "git branch nova_feature",
                "git merge develop"
            ],
            'Documentação': [
                "docs python requests",
                "docs react hooks",
                "cheatsheet git",
                "cheatsheet docker",
                "pesquisar docs javascript array"
            ],
            'Pacotes': [
                "package info express",
                "instalar pacote lodash",
                "buscar pacote pandas",
                "listar pacotes",
                "npm install react"
            ],
            'Tarefas': [
                "criar tarefa 'implementar login'",
                "listar tarefas",
                "completar tarefa abc123",
                "estatísticas tarefas"
            ],
            'Dados Falsos': [
                "gerar dados falsos",
                "gerar nomes falsos",
                "gerar emails falsos",
                "gerar json fake"
            ],
            'Sistema': [
                "data e hora",
                "info sistema",
                "help",
                "status projeto"
            ]
        }
        
        if partial_input:
            # Filtrar sugestões baseadas na entrada parcial
            partial = partial_input.lower()
            filtered_suggestions = []
            
            for category, suggestions in all_suggestions.items():
                category_suggestions = [s for s in suggestions if partial in s.lower()]
                if category_suggestions:
                    filtered_suggestions.extend(category_suggestions[:2])  # Máximo 2 por categoria
            
            return filtered_suggestions[:8]  # Máximo 8 sugestões
        else:
            # Retornar sugestões populares
            popular = [
                "criar projeto python",
                "git status",
                "docs python",
                "gerar dados falsos",
                "listar tarefas",
                "package info",
                "help",
                "criar arquivo"
            ]
            return popular
    
    def get_available_commands(self) -> Dict[str, List[str]]:
        """Retorna todos os comandos disponíveis organizados por categoria"""
        
        command_descriptions = {
            'Geração de Código': [
                "criar projeto <tipo> <nome> - Cria novo projeto com boilerplate",
                "criar componente <nome> <tipo> - Cria componente (React, Vue, etc.)",
                "gerar snippet <linguagem> <tipo> - Gera snippet de código",
                "template <tipo> - Cria template personalizado"
            ],
            'Git Avançado': [
                "git status - Status detalhado do repositório",
                "commit <mensagem> - Commit inteligente com auto-stage",
                "git push/pull - Sincronização com remote",
                "git branch <nome> - Gerenciamento de branches",
                "git merge <branch> - Merge de branches",
                "git stash - Gerenciamento de stash"
            ],
            'Documentação': [
                "docs <linguagem> <termo> - Pesquisa documentação",
                "cheatsheet <ferramenta> - Mostra cheatsheet",
                "pesquisar docs <termo> - Busca em múltiplas fontes",
                "referência <linguagem> - Referência rápida"
            ],
            'Gerenciamento de Pacotes': [
                "package info <nome> - Informações do pacote",
                "instalar pacote <nome> - Instala pacote",
                "buscar pacote <termo> - Busca pacotes",
                "listar pacotes - Lista pacotes instalados",
                "atualizar pacotes - Verifica atualizações"
            ],
            'Gerenciamento de Tarefas': [
                "criar tarefa <título> - Nova tarefa",
                "listar tarefas - Lista todas as tarefas", 
                "completar tarefa <id> - Marca como concluída",
                "editar tarefa <id> - Edita tarefa existente",
                "buscar tarefa <termo> - Busca tarefas",
                "estatísticas tarefas - Mostra estatísticas"
            ],
            'Automação': [
                "executar script <comando> - Executa script personalizado",
                "watch <padrão> - Monitora alterações em arquivos",
                "build - Compila/constrói o projeto",
                "test - Executa testes",
                "deploy - Faz deploy do projeto"
            ],
            'Geração de Dados': [
                "gerar dados falsos - Dados de teste variados",
                "gerar nomes falsos - Nomes brasileiros",
                "gerar emails falsos - Endereços de email",
                "gerar telefones falsos - Números brasileiros",
                "gerar json fake - Estruturas JSON"
            ],
            'Sistema': [
                "data e hora - Data e hora atual",
                "info sistema - Informações do sistema",
                "status projeto - Status do projeto atual",
                "configuração - Mostra configurações",
                "versão - Versão do Jarvis",
                "help - Esta ajuda"
            ]
        }
        
        return command_descriptions
    
    def analyze_intent(self, user_input: str) -> Dict:
        """Analisa intenção do usuário com mais profundidade"""
        processed = self.process_input(user_input)
        
        # Adicionar análise de sentimento e urgência
        urgency_keywords = ['urgente', 'rápido', 'agora', 'já', 'imediatamente']
        polite_keywords = ['por favor', 'poderia', 'pode', 'obrigado', 'obrigada']
        
        urgency_score = sum(1 for word in urgency_keywords if word in user_input.lower())
        politeness_score = sum(1 for word in polite_keywords if word in user_input.lower())
        
        processed.update({
            'urgency': urgency_score,
            'politeness': politeness_score,
            'intent_analysis': {
                'is_question': '?' in user_input,
                'is_command': any(word in user_input.lower() for word in ['criar', 'fazer', 'executar', 'rodar']),
                'is_request': any(word in user_input.lower() for word in ['poderia', 'pode', 'por favor']),
                'word_count': len(user_input.split()),
                'has_specific_target': bool(processed.get('matches', []))
            }
        })
        
        return processed
"""CLI interface removed.

This file previously contained the interactive CLI implementation. The
project has been converted to an API-only application and the CLI was
removed. The file is intentionally left as a placeholder to avoid
import errors from other modules that might reference it.
"""

def _cli_removed_notice():
    return "CLI interface removed. Use the FastAPI server (main.py) to run the assistant."

from .excel_manager import ExcelManager
from .word_manager import WordManager
from .powerpoint_manager import PowerPointManager

class CLIInterface:
    """Interface de linha de comando avançada para o Jarvis"""
    
    def __init__(self, jarvis_ai, logger):
        self.jarvis_ai = jarvis_ai
        self.logger = logger
        self.session_history = []
        
        # Inicializar módulos avançados
        self.code_generator = CodeGenerator()
        self.git_manager = GitManager()
        self.doc_searcher = DocumentationSearcher()
        self.package_manager = PackageManager()
        self.task_manager = TaskManager()
        self.excel_manager = ExcelManager()
        self.word_manager = WordManager()
        self.powerpoint_manager = PowerPointManager()
        
    def run_interactive(self):
        """Executa modo interativo avançado do Jarvis"""
        self._show_welcome()
        
        while True:
            try:
                # Mostrar informações contextuais
                context_info = self._get_context_info()
                if context_info:
                    print(f"📍 {context_info}")
                
                user_input = input(f"\n{CLI_PROMPT}").strip()
                
                if not user_input:
                    continue
                    
                if user_input.lower() in ['sair', 'exit', 'quit', 'q']:
                    print("👋 Tchau! Volte sempre!")
                    break
                    
                self.execute_command(user_input)
                self.session_history.append(user_input)
                
            except KeyboardInterrupt:
                print("\n👋 Tchau! Jarvis saindo...")
                break
            except Exception as e:
                self.logger.error(f"Erro durante execução: {e}")
                print(f"❌ Erro: {e}")
    
    def execute_command(self, command: str):
        """Executa um comando específico com análise avançada"""
        self.logger.info(f"Executando comando: {command}")
        
        # Processar comando com IA avançada
        processed = self.jarvis_ai.process_input(command)
        
        # Mostrar resposta da IA
        response = self.jarvis_ai.generate_response(processed)
        print(f"\n💭 {response}")
        
        # Executar ação correspondente
        self._execute_advanced_action(processed)
    
    def _execute_advanced_action(self, processed_input: Dict):
        """Executa ações avançadas determinadas pela IA"""
        action = processed_input['action']
        matches = processed_input['matches']
        category = processed_input['category']
        
        try:
            # Actions de arquivo (originais)
            if action == 'create_file':
                self._create_file(matches)
            elif action == 'list_files':
                self._list_files()
                
            # Geração de código
            elif action == 'create_project':
                self._create_project(matches)
            elif action == 'scaffold_project':
                self._scaffold_project(matches)
            elif action == 'create_component':
                self._create_component(matches)
            elif action == 'generate_snippet':
                self._generate_snippet(matches)
                
            # Git avançado
            elif action == 'git_status':
                self._git_status_advanced()
            elif action == 'git_commit':
                self._git_commit_advanced(matches)
            elif action == 'git_push':
                self._git_push()
            elif action == 'git_pull':
                self._git_pull()
            elif action == 'git_branch':
                self._git_branch(matches)
            elif action == 'git_stash':
                self._git_stash(matches)
                
            # Documentação
            elif action == 'search_docs' or action == 'search_documentation':
                self._search_documentation(matches)
            elif action == 'show_cheatsheet':
                self._show_cheatsheet(matches)
                
            # Gerenciamento de pacotes
            elif action == 'package_info':
                self._package_info(matches)
            elif action == 'install_package':
                self._install_package(matches)
            elif action == 'search_package':
                self._search_package(matches)
            elif action == 'list_packages':
                self._list_packages()
                
            # Gerenciamento de tarefas
            elif action == 'create_task':
                self._create_task(matches)
            elif action == 'list_tasks':
                self._list_tasks()
            elif action == 'complete_task':
                self._complete_task(matches)
            elif action == 'task_stats':
                self._task_statistics()
            elif action == 'search_tasks':
                self._search_tasks(matches)
                
            # Manipulação de documentos
            elif action == 'create_excel':
                self.create_excel(processed_input['original_input'])
            elif action == 'read_excel':
                self.read_excel(processed_input['original_input'])
            elif action == 'clean_excel':
                self.clean_excel(processed_input['original_input'])
            elif action == 'convert_excel_csv':
                self.convert_excel_csv(processed_input['original_input'])
            elif action == 'excel_info':
                self.excel_info(processed_input['original_input'])
            elif action == 'create_word':
                self.create_word(processed_input['original_input'])
            elif action == 'read_word':
                self.read_word(processed_input['original_input'])
            elif action == 'extract_text':
                self.extract_text(processed_input['original_input'])
            elif action == 'find_replace':
                self.find_replace(processed_input['original_input'])
            elif action == 'create_ppt':
                self.create_ppt(processed_input['original_input'])
            elif action == 'add_slide':
                self.add_slide(processed_input['original_input'])
            elif action == 'generate_ppt_from_data':
                self.generate_ppt_from_data(processed_input['original_input'])
            elif action == 'ppt_template':
                self.ppt_template(processed_input['original_input'])
            elif action == 'generate_sample_data':
                self.generate_sample_data(processed_input['original_input'])
                
            # Geração de dados (expandida)
            elif action == 'generate_fake_data':
                self._generate_fake_data_advanced()
            elif action == 'generate_names':
                self._generate_names()
            elif action == 'generate_emails':
                self._generate_emails()
            elif action == 'generate_phones':
                self._generate_phones()
                
            # Sistema (expandido)
            elif action == 'show_datetime':
                self._show_datetime()
            elif action == 'system_info':
                self._show_system_info()
            elif action == 'show_help':
                self._show_help_advanced()
            elif action == 'clear_screen':
                self._clear_screen()
            elif action == 'show_version':
                self._show_version()
            elif action == 'project_status':
                self._show_project_status()
                
            # Ação contextual
            elif action == 'contextual_action':
                self._handle_contextual_action(processed_input)
                
            # Comando desconhecido
            elif action == 'unknown_command':
                self._show_suggestions_advanced(processed_input['original_input'])
            else:
                print(f"⚠️  Ação '{action}' ainda não implementada completamente")
                self._show_suggestions_advanced(processed_input['original_input'])
                
        except Exception as e:
            self.logger.error(f"Erro executando ação {action}: {e}")
            print(f"❌ Erro executando comando: {e}")
            if 'matches' in locals():
                print(f"💡 Verifique os parâmetros: {matches}")
    
    # === MÉTODOS DE GERAÇÃO DE CÓDIGO ===
    def _create_project(self, matches):
        """Cria novo projeto com boilerplate"""
        if len(matches) >= 3:
            project_type = matches[2]
            project_name = matches[3] if len(matches) > 3 else input("📝 Nome do projeto: ")
        else:
            project_type = input("📝 Tipo do projeto (python/nodejs/react): ")
            project_name = input("📝 Nome do projeto: ")
        
        description = input("📝 Descrição (opcional): ")
        
        success = self.code_generator.create_project(project_type, project_name, description)
        if not success:
            print("💡 Tipos disponíveis:", ", ".join(self.code_generator.get_supported_types()))
    
    def _scaffold_project(self, matches):
        """Cria scaffold básico de projeto"""
        if len(matches) >= 2:
            project_type = matches[2]
        else:
            project_type = input("📝 Tipo do projeto: ")
        
        project_name = input("📝 Nome do projeto: ")
        self.code_generator.create_project(project_type, project_name)
    
    def _create_component(self, matches):
        """Cria componente"""
        if len(matches) >= 3:
            component_name = matches[2]
            component_type = matches[3] if len(matches) > 3 else "react"
        else:
            component_name = input("📝 Nome do componente: ")
            component_type = input("📝 Tipo (react/vue): ") or "react"
        
        self.code_generator.create_component(component_type, component_name)
    
    def _generate_snippet(self, matches):
        """Gera snippet de código"""
        if len(matches) >= 2:
            language = matches[1]
            snippet_type = matches[2] if len(matches) > 2 else "function"
        else:
            language = input("📝 Linguagem: ")
            snippet_type = input("📝 Tipo de snippet: ") or "function"
        
        snippet = self.code_generator.get_code_snippets(language, snippet_type)
        print(f"\n💻 Snippet {language} - {snippet_type}:")
        print("```" + language)
        print(snippet)
        print("```")
    
    # === MÉTODOS GIT AVANÇADOS ===
    def _git_status_advanced(self):
        """Status avançado do Git"""
        status = self.git_manager.get_status()
        formatted_status = self.git_manager.format_status_display(status)
        print(f"\n{formatted_status}")
    
    def _git_commit_advanced(self, matches):
        """Commit avançado com análise inteligente"""
        message = matches[1] if len(matches) > 1 else ""
        commit_type = input("📝 Tipo do commit (feat/fix/docs/etc, Enter para auto): ") or ""
        
        success = self.git_manager.smart_commit(message, commit_type)
        if success:
            # Mostrar log recente
            recent_commits = self.git_manager.get_log(limit=3)
            print("\n📜 Commits recentes:")
            for commit in recent_commits:
                print(f"   {commit}")
    
    def _git_push(self):
        """Push para remote"""
        self.git_manager.push()
    
    def _git_pull(self):
        """Pull do remote"""
        self.git_manager.pull()
    
    def _git_branch(self, matches):
        """Gerenciamento de branches"""
        if len(matches) > 1 and matches[1]:
            branch_name = matches[1]
            action = input("📝 Ação (criar/trocar/deletar): ").lower()
            
            if action in ['criar', 'create']:
                self.git_manager.create_branch(branch_name)
            elif action in ['trocar', 'switch', 'checkout']:
                self.git_manager.switch_branch(branch_name)
            elif action in ['deletar', 'delete']:
                self.git_manager.delete_branch(branch_name)
        else:
            # Listar branches
            branches = self.git_manager.list_branches(include_remote=True)
            print("\n🌳 Branches:")
            for branch in branches:
                print(f"   {branch}")
    
    def _git_stash(self, matches):
        """Gerenciamento de stash"""
        if len(matches) > 1 and 'pop' in matches[1]:
            self.git_manager.stash(pop=True)
        else:
            message = matches[1] if len(matches) > 1 else input("📝 Mensagem do stash (opcional): ")
            self.git_manager.stash(message)
        
        # Mostrar stashes
        stashes = self.git_manager.list_stashes()
        if len(stashes) > 1:
            print("\n💾 Stashes:")
            for stash in stashes[:5]:
                print(f"   {stash}")
    
    # === MÉTODOS DE DOCUMENTAÇÃO ===
    def _search_documentation(self, matches):
        """Pesquisa documentação"""
        if len(matches) >= 2:
            query = matches[1]
            language = matches[2] if len(matches) > 2 else None
        else:
            query = input("📝 O que pesquisar: ")
            language = input("📝 Linguagem específica (opcional): ") or None
        
        print("🔍 Pesquisando documentação...")
        results = self.doc_searcher.search_docs(query, language)
        formatted_results = self.doc_searcher.format_search_results(results)
        print(f"\n{formatted_results}")
    
    def _show_cheatsheet(self, matches):
        """Mostra cheatsheet"""
        if len(matches) >= 2:
            tool = matches[1]
        else:
            available = self.doc_searcher.list_available_cheatsheets()
            print(f"📋 Cheatsheets disponíveis: {', '.join(available)}")
            tool = input("📝 Qual ferramenta: ")
        
        cheatsheet = self.doc_searcher.get_cheatsheet(tool)
        formatted_cheatsheet = self.doc_searcher.format_cheatsheet(cheatsheet)
        print(f"\n{formatted_cheatsheet}")
    
    # === MÉTODOS DE GERENCIAMENTO DE PACOTES ===
    def _package_info(self, matches):
        """Informações do pacote"""
        if len(matches) >= 3:
            package_name = matches[2]
        else:
            package_name = input("📝 Nome do pacote: ")
        
        print(f"🔍 Buscando informações de {package_name}...")
        info = self.package_manager.search_package(package_name)
        formatted_info = self.package_manager.format_package_info(info)
        print(f"\n{formatted_info}")
    
    def _install_package(self, matches):
        """Instala pacote"""
        if len(matches) >= 3:
            package_name = matches[2]
        else:
            package_name = input("📝 Nome do pacote: ")
        
        dev = input("📝 É dependência de desenvolvimento? (s/n): ").lower().startswith('s')
        
        print(f"📦 Instalando {package_name}...")
        result = self.package_manager.install_package(package_name, dev=dev)
        
        if result.get('success'):
            print(f"✅ {package_name} instalado com sucesso!")
        else:
            print(f"❌ Erro: {result.get('error', 'Falha na instalação')}")
    
    def _search_package(self, matches):
        """Busca pacotes"""
        if len(matches) >= 3:
            query = matches[2]
        else:
            query = input("📝 Buscar por: ")
        
        print(f"🔍 Buscando pacotes: {query}...")
        results = self.package_manager.search_package(query)
        formatted_results = self.package_manager.format_package_info(results)
        print(f"\n{formatted_results}")
    
    def _list_packages(self):
        """Lista pacotes instalados"""
        print("📦 Listando pacotes instalados...")
        packages = self.package_manager.list_installed_packages()
        
        if 'error' in packages:
            print(f"❌ {packages['error']}")
            return
        
        if packages.get('registry') == 'npm':
            deps = packages.get('dependencies', {})
            dev_deps = packages.get('devDependencies', {})
            
            print(f"\n📦 Dependências ({len(deps)}):")
            for name, version in deps.items():
                print(f"   • {name}: {version}")
            
            if dev_deps:
                print(f"\n🔧 Dependências de desenvolvimento ({len(dev_deps)}):")
                for name, version in dev_deps.items():
                    print(f"   • {name}: {version}")
        
        elif packages.get('registry') == 'pypi':
            pkg_list = packages.get('packages', {})
            print(f"\n🐍 Pacotes Python ({len(pkg_list)}):")
            for name, version in list(pkg_list.items())[:20]:  # Primeiros 20
                print(f"   • {name}: {version}")
            if len(pkg_list) > 20:
                print(f"   ... e mais {len(pkg_list) - 20} pacotes")
    
    # === MÉTODOS DE GERENCIAMENTO DE TAREFAS ===
    def _create_task(self, matches):
        """Cria nova tarefa"""
        if len(matches) >= 3:
            title = matches[2]
        else:
            title = input("📝 Título da tarefa: ")
        
        description = input("📝 Descrição (opcional): ")
        priority = input("📝 Prioridade (low/medium/high/urgent): ") or "medium"
        
        task = self.task_manager.create_task(title, description, priority)
        print(f"✅ Tarefa criada: [{task.id}] {task.title}")
    
    def _list_tasks(self):
        """Lista tarefas"""
        status_filter = input("📝 Filtrar por status (todo/doing/done, Enter para todos): ") or None
        tasks = self.task_manager.list_tasks(status=status_filter)
        
        formatted_list = self.task_manager.format_task_list(tasks)
        print(f"\n{formatted_list}")
    
    def _complete_task(self, matches):
        """Completa tarefa"""
        if len(matches) >= 3:
            task_id = matches[2]
        else:
            task_id = input("📝 ID da tarefa: ")
        
        success = self.task_manager.update_task_status(task_id, "done")
        if success:
            print(f"✅ Tarefa {task_id} marcada como concluída!")
        else:
            print(f"❌ Tarefa {task_id} não encontrada")
    
    def _task_statistics(self):
        """Mostra estatísticas das tarefas"""
        stats = self.task_manager.get_statistics()
        formatted_stats = self.task_manager.format_statistics(stats)
        print(f"\n{formatted_stats}")
        
        # Mostrar tarefas urgentes
        overdue = self.task_manager.get_overdue_tasks()
        if overdue:
            print(f"\n⏰ Tarefas atrasadas ({len(overdue)}):")
            for task in overdue[:5]:
                print(f"   {self.task_manager.format_task(task)}")
    
    def _search_tasks(self, matches):
        """Busca tarefas"""
        if len(matches) >= 3:
            query = matches[2]
        else:
            query = input("📝 Buscar por: ")
        
        tasks = self.task_manager.search_tasks(query)
        formatted_list = self.task_manager.format_task_list(tasks)
        print(f"\n{formatted_list}")
    
    # === MÉTODOS EXPANDIDOS ===
    def _generate_fake_data_advanced(self):
        """Geração avançada de dados falsos"""
        print("\n🎭 Tipos de dados disponíveis:")
        print("1. 👤 Nomes")
        print("2. 📧 Emails") 
        print("3. 📱 Telefones")
        print("4. 🏠 Endereços")
        print("5. 🏢 Empresas")
        print("6. 📝 Lorem ipsum")
        print("7. 🔢 Números")
        print("8. 🗂️  JSON estruturado")
        
        choice = input("\n📝 Escolha (1-8) ou Enter para mix: ")
        
        if choice == "1":
            self._generate_names()
        elif choice == "2":
            self._generate_emails()
        elif choice == "3":
            self._generate_phones()
        elif choice == "4":
            self._generate_addresses()
        elif choice == "5":
            self._generate_companies()
        elif choice == "6":
            self._generate_lorem()
        elif choice == "7":
            self._generate_numbers()
        elif choice == "8":
            self._generate_json_data()
        else:
            # Mix de dados
            self._generate_fake_data()
    
    def _generate_names(self):
        """Gera nomes falsos"""
        nomes = FAKE_DATA['nomes']
        sobrenomes = FAKE_DATA['sobrenomes']
        
        print("\n👤 Nomes Gerados:")
        for _ in range(5):
            nome_completo = f"{random.choice(nomes)} {random.choice(sobrenomes)}"
            print(f"   • {nome_completo}")
    
    def _generate_emails(self):
        """Gera emails falsos"""
        nomes = FAKE_DATA['nomes']
        sobrenomes = FAKE_DATA['sobrenomes']
        dominios = FAKE_DATA['dominios_email']
        
        print("\n📧 Emails Gerados:")
        for _ in range(5):
            nome = random.choice(nomes).lower().replace(' ', '')
            sobrenome = random.choice(sobrenomes).lower()
            dominio = random.choice(dominios)
            
            # Variações de formato
            formats = [
                f"{nome}.{sobrenome}@{dominio}",
                f"{nome}{sobrenome}@{dominio}",
                f"{nome[0]}.{sobrenome}@{dominio}",
                f"{nome}_{sobrenome}@{dominio}"
            ]
            
            email = random.choice(formats)
            print(f"   • {email}")
    
    def _generate_phones(self):
        """Gera telefones falsos"""
        ddds = FAKE_DATA['ddd_telefones']
        
        print("\n📱 Telefones Gerados:")
        for _ in range(5):
            ddd = random.choice(ddds)
            numero = f"9{random.randint(1000,9999)}-{random.randint(1000,9999)}"
            celular = f"({ddd}) {numero}"
            print(f"   • {celular}")
    
    def _generate_addresses(self):
        """Gera endereços falsos"""
        ruas = ["Rua das Flores", "Av. Paulista", "Rua Augusta", "Rua Oscar Freire", "Av. Faria Lima"]
        cidades = ["São Paulo", "Rio de Janeiro", "Belo Horizonte", "Brasília", "Salvador"]
        
        print("\n🏠 Endereços Gerados:")
        for _ in range(3):
            rua = random.choice(ruas)
            numero = random.randint(1, 9999)
            cidade = random.choice(cidades)
            cep = f"{random.randint(10000,99999)}-{random.randint(100,999)}"
            
            endereco = f"{rua}, {numero} - {cidade} - CEP: {cep}"
            print(f"   • {endereco}")
    
    def _generate_companies(self):
        """Gera empresas falsas"""
        tipos = ["Tech", "Solutions", "Systems", "Digital", "Software", "Data"]
        sufixos = ["Ltda", "S.A.", "EIRELI", "ME"]
        
        print("\n🏢 Empresas Geradas:")
        for _ in range(3):
            nome = f"{random.choice(FAKE_DATA['sobrenomes'])} {random.choice(tipos)}"
            sufixo = random.choice(sufixos)
            empresa = f"{nome} {sufixo}"
            print(f"   • {empresa}")
    
    def _generate_lorem(self):
        """Gera texto lorem ipsum"""
        palavras = ["lorem", "ipsum", "dolor", "sit", "amet", "consectetur", "adipiscing", "elit",
                   "sed", "do", "eiusmod", "tempor", "incididunt", "ut", "labore", "et", "dolore"]
        
        print("\n📝 Lorem Ipsum Gerado:")
        for _ in range(3):
            frase = " ".join(random.choices(palavras, k=random.randint(8, 15)))
            print(f"   • {frase.capitalize()}.")
    
    def _generate_numbers(self):
        """Gera números aleatórios"""
        print("\n🔢 Números Gerados:")
        print(f"   • Inteiro: {random.randint(1, 1000000)}")
        print(f"   • Decimal: {random.uniform(0, 100):.2f}")
        print(f"   • Percentual: {random.randint(0, 100)}%")
        print(f"   • Moeda: R$ {random.uniform(10, 10000):.2f}")
    
    def _generate_json_data(self):
        """Gera dados JSON estruturados"""
        nome = random.choice(FAKE_DATA['nomes'])
        sobrenome = random.choice(FAKE_DATA['sobrenomes'])
        
        fake_user = {
            "id": random.randint(1, 99999),
            "nome": f"{nome} {sobrenome}",
            "email": f"{nome.lower()}.{sobrenome.lower()}@{random.choice(FAKE_DATA['dominios_email'])}",
            "idade": random.randint(18, 70),
            "ativo": random.choice([True, False]),
            "criado_em": datetime.now().isoformat()
        }
        
        print("\n🗂️  JSON Gerado:")
        print(json.dumps(fake_user, indent=2, ensure_ascii=False))
    
    def _show_help_advanced(self):
        """Mostra ajuda avançada com todas as funcionalidades"""
        commands = self.jarvis_ai.get_available_commands()
        
        print(f"\n📚 {APP_NAME} v{APP_VERSION} - Comandos Disponíveis:\n")
        
        for category, command_list in commands.items():
            print(f"📂 {category}:")
            for command in command_list:
                print(f"   • {command}")
            print()
        
        # Adiciona comandos de documentos
        print("📂 Manipulação de Documentos:")
        print("   • criar excel planilha.xlsx - Cria arquivo Excel")
        print("   • ler excel dados.xlsx - Lê arquivo Excel")
        print("   • limpar excel arquivo.xlsx - Remove linhas/colunas vazias")
        print("   • converter excel dados.xlsx - Converte Excel para CSV")
        print("   • info excel planilha.xlsx - Informações do arquivo")
        print("   • criar word documento.docx - Cria documento Word")
        print("   • ler word arquivo.docx - Lê documento Word")
        print("   • extrair texto documento.docx - Extrai texto para .txt")
        print("   • substituir \"old\" por \"new\" em doc.docx - Busca e substitui")
        print("   • criar ppt apresentacao.pptx - Cria PowerPoint")
        print("   • adicionar slide apresentacao.pptx - Adiciona slide")
        print("   • gerar ppt do excel dados.xlsx - Gera slides do Excel")
        print("   • gerar ppt do json template.json - Gera slides do JSON")
        print("   • template ppt json - Cria template JSON")
        print("   • dados exemplo excel 100 - Gera dados para teste")
        print()
        
        print("💡 Dicas:")
        print("   • Fale naturalmente: 'criar um projeto react chamado minha-app'")
        print("   • Use 'help <categoria>' para ajuda específica")
        print("   • Digite 'sair' para encerrar")
    
    def _show_version(self):
        """Mostra informações de versão"""
        print(f"\n🤖 {APP_NAME} v{APP_VERSION}")
        print(f"📅 Data: {datetime.now().strftime('%d/%m/%Y')}")
        print(f"🐍 Python: {sys.version.split()[0]}")
        print(f"📁 Diretório: {os.getcwd()}")
    
    def _show_project_status(self):
        """Mostra status completo do projeto"""
        print("\n📊 Status do Projeto:")
        
        # Git status
        if self.git_manager.is_git_repo():
            git_status = self.git_manager.get_status()
            branch = git_status.get('branch', 'N/A')
            print(f"🌳 Git: {branch}")
            
            if git_status.get('modified') or git_status.get('untracked'):
                print(f"📝 Mudanças pendentes: {len(git_status.get('modified', [])) + len(git_status.get('untracked', []))}")
        else:
            print("🌳 Git: Não é um repositório")
        
        # Tarefas
        task_stats = self.task_manager.get_statistics()
        if task_stats['total'] > 0:
            todo_count = task_stats.get('by_status', {}).get('todo', 0)
            done_count = task_stats.get('by_status', {}).get('done', 0)
            print(f"📝 Tarefas: {todo_count} pendentes, {done_count} concluídas")
        
        # Pacotes (se aplicável)
        packages = self.package_manager.list_installed_packages()
        if not packages.get('error'):
            total_packages = packages.get('total', 0)
            print(f"📦 Pacotes: {total_packages} instalados")
        
        print(f"📁 Arquivos: {len([f for f in os.listdir('.') if os.path.isfile(f)])}")
    
    def _handle_contextual_action(self, processed_input):
        """Lida com ações contextuais baseadas na categoria detectada"""
        category = processed_input['category']
        original_input = processed_input['original_input']
        
        print(f"🤔 Detectei que você quer trabalhar com {category.replace('_', ' ')}")
        
        if category == 'code_generation':
            print("💡 Posso ajudar a criar projetos, componentes ou snippets de código")
            self._show_code_generation_help()
        elif category == 'git_operations':
            print("💡 Posso ajudar com Git: status, commits, branches, etc.")
            self._git_status_advanced()
        elif category == 'documentation':
            print("💡 Posso pesquisar documentação ou mostrar cheatsheets")
            self._show_documentation_help()
        elif category == 'package_management':
            print("💡 Posso buscar, instalar ou listar pacotes")
            self._show_package_help()
        elif category == 'task_management':
            print("💡 Posso gerenciar suas tarefas e to-dos")
            self._list_tasks()
        else:
            self._show_suggestions_advanced(original_input)
    
    def _show_code_generation_help(self):
        """Ajuda específica para geração de código"""
        print("\n💻 Geração de Código:")
        print("   • criar projeto python meu_projeto")
        print("   • criar projeto react minha_app") 
        print("   • criar componente Button react")
        print("   • gerar snippet python function")
    
    def _show_documentation_help(self):
        """Ajuda específica para documentação"""
        print("\n📚 Documentação:")
        print("   • docs python requests")
        print("   • docs react hooks")
        print("   • cheatsheet git")
        print("   • cheatsheet docker")
    
    def _show_package_help(self):
        """Ajuda específica para pacotes"""
        print("\n📦 Gerenciamento de Pacotes:")
        print("   • package info express")
        print("   • instalar pacote lodash")
        print("   • buscar pacote pandas")
        print("   • listar pacotes")
    
    def _get_context_info(self) -> str:
        """Retorna informações contextuais para mostrar no prompt"""
        info_parts = []
        
        # Branch do Git
        if self.git_manager.is_git_repo():
            branch = self.git_manager.get_current_branch()
            if branch != "N/A":
                info_parts.append(f"🌳 {branch}")
        
        # Tarefas pendentes
        todo_tasks = self.task_manager.list_tasks(status="todo")
        if todo_tasks:
            info_parts.append(f"📝 {len(todo_tasks)} tarefas")
        
        return " | ".join(info_parts) if info_parts else ""
    
    def _show_suggestions_advanced(self, input_text: str):
        """Mostra sugestões avançadas para comando não reconhecido"""
        suggestions = self.jarvis_ai.get_suggestions(input_text)
        
        if suggestions:
            print("\n💡 Talvez você quis dizer:")
            for i, suggestion in enumerate(suggestions, 1):
                print(f"  {i}. {suggestion}")
        else:
            print("\n💡 Comandos populares:")
            popular = [
                "criar projeto python meu_projeto",
                "git status",
                "docs python requests", 
                "package info express",
                "criar tarefa 'nova feature'",
                "gerar dados falsos",
                "help"
            ]
            for i, cmd in enumerate(popular, 1):
                print(f"  {i}. {cmd}")
        
        print(f"\n📚 Digite 'help' para ver todos os comandos disponíveis")
    
    # Métodos originais mantidos
    def _create_file(self, matches):
        """Cria um arquivo (método original expandido)"""
        filename = matches[2] if len(matches) > 2 else input("📝 Nome do arquivo: ")
        
        try:
            # Conteúdo baseado em templates da configuração
            content = self._get_default_content(filename)
            
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"✅ Arquivo '{filename}' criado com sucesso!")
            
            # Sugerir próximos passos
            ext = filename.split('.')[-1].lower() if '.' in filename else ''
            if ext == 'py':
                print("💡 Execute: python " + filename)
            elif ext in ['js', 'jsx']:
                print("💡 Execute: node " + filename)
            
        except Exception as e:
            print(f"❌ Erro criando arquivo: {e}")
    
    def _get_default_content(self, filename: str) -> str:
        """Retorna conteúdo padrão baseado na extensão do arquivo"""
        ext = filename.split('.')[-1].lower() if '.' in filename else 'txt'
        
        # Preparar variáveis para o template
        template_vars = {
            'filename': filename,
            'title': filename.replace('.md', '').replace('_', ' ').title(),
            'name': filename.split('.')[0],
            'datetime': datetime.now().strftime('%d/%m/%Y %H:%M:%S')
        }
        
        # Buscar template na configuração
        template = FILE_TEMPLATES.get(ext, FILE_TEMPLATES['txt'])
        
        try:
            return template.format(**template_vars)
        except KeyError as e:
            # Se alguma variável estiver faltando, usar template simples
            return f"# {filename}\n\nArquivo criado pelo Jarvis CLI em {template_vars['datetime']}\n"
    
    def _list_files(self):
        """Lista arquivos do diretório atual (método original)"""
        try:
            files = []
            dirs = []
            
            for item in os.listdir('.'):
                if os.path.isdir(item):
                    dirs.append(item)
                else:
                    files.append(item)
            
            print("\n📁 Diretórios:")
            for d in sorted(dirs):
                print(f"  📂 {d}/")
            
            print("\n📄 Arquivos:")
            for f in sorted(files):
                size = os.path.getsize(f)
                print(f"  📄 {f} ({self._format_size(size)})")
                
        except Exception as e:
            print(f"❌ Erro listando arquivos: {e}")
    
    # Manter outros métodos originais...
    def _generate_fake_data(self):
        """Gera dados falsos simples (método original mantido)"""
        print("\n🎭 Dados Falsos Gerados:")
        
        # Usar dados da configuração
        nomes = FAKE_DATA['nomes']
        sobrenomes = FAKE_DATA['sobrenomes']
        dominios = FAKE_DATA['dominios_email']
        ddds = FAKE_DATA['ddd_telefones']
        
        print("👤 Nomes:")
        for _ in range(3):
            nome_completo = f"{random.choice(nomes)} {random.choice(sobrenomes)}"
            print(f"  • {nome_completo}")
        
        print("\n📧 Emails:")
        for _ in range(3):
            nome = random.choice(nomes).lower()
            sobrenome = random.choice(sobrenomes).lower()
            dominio = random.choice(dominios)
            email = f"{nome}.{sobrenome}@{dominio}"
            print(f"  • {email}")
        
        print("\n📱 Telefones:")
        for _ in range(3):
            ddd = random.choice(ddds)
            numero = f"9{random.randint(1000,9999)}-{random.randint(1000,9999)}"
            telefone = f"({ddd}) {numero}"
            print(f"  • {telefone}")
    
    def _show_datetime(self):
        """Mostra data e hora atual"""
        now = datetime.now()
        print(f"\n🕐 Data e Hora: {now.strftime('%d/%m/%Y %H:%M:%S')}")
        print(f"📅 Dia da semana: {self._get_weekday_pt(now.weekday())}")
    
    def _show_system_info(self):
        """Mostra informações do sistema"""
        print(f"\n💻 Sistema Operacional: {os.name}")
        print(f"🏠 Diretório atual: {os.getcwd()}")
        print(f"👤 Usuário: {os.getenv('USERNAME', 'Desconhecido')}")
        print(f"🐍 Python: {sys.version.split()[0]}")
    
    def _clear_screen(self):
        """Limpa a tela"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def _show_welcome(self):
        """Mostra mensagem de boas-vindas"""
        print("=" * 70)
        print(f"🤖 {APP_NAME} v{APP_VERSION} - Assistente Inteligente Avançado")
        print("=" * 70)
        print("💡 Agora com geração de código, Git avançado, documentação e muito mais!")
        print("🚪 Digite 'help' para ver todos os comandos ou 'sair' para encerrar.")
        
        # Mostrar informações contextuais
        context = self._get_context_info()
        if context:
            print(f"📍 Status: {context}")
    
    def _format_size(self, size_bytes: int) -> str:
        """Formata tamanho do arquivo"""
        if size_bytes < 1024:
            return f"{size_bytes} B"
        elif size_bytes < 1024 * 1024:
            return f"{size_bytes / 1024:.1f} KB"
        else:
            return f"{size_bytes / (1024 * 1024):.1f} MB"
    
    def _get_weekday_pt(self, weekday: int) -> str:
        """Retorna dia da semana em português"""
        days = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"]
        return days[weekday]
    
    # ===============================
    # MANIPULAÇÃO DE DOCUMENTOS
    # ===============================
    
    def create_excel(self, user_input: str) -> bool:
        """Cria arquivo Excel"""
        try:
            # Extrai nome do arquivo
            parts = user_input.split()
            filename = None
            for part in parts:
                if part.endswith('.xlsx') or part.endswith('.xls'):
                    filename = part
                    break
            
            if not filename:
                filename = "planilha_" + datetime.now().strftime("%Y%m%d_%H%M%S") + ".xlsx"
            
            # Dados de exemplo básicos
            sample_data = {
                "ID": [1, 2, 3, 4, 5],
                "Nome": ["João", "Maria", "Pedro", "Ana", "Carlos"],
                "Idade": [25, 30, 35, 28, 42],
                "Cidade": ["São Paulo", "Rio de Janeiro", "Belo Horizonte", "Brasília", "Salvador"]
            }
            
            return self.excel_manager.create_excel(filename, sample_data)
            
        except Exception as e:
            print(f"❌ Erro ao criar Excel: {str(e)}")
            return False
    
    def read_excel(self, user_input: str) -> bool:
        """Lê arquivo Excel"""
        try:
            parts = user_input.split()
            filename = None
            for part in parts:
                if part.endswith('.xlsx') or part.endswith('.xls'):
                    filename = part
                    break
            
            if not filename:
                print("❌ Nome do arquivo Excel não especificado")
                return False
            
            df = self.excel_manager.read_excel(filename)
            return df is not None
            
        except Exception as e:
            print(f"❌ Erro ao ler Excel: {str(e)}")
            return False
    
    def clean_excel(self, user_input: str) -> bool:
        """Limpa arquivo Excel"""
        try:
            parts = user_input.split()
            filename = None
            for part in parts:
                if part.endswith('.xlsx') or part.endswith('.xls'):
                    filename = part
                    break
            
            if not filename:
                print("❌ Nome do arquivo Excel não especificado")
                return False
            
            return self.excel_manager.clean_excel(filename)
            
        except Exception as e:
            print(f"❌ Erro ao limpar Excel: {str(e)}")
            return False
    
    def convert_excel_csv(self, user_input: str) -> bool:
        """Converte Excel para CSV ou vice-versa"""
        try:
            if "excel" in user_input.lower() and "csv" in user_input.lower():
                parts = user_input.split()
                files = [p for p in parts if p.endswith(('.xlsx', '.xls', '.csv'))]
                
                if len(files) >= 1:
                    input_file = files[0]
                    
                    if input_file.endswith(('.xlsx', '.xls')):
                        # Excel para CSV
                        return self.excel_manager.excel_to_csv(input_file)
                    elif input_file.endswith('.csv'):
                        # CSV para Excel
                        return self.excel_manager.csv_to_excel(input_file)
            
            print("❌ Especifique o arquivo para conversão")
            return False
            
        except Exception as e:
            print(f"❌ Erro na conversão: {str(e)}")
            return False
    
    def excel_info(self, user_input: str) -> bool:
        """Mostra informações do Excel"""
        try:
            parts = user_input.split()
            filename = None
            for part in parts:
                if part.endswith('.xlsx') or part.endswith('.xls'):
                    filename = part
                    break
            
            if not filename:
                print("❌ Nome do arquivo Excel não especificado")
                return False
            
            info = self.excel_manager.get_excel_info(filename)
            if info:
                print(f"📊 Informações do Excel: {info['filename']}")
                print(f"   Tamanho: {info['size']}")
                print(f"   Linhas: {info['rows']}")
                print(f"   Colunas: {info['columns']}")
                print(f"   Planilhas: {', '.join(info['sheets'])}")
                return True
            return False
            
        except Exception as e:
            print(f"❌ Erro ao obter informações: {str(e)}")
            return False
    
    def create_word(self, user_input: str) -> bool:
        """Cria documento Word"""
        try:
            parts = user_input.split()
            filename = None
            for part in parts:
                if part.endswith('.docx') or part.endswith('.doc'):
                    filename = part
                    break
            
            if not filename:
                filename = "documento_" + datetime.now().strftime("%Y%m%d_%H%M%S") + ".docx"
            
            title = "Documento criado pelo Jarvis CLI"
            content = "Este é um documento de exemplo criado automaticamente."
            
            return self.word_manager.create_document(filename, title, content)
            
        except Exception as e:
            print(f"❌ Erro ao criar documento Word: {str(e)}")
            return False
    
    def read_word(self, user_input: str) -> bool:
        """Lê documento Word"""
        try:
            parts = user_input.split()
            filename = None
            for part in parts:
                if part.endswith('.docx') or part.endswith('.doc'):
                    filename = part
                    break
            
            if not filename:
                print("❌ Nome do arquivo Word não especificado")
                return False
            
            content = self.word_manager.read_document(filename)
            if content:
                print(f"\n📄 Conteúdo do documento:")
                print("=" * 50)
                print(content[:500] + "..." if len(content) > 500 else content)
                print("=" * 50)
                return True
            return False
            
        except Exception as e:
            print(f"❌ Erro ao ler documento Word: {str(e)}")
            return False
    
    def extract_text(self, user_input: str) -> bool:
        """Extrai texto de documento"""
        try:
            parts = user_input.split()
            filename = None
            for part in parts:
                if part.endswith(('.docx', '.doc', '.pptx', '.ppt')):
                    filename = part
                    break
            
            if not filename:
                print("❌ Nome do arquivo não especificado")
                return False
            
            if filename.endswith(('.docx', '.doc')):
                return self.word_manager.extract_to_text(filename)
            elif filename.endswith(('.pptx', '.ppt')):
                return self.powerpoint_manager.extract_text(filename)
            
            return False
            
        except Exception as e:
            print(f"❌ Erro ao extrair texto: {str(e)}")
            return False
    
    def find_replace(self, user_input: str) -> bool:
        """Busca e substitui texto em documento"""
        try:
            # Parse do comando: substituir "texto1" por "texto2" em arquivo.docx
            parts = user_input.lower().split()
            
            # Encontra arquivo
            filename = None
            for part in user_input.split():
                if part.endswith(('.docx', '.doc')):
                    filename = part
                    break
            
            if not filename:
                print("❌ Nome do arquivo não especificado")
                return False
            
            # Encontra textos (simplificado)
            if '"' in user_input:
                quoted_texts = []
                in_quote = False
                current_text = ""
                
                for char in user_input:
                    if char == '"':
                        if in_quote:
                            quoted_texts.append(current_text)
                            current_text = ""
                        in_quote = not in_quote
                    elif in_quote:
                        current_text += char
                
                if len(quoted_texts) >= 2:
                    find_text = quoted_texts[0]
                    replace_text = quoted_texts[1]
                    return self.word_manager.find_and_replace(filename, find_text, replace_text)
            
            print("❌ Use o formato: substituir \"texto antigo\" por \"texto novo\" em arquivo.docx")
            return False
            
        except Exception as e:
            print(f"❌ Erro na substituição: {str(e)}")
            return False
    
    def create_ppt(self, user_input: str) -> bool:
        """Cria apresentação PowerPoint"""
        try:
            parts = user_input.split()
            filename = None
            for part in parts:
                if part.endswith('.pptx') or part.endswith('.ppt'):
                    filename = part
                    break
            
            if not filename:
                filename = "apresentacao_" + datetime.now().strftime("%Y%m%d_%H%M%S") + ".pptx"
            
            title = "Apresentação criada pelo Jarvis CLI"
            subtitle = "Gerada automaticamente"
            
            return self.powerpoint_manager.create_presentation(filename, title, subtitle)
            
        except Exception as e:
            print(f"❌ Erro ao criar apresentação: {str(e)}")
            return False
    
    def add_slide(self, user_input: str) -> bool:
        """Adiciona slide à apresentação"""
        try:
            parts = user_input.split()
            filename = None
            for part in parts:
                if part.endswith('.pptx') or part.endswith('.ppt'):
                    filename = part
                    break
            
            if not filename:
                print("❌ Nome do arquivo PowerPoint não especificado")
                return False
            
            slide_title = "Novo Slide"
            slide_content = "Conteúdo do slide adicionado pelo Jarvis CLI"
            
            return self.powerpoint_manager.add_slide(filename, slide_title, slide_content)
            
        except Exception as e:
            print(f"❌ Erro ao adicionar slide: {str(e)}")
            return False
    
    def generate_ppt_from_data(self, user_input: str) -> bool:
        """Gera PowerPoint a partir de dados"""
        try:
            parts = user_input.split()
            input_file = None
            output_file = None
            
            for part in parts:
                if part.endswith(('.xlsx', '.json')):
                    input_file = part
                elif part.endswith('.pptx'):
                    output_file = part
            
            if not input_file:
                print("❌ Arquivo de dados não especificado (.xlsx ou .json)")
                return False
            
            if not output_file:
                output_file = "apresentacao_gerada.pptx"
            
            if input_file.endswith('.xlsx'):
                return self.powerpoint_manager.generate_from_excel(input_file, output_file)
            elif input_file.endswith('.json'):
                return self.powerpoint_manager.generate_from_json(input_file, output_file)
            
            return False
            
        except Exception as e:
            print(f"❌ Erro ao gerar apresentação: {str(e)}")
            return False
    
    def ppt_template(self, user_input: str) -> bool:
        """Cria template JSON para PowerPoint"""
        try:
            return self.powerpoint_manager.create_template_json()
            
        except Exception as e:
            print(f"❌ Erro ao criar template: {str(e)}")
            return False
    
    def generate_sample_data(self, user_input: str) -> bool:
        """Gera dados de exemplo para Excel"""
        try:
            parts = user_input.split()
            filename = None
            rows = 100
            
            for part in parts:
                if part.endswith('.xlsx'):
                    filename = part
                elif part.isdigit():
                    rows = int(part)
            
            if not filename:
                filename = "dados_exemplo.xlsx"
            
            return self.excel_manager.generate_sample_data(filename, rows)
            
        except Exception as e:
            print(f"❌ Erro ao gerar dados de exemplo: {str(e)}")
            return False
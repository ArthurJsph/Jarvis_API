"""
Sistema de geração de código e boilerplates
"""

import os
import json
import yaml
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any
from jinja2 import Environment, FileSystemLoader, Template
import shutil

class CodeGenerator:
    """Gerador de código e estruturas de projeto"""
    
    def __init__(self, config_path: str = "jarvis.config.yml"):
        self.config = self._load_config(config_path)
        self.templates_dir = Path("templates")
        self.jinja_env = Environment(
            loader=FileSystemLoader(str(self.templates_dir)),
            trim_blocks=True,
            lstrip_blocks=True
        )
        
    def _load_config(self, config_path: str) -> Dict:
        """Carrega configuração do arquivo YAML"""
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            return self._get_default_config()
    
    def _get_default_config(self) -> Dict:
        """Retorna configuração padrão"""
        return {
            'code_generation': {
                'default_author': 'Jarvis CLI',
                'default_license': 'MIT',
                'supported_languages': ['python', 'javascript', 'react', 'nodejs']
            }
        }
    
    def create_project(self, project_type: str, project_name: str, 
                      description: str = "", output_dir: str = ".") -> bool:
        """
        Cria um novo projeto com boilerplate
        
        Args:
            project_type: Tipo do projeto (python, nodejs, react, etc.)
            project_name: Nome do projeto
            description: Descrição do projeto
            output_dir: Diretório de saída
        
        Returns:
            bool: True se criado com sucesso
        """
        try:
            project_path = Path(output_dir) / project_name
            
            # Verificar se projeto já existe
            if project_path.exists():
                print(f"❌ Projeto '{project_name}' já existe!")
                return False
            
            # Criar diretório do projeto
            project_path.mkdir(parents=True)
            
            # Variáveis do template
            template_vars = {
                'project_name': project_name,
                'description': description,
                'author': self.config.get('code_generation', {}).get('default_author', 'Jarvis CLI'),
                'license': self.config.get('code_generation', {}).get('default_license', 'MIT'),
                'date': datetime.now().strftime('%Y-%m-%d'),
                'year': datetime.now().year,
                'jarvis_version': self.config.get('app', {}).get('version', '2.1')
            }
            
            # Gerar arquivos baseados no tipo
            success = self._generate_project_files(project_type, project_path, template_vars)
            
            if success:
                print(f"✅ Projeto '{project_name}' criado com sucesso!")
                print(f"📁 Localização: {project_path.absolute()}")
                self._show_next_steps(project_type, project_name)
                return True
            else:
                # Limpar diretório se falhou
                shutil.rmtree(project_path, ignore_errors=True)
                return False
                
        except Exception as e:
            print(f"❌ Erro criando projeto: {e}")
            return False
    
    def _generate_project_files(self, project_type: str, project_path: Path, 
                               template_vars: Dict) -> bool:
        """Gera arquivos do projeto baseado no tipo"""
        
        generators = {
            'python': self._generate_python_project,
            'nodejs': self._generate_nodejs_project,
            'react': self._generate_react_project,
            'express': self._generate_express_project,
            'flask': self._generate_flask_project,
            'html': self._generate_html_project
        }
        
        generator = generators.get(project_type.lower())
        if not generator:
            print(f"❌ Tipo de projeto '{project_type}' não suportado!")
            print(f"💡 Tipos disponíveis: {', '.join(generators.keys())}")
            return False
        
        return generator(project_path, template_vars)
    
    def _generate_python_project(self, project_path: Path, vars: Dict) -> bool:
        """Gera projeto Python"""
        try:
            # Estrutura de diretórios
            (project_path / "src").mkdir()
            (project_path / "tests").mkdir()
            (project_path / "docs").mkdir()
            
            # Arquivos principais
            files_to_generate = [
                ('python/main.py.j2', 'main.py'),
                ('python/requirements.txt.j2', 'requirements.txt'),
                ('README.md.j2', 'README.md')
            ]
            
            for template_file, output_file in files_to_generate:
                self._render_template(template_file, project_path / output_file, vars)
            
            # Arquivos adicionais
            self._create_file(project_path / "__init__.py", "")
            self._create_file(project_path / "src" / "__init__.py", "")
            self._create_file(project_path / "tests" / "__init__.py", "")
            self._create_file(project_path / ".gitignore", self._get_python_gitignore())
            
            return True
            
        except Exception as e:
            print(f"❌ Erro gerando projeto Python: {e}")
            return False
    
    def _generate_nodejs_project(self, project_path: Path, vars: Dict) -> bool:
        """Gera projeto Node.js"""
        try:
            # Estrutura de diretórios
            (project_path / "src").mkdir()
            (project_path / "tests").mkdir()
            (project_path / "public").mkdir()
            
            # Arquivos principais
            files_to_generate = [
                ('nodejs/package.json.j2', 'package.json'),
                ('nodejs/index.js.j2', 'index.js'),
                ('README.md.j2', 'README.md')
            ]
            
            for template_file, output_file in files_to_generate:
                self._render_template(template_file, project_path / output_file, vars)
            
            # Arquivos adicionais
            self._create_file(project_path / ".env", "PORT=3000\nNODE_ENV=development")
            self._create_file(project_path / ".gitignore", self._get_nodejs_gitignore())
            
            return True
            
        except Exception as e:
            print(f"❌ Erro gerando projeto Node.js: {e}")
            return False
    
    def _generate_react_project(self, project_path: Path, vars: Dict) -> bool:
        """Gera projeto React"""
        try:
            # Estrutura de diretórios
            (project_path / "src").mkdir()
            (project_path / "src" / "components").mkdir()
            (project_path / "src" / "hooks").mkdir()
            (project_path / "src" / "utils").mkdir()
            (project_path / "public").mkdir()
            
            # Arquivos principais
            files_to_generate = [
                ('react/package.json.j2', 'package.json'),
                ('README.md.j2', 'README.md')
            ]
            
            for template_file, output_file in files_to_generate:
                self._render_template(template_file, project_path / output_file, vars)
            
            # Arquivos React específicos
            self._create_react_files(project_path, vars)
            self._create_file(project_path / ".gitignore", self._get_react_gitignore())
            
            return True
            
        except Exception as e:
            print(f"❌ Erro gerando projeto React: {e}")
            return False
    
    def _create_react_files(self, project_path: Path, vars: Dict):
        """Cria arquivos específicos do React"""
        
        # index.html
        html_content = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8" />
    <link rel="icon" type="image/svg+xml" href="/vite.svg" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>{vars['project_name']}</title>
</head>
<body>
    <div id="root"></div>
    <script type="module" src="/src/main.jsx"></script>
</body>
</html>"""
        self._create_file(project_path / "index.html", html_content)
        
        # vite.config.js
        vite_config = """import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
})"""
        self._create_file(project_path / "vite.config.js", vite_config)
        
        # src/main.jsx
        main_jsx = f"""import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.jsx'
import './index.css'

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
)"""
        self._create_file(project_path / "src" / "main.jsx", main_jsx)
        
        # src/App.jsx
        app_jsx = f"""import React from 'react'
import './App.css'

function App() {{
  return (
    <div className="App">
      <header className="App-header">
        <h1>🚀 {vars['project_name']}</h1>
        <p>Aplicação React criada pelo Jarvis CLI</p>
        <p>Autor: {vars['author']}</p>
      </header>
    </div>
  )
}}

export default App"""
        self._create_file(project_path / "src" / "App.jsx", app_jsx)
        
        # CSS básico
        app_css = """.App {
  text-align: center;
}

.App-header {
  background-color: #282c34;
  padding: 20px;
  color: white;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}"""
        self._create_file(project_path / "src" / "App.css", app_css)
        
        index_css = """body {
  margin: 0;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen',
    'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue',
    sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}"""
        self._create_file(project_path / "src" / "index.css", index_css)
    
    def _render_template(self, template_path: str, output_path: Path, vars: Dict):
        """Renderiza template Jinja2"""
        try:
            template = self.jinja_env.get_template(template_path)
            content = template.render(**vars)
            self._create_file(output_path, content)
        except Exception as e:
            print(f"⚠️ Erro renderizando template {template_path}: {e}")
            # Criar arquivo vazio se template falhar
            self._create_file(output_path, f"# Arquivo criado pelo Jarvis CLI\n# Template: {template_path}\n")
    
    def _create_file(self, file_path: Path, content: str):
        """Cria arquivo com conteúdo"""
        file_path.parent.mkdir(parents=True, exist_ok=True)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
    
    def _get_python_gitignore(self) -> str:
        """Retorna .gitignore para Python"""
        return """# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# Distribution / packaging
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# PyInstaller
*.manifest
*.spec

# Unit test / coverage reports
htmlcov/
.tox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
.hypothesis/
.pytest_cache/

# Environments
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# IDEs
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db
"""
    
    def _get_nodejs_gitignore(self) -> str:
        """Retorna .gitignore para Node.js"""
        return """# Dependencies
node_modules/
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# Runtime data
pids
*.pid
*.seed
*.pid.lock

# Coverage directory used by tools like istanbul
coverage/

# Build outputs
dist/
build/

# Environment variables
.env
.env.local
.env.development.local
.env.test.local
.env.production.local

# IDEs
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Logs
logs
*.log
"""
    
    def _get_react_gitignore(self) -> str:
        """Retorna .gitignore para React"""
        return self._get_nodejs_gitignore() + """
# React specific
.eslintcache
/build
/dist
"""
    
    def _show_next_steps(self, project_type: str, project_name: str):
        """Mostra próximos passos após criar projeto"""
        print(f"\n🎯 Próximos passos para {project_name}:")
        print(f"   cd {project_name}")
        
        if project_type.lower() in ['python']:
            print("   python -m venv venv")
            print("   venv\\Scripts\\activate  # Windows")
            print("   pip install -r requirements.txt")
            print("   python main.py")
            
        elif project_type.lower() in ['nodejs', 'express']:
            print("   npm install")
            print("   npm run dev")
            
        elif project_type.lower() == 'react':
            print("   npm install")
            print("   npm run dev")
            
        print(f"\n📚 Documentação: Veja o README.md do projeto")

    def create_component(self, component_type: str, component_name: str, 
                        language: str = "javascript") -> bool:
        """
        Cria um componente individual
        
        Args:
            component_type: Tipo do componente (react, vue, etc.)
            component_name: Nome do componente
            language: Linguagem (javascript, typescript)
        
        Returns:
            bool: True se criado com sucesso
        """
        try:
            if component_type.lower() == 'react':
                return self._create_react_component(component_name, language)
            else:
                print(f"❌ Tipo de componente '{component_type}' não suportado!")
                return False
                
        except Exception as e:
            print(f"❌ Erro criando componente: {e}")
            return False
    
    def _create_react_component(self, name: str, language: str) -> bool:
        """Cria componente React"""
        ext = "tsx" if language == "typescript" else "jsx"
        component_dir = Path("src/components")
        component_dir.mkdir(parents=True, exist_ok=True)
        
        # Arquivo do componente
        component_content = f"""import React from 'react';
import './{name}.css';

const {name} = () => {{
  return (
    <div className="{name.lower()}">
      <h2>{name} Component</h2>
      <p>Componente criado pelo Jarvis CLI</p>
    </div>
  );
}};

export default {name};
"""
        
        # Arquivo CSS
        css_content = f""".{name.lower()} {{
  padding: 20px;
  border: 1px solid #ddd;
  border-radius: 8px;
  margin: 10px;
}}

.{name.lower()} h2 {{
  color: #333;
  margin-bottom: 10px;
}}
"""
        
        component_file = component_dir / f"{name}.{ext}"
        css_file = component_dir / f"{name}.css"
        
        self._create_file(component_file, component_content)
        self._create_file(css_file, css_content)
        
        print(f"✅ Componente {name} criado com sucesso!")
        print(f"📁 Arquivos: {component_file}, {css_file}")
        
        return True

    def get_supported_types(self) -> List[str]:
        """Retorna tipos de projeto suportados"""
        return ['python', 'nodejs', 'react', 'express', 'flask', 'html', 'vue']

    def get_code_snippets(self, language: str, snippet_type: str) -> str:
        """Gera snippets de código comuns"""
        snippets = {
            'python': {
                'for_loop': '''for i in range(10):
    print(f"Item {i}")''',
                'function': '''def my_function(param1, param2):
    """
    Descrição da função
    
    Args:
        param1: Primeiro parâmetro
        param2: Segundo parâmetro
    
    Returns:
        Resultado da operação
    """
    return param1 + param2''',
                'class': '''class MyClass:
    """Classe de exemplo"""
    
    def __init__(self, name):
        self.name = name
    
    def greet(self):
        return f"Olá, {self.name}!"'''
            },
            'javascript': {
                'for_loop': '''for (let i = 0; i < 10; i++) {
    console.log(`Item ${i}`);
}''',
                'function': '''function myFunction(param1, param2) {
    // Descrição da função
    return param1 + param2;
}

// Ou arrow function
const myFunction = (param1, param2) => {
    return param1 + param2;
};''',
                'class': '''class MyClass {
    constructor(name) {
        this.name = name;
    }
    
    greet() {
        return `Olá, ${this.name}!`;
    }
}'''
            }
        }
        
        return snippets.get(language, {}).get(snippet_type, f"Snippet '{snippet_type}' não encontrado para {language}")
    
    # Métodos para outros tipos de projeto (flask, express, etc.)
    def _generate_flask_project(self, project_path: Path, vars: Dict) -> bool:
        """Gera projeto Flask"""
        # Implementação similar aos outros geradores
        pass
    
    def _generate_express_project(self, project_path: Path, vars: Dict) -> bool:
        """Gera projeto Express"""
        # Implementação similar aos outros geradores
        pass
    
    def _generate_html_project(self, project_path: Path, vars: Dict) -> bool:
        """Gera projeto HTML simples"""
        # Implementação similar aos outros geradores
        pass
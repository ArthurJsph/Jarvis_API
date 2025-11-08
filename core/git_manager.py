"""
Sistema avançado de integração com Git
"""

import os
import subprocess
from typing import List, Dict, Optional, Tuple
from pathlib import Path
import git
from datetime import datetime
import re

class GitManager:
    """Gerenciador avançado de Git"""
    
    def __init__(self):
        self.repo = None
        self.current_dir = Path.cwd()
        self._initialize_repo()
    
    def _initialize_repo(self):
        """Inicializa repositório Git se existir"""
        try:
            self.repo = git.Repo(search_parent_directories=True)
        except git.InvalidGitRepositoryError:
            self.repo = None
    
    def is_git_repo(self) -> bool:
        """Verifica se está em um repositório Git"""
        return self.repo is not None
    
    def get_status(self) -> Dict:
        """Retorna status detalhado do repositório"""
        if not self.is_git_repo():
            return {"error": "Não é um repositório Git"}
        
        try:
            status = {
                "branch": self.get_current_branch(),
                "remote": self.get_remote_url(),
                "ahead": 0,
                "behind": 0,
                "modified": [],
                "added": [],
                "deleted": [],
                "untracked": [],
                "conflicts": [],
                "stashes": len(list(self.repo.git.stash("list").split('\n'))) if self.repo.git.stash("list") else 0
            }
            
            # Arquivos modificados
            for item in self.repo.index.diff(None):
                if item.change_type == 'M':
                    status["modified"].append(item.a_path)
                elif item.change_type == 'D':
                    status["deleted"].append(item.a_path)
            
            # Arquivos staged
            for item in self.repo.index.diff("HEAD"):
                if item.change_type == 'A':
                    status["added"].append(item.a_path)
                elif item.change_type == 'M':
                    if item.a_path not in status["modified"]:
                        status["added"].append(item.a_path)
            
            # Arquivos não rastreados
            status["untracked"] = self.repo.untracked_files
            
            # Verificar commits ahead/behind
            try:
                tracking_branch = self.repo.active_branch.tracking_branch()
                if tracking_branch:
                    ahead_behind = self.repo.git.rev_list(
                        '--left-right', '--count',
                        f'{tracking_branch.name}...{self.repo.active_branch.name}'
                    ).split('\t')
                    status["behind"] = int(ahead_behind[0])
                    status["ahead"] = int(ahead_behind[1])
            except:
                pass
            
            return status
            
        except Exception as e:
            return {"error": str(e)}
    
    def get_current_branch(self) -> str:
        """Retorna branch atual"""
        if not self.is_git_repo():
            return "N/A"
        
        try:
            return self.repo.active_branch.name
        except:
            return "detached HEAD"
    
    def get_remote_url(self) -> str:
        """Retorna URL do remote"""
        if not self.is_git_repo():
            return "N/A"
        
        try:
            return self.repo.remotes.origin.url
        except:
            return "No remote"
    
    def list_branches(self, include_remote: bool = False) -> List[str]:
        """Lista branches"""
        if not self.is_git_repo():
            return []
        
        branches = []
        
        # Branches locais
        for branch in self.repo.branches:
            marker = "* " if branch == self.repo.active_branch else "  "
            branches.append(f"{marker}{branch.name}")
        
        # Branches remotas
        if include_remote:
            branches.append("\nRemote branches:")
            for remote in self.repo.remotes:
                for ref in remote.refs:
                    if not ref.name.endswith('/HEAD'):
                        branches.append(f"  {ref.name}")
        
        return branches
    
    def create_branch(self, branch_name: str, checkout: bool = True) -> bool:
        """Cria nova branch"""
        if not self.is_git_repo():
            print("❌ Não é um repositório Git")
            return False
        
        try:
            new_branch = self.repo.create_head(branch_name)
            if checkout:
                new_branch.checkout()
            print(f"✅ Branch '{branch_name}' criada{'e ativada' if checkout else ''}")
            return True
        except Exception as e:
            print(f"❌ Erro criando branch: {e}")
            return False
    
    def switch_branch(self, branch_name: str) -> bool:
        """Troca de branch"""
        if not self.is_git_repo():
            print("❌ Não é um repositório Git")
            return False
        
        try:
            self.repo.git.checkout(branch_name)
            print(f"✅ Trocado para branch '{branch_name}'")
            return True
        except Exception as e:
            print(f"❌ Erro trocando branch: {e}")
            return False
    
    def delete_branch(self, branch_name: str, force: bool = False) -> bool:
        """Deleta branch"""
        if not self.is_git_repo():
            print("❌ Não é um repositório Git")
            return False
        
        try:
            if branch_name == self.get_current_branch():
                print("❌ Não é possível deletar a branch atual")
                return False
            
            flag = "-D" if force else "-d"
            self.repo.git.branch(flag, branch_name)
            print(f"✅ Branch '{branch_name}' deletada")
            return True
        except Exception as e:
            print(f"❌ Erro deletando branch: {e}")
            return False
    
    def smart_commit(self, message: str = "", commit_type: str = "") -> bool:
        """Faz commit inteligente baseado nas mudanças"""
        if not self.is_git_repo():
            print("❌ Não é um repositório Git")
            return False
        
        try:
            status = self.get_status()
            
            # Se não há mudanças
            if not any([status.get("modified", []), status.get("untracked", []), 
                       status.get("deleted", [])]):
                print("ℹ️ Nenhuma mudança para commit")
                return False
            
            # Gerar mensagem automática se não fornecida
            if not message:
                message = self._generate_commit_message(status, commit_type)
            
            # Add all e commit
            self.repo.git.add(".")
            self.repo.index.commit(message)
            
            print(f"✅ Commit realizado: {message}")
            return True
            
        except Exception as e:
            print(f"❌ Erro no commit: {e}")
            return False
    
    def _generate_commit_message(self, status: Dict, commit_type: str) -> str:
        """Gera mensagem de commit automática"""
        
        # Tipos de commit convencionais
        if commit_type:
            prefix = f"{commit_type}: "
        else:
            # Tentar determinar tipo automaticamente
            modified = status.get("modified", [])
            added = status.get("untracked", [])
            deleted = status.get("deleted", [])
            
            if any("test" in f.lower() for f in modified + added):
                prefix = "test: "
            elif any(f.endswith(('.md', '.txt', '.rst')) for f in modified + added):
                prefix = "docs: "
            elif deleted:
                prefix = "refactor: "
            elif added:
                prefix = "feat: "
            else:
                prefix = "fix: "
        
        # Gerar descrição baseada nos arquivos
        files_summary = []
        if status.get("modified"):
            files_summary.append(f"modificados {len(status['modified'])} arquivos")
        if status.get("untracked"):
            files_summary.append(f"adicionados {len(status['untracked'])} arquivos")
        if status.get("deleted"):
            files_summary.append(f"removidos {len(status['deleted'])} arquivos")
        
        description = ", ".join(files_summary) if files_summary else "atualizações"
        
        return f"{prefix}{description}"
    
    def get_log(self, limit: int = 10, oneline: bool = True) -> List[str]:
        """Retorna log de commits"""
        if not self.is_git_repo():
            return ["Não é um repositório Git"]
        
        try:
            if oneline:
                log_format = "--oneline"
            else:
                log_format = "--format=fuller"
            
            commits = self.repo.git.log(f"--max-count={limit}", log_format).split('\n')
            return commits
            
        except Exception as e:
            return [f"Erro obtendo log: {e}"]
    
    def push(self, remote: str = "origin", branch: str = None) -> bool:
        """Push para remote"""
        if not self.is_git_repo():
            print("❌ Não é um repositório Git")
            return False
        
        try:
            if not branch:
                branch = self.get_current_branch()
            
            self.repo.git.push(remote, branch)
            print(f"✅ Push realizado para {remote}/{branch}")
            return True
            
        except Exception as e:
            print(f"❌ Erro no push: {e}")
            return False
    
    def pull(self, remote: str = "origin", branch: str = None) -> bool:
        """Pull do remote"""
        if not self.is_git_repo():
            print("❌ Não é um repositório Git")
            return False
        
        try:
            if not branch:
                branch = self.get_current_branch()
            
            self.repo.git.pull(remote, branch)
            print(f"✅ Pull realizado de {remote}/{branch}")
            return True
            
        except Exception as e:
            print(f"❌ Erro no pull: {e}")
            return False
    
    def clone_repo(self, url: str, directory: str = None) -> bool:
        """Clona repositório"""
        try:
            if not directory:
                # Extrair nome do repositório da URL
                directory = url.split('/')[-1].replace('.git', '')
            
            git.Repo.clone_from(url, directory)
            print(f"✅ Repositório clonado em {directory}")
            return True
            
        except Exception as e:
            print(f"❌ Erro clonando repositório: {e}")
            return False
    
    def stash(self, message: str = "", pop: bool = False) -> bool:
        """Gerencia stash"""
        if not self.is_git_repo():
            print("❌ Não é um repositório Git")
            return False
        
        try:
            if pop:
                self.repo.git.stash("pop")
                print("✅ Stash aplicado")
            else:
                if message:
                    self.repo.git.stash("save", message)
                else:
                    self.repo.git.stash()
                print("✅ Mudanças guardadas no stash")
            
            return True
            
        except Exception as e:
            print(f"❌ Erro com stash: {e}")
            return False
    
    def list_stashes(self) -> List[str]:
        """Lista stashes"""
        if not self.is_git_repo():
            return ["Não é um repositório Git"]
        
        try:
            stashes = self.repo.git.stash("list")
            return stashes.split('\n') if stashes else ["Nenhum stash encontrado"]
        except:
            return ["Erro listando stashes"]
    
    def diff(self, file_path: str = None, staged: bool = False) -> str:
        """Mostra diff das mudanças"""
        if not self.is_git_repo():
            return "Não é um repositório Git"
        
        try:
            if staged:
                if file_path:
                    return self.repo.git.diff("--cached", file_path)
                else:
                    return self.repo.git.diff("--cached")
            else:
                if file_path:
                    return self.repo.git.diff(file_path)
                else:
                    return self.repo.git.diff()
        except Exception as e:
            return f"Erro obtendo diff: {e}"
    
    def get_commit_types(self) -> List[str]:
        """Retorna tipos de commit convencionais"""
        return [
            "feat",     # Nova funcionalidade
            "fix",      # Correção de bug
            "docs",     # Documentação
            "style",    # Formatação, espaços em branco, etc.
            "refactor", # Refatoração de código
            "perf",     # Melhoria de performance
            "test",     # Testes
            "chore",    # Tarefas de build, etc.
            "ci",       # Integração contínua
            "build"     # Sistema de build
        ]
    
    def format_status_display(self, status: Dict) -> str:
        """Formata status para exibição"""
        if "error" in status:
            return f"❌ {status['error']}"
        
        lines = []
        lines.append(f"📂 Branch: {status['branch']}")
        lines.append(f"🌐 Remote: {status['remote']}")
        
        if status['ahead'] > 0:
            lines.append(f"⬆️  Ahead: {status['ahead']} commits")
        if status['behind'] > 0:
            lines.append(f"⬇️  Behind: {status['behind']} commits")
        
        if status['modified']:
            lines.append(f"📝 Modificados: {len(status['modified'])}")
            for file in status['modified'][:5]:  # Mostrar apenas primeiros 5
                lines.append(f"   • {file}")
            if len(status['modified']) > 5:
                lines.append(f"   ... e mais {len(status['modified']) - 5}")
        
        if status['added']:
            lines.append(f"✅ Staged: {len(status['added'])}")
            for file in status['added'][:5]:
                lines.append(f"   • {file}")
            if len(status['added']) > 5:
                lines.append(f"   ... e mais {len(status['added']) - 5}")
        
        if status['untracked']:
            lines.append(f"❓ Não rastreados: {len(status['untracked'])}")
            for file in status['untracked'][:5]:
                lines.append(f"   • {file}")
            if len(status['untracked']) > 5:
                lines.append(f"   ... e mais {len(status['untracked']) - 5}")
        
        if status['deleted']:
            lines.append(f"🗑️  Deletados: {len(status['deleted'])}")
            for file in status['deleted']:
                lines.append(f"   • {file}")
        
        if status['stashes'] > 0:
            lines.append(f"💾 Stashes: {status['stashes']}")
        
        if not any([status['modified'], status['added'], status['untracked'], status['deleted']]):
            lines.append("✨ Working directory clean")
        
        return '\n'.join(lines)
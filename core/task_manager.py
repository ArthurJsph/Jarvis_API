"""
Sistema de gerenciamento de tarefas (To-Do)
"""

import json
import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from pathlib import Path
from enum import Enum

class TaskPriority(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"

class TaskStatus(Enum):
    TODO = "todo"
    DOING = "doing" 
    DONE = "done"
    CANCELLED = "cancelled"

class Task:
    """Classe para representar uma tarefa"""
    
    def __init__(self, title: str, description: str = "", priority: TaskPriority = TaskPriority.MEDIUM):
        self.id = str(uuid.uuid4())[:8]
        self.title = title
        self.description = description
        self.priority = priority
        self.status = TaskStatus.TODO
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.due_date = None
        self.tags = []
        self.completed_at = None
    
    def to_dict(self) -> Dict:
        """Converte tarefa para dicionário"""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'priority': self.priority.value,
            'status': self.status.value,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'due_date': self.due_date.isoformat() if self.due_date else None,
            'tags': self.tags,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Task':
        """Cria tarefa a partir de dicionário"""
        task = cls(data['title'], data.get('description', ''))
        task.id = data['id']
        task.priority = TaskPriority(data.get('priority', 'medium'))
        task.status = TaskStatus(data.get('status', 'todo'))
        task.created_at = datetime.fromisoformat(data['created_at'])
        task.updated_at = datetime.fromisoformat(data['updated_at'])
        task.due_date = datetime.fromisoformat(data['due_date']) if data.get('due_date') else None
        task.tags = data.get('tags', [])
        task.completed_at = datetime.fromisoformat(data['completed_at']) if data.get('completed_at') else None
        return task
    
    def update_status(self, new_status: TaskStatus):
        """Atualiza status da tarefa"""
        self.status = new_status
        self.updated_at = datetime.now()
        
        if new_status == TaskStatus.DONE:
            self.completed_at = datetime.now()
        else:
            self.completed_at = None
    
    def set_due_date(self, due_date: datetime):
        """Define data de vencimento"""
        self.due_date = due_date
        self.updated_at = datetime.now()
    
    def add_tag(self, tag: str):
        """Adiciona tag à tarefa"""
        if tag not in self.tags:
            self.tags.append(tag)
            self.updated_at = datetime.now()
    
    def remove_tag(self, tag: str):
        """Remove tag da tarefa"""
        if tag in self.tags:
            self.tags.remove(tag)
            self.updated_at = datetime.now()
    
    def is_overdue(self) -> bool:
        """Verifica se a tarefa está atrasada"""
        if not self.due_date or self.status == TaskStatus.DONE:
            return False
        return datetime.now() > self.due_date

class TaskManager:
    """Gerenciador de tarefas"""
    
    def __init__(self, storage_file: str = "data/tasks.json"):
        self.storage_file = Path(storage_file)
        self.storage_file.parent.mkdir(parents=True, exist_ok=True)
        self.tasks = self._load_tasks()
    
    def _load_tasks(self) -> List[Task]:
        """Carrega tarefas do arquivo"""
        try:
            if self.storage_file.exists():
                with open(self.storage_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return [Task.from_dict(task_data) for task_data in data]
            return []
        except Exception as e:
            print(f"⚠️ Erro carregando tarefas: {e}")
            return []
    
    def _save_tasks(self):
        """Salva tarefas no arquivo"""
        try:
            with open(self.storage_file, 'w', encoding='utf-8') as f:
                data = [task.to_dict() for task in self.tasks]
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"⚠️ Erro salvando tarefas: {e}")
    
    def create_task(self, title: str, description: str = "", priority: str = "medium") -> Task:
        """
        Cria nova tarefa
        
        Args:
            title: Título da tarefa
            description: Descrição da tarefa
            priority: Prioridade (low, medium, high, urgent)
        
        Returns:
            Task: Tarefa criada
        """
        try:
            priority_enum = TaskPriority(priority.lower())
        except ValueError:
            priority_enum = TaskPriority.MEDIUM
        
        task = Task(title, description, priority_enum)
        self.tasks.append(task)
        self._save_tasks()
        
        return task
    
    def get_task(self, task_id: str) -> Optional[Task]:
        """Busca tarefa por ID"""
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None
    
    def list_tasks(self, status: str = None, priority: str = None, tag: str = None) -> List[Task]:
        """
        Lista tarefas com filtros opcionais
        
        Args:
            status: Filtrar por status
            priority: Filtrar por prioridade
            tag: Filtrar por tag
        
        Returns:
            List[Task]: Lista de tarefas filtradas
        """
        filtered_tasks = self.tasks.copy()
        
        if status:
            try:
                status_enum = TaskStatus(status.lower())
                filtered_tasks = [t for t in filtered_tasks if t.status == status_enum]
            except ValueError:
                pass
        
        if priority:
            try:
                priority_enum = TaskPriority(priority.lower())
                filtered_tasks = [t for t in filtered_tasks if t.priority == priority_enum]
            except ValueError:
                pass
        
        if tag:
            filtered_tasks = [t for t in filtered_tasks if tag in t.tags]
        
        # Ordenar por prioridade e data de criação
        priority_order = {TaskPriority.URGENT: 4, TaskPriority.HIGH: 3, TaskPriority.MEDIUM: 2, TaskPriority.LOW: 1}
        filtered_tasks.sort(key=lambda t: (priority_order[t.priority], t.created_at), reverse=True)
        
        return filtered_tasks
    
    def update_task_status(self, task_id: str, new_status: str) -> bool:
        """
        Atualiza status de uma tarefa
        
        Args:
            task_id: ID da tarefa
            new_status: Novo status
        
        Returns:
            bool: True se atualizado com sucesso
        """
        task = self.get_task(task_id)
        if not task:
            return False
        
        try:
            status_enum = TaskStatus(new_status.lower())
            task.update_status(status_enum)
            self._save_tasks()
            return True
        except ValueError:
            return False
    
    def delete_task(self, task_id: str) -> bool:
        """
        Deleta uma tarefa
        
        Args:
            task_id: ID da tarefa
        
        Returns:
            bool: True se deletado com sucesso
        """
        task = self.get_task(task_id)
        if task:
            self.tasks.remove(task)
            self._save_tasks()
            return True
        return False
    
    def edit_task(self, task_id: str, title: str = None, description: str = None, 
                  priority: str = None) -> bool:
        """
        Edita uma tarefa
        
        Args:
            task_id: ID da tarefa
            title: Novo título (opcional)
            description: Nova descrição (opcional)
            priority: Nova prioridade (opcional)
        
        Returns:
            bool: True se editado com sucesso
        """
        task = self.get_task(task_id)
        if not task:
            return False
        
        if title:
            task.title = title
        
        if description:
            task.description = description
        
        if priority:
            try:
                task.priority = TaskPriority(priority.lower())
            except ValueError:
                pass
        
        task.updated_at = datetime.now()
        self._save_tasks()
        return True
    
    def set_due_date(self, task_id: str, due_date: str) -> bool:
        """
        Define data de vencimento para uma tarefa
        
        Args:
            task_id: ID da tarefa
            due_date: Data no formato 'YYYY-MM-DD' ou 'YYYY-MM-DD HH:MM'
        
        Returns:
            bool: True se definido com sucesso
        """
        task = self.get_task(task_id)
        if not task:
            return False
        
        try:
            # Tentar diferentes formatos de data
            formats = ['%Y-%m-%d', '%Y-%m-%d %H:%M', '%d/%m/%Y', '%d/%m/%Y %H:%M']
            
            for fmt in formats:
                try:
                    parsed_date = datetime.strptime(due_date, fmt)
                    task.set_due_date(parsed_date)
                    self._save_tasks()
                    return True
                except ValueError:
                    continue
            
            return False
            
        except Exception:
            return False
    
    def add_tag_to_task(self, task_id: str, tag: str) -> bool:
        """
        Adiciona tag a uma tarefa
        
        Args:
            task_id: ID da tarefa
            tag: Tag a adicionar
        
        Returns:
            bool: True se adicionado com sucesso
        """
        task = self.get_task(task_id)
        if task:
            task.add_tag(tag)
            self._save_tasks()
            return True
        return False
    
    def remove_tag_from_task(self, task_id: str, tag: str) -> bool:
        """
        Remove tag de uma tarefa
        
        Args:
            task_id: ID da tarefa
            tag: Tag a remover
        
        Returns:
            bool: True se removido com sucesso
        """
        task = self.get_task(task_id)
        if task:
            task.remove_tag(tag)
            self._save_tasks()
            return True
        return False
    
    def get_overdue_tasks(self) -> List[Task]:
        """Retorna tarefas atrasadas"""
        return [task for task in self.tasks if task.is_overdue()]
    
    def get_tasks_due_today(self) -> List[Task]:
        """Retorna tarefas que vencem hoje"""
        today = datetime.now().date()
        return [task for task in self.tasks 
                if task.due_date and task.due_date.date() == today and task.status != TaskStatus.DONE]
    
    def get_tasks_due_this_week(self) -> List[Task]:
        """Retorna tarefas que vencem esta semana"""
        today = datetime.now().date()
        week_end = today + timedelta(days=7)
        return [task for task in self.tasks 
                if task.due_date and today <= task.due_date.date() <= week_end and task.status != TaskStatus.DONE]
    
    def get_statistics(self) -> Dict:
        """Retorna estatísticas das tarefas"""
        total = len(self.tasks)
        if total == 0:
            return {'total': 0}
        
        by_status = {}
        by_priority = {}
        overdue = 0
        
        for task in self.tasks:
            # Por status
            status_key = task.status.value
            by_status[status_key] = by_status.get(status_key, 0) + 1
            
            # Por prioridade
            priority_key = task.priority.value
            by_priority[priority_key] = by_priority.get(priority_key, 0) + 1
            
            # Atrasadas
            if task.is_overdue():
                overdue += 1
        
        return {
            'total': total,
            'by_status': by_status,
            'by_priority': by_priority,
            'overdue': overdue,
            'completion_rate': round((by_status.get('done', 0) / total) * 100, 1) if total > 0 else 0
        }
    
    def search_tasks(self, query: str) -> List[Task]:
        """
        Busca tarefas por texto
        
        Args:
            query: Texto a buscar
        
        Returns:
            List[Task]: Tarefas que contêm o texto
        """
        query = query.lower()
        results = []
        
        for task in self.tasks:
            if (query in task.title.lower() or 
                query in task.description.lower() or 
                any(query in tag.lower() for tag in task.tags)):
                results.append(task)
        
        return results
    
    def format_task(self, task: Task, show_details: bool = False) -> str:
        """Formata tarefa para exibição"""
        
        # Emojis por prioridade
        priority_emojis = {
            TaskPriority.LOW: "🟢",
            TaskPriority.MEDIUM: "🟡", 
            TaskPriority.HIGH: "🟠",
            TaskPriority.URGENT: "🔴"
        }
        
        # Emojis por status
        status_emojis = {
            TaskStatus.TODO: "⭕",
            TaskStatus.DOING: "🔵",
            TaskStatus.DONE: "✅",
            TaskStatus.CANCELLED: "❌"
        }
        
        priority_emoji = priority_emojis.get(task.priority, "⚪")
        status_emoji = status_emojis.get(task.status, "⚪")
        
        # Linha principal
        line = f"{status_emoji} {priority_emoji} [{task.id}] {task.title}"
        
        # Adicionar indicadores especiais
        if task.is_overdue():
            line += " ⏰"
        
        if task.due_date and not task.is_overdue() and task.status != TaskStatus.DONE:
            days_until = (task.due_date.date() - datetime.now().date()).days
            if days_until <= 1:
                line += " 📅"
        
        if task.tags:
            line += f" 🏷️ {','.join(task.tags)}"
        
        if show_details:
            details = []
            
            if task.description:
                details.append(f"   📝 {task.description}")
            
            details.append(f"   📊 Status: {task.status.value} | Prioridade: {task.priority.value}")
            
            if task.due_date:
                due_str = task.due_date.strftime('%d/%m/%Y %H:%M')
                details.append(f"   📅 Vence: {due_str}")
            
            details.append(f"   📆 Criado: {task.created_at.strftime('%d/%m/%Y %H:%M')}")
            
            if task.completed_at:
                details.append(f"   ✅ Concluído: {task.completed_at.strftime('%d/%m/%Y %H:%M')}")
            
            line += "\n" + "\n".join(details)
        
        return line
    
    def format_task_list(self, tasks: List[Task], show_details: bool = False) -> str:
        """Formata lista de tarefas para exibição"""
        if not tasks:
            return "📝 Nenhuma tarefa encontrada"
        
        lines = [f"📝 {len(tasks)} tarefa(s) encontrada(s):\n"]
        
        for task in tasks:
            lines.append(self.format_task(task, show_details))
        
        return "\n".join(lines)
    
    def format_statistics(self, stats: Dict) -> str:
        """Formata estatísticas para exibição"""
        if stats['total'] == 0:
            return "📊 Nenhuma tarefa cadastrada"
        
        lines = [
            f"📊 Estatísticas das Tarefas",
            f"📝 Total: {stats['total']}",
            f"✅ Taxa de conclusão: {stats['completion_rate']}%"
        ]
        
        if stats.get('overdue', 0) > 0:
            lines.append(f"⏰ Atrasadas: {stats['overdue']}")
        
        lines.append("\n📊 Por Status:")
        for status, count in stats.get('by_status', {}).items():
            emoji = {"todo": "⭕", "doing": "🔵", "done": "✅", "cancelled": "❌"}.get(status, "⚪")
            lines.append(f"   {emoji} {status.title()}: {count}")
        
        lines.append("\n🏷️ Por Prioridade:")
        for priority, count in stats.get('by_priority', {}).items():
            emoji = {"low": "🟢", "medium": "🟡", "high": "🟠", "urgent": "🔴"}.get(priority, "⚪")
            lines.append(f"   {emoji} {priority.title()}: {count}")
        
        return "\n".join(lines)
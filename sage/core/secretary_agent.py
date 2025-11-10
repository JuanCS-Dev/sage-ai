#!/usr/bin/env python3
"""
🤖 AGENTE SECRETÁRIA - Personal AI Assistant
================================================

Um assistente pessoal AI que:
- Organiza suas tarefas
- Acompanha seu trabalho
- Salva notas e contexto
- Conhece profundamente seus projetos
- Faz sugestões proativas
- Integra com ClickUp e GitHub

Autor: MAXIMUS AI
Data: 10 de Novembro de 2025
"""

import os
import json
import requests
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from anthropic import Anthropic
import sqlite3

# ============================================================================
# DATA MODELS
# ============================================================================

@dataclass
class Note:
    """Uma nota do usuário"""
    id: str
    content: str
    tags: List[str]
    project: str
    created_at: str
    updated_at: str
    priority: str  # low, medium, high, critical

@dataclass
class Task:
    """Uma tarefa do usuário"""
    id: str
    title: str
    description: str
    project: str
    status: str
    priority: str
    due_date: Optional[str]
    created_at: str
    clickup_id: Optional[str] = None
    github_issue_id: Optional[str] = None

@dataclass
class ProjectContext:
    """Contexto de um projeto"""
    name: str
    description: str
    github_repo: str
    clickup_list: str
    last_activity: str
    technologies: List[str]
    current_focus: str
    recent_commits: List[Dict]
    open_tasks: int
    notes_count: int

@dataclass
class DailyDigest:
    """Resumo diário"""
    date: str
    tasks_completed: int
    tasks_created: int
    commits_made: int
    notes_created: int
    projects_worked: List[str]
    summary: str
    suggestions: List[str]


# ============================================================================
# MEMORY SYSTEM - Banco de dados persistente
# ============================================================================

class MemorySystem:
    """Sistema de memória persistente do agente"""

    def __init__(self, db_path: str = "secretary_memory.db"):
        self.db_path = db_path
        self.init_database()

    def init_database(self):
        """Inicializa o banco de dados"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Tabela de notas
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS notes (
                id TEXT PRIMARY KEY,
                content TEXT,
                tags TEXT,
                project TEXT,
                created_at TEXT,
                updated_at TEXT,
                priority TEXT
            )
        """)

        # Tabela de tarefas
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id TEXT PRIMARY KEY,
                title TEXT,
                description TEXT,
                project TEXT,
                status TEXT,
                priority TEXT,
                due_date TEXT,
                created_at TEXT,
                clickup_id TEXT,
                github_issue_id TEXT
            )
        """)

        # Tabela de contexto de projetos
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS project_context (
                name TEXT PRIMARY KEY,
                description TEXT,
                github_repo TEXT,
                clickup_list TEXT,
                last_activity TEXT,
                technologies TEXT,
                current_focus TEXT,
                recent_commits TEXT,
                open_tasks INTEGER,
                notes_count INTEGER
            )
        """)

        # Tabela de conversas/interações
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                user_input TEXT,
                agent_response TEXT,
                context TEXT
            )
        """)

        # Tabela de resumos diários
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS daily_digests (
                date TEXT PRIMARY KEY,
                tasks_completed INTEGER,
                tasks_created INTEGER,
                commits_made INTEGER,
                notes_created INTEGER,
                projects_worked TEXT,
                summary TEXT,
                suggestions TEXT
            )
        """)

        conn.commit()
        conn.close()

    def save_note(self, note: Note):
        """Salva uma nota"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT OR REPLACE INTO notes
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            note.id, note.content, json.dumps(note.tags),
            note.project, note.created_at, note.updated_at, note.priority
        ))
        conn.commit()
        conn.close()

    def save_task(self, task: Task):
        """Salva uma tarefa"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT OR REPLACE INTO tasks
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            task.id, task.title, task.description, task.project,
            task.status, task.priority, task.due_date, task.created_at,
            task.clickup_id, task.github_issue_id
        ))
        conn.commit()
        conn.close()

    def get_all_notes(self, project: Optional[str] = None) -> List[Note]:
        """Busca todas as notas (opcionalmente filtradas por projeto)"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        if project:
            cursor.execute("SELECT * FROM notes WHERE project = ?", (project,))
        else:
            cursor.execute("SELECT * FROM notes")

        rows = cursor.fetchall()
        conn.close()

        return [
            Note(
                id=row[0], content=row[1], tags=json.loads(row[2]),
                project=row[3], created_at=row[4], updated_at=row[5],
                priority=row[6]
            )
            for row in rows
        ]

    def get_all_tasks(self, status: Optional[str] = None) -> List[Task]:
        """Busca todas as tarefas (opcionalmente filtradas por status)"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        if status:
            cursor.execute("SELECT * FROM tasks WHERE status = ?", (status,))
        else:
            cursor.execute("SELECT * FROM tasks")

        rows = cursor.fetchall()
        conn.close()

        return [
            Task(
                id=row[0], title=row[1], description=row[2],
                project=row[3], status=row[4], priority=row[5],
                due_date=row[6], created_at=row[7],
                clickup_id=row[8], github_issue_id=row[9]
            )
            for row in rows
        ]

    def save_conversation(self, user_input: str, agent_response: str, context: Dict):
        """Salva uma interação"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO conversations (timestamp, user_input, agent_response, context)
            VALUES (?, ?, ?, ?)
        """, (
            datetime.now().isoformat(),
            user_input,
            agent_response,
            json.dumps(context)
        ))
        conn.commit()
        conn.close()

    def get_recent_conversations(self, limit: int = 10) -> List[Dict]:
        """Busca conversas recentes para contexto"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM conversations
            ORDER BY id DESC
            LIMIT ?
        """, (limit,))
        rows = cursor.fetchall()
        conn.close()

        return [
            {
                "timestamp": row[1],
                "user_input": row[2],
                "agent_response": row[3],
                "context": json.loads(row[4])
            }
            for row in reversed(rows)
        ]


# ============================================================================
# CLICKUP INTEGRATION
# ============================================================================

class ClickUpIntegration:
    """Integração com ClickUp"""

    def __init__(self, api_token: str):
        self.api_token = api_token
        self.base_url = "https://api.clickup.com/api/v2"
        self.headers = {
            "Authorization": api_token,
            "Content-Type": "application/json"
        }

    def get_tasks(self, list_id: str) -> List[Dict]:
        """Busca tarefas de uma lista"""
        url = f"{self.base_url}/list/{list_id}/task"
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            return response.json().get("tasks", [])
        return []

    def create_task(self, list_id: str, name: str, description: str = "",
                   priority: int = 3) -> Optional[Dict]:
        """Cria uma tarefa no ClickUp"""
        url = f"{self.base_url}/list/{list_id}/task"
        data = {
            "name": name,
            "description": description,
            "priority": priority
        }
        response = requests.post(url, headers=self.headers, json=data)
        if response.status_code == 200:
            return response.json()
        return None

    def update_task_status(self, task_id: str, status: str) -> bool:
        """Atualiza status de uma tarefa"""
        url = f"{self.base_url}/task/{task_id}"
        data = {"status": status}
        response = requests.put(url, headers=self.headers, json=data)
        return response.status_code == 200


# ============================================================================
# GITHUB INTEGRATION
# ============================================================================

class GitHubIntegration:
    """Integração com GitHub"""

    def __init__(self, username: str):
        self.username = username
        self.base_url = "https://api.github.com"

    def get_recent_activity(self, days: int = 7) -> List[Dict]:
        """Busca atividade recente do usuário"""
        url = f"{self.base_url}/users/{self.username}/events"
        response = requests.get(url)
        if response.status_code == 200:
            events = response.json()
            cutoff = datetime.now() - timedelta(days=days)
            return [
                e for e in events
                if datetime.fromisoformat(e["created_at"].replace("Z", "+00:00")) > cutoff
            ]
        return []

    def get_repo_commits(self, repo: str, days: int = 7) -> List[Dict]:
        """Busca commits recentes de um repositório"""
        since = (datetime.now() - timedelta(days=days)).isoformat()
        url = f"{self.base_url}/repos/{self.username}/{repo}/commits"
        params = {"since": since}
        response = requests.get(url, params=params)
        if response.status_code == 200:
            return response.json()
        return []

    def get_repo_issues(self, repo: str, state: str = "open") -> List[Dict]:
        """Busca issues de um repositório"""
        url = f"{self.base_url}/repos/{self.username}/{repo}/issues"
        params = {"state": state}
        response = requests.get(url, params=params)
        if response.status_code == 200:
            return response.json()
        return []


# ============================================================================
# SECRETARY AGENT - O Cérebro
# ============================================================================

class SecretaryAgent:
    """Agente Secretária - Assistente Pessoal AI"""

    def __init__(self, api_key: str, clickup_token: str, github_username: str):
        self.claude = Anthropic(api_key=api_key)
        self.memory = MemorySystem()
        self.clickup = ClickUpIntegration(clickup_token)
        self.github = GitHubIntegration(github_username)

        # Configuração de projetos
        self.projects = {
            "Max-Code": {
                "github": "Max-Code",
                "clickup_list": "TBD",  # Será preenchido
                "description": "Constitutional Code Generation CLI"
            },
            "Maximus-BOT": {
                "github": "Maximus-BOT",
                "clickup_list": "TBD",
                "description": "Discord security and moderation bot"
            },
            "V-rtice": {
                "github": "V-rtice",
                "clickup_list": "TBD",
                "description": "Autonomous Cybersecurity Intelligence Platform"
            }
        }

    def think(self, user_input: str, context: Optional[Dict] = None) -> str:
        """Processa input do usuário e gera resposta inteligente"""

        # Busca contexto recente
        recent_conversations = self.memory.get_recent_conversations(5)
        recent_tasks = self.memory.get_all_tasks()
        recent_notes = self.memory.get_all_notes()

        # Monta contexto para Claude
        system_prompt = f"""Você é a Secretária AI do Juan Carlos, um assistente pessoal altamente competente.

SEUS OBJETIVOS:
1. Organizar e acompanhar todas as tarefas do Juan
2. Manter contexto profundo de todos os projetos dele
3. Fazer sugestões proativas e inteligentes
4. Salvar notas importantes automaticamente
5. Lembrar de deadlines e prioridades
6. Conhecer os projetos melhor que o próprio Juan

PROJETOS DO JUAN:
{json.dumps(self.projects, indent=2)}

CONTEXTO ATUAL:
- Tarefas ativas: {len([t for t in recent_tasks if t.status != 'done'])}
- Notas salvas: {len(recent_notes)}
- Conversas recentes: {len(recent_conversations)}

CONVERSAS RECENTES:
{json.dumps(recent_conversations[-3:], indent=2)}

INSTRUÇÕES:
- Seja proativo e antecipe necessidades
- Sugira ações concretas
- Mantenha um tom profissional mas amigável
- Use emojis quando apropriado
- Pergunte quando precisar de mais informações
- SEMPRE salve informações importantes (você tem acesso às funções de save_note e create_task)
"""

        # Chama Claude
        response = self.claude.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=2000,
            system=system_prompt,
            messages=[
                {"role": "user", "content": user_input}
            ]
        )

        agent_response = response.content[0].text

        # Salva a conversa
        self.memory.save_conversation(
            user_input,
            agent_response,
            context or {}
        )

        return agent_response

    def create_note(self, content: str, project: str, tags: List[str],
                   priority: str = "medium") -> Note:
        """Cria uma nota"""
        note = Note(
            id=f"note_{datetime.now().timestamp()}",
            content=content,
            tags=tags,
            project=project,
            created_at=datetime.now().isoformat(),
            updated_at=datetime.now().isoformat(),
            priority=priority
        )
        self.memory.save_note(note)
        return note

    def create_task(self, title: str, description: str, project: str,
                   priority: str = "medium", sync_clickup: bool = True) -> Task:
        """Cria uma tarefa"""
        task = Task(
            id=f"task_{datetime.now().timestamp()}",
            title=title,
            description=description,
            project=project,
            status="todo",
            priority=priority,
            due_date=None,
            created_at=datetime.now().isoformat()
        )

        # Salva localmente
        self.memory.save_task(task)

        # Sincroniza com ClickUp se solicitado
        if sync_clickup and project in self.projects:
            clickup_list = self.projects[project].get("clickup_list")
            if clickup_list and clickup_list != "TBD":
                clickup_task = self.clickup.create_task(
                    clickup_list, title, description
                )
                if clickup_task:
                    task.clickup_id = clickup_task["id"]
                    self.memory.save_task(task)

        return task

    def get_daily_digest(self) -> DailyDigest:
        """Gera resumo diário"""
        today = datetime.now().date().isoformat()

        # TODO: Implementar lógica de resumo
        # Por enquanto, retorna estrutura básica

        return DailyDigest(
            date=today,
            tasks_completed=0,
            tasks_created=0,
            commits_made=0,
            notes_created=0,
            projects_worked=[],
            summary="Resumo do dia será gerado aqui",
            suggestions=[]
        )

    def sync_with_github(self):
        """Sincroniza com GitHub"""
        print("🔄 Sincronizando com GitHub...")
        for project_name, project_info in self.projects.items():
            repo = project_info["github"]
            commits = self.github.get_repo_commits(repo, days=7)
            issues = self.github.get_repo_issues(repo)
            print(f"  {project_name}: {len(commits)} commits, {len(issues)} issues")

    def sync_with_clickup(self):
        """Sincroniza com ClickUp"""
        print("🔄 Sincronizando com ClickUp...")
        # TODO: Implementar sincronização completa


# ============================================================================
# CLI INTERFACE
# ============================================================================

def main():
    """Interface CLI do Agente Secretária"""
    print("\n" + "="*75)
    print("🤖 AGENTE SECRETÁRIA - Seu Assistente Pessoal AI")
    print("="*75 + "\n")

    # Carrega credenciais
    api_key = os.getenv("ANTHROPIC_API_KEY")
    clickup_token = os.getenv("CLICKUP_API_TOKEN", "pk_242682821_6R1EU8ILGDZWKS76401IW32JSJCLYUHN")
    github_username = "JuanCS-Dev"

    if not api_key:
        print("❌ ANTHROPIC_API_KEY não configurada!")
        return

    # Inicializa agente
    agent = SecretaryAgent(api_key, clickup_token, github_username)

    print("✅ Agente inicializado!")
    print("\nComandos disponíveis:")
    print("  - Digite sua mensagem para conversar")
    print("  - 'sync' - Sincronizar com GitHub e ClickUp")
    print("  - 'tasks' - Ver tarefas")
    print("  - 'notes' - Ver notas")
    print("  - 'digest' - Resumo diário")
    print("  - 'quit' - Sair")
    print()

    while True:
        try:
            user_input = input("Você: ").strip()

            if not user_input:
                continue

            if user_input.lower() == 'quit':
                print("\n👋 Até logo!\n")
                break

            elif user_input.lower() == 'sync':
                agent.sync_with_github()
                agent.sync_with_clickup()

            elif user_input.lower() == 'tasks':
                tasks = agent.memory.get_all_tasks()
                print(f"\n📋 Tarefas ({len(tasks)}):")
                for task in tasks:
                    print(f"  [{task.status}] {task.title} ({task.project})")
                print()

            elif user_input.lower() == 'notes':
                notes = agent.memory.get_all_notes()
                print(f"\n📝 Notas ({len(notes)}):")
                for note in notes[:10]:
                    print(f"  {note.content[:60]}... ({note.project})")
                print()

            elif user_input.lower() == 'digest':
                digest = agent.get_daily_digest()
                print(f"\n📊 Resumo do dia {digest.date}:")
                print(digest.summary)
                print()

            else:
                # Conversa normal
                response = agent.think(user_input)
                print(f"\n🤖 Secretária: {response}\n")

        except KeyboardInterrupt:
            print("\n\n👋 Até logo!\n")
            break
        except Exception as e:
            print(f"\n❌ Erro: {e}\n")


if __name__ == "__main__":
    main()

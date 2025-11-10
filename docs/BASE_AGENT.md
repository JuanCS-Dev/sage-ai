# 🤖 AGENTE SECRETÁRIA - Documentação Completa

**Assistente Pessoal AI que conhece seus projetos melhor que você**

---

## 📋 Visão Geral

O Agente Secretária é um assistente pessoal AI avançado que:
- 📝 Organiza todas as suas tarefas
- 🧠 Mantém memória de longo prazo
- 🔗 Integra com ClickUp e GitHub
- 💡 Faz sugestões proativas
- 📊 Gera resumos diários
- 🎯 Conhece profundamente todos os seus projetos

---

## 🏗️ Arquitetura

```
┌─────────────────────────────────────────────────────────────┐
│                    AGENTE SECRETÁRIA                         │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────┐     ┌──────────────┐     ┌─────────────┐ │
│  │   Claude AI  │────▶│ Agent Brain  │────▶│  Memory DB  │ │
│  │  (Reasoning) │     │   (Logic)    │     │  (SQLite)   │ │
│  └──────────────┘     └──────────────┘     └─────────────┘ │
│         │                     │                     │        │
│         ▼                     ▼                     ▼        │
│  ┌──────────────┐     ┌──────────────┐     ┌─────────────┐ │
│  │   ClickUp    │     │    GitHub    │     │    Notes    │ │
│  │     API      │     │     API      │     │   & Tasks   │ │
│  └──────────────┘     └──────────────┘     └─────────────┘ │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## 🎯 Funcionalidades

### 1. Sistema de Memória Persistente

**Banco de Dados SQLite com:**
- ✅ Notas organizadas por projeto
- ✅ Tarefas com status e prioridades
- ✅ Contexto de cada projeto
- ✅ Histórico de conversas
- ✅ Resumos diários

**Exemplo:**
```python
# Criar uma nota
agent.create_note(
    content="Implementar autenticação OAuth no Max-Code",
    project="Max-Code",
    tags=["authentication", "feature"],
    priority="high"
)

# Criar uma tarefa
agent.create_task(
    title="Fix bug in health command",
    description="Health check não está exibindo latência corretamente",
    project="Max-Code",
    priority="high",
    sync_clickup=True  # Sincroniza automaticamente com ClickUp
)
```

### 2. Integração com ClickUp

**Funcionalidades:**
- ✅ Criar tarefas automaticamente
- ✅ Atualizar status
- ✅ Sincronizar com listas
- ✅ Gerenciar prioridades

**Configuração:**
```python
clickup = ClickUpIntegration(api_token="pk_...")
task = clickup.create_task(
    list_id="901314884024",
    name="Nova feature",
    description="Descrição detalhada",
    priority=3
)
```

### 3. Integração com GitHub

**Funcionalidades:**
- ✅ Monitorar atividade recente
- ✅ Listar commits
- ✅ Rastrear issues
- ✅ Acompanhar progresso

**Exemplo:**
```python
github = GitHubIntegration(username="JuanCS-Dev")
commits = github.get_repo_commits("Max-Code", days=7)
issues = github.get_repo_issues("Max-Code", state="open")
```

### 4. Conversação Inteligente com Claude

**O agente:**
- 🧠 Mantém contexto de todas as conversas anteriores
- 💡 Faz sugestões baseadas no seu trabalho
- 📊 Analisa padrões e tendências
- 🎯 Antecipa necessidades
- 📝 Salva informações importantes automaticamente

**Exemplo de conversa:**
```
Você: "Trabalhei hoje no Max-Code, fiz vários commits"

Secretária: "Ótimo! Vi que você fez 5 commits no Max-Code hoje.
Notei que estava focado na feature de health check.
Quer que eu crie uma tarefa no ClickUp para documentar
essa nova funcionalidade? 📝

Também vi que há 3 issues abertas no GitHub relacionadas
a testes. Quer priorizar alguma delas?"
```

### 5. Resumos Diários Automáticos

**O agente gera diariamente:**
- ✅ Tarefas completadas
- ✅ Commits feitos
- ✅ Notas criadas
- ✅ Projetos trabalhados
- ✅ Sugestões para o próximo dia

---

## 🚀 Como Usar

### Instalação

```bash
cd "/home/maximus/MAXIMUS AI/max-code-cli"

# Instalar dependências
pip install anthropic requests

# Configurar variáveis de ambiente
export ANTHROPIC_API_KEY="sua-api-key"
export CLICKUP_API_TOKEN="pk_242682821_6R1EU8ILGDZWKS76401IW32JSJCLYUHN"
```

### Execução

```bash
# Modo interativo
python3 agents/secretary_agent.py

# Ou adicionar ao PATH
chmod +x agents/secretary_agent.py
ln -s $(pwd)/agents/secretary_agent.py /usr/local/bin/secretary
secretary
```

### Comandos Disponíveis

```
MODO CONVERSAÇÃO:
  - Digite qualquer mensagem para conversar com o agente
  - O agente responderá e salvará contexto automaticamente

COMANDOS ESPECIAIS:
  sync    - Sincronizar com GitHub e ClickUp
  tasks   - Ver todas as tarefas
  notes   - Ver todas as notas
  digest  - Ver resumo do dia
  quit    - Sair
```

---

## 💡 Casos de Uso

### 1. Planejamento Diário

```
Você: "Bom dia! O que devo fazer hoje?"

Secretária: "Bom dia, Juan! 🌅

Baseado nas suas prioridades, sugiro:

1. 🔴 URGENTE: Implementar Tree of Thoughts no Architect Agent
   (Você adicionou o import ontem, mas ainda falta implementar)

2. 🟡 IMPORTANTE: Revisar 3 issues do Maximus-BOT no GitHub
   (Estão abertas há 5 dias)

3. 🟢 DOCUMENTAÇÃO: Atualizar README do V-rtice
   (Último commit foi há 10 dias)

Quer que eu crie tasks no ClickUp para estas ações?"
```

### 2. Acompanhamento de Progresso

```
Você: "Terminei a feature de health check no Max-Code"

Secretária: "Parabéns! 🎉

Registrei que você completou:
✅ Feature: Health check command
✅ 5 commits relacionados
✅ Testes E2E passando

PRÓXIMOS PASSOS SUGERIDOS:
1. Atualizar documentação
2. Criar PR para review
3. Notificar equipe

Criei uma nota com os detalhes técnicos da implementação.
Quer que eu crie as tasks para os próximos passos?"
```

### 3. Organização de Notas

```
Você: "Preciso lembrar que o serviço Eureka precisa de refactor
      na estratégia de dependency upgrade"

Secretária: "Anotado! 📝

Criei uma nota com:
- Projeto: Eureka
- Tags: refactor, dependency-upgrade
- Prioridade: Média

Também vi que há 2 outras notas relacionadas a Eureka.
Quer revisar o contexto completo do projeto?"
```

### 4. Sincronização Automática

```
Você: "sync"

Secretária: "🔄 Sincronizando...

GITHUB:
  Max-Code: 5 commits (últimos 7 dias), 3 issues abertas
  Maximus-BOT: 2 commits, 0 issues
  V-rtice: 0 commits, 1 issue aberta

CLICKUP:
  15 tarefas ativas
  3 tarefas vencidas (ATENÇÃO!)
  8 tarefas completadas esta semana

SUGESTÕES:
⚠️  Você tem 3 tarefas vencidas. Quer reprogramar?
💡 Issue #42 do V-rtice está sem atividade há 15 dias
📊 Produtividade: +20% vs semana passada!

Tudo sincronizado!"
```

---

## 🔧 Configuração Avançada

### Personalizar Projetos

Edite a lista de projetos em `secretary_agent.py`:

```python
self.projects = {
    "Max-Code": {
        "github": "Max-Code",
        "clickup_list": "901314884024",  # ID da List no ClickUp
        "description": "Constitutional Code Generation CLI",
        "technologies": ["Python", "Anthropic", "CLI"],
        "priority": "high"
    },
    # Adicione mais projetos...
}
```

### Ajustar Comportamento do Agente

Modifique o `system_prompt` para personalizar:
- Tom de voz
- Nível de proatividade
- Tipo de sugestões
- Frequência de alertas

### Integrar com Outros Serviços

O agente é extensível. Adicione integrações com:
- Slack/Discord (notificações)
- Google Calendar (deadlines)
- Jira/Linear (project management)
- Email (resumos automáticos)

---

## 📊 Schema do Banco de Dados

### Tabela: notes
```sql
CREATE TABLE notes (
    id TEXT PRIMARY KEY,
    content TEXT,
    tags TEXT,              -- JSON array
    project TEXT,
    created_at TEXT,
    updated_at TEXT,
    priority TEXT           -- low, medium, high, critical
)
```

### Tabela: tasks
```sql
CREATE TABLE tasks (
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
```

### Tabela: conversations
```sql
CREATE TABLE conversations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT,
    user_input TEXT,
    agent_response TEXT,
    context TEXT            -- JSON
)
```

### Tabela: project_context
```sql
CREATE TABLE project_context (
    name TEXT PRIMARY KEY,
    description TEXT,
    github_repo TEXT,
    clickup_list TEXT,
    last_activity TEXT,
    technologies TEXT,       -- JSON array
    current_focus TEXT,
    recent_commits TEXT,     -- JSON array
    open_tasks INTEGER,
    notes_count INTEGER
)
```

---

## 🎓 Próximas Melhorias

### Fase 1 (Atual) ✅
- [x] Memória persistente
- [x] Integração ClickUp
- [x] Integração GitHub
- [x] Conversação com Claude
- [x] CLI interativo

### Fase 2 (Próxima)
- [ ] Interface web (Flask/FastAPI)
- [ ] Notificações push
- [ ] Resumos automáticos por email
- [ ] Dashboard de produtividade
- [ ] Análise de padrões com ML

### Fase 3 (Futuro)
- [ ] App mobile (React Native)
- [ ] Integração com Calendar
- [ ] Voice commands (Speech-to-Text)
- [ ] Auto-complete de tarefas simples
- [ ] Insights preditivos

---

## ⚡ Performance

### Métricas Esperadas:
- 🚀 Resposta do agente: < 2s
- 💾 Busca no banco: < 100ms
- 🔄 Sincronização GitHub: < 3s
- 🔄 Sincronização ClickUp: < 2s

### Otimizações:
- Cache de respostas frequentes
- Batch updates para ClickUp
- Rate limiting para GitHub API
- Compressão de contexto para Claude

---

## 🔐 Segurança

### Dados Protegidos:
- ✅ API tokens em variáveis de ambiente
- ✅ Banco de dados local (não sincronizado)
- ✅ Sem logging de informações sensíveis
- ✅ Rate limiting em APIs externas

### Recomendações:
- Não commite `secretary_memory.db`
- Use `.env` para credenciais
- Backup regular do banco de dados
- Revise permissões do arquivo DB

---

## 📝 Exemplos de Uso Avançado

### 1. Criar Task Complexa

```python
from secretary_agent import SecretaryAgent

agent = SecretaryAgent(api_key, clickup_token, github_username)

task = agent.create_task(
    title="Implementar Tree of Thoughts",
    description="""
    Implementar o módulo core/tree_of_thoughts.py conforme
    planejado no POST_DIAGNOSTIC_CHANGES.md

    Requisitos:
    - Exploração de múltiplos caminhos
    - Avaliação de alternativas
    - Seleção da melhor solução
    - Backtracking

    Integrar com:
    - Architect Agent
    - Task Decomposer
    """,
    project="Max-Code",
    priority="critical",
    sync_clickup=True
)

print(f"Task criada: {task.id}")
if task.clickup_id:
    print(f"Sincronizada com ClickUp: {task.clickup_id}")
```

### 2. Análise de Produtividade

```python
# Buscar todas as tasks completadas esta semana
from datetime import datetime, timedelta

week_ago = datetime.now() - timedelta(days=7)
tasks = agent.memory.get_all_tasks(status="done")

completed_this_week = [
    t for t in tasks
    if datetime.fromisoformat(t.created_at) > week_ago
]

print(f"Completadas esta semana: {len(completed_this_week)}")

# Por projeto
by_project = {}
for task in completed_this_week:
    by_project[task.project] = by_project.get(task.project, 0) + 1

print("\nPor projeto:")
for project, count in sorted(by_project.items(), key=lambda x: -x[1]):
    print(f"  {project}: {count} tasks")
```

### 3. Export de Notas

```python
import json

# Export todas as notas de um projeto
notes = agent.memory.get_all_notes(project="Max-Code")

export_data = [
    {
        "content": note.content,
        "tags": note.tags,
        "created": note.created_at,
        "priority": note.priority
    }
    for note in notes
]

with open("max_code_notes.json", "w") as f:
    json.dump(export_data, f, indent=2)

print(f"Exportadas {len(notes)} notas para max_code_notes.json")
```

---

## 🤝 Contribuindo

Para melhorar o Agente Secretária:

1. Fork o repositório
2. Crie uma branch para sua feature
3. Implemente e teste
4. Submeta um PR

**Áreas que precisam de ajuda:**
- Interface web
- Mais integrações (Notion, Trello, etc.)
- Machine Learning para sugestões
- Testes automatizados

---

## 📞 Suporte

**Problemas comuns:**

1. **"ANTHROPIC_API_KEY não configurada"**
   ```bash
   export ANTHROPIC_API_KEY="sua-key-aqui"
   ```

2. **"Erro ao conectar com ClickUp"**
   - Verifique se o token está correto
   - Teste: `curl -H "Authorization: pk_..." https://api.clickup.com/api/v2/team`

3. **"Banco de dados não encontrado"**
   - O banco é criado automaticamente na primeira execução
   - Verifique permissões da pasta

---

**Criado por:** MAXIMUS AI
**Data:** 10 de Novembro de 2025
**Versão:** 1.0.0
**Status:** Produção Beta ✅

*Soli Deo Gloria*

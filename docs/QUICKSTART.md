# 🚀 MAXIMUS Personal Assistant - Quick Start Guide

**De zero a um TRUE PA em 5 minutos**

---

## ⚡ Setup Rápido

### 1. Verificar Dependências

```bash
# Instalar bibliotecas Python necessárias
pip install anthropic requests aiohttp
```

### 2. Configurar Variáveis de Ambiente

```bash
# API Key do Anthropic (OBRIGATÓRIO)
export ANTHROPIC_API_KEY="sk-ant-api03-..."

# ClickUp Token (já configurado, mas pode trocar)
export CLICKUP_API_TOKEN="pk_242682821_6R1EU8ILGDZWKS76401IW32JSJCLYUHN"

# MAXIMUS Core URL (OPCIONAL - usa fallback se não disponível)
export MAXIMUS_CORE_URL="http://localhost:8150"

# MABA URL (OPCIONAL - usa fallback se não disponível)
export MABA_URL="http://localhost:8152"
```

### 3. Executar o Assistente

```bash
cd "/home/maximus/MAXIMUS AI/max-code-cli"

# Modo 1: Execução direta
python3 agents/maximus_personal_assistant.py

# Modo 2: Criar alias para uso fácil (RECOMENDADO)
chmod +x agents/maximus_personal_assistant.py
echo 'alias maxpa="python3 \"$HOME/MAXIMUS AI/max-code-cli/agents/maximus_personal_assistant.py\""' >> ~/.bashrc
source ~/.bashrc

# Agora pode executar de qualquer lugar:
maxpa
```

---

## 🎯 Primeiro Uso

### Tela Inicial

```
============================================================================
🧠 MAXIMUS PERSONAL ASSISTANT - TRUE AI PA v2.0
============================================================================

✨ Consciência + Desempenho + Execução Autônoma

🔄 Inicializando MAXIMUS Personal Assistant...

✅ MAXIMUS Personal Assistant v2.0 inicializado!

🧠 Consciência: ✅ ATIVA
   Core disponível: ❌ (usando fallback seguro)

🔌 Integrações:
   ClickUp: ✅
   GitHub: ✅
   MABA: ❌ (execução web indisponível)
   Core: ❌ (validação em fallback mode)

📋 Comandos disponíveis:
  - Converse normalmente para interação consciente
  - execute <roadmap> - Executar roadmap com validação
  - status - Ver status e performance
  - performance - Relatório de desempenho
  - quit - Sair

Você: _
```

### Primeiros Comandos

#### 1. Ver Status
```
Você: status

{
  "agent": "MAXIMUS Personal Assistant v2.0",
  "consciousness": {
    "enabled": true,
    "core_available": false
  },
  "performance": {
    "tasks_completed": 0,
    "tasks_failed": 0,
    "success_rate": "0.0%",
    "avg_task_time": "0.00s",
    ...
  },
  ...
}
```

#### 2. Conversação Simples
```
Você: Olá, me ajude a organizar meu dia

🧠 MAXIMUS: Olá! Vou te ajudar a organizar seu dia.

📊 Deixe-me verificar o contexto dos seus projetos...

Encontrei:
- 📁 Max-Code: 7 commits hoje, 3 issues abertas
- 📁 Maximus-BOT: 0 commits (5 dias sem atividade)
- 📁 V-rtice: 1 issue aberta há 15 dias

🎯 Sugestões para hoje:

1. 🔴 URGENTE: Max-Code
   - Implementar Tree of Thoughts (imports adicionados ontem)
   - Tempo estimado: 3-4 horas

2. 🟡 IMPORTANTE: Maximus-BOT
   - Revisar 3 issues pendentes
   - Tempo estimado: 1-2 horas

3. 🟢 DOCUMENTAÇÃO:
   - Atualizar README do V-rtice
   - Tempo estimado: 30 min

Quer que eu crie tasks no ClickUp para estas ações?
```

#### 3. Criar Nota
```
Você: Anota que preciso implementar autenticação OAuth no Max-Code

🧠 MAXIMUS: ✅ Nota criada!

📝 Salva no projeto Max-Code com:
   - Tags: [authentication, feature, oauth]
   - Prioridade: Alta
   - Timestamp: 2025-11-10 10:23:45

💡 Vi que você já tem 2 outras notas relacionadas a autenticação.
   Quer revisar o contexto completo antes de implementar?
```

---

## 🔥 Funcionalidades Essenciais

### 1. Organização de Tarefas

```
# Criar tarefa
Você: Cria uma task para fix bug no health command

# Sincronizar com ClickUp
Você: Sincroniza minhas tasks com o ClickUp

# Ver todas as tasks
Você: Mostra minhas tasks pendentes
```

### 2. Acompanhamento de Projetos

```
# Ver atividade recente
Você: O que aconteceu no Max-Code hoje?

# Analisar progresso
Você: Como está o progresso do V-rtice?

# Sugestões proativas
Você: O que devo priorizar agora?
```

### 3. Execução de Roadmaps

```bash
# 1. Criar um roadmap (Markdown)
cat > roadmaps/exemplo.md << 'EOF'
# Roadmap de Lançamento - Exemplo

## Etapa 1: Preparação
- Criar página de landing
- Preparar assets (imagens, vídeos)
- Escrever descrição do produto

## Etapa 2: Publicação
- Publicar no Product Hunt
- Postar no Twitter
- Enviar para lista de email

## Etapa 3: Acompanhamento
- Responder comentários
- Monitorar métricas
- Coletar feedback
EOF

# 2. Executar roadmap
python3 agents/maximus_personal_assistant.py

Você: execute roadmaps/exemplo.md
```

### 4. Notas e Memória

```
# Criar nota com contexto
Você: Nota: O serviço Eureka precisa refactor na estratégia de dependency upgrade

# Buscar notas de um projeto
Você: Mostra todas as notas do projeto Eureka

# Buscar por tag
Você: Busca notas com tag "refactor"
```

---

## 🛠️ Troubleshooting

### Problema 1: "ANTHROPIC_API_KEY não configurada"

```bash
# Solução
export ANTHROPIC_API_KEY="sua-key-aqui"

# Verificar se foi configurada
echo $ANTHROPIC_API_KEY
```

### Problema 2: "Core não disponível"

**Não é um erro!** O assistente funciona perfeitamente sem o Core.

```
Core Disponível:
✅ Validação consciente com Max AI
✅ Safety checks multicamadas
✅ Orientação das 7 Virtudes

Core Indisponível (Fallback Mode):
✅ Validação básica de segurança
✅ Bloqueio de ações perigosas
✅ Funcionamento normal (sem consciência avançada)
```

**Como iniciar o Core:**
```bash
# Terminal 1: MAXIMUS Core
cd "/home/maximus/MAXIMUS AI/services/core"
python3 -m uvicorn main:app --port 8150

# Terminal 2: MAXIMUS PA
maxpa
```

### Problema 3: "MABA não disponível"

**Também não é erro!** Apenas navegação web fica indisponível.

```
MABA Disponível:
✅ Execução de tarefas web
✅ Navegação automática
✅ Preenchimento de formulários

MABA Indisponível:
✅ Organização funciona normalmente
✅ ClickUp e GitHub funcionam
❌ Execução web indisponível
```

**Como iniciar o MABA:**
```bash
# Terminal 1: MABA
cd "/home/maximus/MAXIMUS AI/services/maba"
python3 -m uvicorn main:app --port 8152

# Terminal 2: MAXIMUS PA
maxpa
```

### Problema 4: "Performance baixa"

```
Você: performance

# Se avg_task_time > 10s:

📊 Performance Report:
   Avg Task Time: 15.42s ⚠️

Possíveis causas:
1. Serviços MAXIMUS lentos/offline
2. Rede lenta
3. Validações muito complexas

Solução:
- Verificar status dos serviços
- Desabilitar temporariamente validação consciente
- Usar modo offline (apenas memória local)
```

---

## 📚 Próximos Passos

Agora que você tem o assistente rodando:

### 1. Explore as Capacidades

```
# Teste conversação
Você: Me conta sobre meus projetos

# Teste organização
Você: Cria uma task para documentar a feature X

# Teste memória
Você: O que eu disse sobre autenticação?

# Teste performance
Você: performance
```

### 2. Configure Seus Projetos

Edite `agents/maximus_personal_assistant.py`:

```python
# Por padrão, herda do secretary_agent.py:
self.projects = {
    "Max-Code": {
        "github": "Max-Code",
        "clickup_list": "901314884024",
        "description": "Constitutional Code Generation CLI",
        "technologies": ["Python", "Anthropic", "CLI"],
        "priority": "high"
    },
    # Adicione seus projetos aqui...
}
```

### 3. Crie Seus Roadmaps

```bash
mkdir -p roadmaps

# Exemplo: Lançamento de produto
cat > roadmaps/launch_product.md << 'EOF'
# Roadmap: Lançamento do Produto X

## Fase 1: Preparação (2 dias)
1. Criar landing page
2. Preparar assets visuais
3. Escrever copy e descrições
4. Configurar analytics

## Fase 2: Soft Launch (1 dia)
1. Publicar em beta restrito
2. Coletar feedback inicial
3. Fazer ajustes necessários

## Fase 3: Lançamento Público (1 dia)
1. Product Hunt
2. HackerNews
3. Reddit
4. Twitter
5. LinkedIn

## Fase 4: Pós-Lançamento (ongoing)
1. Responder comentários
2. Coletar feedback
3. Iterar baseado em uso real
EOF

# Executar
maxpa
Você: execute roadmaps/launch_product.md
```

### 4. Integre com Seu Workflow

```bash
# Adicione ao seu .bashrc ou .zshrc

# Alias úteis
alias maxpa="python3 '$HOME/MAXIMUS AI/max-code-cli/agents/maximus_personal_assistant.py'"
alias pa-status="curl http://localhost:8150/health && curl http://localhost:8152/health"

# Function para notas rápidas
function nota() {
    python3 -c "
from agents.secretary_agent import SecretaryAgent
import os

agent = SecretaryAgent(
    os.getenv('ANTHROPIC_API_KEY'),
    os.getenv('CLICKUP_API_TOKEN'),
    'JuanCS-Dev'
)

agent.create_note('$1', 'General', ['quick-note'], 'medium')
print('✅ Nota criada!')
"
}

# Uso:
# nota "Implementar feature X amanhã"
```

---

## 🎯 Casos de Uso Comuns

### Use Case 1: Planejamento Diário

```
# Manhã (9:00)
Você: Bom dia! O que devo fazer hoje?

🧠 MAXIMUS: [Analisa contexto e sugere prioridades]

# Durante o dia
Você: Terminei a feature X, o que vem depois?

# Final do dia (18:00)
Você: Resumo do dia

🧠 MAXIMUS: [Gera relatório do que foi feito + sugestões para amanhã]
```

### Use Case 2: Lançamento de Produto

```
# Dia do lançamento
Você: execute roadmaps/launch_typecraft.md

🧠 MAXIMUS: [Executa automaticamente todas as etapas automatizáveis]

# Acompanhamento
Você: Como está o progresso do lançamento?

🧠 MAXIMUS: [Reporta métricas e próximos passos]
```

### Use Case 3: Gerenciamento de Projetos

```
# Sincronização semanal
Você: sync

🧠 MAXIMUS: [Sincroniza GitHub + ClickUp, identifica issues]

# Review
Você: O que precisa de atenção nos projetos?

🧠 MAXIMUS: [Lista issues, PRs, tasks vencidas]
```

---

## 📖 Documentação Completa

Para mais detalhes, veja:

- **📘 Documentação Completa**: `docs/MAXIMUS_PERSONAL_ASSISTANT.md`
- **📗 Agente Secretária Base**: `docs/AGENTE_SECRETARIA.md`
- **📕 Código Fonte**: `agents/maximus_personal_assistant.py`

---

## 💡 Dicas Pro

### 1. Use Tags nas Notas

```
Você: Nota sobre OAuth: Usar Supabase Auth
      Tags: authentication, supabase, backend
```

### 2. Priorize Corretamente

```
critical > high > medium > low

"critical" = URGENTE + IMPORTANTE (faz primeiro)
"high"     = IMPORTANTE mas não urgente
"medium"   = Pode esperar alguns dias
"low"      = Quando tiver tempo
```

### 3. Contextualize Tasks

```
# Ruim
Você: Cria task para fix bug

# Bom
Você: Cria task para fix bug no health command do Max-Code,
      onde a latência não está sendo exibida corretamente
```

### 4. Use Roadmaps para Tudo

Crie roadmaps para:
- Lançamentos de produtos
- Features grandes
- Refactorings complexos
- Processos repetitivos

O assistente pode **executar automaticamente** muitos passos!

---

## ✅ Checklist de Setup

- [ ] Python 3.8+ instalado
- [ ] Dependências instaladas (`pip install anthropic requests aiohttp`)
- [ ] `ANTHROPIC_API_KEY` configurada
- [ ] `CLICKUP_API_TOKEN` configurada (opcional mas recomendado)
- [ ] Alias `maxpa` criado
- [ ] Testou comando `status`
- [ ] Testou conversação básica
- [ ] Criou primeira nota
- [ ] Criou primeira task

**Pronto! Você tem um TRUE Personal Assistant rodando! 🎉**

---

**Criado por:** MAXIMUS AI
**Data:** 10 de Novembro de 2025
**Versão:** 2.0.0

*Soli Deo Gloria* 🙏

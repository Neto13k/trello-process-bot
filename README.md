# 🤖 Trello Process Bot

Agente inteligente de automação de fluxo de trabalho integrado ao Trello, desenvolvido com **Google ADK** e **Gemini 2.5 Flash**.

Projeto desenvolvido como atividade prática do Bootcamp **"DIO — Do Prompt ao Agente"**.

---

## 📋 Sobre o Projeto

O **Trello Process Bot** é um agente de IA conversacional que permite gerenciar tarefas no Trello através de linguagem natural. O usuário descreve o que precisa fazer e o agente interpreta, organiza, prioriza e executa as ações diretamente no board do Trello — sem necessidade de acessar a interface manualmente.

---

## ✨ Funcionalidades

- 📌 **Adicionar tarefas** — Cria cards no Trello com nome, descrição e data de vencimento
- 📋 **Listar tarefas** — Consulta tarefas por status: todas, a fazer, em andamento ou concluídas
- 🔄 **Mover tarefas** — Altera o status de um card entre as listas do board
- 🕐 **Contexto temporal** — Obtém a data e hora atual para orientar as interações
- 🧠 **Priorização inteligente** — Classifica tarefas por prioridade: baixa, média, alta ou urgente

---

## 🗂️ Estrutura do Projeto

```
trello-process-bot/
├── deskmanager/
│   ├── __init__.py
│   └── agent.py        # Agente principal e ferramentas
├── .env                # Variáveis de ambiente (não versionar)
├── .gitignore
├── requirements.txt
└── README.md
```

---

## 🚀 Como Executar

### Pré-requisitos

- Python 3.10+
- Conta no [Trello](https://trello.com) com um board chamado **`Bot`**
- Conta no [Google AI Studio](https://aistudio.google.com) para obter a `GOOGLE_API_KEY`
- Board no Trello com as listas: `A FAZER`, `EM ANDAMENTO`, `EM REVISÃO`, `CONCLUÍDO`, `REFINAMENTO`

### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/trello-process-bot.git
cd trello-process-bot
```

### 2. Instale as dependências

```bash
pip install -r requirements.txt
```

### 3. Configure as variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto:

```dotenv
GOOGLE_GENAI_USE_VERTEXAI=0
GOOGLE_API_KEY=sua_google_api_key

TRELLO_API_KEY=sua_trello_api_key
TRELLO_API_SECRET=seu_trello_api_secret
TRELLO_TOKEN=seu_trello_token
```

> ⚠️ **Nunca suba o arquivo `.env` para o repositório.**

### 4. Obtenha as credenciais do Trello

- **API Key e Secret:** Acesse [https://trello.com/power-ups/admin](https://trello.com/power-ups/admin), crie um Power-Up e copie a API Key.
- **Token:** Acesse a URL abaixo substituindo `SUA_API_KEY`:

```
https://trello.com/1/authorize?expiration=never&scope=read,write&response_type=token&key=SUA_API_KEY
```

### 5. Execute o agente

```bash
adk web
```

Acesse `http://localhost:8000` no navegador e comece a conversar com o agente.

---

## 💬 Exemplos de Uso

```
Usuário: Olá!
Agente:  Olá! Hoje é 17/04/2025. Quais tarefas você precisa organizar hoje?

Usuário: Preciso criar uma tarefa para revisar o relatório até sexta-feira.
Agente:  Entendido! Vou cadastrar a tarefa "Revisar relatório" na lista A FAZER
         com vencimento em 18/04 (corrigindo o D-1 do Trello). Confirma?

Usuário: Quais tarefas estão em andamento?
Agente:  [lista as tarefas da lista EM ANDAMENTO]

Usuário: Muda a tarefa "Revisar relatório" para concluído.
Agente:  Tarefa movida de 'A FAZER' para 'CONCLUÍDO' com sucesso!
```

---

## 🛠️ Tecnologias Utilizadas

| Tecnologia | Descrição |
|---|---|
| [Google ADK](https://google.github.io/adk-docs/) | Framework para criação de agentes de IA |
| [Gemini 2.5 Flash](https://deepmind.google/technologies/gemini/) | Modelo de linguagem utilizado pelo agente |
| [py-trello](https://github.com/sarumont/py-trello) | Biblioteca Python para integração com a API do Trello |
| [python-dotenv](https://github.com/theskumar/python-dotenv) | Gerenciamento de variáveis de ambiente |

---

## ⚙️ Variáveis de Ambiente

| Variável | Descrição |
|---|---|
| `GOOGLE_GENAI_USE_VERTEXAI` | Define se usa Vertex AI (`0` = não, usa AI Studio) |
| `GOOGLE_API_KEY` | Chave da API do Google AI Studio |
| `TRELLO_API_KEY` | Chave da API do Trello (32 caracteres) |
| `TRELLO_API_SECRET` | Secret da API do Trello |
| `TRELLO_TOKEN` | Token de acesso do Trello (64 caracteres) |

---

## 📌 Observações Importantes

- O board no Trello deve se chamar exatamente **`Bot`**
- As listas do board devem conter os nomes: `A FAZER`, `EM ANDAMENTO`, `EM REVISÃO`, `CONCLUÍDO`, `REFINAMENTO`
- O Trello possui um **bug de datas (D-1)**: ao cadastrar um card, a data exibida fica um dia antes do esperado. O agente já está configurado para corrigir isso automaticamente, somando 1 dia à data informada.

---

## 📄 Licença

Este projeto foi desenvolvido para fins educacionais no Bootcamp **DIO — Do Prompt ao Agente**.

---

## 👨‍💻 Autor

Desenvolvido por **José Hermes** como atividade prática do Bootcamp **DIO — Do Prompt ao Agente**.
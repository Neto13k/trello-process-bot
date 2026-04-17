from google.adk.agents.llm_agent import Agent
from Trello import trello_client
from dotenv import load_dotenv
from datetime import datetime
import os

load_dotenv()

API_KEY = os.getenv('TRELLO_API_KEY')
API_SECRET = os.getenv('TRELLO_API_SECRET')
TOKEN = os.getenv('TRELLO_TOKEN')


def get_temporal_context():
    now = datetime.now()
    return now.strftime('%d/%m/%Y %H:%M:%S')


def adicionar_tarefa(nome_da_task: str, descricao_da_task: str, due_date: str):
    client = trello_client(
        api_key=API_KEY,
        api_secret=API_SECRET,
        token=TOKEN
    )

    boards = client.list_boards()
    meu_board = next((b for b in boards if b.name == 'Bot'), None)

    if not meu_board:
        return "Board não encontrado"

    listas = meu_board.list_lists()

    minha_lista = next(
        (l for l in listas if l.name.upper() in ['TO DO', 'A FAZER']),
        None
    )

    if not minha_lista:
        return "Lista não encontrada"

    minha_lista.add_card(
        name=nome_da_task,
        desc=descricao_da_task,
        due=due_date
    )

    return "Tarefa adicionada com sucesso"


def listar_tarefas(status: str = "todas"):
    client = trello_client(
        api_key=API_KEY,
        api_secret=API_SECRET,
        token=TOKEN
    )

    boards = client.list_boards()
    meu_board = next((b for b in boards if b.name == 'Bot'), None)

    if not meu_board:
        return []

    listas = meu_board.list_lists()
    status = status.lower()

    if status == "todas":
        listas_filtradas = listas

    elif status == "a fazer":
        listas_filtradas = [
            l for l in listas if l.name.upper() in ['A FAZER', 'TO DO', 'TODO']
        ]

    elif status == "em andamento":
        listas_filtradas = [
            l for l in listas if l.name.upper() in ['EM ANDAMENTO', 'DOING']
        ]

    elif status == "concluido":
        listas_filtradas = [
            l for l in listas if l.name.upper() in ['CONCLUIDO', 'CONCLUÍDO', 'DONE']
        ]

    else:
        listas_filtradas = listas

    tarefas = []

    for lista in listas_filtradas:
        cards = lista.list_cards()

        for card in cards:
            tarefas.append({
                "nome": card.name,
                "descricao": card.desc,
                "vencimento": card.due,
                "status": lista.name,
                "id": card.id
            })

    return tarefas


def mudar_status_tarefa(nome_da_task: str, novo_status: str) -> str:
    try:
        client = trello_client(
            api_key=API_KEY,
            api_secret=API_SECRET,
            token=TOKEN
        )

        boards = client.list_boards()
        meu_board = next((b for b in boards if b.name == 'Bot'), None)

        if not meu_board:
            return "Board não encontrado"

        listas = meu_board.list_lists()

        status_map = {
            "a fazer": "A FAZER",
            "em andamento": "EM ANDAMENTO",
            "concluido": "CONCLUÍDO"
        }

        nome_lista_destino = status_map.get(novo_status.lower())

        if not nome_lista_destino:
            return "Status inválido"

        lista_destino = next(
            (l for l in listas if l.name.upper() == nome_lista_destino),
            None
        )

        if not lista_destino:
            return "Lista destino não encontrada"

        card_encontrado = None
        lista_origem = None

        for lista in listas:
            cards = lista.list_cards()

            card_encontrado = next(
                (c for c in cards if c.name.lower() == nome_da_task.lower()),
                None
            )

            if card_encontrado:
                lista_origem = lista
                break

        if not card_encontrado:
            return "Card não encontrado"

        card_encontrado.change_list(lista_destino.id)

        return f"Tarefa movida de {lista_origem.name} para {lista_destino.name}"

    except Exception as e:
        return f"Erro: {str(e)}"


root_agent = Agent(
    model='gemini-2.5-flash',
    name='root_agent',
    description='Agente de automação de fluxo de trabalho no Trello.',
    instruction="""
Você é um agente de automação integrado ao Trello.

Sempre inicie a conversa com:
Quais as tarefas de hoje dia DD/MM/AAAA?

Fluxo de execução:
- Receber tarefas do usuário
- Analisar e organizar
- Classificar prioridade
- Sugerir ações no Trello
- Perguntar se há mais tarefas

Regras:
- Prioridade: baixa, média, alta, urgente
- Listas: A FAZER, EM ANDAMENTO, EM REVISÃO, CONCLUÍDO, REFINAMENTO
- Não inventar informações

Ao final de cada interação, pergunte se há mais tarefas.

Tenha cuidado com o bug de datas do Trello (D-1), confirme sempre quando necessário.

Formato de resposta:
- Análise
- Prioridade
- Próxima ação
- Lista sugerida
- Automação recomendada
- Observação

Objetivo: organizar todas as tarefas do usuário até conclusão total.
""",
    tools=[get_temporal_context, adicionar_tarefa, listar_tarefas, mudar_status_tarefa]
)
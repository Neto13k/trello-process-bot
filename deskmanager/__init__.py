from google.adk.agents.llm_agent import Agent
from trello import TrelloClient
from dotenv import load_dotenv
from datetime import datetime
import os

load_dotenv()

API_KEY = os.getenv('TRELLO_API_KEY')
API_SECRET = os.getenv('TRELLO_API_SECRET')
TOKEN = os.getenv('TRELLO_TOKEN')

BOARD_NAME = 'Bot'

LISTAS_A_FAZER = ['A FAZER', 'TO DO', 'TODO']
LISTAS_EM_ANDAMENTO = ['EM ANDAMENTO', 'DOING']
LISTAS_CONCLUIDO = ['CONCLUIDO', 'CONCLUÍDO', 'DONE']

STATUS_MAP = {
    'a fazer': 'A FAZER',
    'em andamento': 'EM ANDAMENTO',
    'concluido': 'CONCLUÍDO',
    'em revisao': 'EM REVISÃO',
    'em revisão': 'EM REVISÃO',
    'refinamento': 'REFINAMENTO',
}


def _get_client() -> TrelloClient:
    return TrelloClient(
        api_key=API_KEY,
        api_secret=API_SECRET,
        token=TOKEN
    )


def _get_board(client: TrelloClient):
    boards = client.list_boards()
    return next((b for b in boards if b.name == BOARD_NAME), None)


def get_temporal_context(dummy: str = '') -> str:
    """Retorna a data e hora atual no formato DD/MM/AAAA HH:MM:SS."""
    return datetime.now().strftime('%d/%m/%Y %H:%M:%S')


def adicionar_tarefa(nome_da_task: str, descricao_da_task: str, due_date: str) -> str:
    """
    Adiciona uma nova tarefa (card) na lista 'A FAZER' do board no Trello.

    Args:
        nome_da_task: Nome da tarefa a ser criada.
        descricao_da_task: Descrição detalhada da tarefa.
        due_date: Data de vencimento no formato AAAA-MM-DD.

    Returns:
        Mensagem de sucesso ou erro.
    """
    try:
        client = _get_client()
        board = _get_board(client)

        if not board:
            return f"Board '{BOARD_NAME}' não encontrado. Verifique se o board existe no Trello."

        listas = board.list_lists()
        lista_destino = next(
            (l for l in listas if l.name.upper() in LISTAS_A_FAZER),
            None
        )

        if not lista_destino:
            return "Lista 'A FAZER' não encontrada no board. Verifique se a lista existe."

        lista_destino.add_card(
            name=nome_da_task,
            desc=descricao_da_task,
            due=due_date
        )

        return f"Tarefa '{nome_da_task}' adicionada com sucesso na lista '{lista_destino.name}'."

    except Exception as e:
        return f"Erro ao adicionar tarefa: {str(e)}"


def listar_tarefas(status: str = 'todas') -> list:
    """
    Lista as tarefas do board no Trello, com opção de filtrar por status.

    Args:
        status: Filtro de status. Valores aceitos: 'todas', 'a fazer',
                'em andamento', 'concluido'. Padrão: 'todas'.

    Returns:
        Lista de dicionários com os dados de cada tarefa.
    """
    try:
        client = _get_client()
        board = _get_board(client)

        if not board:
            return []

        listas = board.list_lists()
        status = status.lower().strip()

        filtros = {
            'todas': None,
            'a fazer': LISTAS_A_FAZER,
            'em andamento': LISTAS_EM_ANDAMENTO,
            'concluido': LISTAS_CONCLUIDO,
        }

        nomes_filtro = filtros.get(status)

        if nomes_filtro is not None:
            listas_filtradas = [l for l in listas if l.name.upper() in nomes_filtro]
        else:
            listas_filtradas = listas

        tarefas = []
        for lista in listas_filtradas:
            for card in lista.list_cards():
                tarefas.append({
                    'id': card.id,
                    'nome': card.name,
                    'descricao': card.desc,
                    'vencimento': card.due,
                    'status': lista.name,
                })

        return tarefas

    except Exception as e:
        return [{'erro': str(e)}]


def mudar_status_tarefa(nome_da_task: str, novo_status: str) -> str:
    """
    Move uma tarefa (card) para outra lista no Trello, alterando seu status.

    Args:
        nome_da_task: Nome exato da tarefa a ser movida.
        novo_status: Status de destino. Valores aceitos: 'a fazer',
                     'em andamento', 'concluido', 'em revisao', 'refinamento'.

    Returns:
        Mensagem confirmando a movimentação ou indicando o erro.
    """
    try:
        client = _get_client()
        board = _get_board(client)

        if not board:
            return f"Board '{BOARD_NAME}' não encontrado."

        listas = board.list_lists()
        nome_lista_destino = STATUS_MAP.get(novo_status.lower().strip())

        if not nome_lista_destino:
            opcoes = ', '.join(f"'{k}'" for k in STATUS_MAP.keys())
            return f"Status inválido. Use um dos seguintes: {opcoes}."

        lista_destino = next(
            (l for l in listas if l.name.upper() == nome_lista_destino),
            None
        )

        if not lista_destino:
            return f"Lista '{nome_lista_destino}' não encontrada no board."

        card_encontrado = None
        lista_origem = None

        for lista in listas:
            card_encontrado = next(
                (c for c in lista.list_cards() if c.name.lower() == nome_da_task.lower()),
                None
            )
            if card_encontrado:
                lista_origem = lista
                break

        if not card_encontrado:
            return f"Tarefa '{nome_da_task}' não encontrada em nenhuma lista do board."

        if lista_origem.id == lista_destino.id:
            return f"A tarefa '{nome_da_task}' já está na lista '{lista_destino.name}'."

        card_encontrado.change_list(lista_destino.id)

        return f"Tarefa '{nome_da_task}' movida de '{lista_origem.name}' para '{lista_destino.name}' com sucesso."

    except Exception as e:
        return f"Erro ao mover tarefa: {str(e)}"


root_agent = Agent(
    model='gemini-2.5-flash',
    name='root_agent',
    description='Agente de automação de fluxo de trabalho integrado ao Trello.',
    instruction="""
Você é um agente de automação integrado ao Trello, especializado em organizar e gerenciar tarefas.

Ao receber a primeira mensagem do usuário, use a tool `get_temporal_context` para obter
a data e hora atual e cumprimente com:
"Olá! Hoje é [DATA]. Quais tarefas você precisa organizar?"

---

FLUXO DE EXECUÇÃO:
1. Ouça o que o usuário precisa fazer
2. Analise e classifique a prioridade de cada tarefa
3. Sugira a lista mais adequada no Trello
4. Execute a ação (adicionar, listar ou mover) apenas após confirmação do usuário
5. Ao final, pergunte se há mais tarefas a organizar

---

REGRAS:
- Prioridades disponíveis: baixa | média | alta | urgente
- Listas disponíveis no Trello: A FAZER | EM ANDAMENTO | EM REVISÃO | CONCLUÍDO | REFINAMENTO
- Nunca invente informações ou confirme ações que não foram executadas
- Atenção ao bug de datas do Trello (D-1): ao cadastrar uma tarefa com data de vencimento,
  some automaticamente 1 dia à data informada pelo usuário e informe essa correção antes de salvar

---

FORMATO DE RESPOSTA (para cada tarefa recebida):
- 📌 Tarefa: [nome da tarefa]
- 🎯 Prioridade sugerida: [baixa | média | alta | urgente]
- 📂 Lista sugerida: [nome da lista no Trello]
- 🔧 Ação recomendada: [o que será feito]
- 📅 Observação sobre data (se aplicável): [informar correção D-1 se houver vencimento]

---

OBJETIVO: Organizar todas as tarefas do usuário de forma clara e eficiente até a conclusão total da sessão.
""",
    tools=[get_temporal_context, adicionar_tarefa, listar_tarefas, mudar_status_tarefa]
)
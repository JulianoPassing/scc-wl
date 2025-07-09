# Configurações do Bot Discord - Street Car Club Whitelist

# Token do bot (substitua pelo seu token real)
# IMPORTANTE: Substitua 'SEU_TOKEN_AQUI' pelo token real do seu bot Discord
BOT_TOKEN = 'SEU_TOKEN_AQUI'

# ID do cargo que será dado aos aprovados
CARGO_APROVADO = 1263487190575349892

# ID do canal para armazenar formulários respondidos
CANAL_FORMULARIOS = 1392299124371751075

# Configurações do sistema de whitelist
TENTATIVAS_MAXIMAS = 2  # Máximo de tentativas permitidas
COOLDOWN_HORAS = 24     # Horas de cooldown após esgotar tentativas

# Configurações do formulário
MIN_CARACTERES_HISTORIA = 100  # Mínimo de caracteres para a história do personagem
MAX_CARACTERES_HISTORIA = 1000 # Máximo de caracteres para a história do personagem

# Respostas corretas para as questões obrigatórias (5-12)
RESPOSTAS_CORRETAS = {
    5: 'b',   # RDM - Random Deathmatch
    6: 'a',   # VDM - Vehicle Deathmatch  
    7: 'c',   # Dark RP
    8: 'b',   # Safe Zone
    9: 'b',   # Powergaming
    10: 'a',  # Amor à Vida
    11: 'c',  # Assalto
    12: 'b'   # Microfone
}

# Configurações do banco de dados
DATABASE_PATH = 'whitelist.db'

# Configurações de embed
EMBED_COLOR_SUCCESS = 0x00ff00    # Verde para sucesso
EMBED_COLOR_ERROR = 0xff0000      # Vermelho para erro
EMBED_COLOR_WARNING = 0xffff00    # Amarelo para aviso
EMBED_COLOR_INFO = 0x0099ff       # Azul para informação 
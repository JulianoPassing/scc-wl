import discord
from discord.ext import commands
import sqlite3
import asyncio
from datetime import datetime, timedelta
import json

# Configurações do bot
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix='/', intents=intents)

# ID do cargo aprovado
CARGO_APROVADO = 1263487190575349892

# Respostas corretas para as questões obrigatórias
RESPOSTAS_CORRETAS = {
    5: 'b',  # RDM
    6: 'a',  # VDM
    7: 'c',  # Dark RP
    8: 'b',  # Safe Zone (nota: você colocou B como correta, mas a resposta A parece mais apropriada)
    9: 'b',  # Powergaming
    10: 'a', # Amor à Vida
    11: 'c', # Assalto
    12: 'b'  # Microfone
}

# Inicializar banco de dados
def init_db():
    conn = sqlite3.connect('whitelist.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tentativas (
            user_id INTEGER,
            tentativas INTEGER DEFAULT 0,
            last_attempt TEXT,
            aprovado INTEGER DEFAULT 0
        )
    ''')
    conn.commit()
    conn.close()

# Verificar se usuário pode tentar
def pode_tentar(user_id):
    conn = sqlite3.connect('whitelist.db')
    cursor = conn.cursor()
    cursor.execute('SELECT tentativas, last_attempt, aprovado FROM tentativas WHERE user_id = ?', (user_id,))
    result = cursor.fetchone()
    conn.close()
    
    if not result:
        return True, 0
    
    tentativas, last_attempt, aprovado = result
    
    if aprovado:
        return False, -1  # Já aprovado
    
    if tentativas >= 2:
        if last_attempt:
            last_time = datetime.fromisoformat(last_attempt)
            if datetime.now() - last_time < timedelta(hours=24):
                return False, tentativas
    
    return True, tentativas

# Atualizar tentativas
def atualizar_tentativas(user_id, aprovado=False):
    conn = sqlite3.connect('whitelist.db')
    cursor = conn.cursor()
    cursor.execute('SELECT tentativas FROM tentativas WHERE user_id = ?', (user_id,))
    result = cursor.fetchone()
    
    if result:
        tentativas = result[0] + 1
        cursor.execute('UPDATE tentativas SET tentativas = ?, last_attempt = ?, aprovado = ? WHERE user_id = ?',
                      (tentativas, datetime.now().isoformat(), 1 if aprovado else 0, user_id))
    else:
        cursor.execute('INSERT INTO tentativas (user_id, tentativas, last_attempt, aprovado) VALUES (?, ?, ?, ?)',
                      (user_id, 1, datetime.now().isoformat(), 1 if aprovado else 0))
    
    conn.commit()
    conn.close()

class WhitelistModal(discord.ui.Modal):
    def __init__(self):
        super().__init__(title="Whitelist Street Car Club - Parte 1")
        
        self.nome = discord.ui.TextInput(
            label="1. Qual seu nome e sobrenome completo?",
            placeholder="Por extenso...",
            required=True,
            max_length=100
        )
        
        self.motivo = discord.ui.TextInput(
            label="2. Por que você quer jogar no Street Car Club?",
            placeholder="Por extenso...",
            required=True,
            max_length=500,
            style=discord.TextStyle.paragraph
        )
        
        self.add_item(self.nome)
        self.add_item(self.motivo)
    
    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.send_message("Continuando o formulário...", ephemeral=True)
        
        view = WhitelistView2(self.nome.value, self.motivo.value)
        embed = discord.Embed(
            title="Whitelist Street Car Club - Parte 2",
            description="3. Conheceu o servidor por onde?",
            color=0x00ff00
        )
        await interaction.followup.send(embed=embed, view=view, ephemeral=True)

class WhitelistView2(discord.ui.View):
    def __init__(self, nome, motivo):
        super().__init__(timeout=300)
        self.nome = nome
        self.motivo = motivo
        self.conheceu = None
    
    @discord.ui.button(label="A - Google", style=discord.ButtonStyle.primary)
    async def google(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.conheceu = "a"
        await self.continuar(interaction)
    
    @discord.ui.button(label="B - YouTube", style=discord.ButtonStyle.primary)
    async def youtube(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.conheceu = "b"
        await self.continuar(interaction)
    
    @discord.ui.button(label="C - Amigos", style=discord.ButtonStyle.primary)
    async def amigos(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.conheceu = "c"
        await self.continuar(interaction)
    
    @discord.ui.button(label="D - Outros", style=discord.ButtonStyle.primary)
    async def outros(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.conheceu = "d"
        await self.continuar(interaction)
    
    async def continuar(self, interaction):
        modal = HistoriaModal(self.nome, self.motivo, self.conheceu)
        await interaction.response.send_modal(modal)

class HistoriaModal(discord.ui.Modal):
    def __init__(self, nome, motivo, conheceu):
        super().__init__(title="Whitelist Street Car Club - História")
        self.nome = nome
        self.motivo = motivo
        self.conheceu = conheceu
        
        self.historia = discord.ui.TextInput(
            label="4. Crie a história sobre seu personagem...",
            placeholder="Mínimo 100 caracteres...",
            required=True,
            min_length=100,
            max_length=1000,
            style=discord.TextStyle.paragraph
        )
        
        self.add_item(self.historia)
    
    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.send_message("Iniciando questões obrigatórias...", ephemeral=True)
        
        view = QuestaoView(self.nome, self.motivo, self.conheceu, self.historia.value, 5, {})
        embed = discord.Embed(
            title="Questão 5/12 - OBRIGATÓRIA",
            description="O que é Random Deathmatch (RDM)?",
            color=0xff0000
        )
        await interaction.followup.send(embed=embed, view=view, ephemeral=True)

class QuestaoView(discord.ui.View):
    def __init__(self, nome, motivo, conheceu, historia, questao_atual, respostas):
        super().__init__(timeout=300)
        self.nome = nome
        self.motivo = motivo
        self.conheceu = conheceu
        self.historia = historia
        self.questao_atual = questao_atual
        self.respostas = respostas
        
        # Configurar questões
        self.questoes = {
            5: {
                "titulo": "O que é Random Deathmatch (RDM)?",
                "a": "É quando um jogador decide iniciar um combate e matar outro jogador, mas apenas depois de ter um motivo justo e uma longa interação de roleplay que justifique o conflito.",
                "b": "É o ato de um jogador matar outro (ou vários outros) de forma aleatória, sem qualquer motivo, história ou interação prévia que justifique a ação. É uma quebra grave da imersão no roleplay.",
                "c": "Refere-se a um evento oficial do servidor onde os jogadores são autorizados a lutar entre si em uma área designada para determinar o campeão do 'mata-mata'."
            },
            6: {
                "titulo": "O que é VDM ou Vehicle Deathmatch?",
                "a": "É usar o veículo como uma arma para atropelar e matar outros jogadores de propósito e sem um motivo de RP.",
                "b": "É usar o veículo para fugir da polícia em alta velocidade.",
                "c": "É participar em corridas de rua organizadas por outros jogadores."
            },
            7: {
                "titulo": "O que é Dark RP?",
                "a": "É um modo de jogo onde se interpreta apenas personagens policiais ou de forças especiais.",
                "b": "É um estilo de RP focado em realizar atividades criminosas apenas durante a noite no jogo.",
                "c": "É a prática de roleplay com temas pesados como tortura, assédio ou preconceito, geralmente proibidos nos servidores."
            },
            8: {
                "titulo": "O que é Safe Zone (Área Segura)?",
                "a": "São áreas designadas no mapa, como hospitais e praças, onde é proibido cometer crimes, agressões ou sequestros.",
                "b": "É qualquer local onde o jogador pode esconder seu dinheiro e itens ilegais.",
                "c": "É uma área onde apenas jogadores com permissão de administrador podem entrar."
            },
            9: {
                "titulo": "O que é Powergaming?",
                "a": "É usar o seu conhecimento de mecânicas do jogo para ter o máximo de dinheiro e as melhores armas.",
                "b": "É abusar de mecânicas do jogo ou forçar ações que seu personagem não seria capaz de fazer, para obter vantagens e 'vencer' no RP.",
                "c": "É interpretar um personagem que é fisicamente muito forte, como um lutador ou um guarda-costas."
            },
            10: {
                "titulo": "O que é Amor à Vida?",
                "a": "É agir de forma que valorize a vida do seu personagem, evitando se colocar em perigo desnecessário e reagindo ao medo.",
                "b": "É a regra que proíbe namorar outros personagens dentro do jogo.",
                "c": "É a obrigação de sempre chamar uma ambulância quando outro jogador se machuca."
            },
            11: {
                "titulo": "Em qual situação você assaltaria uma pessoa?",
                "a": "A partir das 22 horas.",
                "b": "Das 00 às 5 horas.",
                "c": "Não é permitido assalto."
            },
            12: {
                "titulo": "Você tem MICROFONE?",
                "a": "SIM",
                "b": "NÃO",
                "c": None
            }
        }
        
        # Configurar botões baseado na questão atual
        questao = self.questoes[questao_atual]
        
        self.add_item(discord.ui.Button(label=f"A - {questao['a']}", style=discord.ButtonStyle.primary, custom_id="a"))
        self.add_item(discord.ui.Button(label=f"B - {questao['b']}", style=discord.ButtonStyle.primary, custom_id="b"))
        
        if questao['c']:
            self.add_item(discord.ui.Button(label=f"C - {questao['c']}", style=discord.ButtonStyle.primary, custom_id="c"))
    
    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        button_id = interaction.data['custom_id']
        self.respostas[self.questao_atual] = button_id
        
        if self.questao_atual == 12:
            await self.finalizar(interaction)
        else:
            await self.proxima_questao(interaction)
        
        return True
    
    async def proxima_questao(self, interaction):
        proxima = self.questao_atual + 1
        questao = self.questoes[proxima]
        
        view = QuestaoView(self.nome, self.motivo, self.conheceu, self.historia, proxima, self.respostas)
        embed = discord.Embed(
            title=f"Questão {proxima}/12 - OBRIGATÓRIA",
            description=questao["titulo"],
            color=0xff0000
        )
        
        await interaction.response.edit_message(embed=embed, view=view)
    
    async def finalizar(self, interaction):
        # Verificar respostas obrigatórias
        corretas = 0
        for q in range(5, 13):
            if self.respostas.get(q) == RESPOSTAS_CORRETAS[q]:
                corretas += 1
        
        aprovado = corretas == 8  # Todas as 8 questões obrigatórias
        
        # Atualizar tentativas
        atualizar_tentativas(interaction.user.id, aprovado)
        
        if aprovado:
            # Dar cargo
            try:
                role = interaction.guild.get_role(CARGO_APROVADO)
                if role:
                    await interaction.user.add_roles(role)
                    embed = discord.Embed(
                        title="🎉 APROVADO! 🎉",
                        description=f"Parabéns {interaction.user.mention}! Você foi aprovado na whitelist do Street Car Club!\n\nTodas as questões obrigatórias foram respondidas corretamente.",
                        color=0x00ff00
                    )
                else:
                    embed = discord.Embed(
                        title="✅ APROVADO!",
                        description="Você foi aprovado! Porém houve um erro ao dar o cargo. Contate um administrador.",
                        color=0xffff00
                    )
            except:
                embed = discord.Embed(
                    title="✅ APROVADO!",
                    description="Você foi aprovado! Porém houve um erro ao dar o cargo. Contate um administrador.",
                    color=0xffff00
                )
        else:
            embed = discord.Embed(
                title="❌ REPROVADO",
                description=f"Você foi reprovado na whitelist.\n\nAcertou {corretas}/8 questões obrigatórias.\nÉ necessário acertar todas as questões de 5 a 12.",
                color=0xff0000
            )
        
        await interaction.response.edit_message(embed=embed, view=None)

class WhitelistView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    
    @discord.ui.button(label="🎯 Iniciar Whitelist", style=discord.ButtonStyle.green, custom_id="iniciar_wl")
    async def iniciar_whitelist(self, interaction: discord.Interaction, button: discord.ui.Button):
        # Verificar se pode tentar
        pode, tentativas = pode_tentar(interaction.user.id)
        
        if not pode:
            if tentativas == -1:
                embed = discord.Embed(
                    title="❌ Acesso Negado",
                    description="Você já foi aprovado na whitelist!",
                    color=0xff0000
                )
                await interaction.response.send_message(embed=embed, ephemeral=True)
                return
            else:
                embed = discord.Embed(
                    title="⏰ Cooldown Ativo",
                    description=f"Você já fez {tentativas} tentativas. Aguarde 24 horas para tentar novamente.",
                    color=0xff0000
                )
                await interaction.response.send_message(embed=embed, ephemeral=True)
                return
        
        # Iniciar formulário
        modal = WhitelistModal()
        await interaction.response.send_modal(modal)

@bot.event
async def on_ready():
    print(f'{bot.user} está online!')
    init_db()
    
    # Sincronizar comandos
    try:
        synced = await bot.tree.sync()
        print(f'Sincronizados {len(synced)} comandos')
    except Exception as e:
        print(f'Erro ao sincronizar comandos: {e}')

@bot.tree.command(name="formwlscc", description="Criar painel de whitelist do Street Car Club")
@discord.app_commands.describe(canal="Canal onde será criado o painel")
async def criar_painel(interaction: discord.Interaction, canal: discord.TextChannel = None):
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message("❌ Você não tem permissão para usar este comando!", ephemeral=True)
        return
    
    if canal is None:
        canal = interaction.channel
    
    embed = discord.Embed(
        title="🏁 Whitelist Street Car Club",
        description="""
        **Bem-vindo ao processo de whitelist!**
        
        Para fazer parte do nosso servidor de GTA RP, você precisa passar por um formulário de perguntas.
        
        **⚠️ IMPORTANTE:**
        • Questões 5 a 12 são obrigatórias
        • É necessário acertar TODAS para ser aprovado
        • Você tem 2 tentativas com cooldown de 24h
        
        **📋 O formulário inclui:**
        • Informações pessoais
        • História do personagem
        • Conhecimento sobre regras do servidor
        
        Clique no botão abaixo para começar!
        """,
        color=0x00ff00
    )
    
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1234567890/gta-rp-logo.png")  # Substitua pela URL real
    embed.set_footer(text="Street Car Club • Sistema de Whitelist")
    
    view = WhitelistView()
    await canal.send(embed=embed, view=view)
    
    await interaction.response.send_message(f"✅ Painel criado no canal {canal.mention}!", ephemeral=True)

@bot.tree.command(name="wlstatus", description="Verificar status da whitelist de um usuário")
@discord.app_commands.describe(usuario="Usuário para verificar (deixe vazio para verificar o seu)")
async def wl_status(interaction: discord.Interaction, usuario: discord.Member = None):
    if usuario is None:
        usuario = interaction.user
    
    # Verificar se o usuário que executou o comando tem permissão (apenas para outros usuários)
    if usuario != interaction.user and not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message("❌ Você não tem permissão para verificar outros usuários!", ephemeral=True)
        return
    
    conn = sqlite3.connect('whitelist.db')
    cursor = conn.cursor()
    cursor.execute('SELECT tentativas, last_attempt, aprovado FROM tentativas WHERE user_id = ?', (usuario.id,))
    result = cursor.fetchone()
    conn.close()
    
    if not result:
        embed = discord.Embed(
            title="📊 Status da Whitelist",
            description=f"**Usuário:** {usuario.mention}\n**Status:** Nunca tentou a whitelist",
            color=0x808080
        )
    else:
        tentativas, last_attempt, aprovado = result
        
        if aprovado:
            status = "✅ Aprovado"
            color = 0x00ff00
        else:
            status = "❌ Reprovado"
            color = 0xff0000
        
        embed = discord.Embed(
            title="📊 Status da Whitelist",
            description=f"**Usuário:** {usuario.mention}\n**Status:** {status}\n**Tentativas:** {tentativas}/2",
            color=color
        )
        
        if last_attempt:
            embed.add_field(name="Última tentativa", value=f"<t:{int(datetime.fromisoformat(last_attempt).timestamp())}:R>", inline=False)
    
    await interaction.response.send_message(embed=embed, ephemeral=True)

@bot.tree.command(name="resetwl", description="Resetar whitelist de um usuário")
@discord.app_commands.describe(usuario="Usuário para resetar")
async def reset_wl(interaction: discord.Interaction, usuario: discord.Member):
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message("❌ Você não tem permissão para usar este comando!", ephemeral=True)
        return
    
    conn = sqlite3.connect('whitelist.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM tentativas WHERE user_id = ?', (usuario.id,))
    conn.commit()
    conn.close()
    
    # Remover cargo se tiver
    try:
        role = interaction.guild.get_role(CARGO_APROVADO)
        if role and role in usuario.roles:
            await usuario.remove_roles(role)
    except:
        pass
    
    embed = discord.Embed(
        title="🔄 Whitelist Resetada",
        description=f"A whitelist de {usuario.mention} foi resetada com sucesso!",
        color=0x00ff00
    )
    
    await interaction.response.send_message(embed=embed, ephemeral=True)

# Token do bot - SUBSTITUA PELO SEU TOKEN
bot.run('SEU_TOKEN_AQUI') 
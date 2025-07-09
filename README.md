# Bot Discord - Sistema de Whitelist Street Car Club

Bot para sistema de whitelist automático para servidor de GTA RP do Street Car Club.

## 🚀 Funcionalidades

- **Formulário completo**: 12 perguntas incluindo informações pessoais e conhecimento de regras
- **Questões obrigatórias**: Questões 5-12 devem ser respondidas corretamente para aprovação
- **Sistema de tentativas**: Máximo 2 tentativas com cooldown de 24h
- **Atribuição automática de cargo**: Usuários aprovados recebem cargo automaticamente
- **Painel interativo**: Interface moderna com botões e modais
- **Banco de dados**: Armazena histórico de tentativas e status dos usuários
- **📋 Armazenamento de formulários**: Todos os formulários são salvos automaticamente em um canal específico

## 📋 Estrutura do Formulário

### Questões Livres (1-4)
1. **Nome completo** - Resposta por extenso
2. **Motivação** - Por que quer jogar no servidor
3. **Como conheceu** - Opções: Google, YouTube, Amigos, Outros
4. **História do personagem** - Mínimo 100 caracteres

### Questões Obrigatórias (5-12)
5. **RDM (Random Deathmatch)** - Resposta correta: **B**
6. **VDM (Vehicle Deathmatch)** - Resposta correta: **A**
7. **Dark RP** - Resposta correta: **C**
8. **Safe Zone** - Resposta correta: **B**
9. **Powergaming** - Resposta correta: **B**
10. **Amor à Vida** - Resposta correta: **A**
11. **Situação de assalto** - Resposta correta: **C**
12. **Microfone** - Resposta correta: **B**

## 🛠️ Configuração

### 1. Pré-requisitos
- Python 3.8 ou superior
- Conta Discord Developer
- Servidor Discord com permissões de administrador

### 2. Instalação

```bash
# Clone ou baixe os arquivos
cd discord_bot

# Instale as dependências
pip install -r requirements.txt
```

### 3. Configuração do Bot

1. **Crie um bot no Discord Developer Portal**:
   - Acesse https://discord.com/developers/applications
   - Crie uma nova aplicação
   - Vá em "Bot" e copie o token

2. **Configure as permissões**:
   - Administrator (recomendado)
   - Ou: Manage Roles, Send Messages, Use Slash Commands

3. **Edite o arquivo `config.py`**:
   ```python
   BOT_TOKEN = 'SEU_TOKEN_AQUI'  # Substitua pelo token do seu bot
   CARGO_APROVADO = 1263487190575349892  # ID do cargo para aprovados
   CANAL_FORMULARIOS = 1392299124371751075  # ID do canal para salvar formulários
   ```

4. **Encontre o ID do cargo**:
   - Ative o modo desenvolvedor no Discord
   - Clique com botão direito no cargo desejado
   - Copie o ID

### 4. Executar o Bot

```bash
python bot.py
```

## 📝 Comandos Disponíveis

### `/formwlscc`
- **Descrição**: Cria o painel de whitelist no canal
- **Permissão**: Administrador
- **Uso**: `/formwlscc` ou `/formwlscc canal:#canal`

### `/wlstatus`
- **Descrição**: Verifica status da whitelist de um usuário
- **Permissão**: Próprio usuário ou administrador
- **Uso**: `/wlstatus` ou `/wlstatus usuário:@usuario`

### `/resetwl`
- **Descrição**: Reseta whitelist de um usuário
- **Permissão**: Administrador
- **Uso**: `/resetwl usuário:@usuario`

## 🗄️ Banco de Dados

O bot usa SQLite para armazenar:
- **user_id**: ID do usuário Discord
- **tentativas**: Número de tentativas feitas
- **last_attempt**: Data da última tentativa
- **aprovado**: Status de aprovação (0 ou 1)

## 📋 Armazenamento de Formulários

### 🔧 Configuração
- **Canal configurado:** `1392299124371751075`
- **Variável:** `CANAL_FORMULARIOS` no arquivo `config.py`

### 📊 Informações Salvas
Quando alguém responde o formulário, o bot envia automaticamente um embed no canal com:

**👤 Dados do Usuário:**
- Nome Discord e ID
- Tag completa

**📝 Informações Pessoais:**
- Nome completo informado
- Como conheceu o servidor

**💭 Respostas Completas:**
- Motivação para jogar no servidor
- História do personagem (limitado a 500 caracteres por campo)

**📊 Questões Obrigatórias:**
- Todas as 8 respostas com status visual (✅/❌)
- Comparação com respostas corretas

**🎯 Resultado Final:**
- Status: Aprovado/Reprovado
- Número de acertos das questões obrigatórias

### 🎨 Visual dos Embeds
- **🟢 Verde:** Usuário aprovado
- **🔴 Vermelho:** Usuário reprovado
- **🕐 Timestamp:** Data e hora da resposta
- **🖼️ Avatar:** Foto do usuário como thumbnail

## 🔧 Personalização

### Alterar Questões
Edite as questões no arquivo `bot.py` na classe `QuestaoView`:

```python
self.questoes = {
    5: {
        "titulo": "Sua pergunta aqui",
        "a": "Opção A",
        "b": "Opção B",
        "c": "Opção C"
    }
}
```

### Alterar Respostas Corretas
Edite o dicionário `RESPOSTAS_CORRETAS` no arquivo `config.py`:

```python
RESPOSTAS_CORRETAS = {
    5: 'b',  # Altere para 'a', 'b' ou 'c'
    # ...
}
```

### Personalizar Embeds
Altere as cores e mensagens no arquivo `config.py`:

```python
EMBED_COLOR_SUCCESS = 0x00ff00  # Verde
EMBED_COLOR_ERROR = 0xff0000    # Vermelho
```

### Alterar Canal de Armazenamento
Para alterar o canal onde os formulários são salvos:

1. **Obtenha o ID do canal:**
   - Ative o modo desenvolvedor no Discord
   - Clique com botão direito no canal desejado
   - Copie o ID

2. **Edite o arquivo `config.py`:**
   ```python
   CANAL_FORMULARIOS = 1392299124371751075  # Substitua pelo ID do seu canal
   ```

## 🛡️ Segurança

- **Respostas privadas**: Formulário é enviado apenas para o usuário
- **Cooldown**: Previne spam de tentativas
- **Validação**: Verifica permissões antes de executar comandos
- **Backup**: Banco de dados pode ser facilmente backupeado

## 📊 Status e Monitoramento

O bot registra no console:
- Status de conexão
- Sincronização de comandos
- Erros e eventos importantes

## 🆘 Resolução de Problemas

### Bot não responde
- Verifique se o token está correto
- Confirme se o bot tem permissões necessárias
- Verifique se os comandos foram sincronizados

### Cargo não é atribuído
- Confirme se o ID do cargo está correto
- Verifique se o bot tem permissão "Manage Roles"
- Confirme se o cargo do bot está acima do cargo a ser atribuído

### Questões não aparecem
- Verifique se não há erros de sintaxe no código
- Confirme se o banco de dados foi criado corretamente

## 📄 Licença

Este projeto é de uso livre para servidores de GTA RP. Mantenha os créditos do desenvolvedor.

---

**Desenvolvido para Street Car Club**
*Sistema de Whitelist Automático v1.0* 
# 🚀 Como Executar o Bot

## ❌ Erro Comum
**NÃO execute com Node.js:**
```bash
node bot.py  # ❌ ERRO! Não funciona
```

## ✅ Forma Correta

### 1. Instalar dependências
```bash
pip3 install -r requirements.txt
```

### 2. Configurar token e canal
Edite o arquivo `config.py` e configure:
- `BOT_TOKEN`: Substitua `'SEU_TOKEN_AQUI'` pelo token real do seu bot Discord
- `CANAL_FORMULARIOS`: ID do canal onde os formulários serão salvos (já configurado: 1392299124371751075)

### 3. Executar o bot
```bash
python3 bot.py
```

**OU use o script automático:**
```bash
bash start.sh
```

## 📝 Resumo
- O bot é feito em **Python**, não JavaScript
- Use `python3` ao invés de `node`
- Configure o token antes de executar
- Instale as dependências primeiro

## 📋 Nova Funcionalidade - Armazenamento de Formulários
O bot agora salva automaticamente todos os formulários respondidos no canal configurado:

### 🔧 Configuração
- **Canal configurado:** `1392299124371751075`
- **Local da configuração:** `config.py` → `CANAL_FORMULARIOS`

### 📊 Informações Salvas
Quando alguém responde o formulário, o bot envia um embed no canal com:
- **Dados do usuário:** Nome, ID, tag Discord
- **Informações pessoais:** Nome completo, como conheceu o servidor
- **Motivação:** Por que quer jogar no servidor
- **História:** História do personagem criado
- **Questões obrigatórias:** Todas as 8 respostas com status (✅/❌)
- **Resultado final:** Aprovado/Reprovado + número de acertos

### 🎯 Cores dos Embeds
- **Verde:** ✅ Aprovado
- **Vermelho:** ❌ Reprovado

## 🔧 Verificar se Python está instalado
```bash
python3 --version
```

Se não tiver Python instalado, instale primeiro:
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install python3 python3-pip

# CentOS/RHEL
sudo yum install python3 python3-pip
``` 
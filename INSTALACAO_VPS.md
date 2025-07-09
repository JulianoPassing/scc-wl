# 🚀 Instalação Rápida - VPS

## Arquivos Necessários
- `bot.py` - Código principal do bot
- `config.py` - Configurações (EDITAR O TOKEN!)
- `requirements.txt` - Dependências Python
- `start.sh` - Script de inicialização Linux

## ⚡ Configuração Rápida

### 1. Upload dos arquivos para VPS
```bash
# Crie uma pasta para o bot
mkdir streetcar-whitelist
cd streetcar-whitelist

# Faça upload dos arquivos via FTP/SFTP ou git
```

### 2. Configurar Token
```bash
# Edite o arquivo config.py
nano config.py

# Altere esta linha:
BOT_TOKEN = 'SEU_TOKEN_AQUI'  # ← Coloque seu token aqui
```

### 3. Executar
```bash
# Dar permissão de execução
chmod +x start.sh

# Executar
./start.sh
```

## 🔧 Configuração do Bot Discord

1. **Discord Developer Portal**: https://discord.com/developers/applications
2. **Permissões necessárias**:
   - Administrator (recomendado)
   - Ou: Manage Roles + Send Messages + Use Slash Commands

## 📝 Comandos do Bot

- `/formwlscc` - Criar painel whitelist
- `/wlstatus` - Verificar status usuário  
- `/resetwl` - Resetar whitelist usuário

## 🏃‍♂️ Executar em Background

```bash
# Com screen
screen -S streetcar-bot
./start.sh
# Ctrl+A+D para desacoplar

# Com nohup
nohup python3 bot.py > bot.log 2>&1 &

# Com systemd (recomendado)
sudo systemctl enable streetcar-bot
sudo systemctl start streetcar-bot
```

## ⚙️ Cargo Aprovado

Altere o ID do cargo no `config.py`:
```python
CARGO_APROVADO = 1263487190575349892  # ← Seu ID do cargo
```

**Como pegar ID do cargo:**
1. Ativar modo desenvolvedor no Discord
2. Botão direito no cargo → "Copiar ID"

---
**Pronto para uso!** 🎯 
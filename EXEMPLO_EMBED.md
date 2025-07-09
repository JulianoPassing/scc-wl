# 📋 Exemplo do Embed Salvo no Canal

Quando um usuário responde o formulário, o bot envia automaticamente um embed no canal configurado (`1392299124371751075`) com o seguinte formato:

## 🟢 Exemplo - Usuário Aprovado

```
📋 Formulário de Whitelist Respondido

👤 Usuário
@João#1234
ID: 123456789012345678
Tag: João#1234

📝 Informações Pessoais
Nome: João Silva Santos
Conheceu por: YouTube

💭 Motivação
Quero jogar no servidor porque sempre gostei de GTA RP e quero fazer parte de uma comunidade organizada onde posso criar boas histórias de roleplay...

📖 História do Personagem
Meu personagem nasceu em Los Santos, sempre trabalhou como mecânico mas sonha em ter sua própria oficina. Veio de uma família humilde e sempre lutou para conseguir o que tem...

📊 Questões Obrigatórias (5-12)
Q5: B ✅
Q6: A ✅
Q7: C ✅
Q8: B ✅
Q9: B ✅
Q10: A ✅
Q11: C ✅
Q12: B ✅

🎯 Resultado Final
✅ APROVADO
Acertos: 8/8
```

## 🔴 Exemplo - Usuário Reprovado

```
📋 Formulário de Whitelist Respondido

👤 Usuário
@Maria#5678
ID: 987654321098765432
Tag: Maria#5678

📝 Informações Pessoais
Nome: Maria Oliveira
Conheceu por: Amigos

💭 Motivação
Quero jogar porque meus amigos jogam...

📖 História do Personagem
Minha personagem é legal e gosta de dirigir carros rápidos. Ela mora em Los Santos e trabalha...

📊 Questões Obrigatórias (5-12)
Q5: A ❌
Q6: B ❌
Q7: C ✅
Q8: A ❌
Q9: B ✅
Q10: B ❌
Q11: C ✅
Q12: A ❌

🎯 Resultado Final
❌ REPROVADO
Acertos: 3/8
```

## 🔧 Características do Embed

- **Cor:** Verde (aprovado) ou Vermelho (reprovado)
- **Timestamp:** Data e hora da resposta
- **Avatar:** Foto do usuário como thumbnail
- **Limites:** Textos longos são cortados em 500 caracteres
- **Status visual:** ✅ para correto, ❌ para incorreto
- **Automático:** Enviado sempre que alguém finaliza o formulário 
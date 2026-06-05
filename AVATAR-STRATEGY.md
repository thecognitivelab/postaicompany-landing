# Post AI Company — Avatar Strategy

## O Avatar

**Nome:** August (Auggie)
**Role:** Host e fundador visual da Post AI Company
**Personalidade:** Curioso, provocativo, acessível. Não é acadêmico. Não é corporativo. É o cara que lê a newsletter toda quarta, ouve o podcast, e traduz o que importa em 60 segundos.

**Tom de voz:** 
- "Marco e Lena passaram 47 minutos discutindo Midjourney. Eu resumo em 60 segundos."
- "Esse número me parou. $3.48 milhões por funcionário. Isso é 5.7x mais que uma empresa tradicional."
- "O que você faria na segunda de manhã com essa informação?"

**Aparência:** 
- ~35-40 anos, visual contemporâneo
- Fundo escuro, estúdio/quarto com iluminação lateral
- Vestuário casual-elegante (camisa escura, sem gravata)
- Gesticula naturalmente, olha pra câmera

**Relação com Marco e Lena:**
- August é fã do podcast. Ele escuta, reage, discorda também às vezes.
- "Marco falou uma coisa que eu nunca tinha pensado..."
- "Lena trouxe um dado que me fez parar tudo."

## Formatos de Clipe com August

### Formato 1: The Hook (30-45s)
August introduz o debate com a frase mais polêmica.

**Exemplo:**
```
[AUGUST na tela, olhando pra câmera]
"Onze pessoas. Duzentos milhões de dólares. Nenhum vendedor. Nenhum marketing.
Marco acha que é um outlier irrepetível. Lena acha que é o blueprint de toda empresa.
Eles discutiram por 47 minutos. Olha 60 segundos."

[CORTE para o áudio do podcast com waveform/legenda animada]
MARCO: "I don't buy that Midjourney is a blueprint..."
LENA: "Here's what the data actually says..."

[VOLTA AUGUST]
"Outlier ou blueprint? Comenta aqui. Episódio completo no link da bio."
```

### Formato 2: The Breakdown (60-75s)
August explica um conceito do episódio com suas palavras, intercalando com trechos do áudio.

### Formato 3: The Question (30s)
August faz uma pergunta provocativa baseada no episódio. Respostas nos comentários viram conteúdo pro próximo.

### Formato 4: The Data Drop (45s)
August apresenta um número do Post AI Index, com o gráfico na tela.

### Formato 5: Behind the Scenes (30s)
August comenta como o episódio foi feito. "A Lena e o Marco gravaram isso às 3 da manhã. O Marco tava de mau humor. Dá pra ouvir."

## Criação do Avatar no HeyGen

### Opção A: Photo Avatar (mais rápido, ~$1/criação)
1. Gerar uma foto do August via AI (Midjourney/DALL-E/Stable Diffusion)
2. Upload no HeyGen como Photo Avatar
3. HeyGen anima a foto com o áudio

**Custo:** $0.05/segundo de vídeo → ~$2-3/clipe de 60s

### Opção B: Studio Avatar (mais realista, ~$1/criação + $0.07/s)
1. Gerar foto de altíssima qualidade
2. Criar como Studio Avatar no HeyGen
3. Qualidade superior de movimentação labial e expressões

**Custo:** $0.067/segundo → ~$4/clipe de 60s

### Opção C: Digital Twin (mais caro, requer vídeo real)
1. Gravar 2 minutos de vídeo de uma pessoa real
2. HeyGen cria um digital twin
3. Qualidade máxima

**Custo:** $0.067/segundo + criação do twin

**Recomendação:** Começar com Photo Avatar (Opção A). Barato, rápido, testa o formato. Se engajar, upgrade pra Studio Avatar.

## Volume de Conteúdo

| Frequência | Formato | Duração |
|------------|---------|---------|
| 3x/semana | The Hook | 45s |
| 1x/semana | The Breakdown | 60-75s |
| 1x/semana | The Question | 30s |
| 1x/semana | The Data Drop | 45s |
| 1x/mês | Behind the Scenes | 30s |

**Total:** ~6 clipes por semana = ~24 por mês
**Custo mensal estimado (Photo Avatar):** ~$48-72/mês

## Pipeline Técnico

1. **Roteiro do clipe:** postai-writer gera script de 30-75s pro August
2. **Áudio August:** ElevenLabs com voz masculina dedicada
3. **Trechos podcast:** Cortar do áudio já gerado (Marco/Lena)
4. **Vídeo August:** HeyGen API com avatar + áudio August
5. **Edição:** Concatenar August + trechos podcast + legendas animadas
6. **Postagem:** Instagram Reels + TikTok + YouTube Shorts

## Próximos Passos

1. Gerar foto do August (preciso de descrição física detalhada)
2. Criar conta HeyGen e obter API key
3. Criar o avatar no HeyGen
4. Produzir os primeiros 3 clipes do Ep.1

# Post AI Sessions — Production Plan

## Reference: Lenny's Podcast
- Duração: 45-90 min
- Estilo: conversa entre hosts que se conhecem bem, tangentes naturais, momentos de humor, discordância real
- Distribuição: YouTube (vídeo) + Spotify/Apple (áudio) + transcrição no site
- Tom: rigoroso no conteúdo, descontraído na entrega

## Our Format: "Post AI Sessions"
- Duração alvo: 55-70 min
- Hosts: Marco (cético, ex-founder) e Lena (estrategista, data-driven)
- Frequência: quinzenal, quinta-feira

## Episódio 1 — Estrutura (60 min)

### Cold Open (3 min)
Marco e Lena conversam sobre algo aleatório da semana. Um experimento mental, uma notícia bizarra, uma ferramenta que um deles testou. Isso estabelece que são pessoas, não robôs.

Exemplo: Marco testou um AI agent que prometia substituir seu CFO. Durou 3 dias. Ele conta o que deu errado.

### Main Topic: Midjourney (35 min)
Dividido em atos, não em rounds rígidos:

**Ato 1: The Numbers (10 min)**
Lena apresenta os dados crus. Marco interrompe com perguntas. Eles discutem as fontes. Marco questiona a metodologia do Post AI Index. Lena defende. Isso não é um debate estruturado. É uma conversa onde um deles eventualmente diz "ok, fair point."

**Ato 2: The Architecture (15 min)**
Mergulham nas decisões de design organizacional do Midjourney. Discord, pricing, funding. Marco traz um contra-exemplo de uma empresa que tentou o mesmo e falhou. Lena conecta com os dados do Index.

**Ato 3: So What (10 min)**
O que um founder ou executivo faz com essa informação na segunda de manhã? Tangentes bem-vindas. Se Marco menciona um founder que conhece, eles exploram essa história por 3 minutos.

### Signals (7 min)
Cada um recomenda 2 coisas. Não só links. Marco recomenda um paper que leu e explica por que mudou sua opinião sobre algo. Lena recomenda uma ferramenta e conta como usou.

### Lightning Round (5 min)
Perguntas rápidas. "Worst AI take you saw this week?" "One thing you changed your mind about?" "What are you most worried about?"

### Outro (2 min)
Preview do próximo episódio. Call to action. Uma piada interna que só faz sentido se você ouviu o episódio todo.

## Produção Técnica

### Vozes
- ElevenLabs API para geração de voz
- Marco: voz masculina, ~35-45 anos, tom conversacional, pausas naturais
- Lena: voz feminina, ~30-40 anos, tom analítico mas caloroso
- Configurar "voice settings": stability 0.5, similarity 0.75, style 0.3

### Áudio
- Gerar falas individualmente e concatenar
- Adicionar pausas entre falas (0.3-0.8s)
- Respirações e hesitações ocasionais ("um", "hmm", "you know")
- Música: intro/outro curtos (10s), transições suaves
- Mixagem: compressão leve, EQ pra uniformizar vozes

### Vídeo (Fase 2)
- Opção A: Avatars animados (HeyGen/Synthesia) — mais caro, mais impacto
- Opção B: Waveform animado + slides com dados — mais barato, mais rápido
- Opção C: Só áudio no Spotify/Apple, YouTube com capa estática

### Transcrição
- Whisper (local) ou API para transcrição precisa
- Formatar com timestamps, nomes dos speakers
- Publicar no site como página complementar ao episódio

### Distribuição
- YouTube: vídeo com waveform/capa
- Spotify for Podcasters (Anchor): áudio
- Apple Podcasts: via RSS
- Site: player embed + transcrição + shownotes

## Stack
| Componente | Ferramenta | Custo estimado |
|------------|------------|-----------------|
| Vozes | ElevenLabs | ~$0.30/min → ~$20/ep |
| Roteiro | postai-writer + postai-audio | $0 (agente) |
| Edição áudio | pydub/ffmpeg | $0 |
| Transcrição | Whisper local | $0 |
| Vídeo | A decidir | $0-50/ep |
| Distribuição | Anchor (gratuito) | $0 |

## Próximos Passos
1. Reescrever roteiro Ep.1 no estilo Lenny (60 min, conversa fluida)
2. Configurar ElevenLabs (precisa de API key)
3. Gerar áudio do Ep.1
4. Publicar no Spotify + site
5. Vídeo (YouTube) na Fase 2

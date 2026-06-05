# Post AI Company — Autonomous Growth System

## Objetivo
Gerar tráfego, inscritos e conteúdo para postaicompany.com de forma 100% autônoma, sem intervenção humana após setup inicial.

## Arquitetura

```
┌─────────────────────────────────────────────────────────┐
│                    CRONJOBS (automáticos)                 │
│                                                          │
│  Seg 10h → Radar (curadoria newsletters)                 │
│  Seg 12h → Newsletter pipeline (Writer→FactCheck→Edit)  │
│  Qua 09h → Clipes D-ID (8 novos)                        │
│  Qui 09h → Postagem redes sociais (Buffer/Later)        │
│  Sex 10h → SEO report + indexação                        │
│  Dom 18h → Edição da semana seguinte (rascunho)         │
│                                                          │
│  Contínuo → Sitemap ping, GSC indexação, RSS update     │
└─────────────────────────────────────────────────────────┘
```

## Canais de Aquisição (100% autônomos)

### 1. SEO (Orgânico) — Totalmente autônomo ✅
- Site indexado com sitemap
- 7 páginas publicadas, crescendo 2-3/semana
- Palavras-chave: "revenue per employee AI", "post AI company", "AI-native startup"
- Interlinking entre edições
- Schema markup em cada página

### 2. Newsletter (Proprietário) — Totalmente autônomo ✅
- Pipeline automático toda segunda
- Resend para envio
- Meta: 5,000 subscribers em 6 meses

### 3. Podcast (Plataformas) — Semi-autônomo ⚠️
- RSS feed pronto
- Precisa: submeter 1x no Spotify/Apple (você)
- Depois: atualiza automaticamente a cada episódio

### 4. Redes Sociais (Clipes) — Precisa setup inicial ⚠️
- 8 clipes D-ID prontos por semana
- Precisa: conta Buffer ou Later (você cria 1x)
- Depois: postagem automática 3-4x/semana

## Setup Único (15 minutos seus)

### Ação 1: Buffer (5 min)
1. Acessar https://buffer.com
2. Criar conta (free tier: 3 canais)
3. Conectar Instagram Business + TikTok
4. Me passar o Buffer Access Token
5. → Eu configuro postagem automática

### Ação 2: Spotify for Podcasters (5 min)
1. Acessar https://podcasters.spotify.com
2. Login com conta Spotify
3. "Add podcast" → "I have an RSS feed"
4. Colar: https://postaicompany.com/podcast/feed.xml
5. → Pronto. Novos episódios entram automaticamente

### Ação 3: Apple Podcasts Connect (5 min)
1. Acessar https://podcastsconnect.apple.com
2. Login com Apple ID
3. "+" → "Add a show with an RSS feed"
4. Colar: https://postaicompany.com/podcast/feed.xml
5. → Pronto. Mesmo RSS, atualiza sozinho

## Métricas e Relatórios (automáticos)

Toda sexta-feira, um cronjob gera relatório com:
- Novos inscritos na newsletter
- Tráfego do site (Google Analytics ou Cloudflare)
- Clipes publicados e views
- Créditos D-ID restantes
- Rankings de SEO

## Pipeline de Conteúdo Semanal (zero intervenção)

| Dia | Ação | Output |
|-----|------|--------|
| Segunda 10h | Radar: curadoria 7 newsletters | /radar atualizado |
| Segunda 12h | Newsletter: Writer→FactCheck→Edit | /editions/00X publicado |
| Segunda 14h | Distribuição: SEO + social | Meta tags, GSC ping |
| Quarta 09h | Clipes: 8 vídeos D-ID | /clips/clip-XXX.mp4 |
| Quinta 09h | Postagem: Buffer → Instagram + TikTok | 3-4 posts |
| Sexta 10h | Relatório: métricas da semana | Relatório no Telegram |
| Domingo 18h | Rascunho: pauta da próxima edição | Rascunho pra revisão |

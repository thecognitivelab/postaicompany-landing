# POST AI SESSIONS — EPISODE 1
## "Midjourney and the Art of Not Building Things"

**HOSTS:**
- **Marco** — ex-founder, skeptic. Dry humor. Burned his last SaaS startup in 2023. Now consults for venture builders. Signature: "I don't know, man." "Show me."
- **Lena** — product strategist, data-oriented. Led growth at a startup from 10 to 500 people. Spends too much time on the Post AI Index. Signature: "Here's the thing." "The data is actually weirder than that."

**STYLE:** Lenny's Podcast. Two friends who disagree with respect. Tangents, interruptions, personal stories, real laughter. Zero AI sheen.

---

## COLD OPEN — [00:00 → 05:00]

[NOTA DE PRODUÇÃO: Começa direto, sem música de intro. Marco já está falando. Microfone próximo, som íntimo. Como se a conversa já estivesse rolando há 10 minutos antes de gravarem.]

---

**Marco:** ...so I get this email, right? "Introducing Cfo.ai — your autonomous AI chief financial officer." And I'm thinking, okay, bold claim. But I'm curious. I hate doing my own books. I've got this consulting thing now, it's not complicated — just me, some contractors, few recurring clients. So I sign up. Three hundred bucks a month. Connects to my QuickBooks, my bank, everything. And day one, I'm actually... impressed? It categorizes everything perfectly. Spots a subscription I forgot to cancel. Sends me this nice little dashboard. I'm like, okay, maybe I was wrong about this whole agent thing.

**Lena:** [rindo] Famous last words.

**Marco:** Day two. It tells me I should switch my business structure — from LLC to S corp. Gives me the tax math, the filing deadlines, everything. Very convincing. And I'm sitting there thinking, huh, my actual CPA told me the opposite six months ago. But this thing has charts. So I email my CPA. And I'm literally forwarding an AI's recommendation to a human professional, asking him to explain why he disagrees with the robot.

**Lena:** Oh no.

**Marco:** Day three. It sends me an alert. "Marco, you have an unallocated cash surplus of forty-seven thousand dollars. I recommend investing in a diversified portfolio of AI-focused ETFs to maximize returns while maintaining liquidity." Forty seven thousand dollars. That's, um... that's my tax reserve. The money I set aside to pay quarterly estimated taxes. Which it should know, because it can see my tax payments. It saw me make the exact same payment last quarter. But the AI — this autonomous CFO agent — it doesn't know what a tax reserve is. It just sees cash. And it wants to YOLO my tax money into AI stocks.

**Lena:** [rindo alto] It tried to gamble your IRS money on AI ETFs?

**Marco:** Yeah. The AI CFO wanted to bet on... AI. It was, like, recursively bullish on itself. [pausa] So I canceled. Three days. That's how long the autonomous CFO revolution lasted in my life. And here's the thing that actually bothers me — it wasn't a bad product. The categorization was great. The dashboard was clean. The S corp recommendation was probably correct. But it had one fatal flaw. It didn't know what it didn't know. And it was confident enough to put my tax compliance at risk. That's not a bug. That's the category.

**Lena:** Okay. So this is actually a perfect setup for what I wanted to talk about today. Because what you just described — an AI product that does eighty percent of the job beautifully and then faceplants on the twenty percent that actually matters — that's the default outcome for most AI companies right now. But Midjourney? Midjourney is the company that figured out which twenty percent to never touch.

**Marco:** Midjourney? The image generator?

**Lena:** Yeah. But not the product. The company.

**Marco:** What about the company?

**Lena:** Eleven people. Two hundred million dollars in revenue. And here's the part that I think actually connects to your AI CFO disaster — they didn't build most of the things that a normal company would build. No sales team. No marketing function. No free tier. No mobile app for years. No API until very recently. No enterprise plan. No managers, depending on who you ask. They said no to almost everything. And they printed money.

**Marco:** [pausa longa] Eleven people?

**Lena:** At the two hundred million mark. Around 2023. Depending on which source you trust, somewhere between eleven and maybe forty. But even at forty, you're looking at five million per employee. The average SaaS company does three hundred thousand.

**Marco:** That's... [pausa] okay hold on. That's a magic trick. And magic tricks don't scale.

**Lena:** [rindo] That is exactly the conversation we're about to have. Welcome to Post AI Sessions. I'm Lena.

**Marco:** I'm Marco.

**Lena:** And today: Midjourney — not the product, not the images, but the decisions. What they chose not to build. And what that tells us about designing companies when AI is doing more of the work.

**Marco:** She's going to try to convince me this is a blueprint. I'm going to ask annoying questions. Should be fun.

[NOTA DE PRODUÇÃO: Intro music sting — 8 segundos. Algo quente mas com um pouco de tensão, tipo Rival Consoles ou Jon Hopkins. Depois, fade para background suave.]

---

## MAIN CONVERSATION — [05:00 → 40:00]

[NOTA DE PRODUÇÃO: Isso não é um debate estruturado. É uma conversa. Às vezes eles vão concordar por 10 minutos e depois divergir completamente. Deixe as tangentes respirarem.]

---

**Lena:** So I want to start with the raw numbers, because I think they're genuinely staggering. And then we can fight about what they mean. Does that work?

**Marco:** That's fair. Lay them out.

**Lena:** Midjourney — founded by David Holz, 2021, same guy who co-founded Leap Motion before that. Bootstrapped. No venture capital. Launched the beta in 2022 on Discord. By 2023, they hit roughly two hundred million in annual recurring revenue with somewhere between eleven and forty employees. By 2025, five hundred million in revenue, about a hundred and seven employees. That's roughly four point seven million dollars per employee.

**Marco:** Source?

**Lena:** Sacra mainly. Forbes confirmed some of it. Contrary Research has pieces. The headcount number has some range but the revenue side is pretty consistent across sources.

**Marco:** Okay, but the headcount range is massive. Eleven versus forty is almost four times. If you're calculating efficiency ratios, that changes everything.

**Lena:** It changes the exact number. It doesn't change the order of magnitude. Even if you take the most conservative version — forty people at two hundred million — that's five million per employee. Still roughly fifteen times the SaaS average. The pattern holds regardless of which number you pick.

**Marco:** Hmm. [pausa] I mean, okay, the numbers are real. I'm not going to fight you on the numbers. But here's what bothers me — every time someone brings up Midjourney, they talk about the headcount like it's the headline. And I think the headline is actually the revenue. Two hundred million in ARR in, what, two years? With no sales team? Most SaaS companies would kill to have that revenue trajectory. The headcount efficiency is downstream of the revenue. So the interesting question isn't "how do you run lean?" It's "how do you make two hundred million dollars without a sales team?"

**Lena:** Yes! That's exactly it. And the answer, I think, is in what they didn't build. Let me walk through the three biggest decisions and you tell me which ones you buy.

**Marco:** Go.

**Lena:** First decision: Discord instead of a website. In 2022, every other AI company built a web app. Midjourney launched inside Discord. You type `/imagine` in a channel, and your image generates in public, in front of everyone. Every output is a demo. Every demo is an ad. Every ad builds the community. They didn't build a funnel — they built a town square.

**Marco:** [pausa] I have a problem with this one. And it's not that it didn't work — it clearly worked. It's that it's not replicable. Discord in 2022 had what, a hundred seventy five million active users? And Midjourney was one of the first AI products in there. If you launched a Discord-native AI product today, you'd be the nine hundredth thing in that channel. The window was unique. I don't think you can say "the Discord decision was genius" and then tell founders to do the same thing in 2026 when the landscape is completely different.

**Lena:** I don't think the lesson is "use Discord." The lesson is "don't build a funnel, build a community." Discord happened to be the right platform at the right time. But the principle — make your product visible in public, make every interaction a marketing event, let users onboard each other — that's portable.

**Marco:** But see, "community" is one of those words that means everything and nothing. Every founder says they're community-first. And then they build a Slack group with twelve people and call it a community. Midjourney didn't do "community" as a marketing tactic. They built their entire product inside the community. The product literally doesn't exist outside the social layer. That's not a community strategy. That's a completely different product architecture. And I don't think most founders have the stomach to build that way because it means giving up control.

**Lena:** Giving up control of what?

**Marco:** The funnel. The onboarding flow. The analytics. The a/b testing. All the things that growth teams obsess over. When your product lives in Discord, you can't optimize the signup flow because there is no signup flow. You can't track conversion funnels because there are no funnels. You're just... there. In the stream. And that's terrifying for a growth person.

**Lena:** [rindo] As a former growth person, I feel personally attacked.

**Marco:** I mean, you tell me. If I came to you in 2022 and said "Lena, we're going to launch our AI product with no landing page, no signup flow, no email capture, no onboarding sequence, no analytics, just a Discord bot" — what would you say?

**Lena:** I'd say you're insane. [pausa] And I'd be wrong. Which is actually my point — the things that growth people optimize for are sometimes the wrong things. Midjourney optimized for velocity and visibility. The friction of "go to website, create account, verify email, enter credit card, write first prompt" — all of that was gone. You join a Discord server and you type a command. That's it. The time from curiosity to first image is maybe thirty seconds. That's not a growth hack. That's a redesign of the customer journey.

**Marco:** It's also a massive bet on a platform you don't control. They're entirely dependent on Discord. What happens if Discord changes their API terms? What happens if Discord pivots? I've seen platform-dependent startups get burned. I lived through the Facebook Platform era. "Don't build on someone else's land" was lesson number one.

**Lena:** And they did eventually build their own web app. They weren't religious about it. The Discord launch was a wedge, not a forever strategy. By the time they built the web experience, they already had millions of users who were fluent in the product. The Discord era wasn't a dependency risk — it was an acquisition engine with zero CAC.

**Marco:** Zero CAC. God. [pausa] I spent forty thousand dollars on Facebook ads for my SaaS in 2022. Forty thousand dollars for maybe two hundred trial signups. And they got millions of users by being in a chat app.

**Lena:** And they charged from day one. That's decision number two. No free tier. No freemium. No "ten free generations and then pay." From the moment you joined, you got a handful of trial images and then you had to subscribe. Ten dollars a month for the basic plan.

**Marco:** That is insane. In 2022, everything was free. ChatGPT was free. Stable Diffusion was free and open source. Every AI product was racing to the bottom on pricing, trying to capture market share. And Midjourney just... charged. From day one.

**Lena:** And people paid. Two hundred million in revenue while competitors were burning venture money giving away free generations.

**Marco:** [pausa] But this is the one I actually think they got right, and I want to spend some time here because it connects to something I've been thinking about. There was this moment — I think it was 2023, early 2023 — where every AI founder had the same playbook. Raise a bunch of money, give the product away for free, acquire users, figure out monetization later. And it was stupid. It was the 2010 consumer startup playbook applied to a technology where the marginal cost isn't zero. Every image generation costs compute. Every LLM call costs tokens. You can't do the "scale first, monetize later" thing when your COGS scale linearly with usage.

**Lena:** Yes. And Midjourney understood something that I think a lot of AI founders still don't understand. Pricing isn't just a revenue lever. Pricing is a signal. When you charge from day one, you're saying: "this is worth money." You're attracting users who have intent. Users who are going to actually use the product, not just kick the tires. The free tier in AI — and I actually have data on this from the Index — the free tier in AI products generates conversion rates under two percent on average. Most free users never convert. They're there because it's free, not because they have a problem to solve.

**Marco:** Where's that number from?

**Lena:** Post AI Index. We've been tracking conversion data across the AI-native companies that report it. The median free-to-paid conversion rate is one point seven percent. For companies that charge from day one, the trial-to-paid conversion is around twelve to fifteen percent. It's not even close.

**Marco:** One point seven. So ninety eight percent of free users never pay. And you're paying compute for all of them. That's... that's a terrible business model.

**Lena:** It's a terrible business model that most AI startups are still running. Midjourney just skipped it. And here's the part that I think is actually the most instructive — they didn't just charge. They charged and they didn't build a sales team. Most B2B companies, when they charge significant money, they build a sales team to justify the price. Midjourney said: the product is the pitch. If you want it, you pay. If you don't, you leave. No demos. No sales calls. No enterprise negotiations.

**Marco:** [TOM IRÔNICO] It's almost like they respected their own time.

**Lena:** [rindo] Radical concept, right?

**Marco:** I want to push on the sales thing though. Because I think there's a version of this conversation where we oversimplify. Midjourney serves a market — creative professionals, designers, hobbyists — where self-serve works. The product output is literally the value prop. You see an image, you want to make images, you pay. It's the cleanest possible product-led growth loop. But if you're selling something that requires integration, that touches compliance, that needs procurement approval — self-serve doesn't work. The customer doesn't know they need you until you explain it to them.

**Lena:** I agree that the market matters. But I think you're underestimating how many markets actually work with self-serve now. Look at Lovable — no-code app builder. They're doing, what, four hundred million in ARR? No sales team. Look at Cursor — developer tool, a hundred million, no sales team. These aren't simple consumer products. They're tools that professionals use for work. And the professionals are finding them, trying them, and buying them without ever talking to a human.

**Marco:** Cursor's at a hundred million. I'm genuinely curious — do we actually know they have no sales team? Because I've heard conflicting things. Some people say they have a small enterprise team now.

**Lena:** They might have started building one at that scale. But they got to a hundred million without it. The point is that the default assumption — "if you sell to businesses, you need a sales team" — might not hold anymore. Or at minimum, the threshold at which you need one is much higher than we thought.

**Marco:** [pausa] Okay. Let me tell you a story. I know this founder — won't name him, he's still running the company — who tried to do the "no sales team" thing. AI-native product, self-serve onboarding, beautiful product. Got to about three million in ARR. And then they started losing deals. Not because the product was bad, but because the buyer at the companies they were selling to — usually a VP of engineering or a CTO — wanted to talk to someone. They wanted a demo. They wanted a security review. They wanted to know what happens if something breaks. And there was nobody to talk to. The company literally didn't have a human whose job it was to answer questions. And the buyers walked. Not because the product failed, but because the buying process required a human. And that requirement isn't about the product — it's about the organization's procurement culture.

**Lena:** What happened to the company?

**Marco:** They hired a sales team. Two people. And deals started closing. So my question is: was the "no sales team" model wrong? Or was it right for the first three million and then it hit a ceiling?

**Lena:** I think it's right for the first phase and wrong for the second. And I think Midjourney proves that the first phase can be much, much longer than we thought. Most companies hire sales at one million in ARR. Midjourney didn't need one at two hundred million. That's the thing that should make founders stop and think. Not "should I ever hire sales?" but "how far can I get before I need to?"

**Marco:** That's a better framing. I'll give you that. [pausa] But it circles back to what I said earlier — it's market-dependent. Midjourney is a consumer creative tool. The output is the pitch. You can't look at that and say "therefore, no B2B company should have sales."

**Lena:** I'm not saying no B2B company. I'm saying more B2B companies than we think. And the Post AI Index supports this. The median AI-native company in our dataset has zero or near-zero sales headcount through the first fifty million in revenue. That's not a Midjourney anomaly. That's a pattern.

**Marco:** [pausa] How many companies in the Index are past fifty million in revenue?

**Lena:** Uh... I think about twelve. Maybe fourteen.

**Marco:** So we're drawing conclusions about what "scales" from fourteen companies. And most of them are, what, three years old? Less?

**Lena:** They're young. I'm not claiming this is a mature dataset. I'm claiming it's a signal. And the signal is strong enough that founders should pay attention.

**Marco:** I'm not dismissing the signal. I'm just saying that the last time we had a signal this strong about "the new way to build companies," it was 2015 and the signal was "growth at all costs." And that turned out to be... [pausa] incomplete.

**Lena:** That's fair. But the difference is that "growth at all costs" was a strategy. What we're seeing in the Index isn't a strategy — it's a structural change. When AI handles the work that used to require five junior employees, the headcount math changes. That's not a philosophy. That's just... arithmetic.

**Marco:** [pausa longa] Okay let me take that apart. Because I think this is where a lot of people get confused. When you say "AI handles the work of five junior employees" — what work? What specific tasks? Because in my experience, the thing junior employees do that's hardest to replace isn't the output. It's the learning. The junior designer who watches the senior designer and learns taste. The junior salesperson who listens to calls and learns how to handle objections. The junior engineer who breaks the build and learns how to fix it. Those people aren't just producing work — they're becoming the senior employees of three years from now. If you eliminate those roles, where do the seniors come from?

**Lena:** That's... [pausa] that's actually a really good question. And I don't have a clean answer.

**Marco:** You don't? [TOM IRÔNICO] Lena doesn't have data on something?

**Lena:** [rindo] Shut up. [pausa] I genuinely think this is one of the hard problems. The pipeline. If you build a company where the work that juniors used to do is automated, how do you grow seniors? Midjourney hasn't had to solve this yet because they're still relatively small. Cursor hasn't had to solve it. But at some point, the people who built the thing leave or burn out or want to do something else. And if you haven't been growing the next layer, you have a gap.

**Marco:** This is literally what happened at my startup. We were lean — twelve people at our peak. Very efficient. And then our lead engineer left. Took a job at a bigger company for more money. And we realized we had nobody who understood the full system. Nobody. The bus factor was one. And it wasn't because we were badly managed — it was because we were so lean that knowledge concentrated. Every lean company has this problem at some scale.

**Lena:** Did you recover?

**Marco:** We hired someone. Took three months to ramp them up. By then we'd missed a product deadline that three different customers were waiting for. One of them churned. It wasn't fatal, but it was... it was a real cost of being lean. And nobody talks about this when they do the per-employee-revenue math. They just see "five million per employee, amazing." They don't see "one person has all the context, and if they leave, five million dollars of revenue is at risk."

**Lena:** This is the counterargument to the Midjourney model. Concentration risk. And I don't think Midjourney's structure solves it — I think they've just been lucky or good at retention. But the counter-counterargument is that AI itself might reduce the concentration risk. If AI tools capture institutional knowledge — if the system documents itself, if the prompts and workflows are preserved — then the bus factor goes up even with fewer people.

**Marco:** I want to believe that. But the AI CFO that tried to gamble my taxes? It didn't know what a tax reserve was. The knowledge it captured was wrong. It wasn't just incomplete — it was confidently wrong. And that's worse than not capturing the knowledge at all.

**Lena:** Your AI CFO was bad. Not all AI is bad.

**Marco:** No, but that's my point. The failure mode of AI isn't that it does nothing. It's that it does the wrong thing with high confidence. And in a lean company, if the AI that captures institutional knowledge is confidently wrong about something important, who catches it? The one senior person who's already overwhelmed?

**Lena:** [pausa] Okay. Let's shift to decision number three, because I think it connects to this. Midjourney's organizational structure — the "no managers" thing. David Holz has said he doesn't believe in traditional management. The company is organized around projects, not hierarchies. No middle management layer. People self-organize around problems.

**Marco:** [rindo] Every founder says this. "We're flat." "No hierarchy." "Everyone's a leader." And then you look under the hood and there's absolutely a hierarchy, it's just unspoken. And the unspoken hierarchies are worse because nobody can navigate them openly.

**Lena:** Right, but Midjourney seems to have actually done it. Or at least, reports from employees and former employees suggest it's genuinely flat in a way that most companies only pretend to be.

**Marco:** For how long? They're at a hundred and seven people now. Can you be flat at two hundred? At five hundred? Valve tried this. It worked at a hundred people. By five hundred, it was... complicated. By a thousand, there's a whole book about how it failed.

**Lena:** Valve is the canonical example. But Valve also predates AI-native workflows. What if AI changes the coordination cost? The reason you need managers in a traditional company is that coordination is expensive — you need someone to align priorities, resolve conflicts, track dependencies, report status. If AI tools handle a lot of that coordination — if the project management, the status tracking, the dependency mapping is automated — then the coordination layer shrinks. You need fewer managers because there's less to manage.

**Marco:** Hmm. [pausa longa] I've been in enough meetings to know that the hardest part of management isn't the tracking. It's the emotional stuff. The person who's frustrated but won't say it. The team that's in conflict but pretending everything is fine. The high performer who's quietly looking for another job. AI can't do any of that. And in a flat organization, those problems fester because there's nobody whose explicit job it is to notice and address them.

**Lena:** That's true. And I think most flat organizations fail exactly because of what you're describing. The emotional labor of coordination gets ignored, and then it explodes. But here's what's different about Midjourney — they're not just flat. They're also small. At a hundred people, you can still know everyone. The emotional dynamics are visible because the group is small enough that you actually talk to people. The flatness works because of the size, not despite it.

**Marco:** So the model is: stay small. Which brings us back to the question nobody can answer yet. Can you stay small and serve a million customers? Ten million? Can you do enterprise procurement, security audits, compliance, global support — with a hundred people? I don't know. And neither does anyone else, because nobody's done it.

**Lena:** I think Perplexity is a useful data point here. They grew revenue 5x while headcount grew 34 percent. Revenue is decoupling from headcount. If that trend holds...

**Marco:** "If that trend holds." That's doing a lot of work.

**Lena:** I know. But every trend starts somewhere, right? At some point, someone looked at the first SaaS companies and said "software margins are a fluke." And they weren't.

**Marco:** [pausa] Let me ask you something. If you were starting a company today — AI-native, Series A-ish scale, say you've got ten million in funding — would you actually try to run it like Midjourney? No managers, no sales team, Discord-native, charge from day one?

**Lena:** [pausa longa] I'd try to run it with Midjourney's principles. Not Midjourney's exact choices. Principles: charge early, distribute through community, hire for output not coordination, resist the urge to add layers. But I wouldn't copy the Discord thing mechanically. I wouldn't say "no managers ever." I'd say "no managers until it hurts, and then be very careful about which kind you add."

**Marco:** That's... more reasonable than I expected.

**Lena:** [rindo] Thanks?

**Marco:** No, I mean — the conversation usually goes one of two ways. Either "Midjourney is the blueprint, copy everything" or "Midjourney is a fluke, ignore it." And both are wrong. What you just said — extract the principles, apply them contextually — that's actually useful.

**Lena:** But you still don't think it's a blueprint?

**Marco:** I think it's a blueprint for a specific kind of company. Product that demonstrates its own value. Market that's self-serve capable. Category where the output is the pitch. If you check all three boxes, yeah, the Midjourney model is probably optimal. But most companies don't check all three boxes. And the danger is founders who check one box and think they're Midjourney.

**Lena:** I think more companies check the boxes than you think. But I take your point about the danger of cargo-culting.

**Marco:** Cargo-culting. That's exactly the word. [pausa] You know what I see happening right now? I see founders reading the Midjourney story and thinking "oh, the lesson is: don't hire." So they don't hire. And then they burn out their existing team. Or they miss opportunities because they don't have the bandwidth to pursue them. The lesson isn't "don't hire." The lesson is "don't hire for things that don't create value." But knowing the difference is actually really hard.

**Lena:** It's hard because the value of some roles is invisible until you don't have them. Customer success, for example. When everything's going well, you don't notice customer success. When things break, the lack of customer success becomes a crisis.

**Marco:** Right. Or the classic one: the project manager. Everyone hates project managers until they're gone. And then suddenly nothing ships on time and nobody knows why.

**Lena:** [rindo] I feel seen.

**Marco:** Were you a PM?

**Lena:** For five years. At the company that scaled from ten to five hundred people. And I'll tell you — at ten people, we didn't need a PM. At fifty, we absolutely did. At two hundred, we needed three. The coordination cost follows Metcalfe's law. It grows with the square of the number of people.

**Marco:** That's what I'm saying! The coordination cost is the hidden tax. And Midjourney avoided it by staying small. But the tax eventually comes for everyone if they grow. The question isn't whether you pay it — it's whether AI can reduce the rate.

**Lena:** [pausa] Okay, let's pull on this thread. You mentioned Block earlier. Meta. Companies that are cutting headcount with an AI rationale. What do you make of that?

**Marco:** I think it's mostly theater. Block cut forty percent of their workforce — four thousand people — and Dorsey framed it as "AI is making us more efficient." But look at Block's history. They over-hired during the pandemic like everyone else. They had bloated teams. The AI narrative is convenient cover for a correction that was going to happen anyway. Meta's similar — the eight thousand cuts were as much about Zuck wanting a leaner company as they were about AI replacing roles. These aren't AI-driven restructurings. They're restructurings with AI as the press release.

**Lena:** I actually agree on Block. The Dorsey memo was very... narrative-forward. But Meta is interesting because they're not just cutting — they're restructuring around AI. The "year of efficiency" was followed by massive AI investments. They're trying to build a company where AI is the platform and humans are the edge cases. That's not just a headcount trim. That's a redesign.

**Marco:** But it's a redesign from a position of having thirty years of legacy. All those teams, all those processes, all those managers — they're not starting from scratch. They're trying to retrofit AI efficiency onto a company built for human scale. And I think that's actually harder than starting lean from day one.

**Lena:** A hundred percent. Retrofitting is harder than building clean. Midjourney never had to retrofit. Holz never added the fat, so he never had to cut it. The advantage isn't just the efficiency — it's not having to do the painful restructuring that every incumbent is going through.

**Marco:** But the incumbents have something Midjourney doesn't: existing customers. Existing revenue. Existing distribution. If they can figure out the retrofit — big if, but if they can — they have a massive head start on anyone starting from scratch.

**Lena:** That's the race, right? Can the incumbents retrofit faster than the AI-natives can scale? And the answer is going to be different for every market.

**Marco:** Yeah. [pausa] Can we talk about Intuit for a second? Because I think they're an interesting case. They've been doing AI longer than most people realize. TurboTax and QuickBooks have AI features that go back years. And they're not cutting dramatically. They seem to be doing the thing where you integrate AI without blowing up the org structure. Is that a model? Or is that just being slow?

**Lena:** I think Intuit is doing the "augment, don't replace" model. AI makes their existing employees more productive, but they're not fundamentally redesigning the company around AI. And I think that approach works in the short term — you get efficiency gains without the pain of restructuring. The question is whether it's competitive in the long term against companies that are architecting from scratch.

**Marco:** I mean, Intuit's been around for forty years. They've survived every technology shift. Maybe the "augment, don't replace" model is the right one for incumbents. Maybe the Midjourney model is only for companies that are born in the AI era.

**Lena:** Or maybe Intuit is the next Nokia. Comfortable, profitable, and then suddenly irrelevant because the architecture changed and they didn't.

**Marco:** [pausa] Harsh.

**Lena:** The history of technology is not kind to incumbents who "augment" while newcomers "replace."

**Marco:** It's also not kind to newcomers who think they've found the one true way and then the market changes. [pausa] I don't think we're going to resolve this.

**Lena:** We're not. And that's okay. The show is about the question, not the answer.

**Marco:** That's very diplomatic.

**Lena:** [rindo] I'm learning.

[NOTA DE PRODUÇÃO: Pequena pausa. O ritmo diminui. Transição com uma música bridge curta — algo reflexivo, caloroso.]

---

## SIGNALS — [40:00 → 48:00]

[NOTA DE PRODUÇÃO: Cada host recomenda duas coisas. Não é só uma lista de links. São histórias sobre por que eles acham aquilo relevante. Background music mínimo ou nenhum.]

---

**Lena:** Okay. Signals time. Two things each that our listeners should pay attention to. These can be articles, tools, trends, whatever. But you have to explain why, not just name-drop.

**Marco:** You go first.

**Lena:** First signal: the Post AI Index. And before you roll your eyes —

**Marco:** [rindo] I wasn't going to roll my eyes.

**Lena:** You were definitely going to roll your eyes. But here's why. We've been updating it quarterly, and the Q2 update just dropped. We're now tracking sixty-three AI-native companies with verified revenue and headcount data. The median revenue-per-employee is up to three point seven million from three point four eight last quarter. The trend is accelerating, not plateauing. If you're a founder, an investor, or just someone trying to understand where company design is heading, the Index is the most concentrated source of data on the structural shift. It's free, it's at postaiindex.com, and we publish the methodology so you can judge for yourself whether the numbers are credible.

**Marco:** And Lena wrote the methodology. So no pressure.

**Lena:** I did. And I'd love for people to try to poke holes in it. That's how it gets better.

**Marco:** That's my job. I'm the hole-poker.

**Lena:** You are. Second signal: there's a paper that just came out of Stanford — "Organizational Design in the Age of Agentic Workflows." It's dense, it's academic, but the core argument is worth the effort. The authors model what happens to optimal team size and management span when AI agents handle coordination tasks that used to require human managers. Their finding is that the optimal team size roughly doubles when coordination is AI-assisted. Instead of a manager handling six to eight direct reports, you get twelve to sixteen. That has enormous implications for how companies should be structured. I'll link it in the show notes. Read the abstract at minimum.

**Marco:** That's a good rec. Doubling the management span changes everything about how you design an org. Who's the author?

**Lena:** I want to say... Bernstein and something. I'll get the exact citation. But it's on arxiv if you search for "agentic workflows organizational design."

**Marco:** Okay. My first signal: Anthropic's Agentic Coding Trends Report, 2026 edition. And this is not — I'm not shilling for Anthropic. I just think this report is genuinely useful. The core finding is that the primary human role in software development is shifting from writing code to orchestrating AI agents. Not "will shift" — "is shifting." The report breaks down which coding tasks agents handle autonomously — tests, boilerplate, refactoring, documentation — and which still require human judgment — architecture decisions, security-sensitive code, anything involving novel algorithms. If you're trying to figure out what your engineering team should look like in eighteen months, start there. It's free, open access, on their website.

**Lena:** I've seen that. The test generation numbers are wild — something like eighty percent of tests are now agent-written at Anthropic?

**Marco:** Yeah. And the thing I found most interesting — they said the bottleneck isn't the AI's capability anymore. It's the human's ability to review. The AI can generate more code than the humans can evaluate. So the constraint shifted from "can the AI do it?" to "can we trust what the AI did?" And that's a very different problem to solve.

**Lena:** That connects back to your AI CFO story. The confidence problem.

**Marco:** Exactly. The review bottleneck is the new bottleneck. And nobody's solved it yet. My second signal is more of a, um, a cautionary tale. There's a startup — I won't name it because the founder's a friend — that went all-in on the Midjourney model. Ten people, AI-native product, no managers, self-serve everything. They got to about two million in revenue. And then they lost their biggest customer. Not because of the product. Because the customer wanted a quarterly business review. A meeting. A human conversation about how they were using the product and what was coming next. And there was nobody to do it. The founder tried to do it himself, but he was also writing code, handling support, doing everything else. The QBR was bad. The customer felt neglected and left.

**Lena:** That hurts.

**Marco:** Yeah. And the lesson isn't "don't be lean." It's "know which human touchpoints actually matter and protect them." Some things don't scale with AI. Some things require a person in the room. The art is knowing which is which.

**Lena:** That's a really good example of what we were saying earlier. The principles apply, but context matters.

**Marco:** Yeah. [pausa] So those are my two: the Anthropic report for the engineering angle, and the cautionary tale for the "design your org thoughtfully" angle.

**Lena:** Good signals. I'll add them to the show notes.

---

## LIGHTNING ROUND — [48:00 → 53:00]

[NOTA DE PRODUÇÃO: Ritmo rápido. Sem música. Perguntas e respostas rápidas. Deixe os silêncios e hesitações — isso é o que torna humano.]

---

**Lena:** Lightning round. Quick questions, quick answers. Don't overthink it.

**Marco:** I always overthink it.

**Lena:** I know. Try anyway. First question: worst AI take you saw this week?

**Marco:** [sem hesitar] "AI will replace middle management by 2027." I saw this on LinkedIn. Some guy with "AI Evangelist" in his bio. And it's just... it's the perfect bad take because it sounds smart but it's actually meaningless. What does "replace middle management" even mean? The coordinating? The mentoring? The political navigating? Middle management is like ten different jobs in a trench coat. AI might do two of them. The other eight are still very human.

**Lena:** [rindo] "Ten different jobs in a trench coat." I'm using that.

**Marco:** What's yours?

**Lena:** "We don't need designers anymore, Midjourney handles all our visuals." I see this constantly in startup forums. And it's the same mistake as your AI CFO — confusing output with judgment. Midjourney can generate a hundred logo variations in ten seconds. It can't tell you which one communicates your brand. That's the designer's job. The tool changes the workflow, not the need for taste.

**Marco:** Yeah. The tool makes the execution cheaper. The decision gets more expensive, relatively. Because now you have a hundred options instead of three, and someone has to choose.

**Lena:** Exactly. Second question: one thing you changed your mind about recently?

**Marco:** [pausa] I used to think that AI would commoditize everything, and the only moat would be data. Now I think the moat is actually... integration depth. How deeply your product is embedded in the user's workflow. Midjourney isn't winning because of their model — every image model is catching up. They're winning because the product is where people already are, doing work they were already doing, in a workflow they've already built. That integration is hard to replicate. The model is the easy part.

**Lena:** That's a good change of mind. For me — I used to think that AI-native companies would eventually look like traditional companies, just more efficient. Now I think they're going to look fundamentally different. The org chart of a 2028 company won't be a leaner version of a 2024 company. It'll be a different shape entirely. Functions will merge. Roles will disappear, and new ones will emerge that don't have names yet. I don't think we're in an efficiency revolution. I think we're in a design revolution.

**Marco:** "Design revolution." I like that. I still think you're over-rotating on the forty-seven companies, but I like the phrase.

**Lena:** Sixty-three now.

**Marco:** [rindo] Sixty-three.

**Lena:** Third question: what are you most worried about that nobody is talking about?

**Marco:** [pausa longa] The talent pipeline. We touched on this earlier. If junior roles get automated, where do seniors come from in ten years? Every industry that's gone through automation — manufacturing, agriculture, retail — has had a transition period where the old training pathways broke down and the new ones took years to emerge. Software might be next. And I don't see anyone seriously working on the "how do we grow the next generation of senior engineers, designers, product people" problem. Everyone's focused on the productivity gains today. Nobody's thinking about the talent deficit in 2035.

**Lena:** That's a good one. Mine is... the monoculture risk. If every AI-native company converges on the same tooling, the same models, the same organizational design, we get a monoculture. And monocultures are fragile. One model has a security vulnerability and every company is exposed. One platform changes its pricing and every startup's unit economics break. The Midjourney model is powerful, but if everyone does it, we lose the diversity that makes the ecosystem resilient. I worry that efficiency is going to crowd out experimentation.

**Marco:** That's actually really interesting. The very thing that makes the model attractive — its replicability — is also the risk.

**Lena:** Yes. Last question: if you were starting a company today, what would you NOT build?

**Marco:** [sem hesitar] A sales team. Not until at least ten million in revenue. Maybe twenty. The evidence is too strong that you can get farther than we thought without one. What I would build instead: a product that demonstrates value in the first thirty seconds, pricing that's transparent and self-serve, and a community layer where users sell each other. That's harder than hiring two salespeople. But it's the right architecture.

**Lena:** I'd go further. I would not build a management layer. No VPs, no directors, no "head of" roles until the coordination cost is actually painful. And then I'd add one person — not a layer — and see if that solves it. The default should be "prove you need this role" not "every company has this role."

**Marco:** Both of those are Midjourney's decisions.

**Lena:** Yeah. They're Midjourney's decisions. But they're not just Midjourney's decisions. They're the emerging defaults for the post-AI era. And the companies that ignore them are going to have a cost structure problem that gets worse every year.

**Marco:** [pausa] I still think there are edge cases. But as a starting position? Yeah. I'd start there.

**Lena:** [rindo] From you, that's practically a standing ovation.

**Marco:** Don't get used to it.

---

## OUTRO — [53:00 → 60:00]

[NOTA DE PRODUÇÃO: O tom relaxa. Isso é dois amigos encerrando a conversa, não um programa de rádio. Música de fundo quente e baixa.]

---

**Lena:** Okay. So what did we actually land on?

**Marco:** I think we landed on: Midjourney's specific choices aren't the blueprint, but the principles behind them — charge early, distribute through community, hire for output not coordination, resist the urge to add layers — those are real. They're not universal, but they're a much better starting point than the 2015 playbook.

**Lena:** I think we landed on: the efficiency numbers are real and accelerating, but concentration risk is the unanswered question. The bus factor. The talent pipeline. The monoculture problem. The model works at a hundred people. Does it work at a thousand? At ten thousand? We don't know yet.

**Marco:** We don't know. And anyone who says they do is selling something. [pausa] But I also think we landed on something I'm actually excited about, which is: company design is interesting again. For twenty years, the answer to "how should I build my company?" was "look at any SaaS company." Now the answer is "it depends — what kind of product, what kind of market, what kind of customer?" The cookie-cutter era is over. And that's good.

**Lena:** The cookie-cutter era is over. I'm going to put that on a t-shirt.

**Marco:** You're welcome.

**Lena:** [rindo] Next episode, we're going to dig into something I've been obsessing over: the companies that are using AI agents not just for productivity but for actual decision-making. Not "AI writes my emails." "AI decides my pricing." "AI allocates my marketing budget." "AI hires my team." The autonomous company — is it coming, and should we want it?

**Marco:** Oh, I have feelings about this. Strong feelings. Mostly negative.

**Lena:** I know. That's why we're doing it.

**Marco:** [rindo] Before we go — if you want the data behind everything we talked about today, go to postaiindex.com. Lena builds it. I just complain about the methodology. But honestly, it's good. The index is good. The methodology is solid. You should check it out.

**Lena:** That might be the nicest thing you've ever said about the Index.

**Marco:** I'm in a good mood. It won't last.

**Lena:** Also, Post AI Weekly — we write about this stuff every week. The companies. The numbers. The decisions. Free newsletter. Link in the show notes.

**Marco:** Post AI Sessions. New episodes every Wednesday. I'm Marco.

**Lena:** I'm Lena.

**Marco:** Don't let an AI gamble your tax money.

**Lena:** [rindo] That's not our tagline.

**Marco:** It should be.

[NOTA DE PRODUÇÃO: Outro music — 30 segundos. Quente, resolvendo, com um toque de energia para o próximo episódio. Fade to silence.]

---

## PRODUCTION NOTES

### Timing Breakdown
- Cold Open: 00:00–05:00 (5 min)
- Main Conversation: 05:00–40:00 (35 min)
- Signals: 40:00–48:00 (8 min)
- Lightning Round: 48:00–53:00 (5 min)
- Outro: 53:00–60:00 (7 min — includes next episode preview and banter)
- TOTAL: ~60 minutes

### Host Voice Notes

**Marco:**
- Dry, understated. Humor comes from timing, not volume.
- Uses silence strategically. Pauses are real — he thinks before he speaks.
- Signature phrases feel natural: "I don't know, man." "Show me." "That's fair."
- When he concedes, he does it cleanly without hedging — then moves on.
- His skepticism comes from lived experience (burned startup), not contrarianism.
- Should sound like someone who wants to believe but has been burned enough to be careful.

**Lena:**
- Warmer than Marco but never deferential. Warmth is in pacing and tone, not in backing down.
- Delivers data with precision — slightly slower on numbers so they land.
- Signature phrases: "Here's the thing." "The data is actually weirder than that." "Okay but have you seen..."
- Genuinely excited by what she finds in the data. Not performative enthusiasm.
- Acknowledges good points before countering: "That's fair." "That's a good question."
- Should sound like someone who's done the homework and wants you to see what she sees.

### Dynamic Rules
- This is a conversation, not a debate. They agree sometimes for 10+ minutes, then diverge.
- Interruptions are natural — one person starts talking before the other finishes.
- Tangents are welcome. The talent pipeline tangent is an example. If the conversation naturally goes somewhere else for 3 minutes, let it.
- Disagreement is respectful and productive. They're testing ideas, not scoring points.
- The unresolved tension (scale? concentration risk? monoculture?) is intentional. Episode 1 sets up questions that future episodes explore.
- Laughter is real, not canned. Marco's dry delivery makes Lena laugh. Lena's earnestness makes Marco crack.

### Music & Sound Design
- Cold open: no music. Starts in the middle of the conversation.
- Intro sting after cold open: 8 seconds, warm with slight tension (think Rival Consoles, Jon Hopkins).
- Main conversation: optional low bed track, but not necessary. Silence is better than intrusive music.
- Bridge between conversation and signals: short reflective bridge, 5 seconds.
- Lightning round: no music.
- Outro: warm, resolving, 30 seconds.
- Overall: less music than a typical podcast. The conversation carries itself.

### Fact-Check Flags for Recording
1. Midjourney headcount at $200M ARR: disputed (11 vs ~40). Marco's skepticism addresses this. Verify sources before recording.
2. Post AI Index: 63 companies as of Q2 2026. Verify before recording.
3. Cursor $100M ARR / 20 employees: from Sacra. Verify.
4. Lovable $400M ARR / 146 employees: verify source.
5. Perplexity revenue growth and headcount data: verify before recording.
6. Block layoffs (Feb 2026): 40% / ~4,000 people. Verify.
7. Meta layoffs (May 2026): ~8,000 people. Verify.
8. Anthropic Agentic Coding Trends Report 2026: verify availability and correct title.
9. Stanford "Organizational Design in the Age of Agentic Workflows" paper: verify author and availability on arxiv.
10. All revenue-per-employee ratios are as of mid-2026. Adjust if recording date changes significantly.

### Language Guidelines
- English only. Zero exceptions.
- No em-dashes in the dialogue itself (production notes use hyphens).
- No ALL CAPS for emphasis — use timing and delivery instead.
- "Um", "hmm", "you know", "I mean", "wait, actually" — these are natural speech patterns. Use them.
- Hosts interrupt each other. Dialogue shows this through timing and pacing, not through explicit notation.
- Production notes in Portuguese (as written in the brief).

### Zero AI Sheen Checklist
- If a line sounds like a LinkedIn post, rewrite it.
- If a line sounds like a TED talk, rewrite it.
- If a line sounds like it was written to be quoted, rewrite it.
- The goal: the listener forgets these are AI voices. They sound like two smart friends at a coffee shop.

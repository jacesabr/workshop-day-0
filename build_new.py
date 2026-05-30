# -*- coding: utf-8 -*-
# Generates index-new.html from index.html: keeps all CSS + JS, swaps the
# section-nav menu, injects a small cue-deck style block, and replaces the
# <main> body with the new 12-slide cue deck.

import re

src = open('index.html', encoding='utf-8').read()

# ---------------------------------------------------------------- title
src = re.sub(r'<title>.*?</title>',
             '<title>Workshop Day 0 — Hello World (cue deck)</title>',
             src, count=1, flags=re.S)

# ---------------------------------------------------------------- new style
NEW_STYLE = """<style>
/* ─────────── CUE-DECK ADDITIONS ─────────── */
.ask {
  font-family: var(--serif);
  font-weight: 500;
  font-style: italic;
  font-size: clamp(28px, 4.6vw, 60px);
  line-height: 1.08;
  letter-spacing: -0.02em;
  color: var(--ink);
  max-width: 22ch;
  margin: 6px 0 18px;
  font-variation-settings: "SOFT" 50, "opsz" 96;
}
.ask em { font-style: italic; color: var(--vermillion); font-variation-settings: "SOFT" 100, "opsz" 96; }
.ask-tag {
  font-family: var(--mono);
  font-size: 10.5px;
  letter-spacing: 0.2em;
  text-transform: uppercase;
  color: var(--vermillion);
  font-weight: 700;
  margin-bottom: 14px;
  display: block;
}
.cue-note {
  margin-top: 18px;
  max-width: 74ch;
  font-family: var(--sans);
  font-size: clamp(17px, 1.8vw, 23px);
  line-height: 1.5;
  color: var(--ink-2);
  padding: 12px 18px;
  border-left: 3px solid var(--vermillion);
  background: rgba(214,62,42,0.05);
  border-radius: 0 4px 4px 0;
}
.cue-note em { font-style: italic; color: var(--vermillion); font-weight: 600; }

/* opener prompts — questions I ask the room (numbered presenter aid) */
.prompt-list { list-style: none; margin: 22px 0 0; padding: 0; max-width: 72ch; counter-reset: prompt; }
.prompt-list > li {
  position: relative;
  padding-left: 2.6ch;
  font-family: var(--serif);
  font-weight: 500;
  font-size: clamp(22px, 2.8vw, 38px);
  line-height: 1.14;
  color: var(--ink);
  margin-bottom: 24px;
  font-variation-settings: "SOFT" 40, "opsz" 48;
  counter-increment: prompt;
}
.prompt-list > li::before {
  content: counter(prompt);
  position: absolute;
  left: 0;
  top: 0.45em;
  font-family: var(--mono);
  font-size: 13px;
  font-weight: 700;
  letter-spacing: 0.04em;
  color: var(--vermillion);
}
.prompt-list em { font-style: italic; color: var(--vermillion); }
/* indented sub-cues under a question — referenced as 1a, 2a ... */
.sub-cues { list-style: none; margin: 10px 0 0; padding: 0; counter-reset: subcue; }
.sub-cues li {
  position: relative;
  padding-left: 2.6em;
  font-family: var(--sans);
  font-size: clamp(15px, 1.5vw, 19px);
  font-weight: 400;
  line-height: 1.35;
  color: var(--muted);
  margin-bottom: 6px;
  counter-increment: subcue;
}
.sub-cues li::before {
  content: counter(prompt) counter(subcue, lower-alpha);
  position: absolute;
  left: 0.2em;
  top: 0.1em;
  font-family: var(--mono);
  font-weight: 700;
  font-size: 0.95em;
  letter-spacing: 0.03em;
  color: var(--vermillion);
}

/* big lettered sub-points — quick reference handles for the presenter */
.lettered { counter-reset: subpt; }
.lettered > li { counter-increment: subpt; padding-left: 2em !important; }
.lettered > li::before {
  content: counter(subpt, upper-alpha) !important;
  position: absolute !important;
  left: 0 !important; top: -0.02em !important;
  width: auto !important; height: auto !important;
  background: none !important; border-radius: 0 !important;
  font-family: var(--mono); font-weight: 700;
  font-size: 1.3em; letter-spacing: 0.02em;
  color: var(--vermillion); line-height: 1.1;
}
/* lettered capability cards (slide 03) */
.modality-strip { counter-reset: ms; }
.ms-item { counter-increment: ms; }
.ms-item .ms-name::before {
  content: counter(ms, upper-alpha);
  display: inline-block;
  margin-right: 8px;
  font-family: var(--mono); font-weight: 700;
  color: var(--vermillion); font-size: 0.85em;
}

/* live-demo copy-paste prompts (slide 05) */
.demo-block { margin-top: 20px; width: 100%; max-width: 1120px; }
.demo-label {
  font-family: var(--mono); font-size: 11px; letter-spacing: 0.12em;
  text-transform: uppercase; color: var(--muted); margin-bottom: 10px;
}
.demo-prompts { display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; }
.prompt-card {
  border: 1px solid var(--hairline); border-radius: 4px;
  background: rgba(255,255,255,0.24); padding: 12px 13px;
}
.prompt-card .pc-genre {
  display: block; font-family: var(--mono); font-weight: 700;
  font-size: 10.5px; letter-spacing: 0.1em; text-transform: uppercase;
  color: var(--vermillion); margin-bottom: 10px;
}
.pc-field { margin-bottom: 10px; }
.pc-field:last-child { margin-bottom: 0; }
.pc-label {
  display: block; font-family: var(--mono); font-weight: 700;
  font-size: 9.5px; letter-spacing: 0.16em; color: var(--muted); margin-bottom: 3px;
}
.pc-text { font-family: var(--mono); font-size: 11.5px; line-height: 1.5; color: var(--ink-2); margin: 0; }
@media (max-width: 520px){ .demo-prompts { grid-template-columns: 1fr; } }

/* example-answer cues (slide 01) — lettered presenter prompts */
.ex-cues { list-style: none; margin: 12px 0 0; padding: 0; counter-reset: excue; max-width: 78ch; }
.ex-cues li {
  position: relative; padding-left: 2.4em;
  font-family: var(--sans); font-size: clamp(15px, 1.6vw, 21px);
  line-height: 1.4; color: var(--ink-2); margin-bottom: 8px;
  counter-increment: excue;
}
.ex-cues li::before {
  content: counter(excue, upper-alpha);
  position: absolute; left: 0; top: 0;
  font-family: var(--mono); font-weight: 700; font-size: 1.15em;
  color: var(--vermillion); line-height: 1.15;
}
.ex-cues li em { font-style: italic; color: var(--ink-2); }
.reflect-punch {
  margin-top: 20px; max-width: 900px;
  font-family: var(--serif); font-weight: 500;
  font-size: clamp(20px, 2.4vw, 32px); line-height: 1.2; color: var(--ink);
  font-variation-settings: "SOFT" 50, "opsz" 48;
}
.reflect-punch em { font-style: italic; color: var(--vermillion); }

/* the fork: not-this vs this */
.fork {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 18px;
  max-width: 940px;
  margin: 30px 0 0;
}
.fork-side {
  border: 1px solid var(--hairline);
  border-radius: 4px;
  padding: 22px 26px;
  background: rgba(255,255,255,0.20);
}
.fork-side .fs-tag {
  font-family: var(--mono);
  font-size: 10.5px;
  letter-spacing: 0.2em;
  text-transform: uppercase;
  margin-bottom: 12px;
  display: flex; align-items: center; gap: 9px;
}
.fork-side .fs-tag span { font-size: 14px; }
.fork-side .fs-line {
  font-family: var(--serif);
  font-size: clamp(20px, 2.3vw, 30px);
  line-height: 1.15;
  font-weight: 500;
  font-variation-settings: "SOFT" 40, "opsz" 48;
}
.fork-side.bad .fs-tag { color: var(--muted); }
.fork-side.bad .fs-line { color: var(--muted); }
.fork-side.good { border-color: var(--vermillion); background: rgba(214,62,42,0.06); }
.fork-side.good .fs-tag { color: var(--vermillion); }
.fork-side.good .fs-line { color: var(--ink); }
.fork-side.good .fs-line em { font-style: italic; color: var(--vermillion); }

.fork-q {
  margin: 26px 0 0;
  font-family: var(--serif);
  font-style: italic;
  font-size: clamp(22px, 3vw, 42px);
  line-height: 1.1;
  color: var(--ink);
  font-variation-settings: "SOFT" 60, "opsz" 72;
}
.fork-q em { color: var(--vermillion); }

@media (max-width: 720px){
  .fork { grid-template-columns: 1fr; }
}
</style>"""

src = src.replace('</style>\n</head>', '</style>\n' + NEW_STYLE + '\n</head>', 1)

# ---------------------------------------------------------------- nav menu
NEW_MENU = """    <div class="sn-menu" id="snMenu" role="menu" aria-label="Sections">
      <button class="dm-item active" type="button" role="menuitem"><span class="dm-num">00</span><span class="dm-name">Let&rsquo;s talk</span></button>
      <button class="dm-item" type="button" role="menuitem"><span class="dm-num">01</span><span class="dm-name">Reality check</span></button>
      <button class="dm-item" type="button" role="menuitem"><span class="dm-num">02</span><span class="dm-name">The big idea</span></button>
      <button class="dm-item" type="button" role="menuitem"><span class="dm-num">03</span><span class="dm-name">What AI can do</span></button>
      <button class="dm-item" type="button" role="menuitem"><span class="dm-num">05</span><span class="dm-name">Make a song</span></button>
      <button class="dm-item" type="button" role="menuitem"><span class="dm-num">06</span><span class="dm-name">Camera-shy</span></button>
      <button class="dm-item" type="button" role="menuitem"><span class="dm-num">07</span><span class="dm-name">You, with AI</span></button>
      <button class="dm-item" type="button" role="menuitem"><span class="dm-num">10</span><span class="dm-name">The expectation</span></button>
      <button class="dm-item" type="button" role="menuitem"><span class="dm-num">11</span><span class="dm-name">The 10 days</span></button>
    </div>
  </div>
</header>"""

mstart = src.find('    <div class="sn-menu" id="snMenu"')
mend = src.find('</header>', mstart) + len('</header>')
src = src[:mstart] + NEW_MENU + src[mend:]

# ---------------------------------------------------------------- main body
NEW_MAIN = """
    <!-- 00 Let's talk (conversation + fork) -->
    <section class="section in-view" id="s0">
      <div class="sec-eyebrow"><span class="num">00</span><span class="dot"></span><span>Day Zero &middot; Hello World</span><span class="rule"></span></div>
      <span class="ask-tag">Before anything &mdash; let&rsquo;s talk</span>
      <ul class="prompt-list">
        <li>Who&rsquo;s used an AI tool <em>this week</em>?
          <ul class="sub-cues">
            <li>what for?</li>
          </ul>
        </li>
        <li>Who feels like there&rsquo;s <em>so much</em> AI could do &mdash; but the second it&rsquo;s serious, complicated work, it just gets <em>confusing?</em>
          <ul class="sub-cues">
            <li>past the games and the gimmicks other people made</li>
          </ul>
        </li>
      </ul>
      <button class="next-btn">Begin <span class="arrow">&darr;</span></button>
    </section>

    <!-- 01 Reality check (imagine the person next to you) -->
    <section class="section" id="s_reality">
      <div class="sec-eyebrow"><span class="num">01</span><span class="dot"></span><span>Reality check</span><span class="rule"></span></div>
      <p class="sec-lede">Picture yourself in two years &mdash; college, a job, or running your own thing. The person next to you spent all that time using AI as an <em>extension to supercharge their abilities.</em></p>
      <p class="ask">What can they do now &mdash; that <em>you can&rsquo;t?</em></p>
      <ul class="ex-cues">
        <li>Reads a 300-page report in 10 minutes &mdash; walks in knowing the <em>5 things that matter</em></li>
        <li>Turns a rough idea into a working app in <em>10 minutes</em> &mdash; all his friends trying it and giving feedback &mdash; no coding background</li>
      </ul>
      <p class="reflect-punch">Two years in, that version of you has powerful abilities you <em>can&rsquo;t even picture right now</em> &mdash; that&rsquo;s how supercharged and enhanced you become.</p>
      <p class="cue-note">&hellip; the only thing between you and them is whether you start now. Let it sit for a second.</p>
      <button class="next-btn">Next: The big idea <span class="arrow">&darr;</span></button>
    </section>

    <!-- 02 The big idea (image-read engagement, not a statement) -->
    <section class="section" id="s_bigidea">
      <div class="sec-eyebrow"><span class="num">02</span><span class="dot"></span><span>The big idea</span><span class="rule"></span></div>
      <p class="ask">Is AI here to <em>replace</em> you &mdash; or make you <em>far more capable?</em></p>
      <div class="story-photo">
        <svg viewBox="0 0 480 270" xmlns="http://www.w3.org/2000/svg" preserveAspectRatio="xMidYMid meet" role="img" aria-label="A brain crackling with lightning and sparks">
          <circle cx="240" cy="135" r="58" fill="#F2ECDE" stroke="#1B1714" stroke-width="5"/>
          <path d="M240 77 q-14 28 0 58 q-14 28 0 58" fill="none" stroke="#1B1714" stroke-width="2.5"/>
          <path d="M204 108 q16 8 0 18 M204 138 q16 8 0 18 M276 108 q-16 8 0 18 M276 138 q-16 8 0 18" fill="none" stroke="#1B1714" stroke-width="2"/>
          <path d="M150 70 L185 100" stroke="#D63E2A" stroke-width="5" stroke-linecap="round"/>
          <path d="M330 70 L295 100" stroke="#D63E2A" stroke-width="5" stroke-linecap="round"/>
          <path d="M120 140 L165 140" stroke="#D63E2A" stroke-width="5" stroke-linecap="round"/>
          <path d="M360 140 L315 140" stroke="#D63E2A" stroke-width="5" stroke-linecap="round"/>
          <path d="M150 210 L185 180" stroke="#D63E2A" stroke-width="5" stroke-linecap="round"/>
          <path d="M330 210 L295 180" stroke="#D63E2A" stroke-width="5" stroke-linecap="round"/>
          <circle cx="106" cy="86" r="4" fill="#D63E2A"/>
          <circle cx="374" cy="86" r="4" fill="#D63E2A"/>
          <circle cx="240" cy="36" r="5" fill="#D63E2A"/>
          <circle cx="106" cy="194" r="3" fill="#D63E2A"/>
          <circle cx="374" cy="194" r="3" fill="#D63E2A"/>
        </svg>
      </div>
      <p class="cue-note">Let them throw out answers first &mdash; then land it: AI doesn&rsquo;t replace the brain, it amplifies it. A multiplier on what you can already do.</p>
      <button class="next-btn">Next: What it can do <span class="arrow">&darr;</span></button>
    </section>

    <!-- 03 What AI can do (ask what they use it for -> the wider expectation) -->
    <section class="section" id="s_modal">
      <div class="sec-eyebrow"><span class="num">03</span><span class="dot"></span><span>What AI can do now</span><span class="rule"></span></div>
      <p class="ask">What do <em>you</em> use AI for?</p>
      <p class="cue-note">Take their answers &mdash; then land it: a future employer will <em>appreciate</em> that you already do this&hellip; but they&rsquo;ll <em>require</em> you to naturally reach for &mdash; and combine &mdash; the other ways below, too.</p>
      <div class="modality-strip">
        <div class="ms-item"><div class="ms-name">Speak</div><div class="ms-desc">talk &amp; listen</div></div>
        <div class="ms-item"><div class="ms-name">See</div><div class="ms-desc">read your photos</div></div>
        <div class="ms-item"><div class="ms-name">Draw</div><div class="ms-desc">make images</div></div>
        <div class="ms-item"><div class="ms-name">Animate</div><div class="ms-desc">generate video</div></div>
        <div class="ms-item"><div class="ms-name">Compose</div><div class="ms-desc">write music</div></div>
      </div>
      <button class="next-btn">Next: Make a song <span class="arrow">&darr;</span></button>
    </section>

    <!-- 05 Suno (live creative activity + copy-paste demo prompts) -->
    <section class="section" id="s_suno">
      <div class="sec-eyebrow"><span class="num">05</span><span class="dot"></span><span>Example 1 &middot; Music</span><span class="rule"></span></div>
      <h2 class="payoff-lead">Let&rsquo;s make a song &mdash; <em>right now.</em></h2>
      <p class="cue-note">Say it: &ldquo;Okay everyone &mdash; let&rsquo;s have a little fun and see how creative you are. Download this app, type out a <em>vibe</em> and a <em>style of music</em>, give it some lyrics &mdash; and show us all how imaginative you can be.&rdquo;</p>
      <p class="sec-lede">Everyone: open <em>Suno</em> (suno.com or the app) &rarr; type a vibe + style &rarr; add a few lines of lyrics &rarr; generate &rarr; share your best one.</p>
      <div class="demo-block">
        <div class="demo-label">My laptop demo &mdash; Custom mode: paste the STYLE box, then the LYRICS box</div>
        <div class="demo-prompts">
          <div class="prompt-card">
            <span class="pc-genre">Pop-punk anthem</span>
            <div class="pc-field"><span class="pc-label">Style</span><p class="pc-text">Anthemic pop-punk, high energy, gang-vocal chorus, bright male tenor, distorted guitars, punchy live drums, 165 BPM</p></div>
            <div class="pc-field"><span class="pc-label">Lyrics</span><p class="pc-text">[Verse]<br>Alarm screaming, 6AM dread<br>Coffee cold, the cat's on my head<br>[Chorus]<br>Monday, you don't scare me anymore<br>Monday, I was built for this war</p></div>
          </div>
          <div class="prompt-card">
            <span class="pc-genre">Lo-fi study</span>
            <div class="pc-field"><span class="pc-label">Style</span><p class="pc-text">Lo-fi hip hop, warm and nostalgic, soft female vocals, breathy delivery, mellow Rhodes piano, vinyl crackle, brushed drums, 80 BPM</p></div>
            <div class="pc-field"><span class="pc-label">Lyrics</span><p class="pc-text">[Verse]<br>Two AM, the lamp still glows<br>Highlighter dreams, the coffee's cold<br>[Chorus]<br>One more page and then I'll go<br>Quiet little hours, just me and the snow</p></div>
          </div>
          <div class="prompt-card">
            <span class="pc-genre">Epic cinematic</span>
            <div class="pc-field"><span class="pc-label">Style</span><p class="pc-text">Epic cinematic orchestral, dramatic and tense, booming choir, thunderous taiko drums, soaring strings, trailer build, 140 BPM</p></div>
            <div class="pc-field"><span class="pc-label">Lyrics</span><p class="pc-text">[Verse]<br>The bars were full, the world was bright<br>Then the router died into the night<br>[Chorus]<br>The wifi's gone, the wifi's gone<br>We have to make it 'til the dawn</p></div>
          </div>
        </div>
      </div>
      <button class="next-btn">Next: Camera-shy <span class="arrow">&darr;</span></button>
    </section>

    <!-- 06 HeyGen (camera-shy -> live plastic-reel activity) -->
    <section class="section" id="s_heygen">
      <div class="sec-eyebrow"><span class="num">06</span><span class="dot"></span><span>Example 2 &middot; Video</span><span class="rule"></span></div>
      <ul class="prompt-list">
        <li>Who here makes <em>Insta reels?</em></li>
        <li>How long does it take to plan a reel that actually <em>makes an impact</em> on a topic?
          <ul class="sub-cues">
            <li>scripting, filming, the re-takes, editing&hellip;</li>
          </ul>
        </li>
      </ul>
      <p class="sec-lede">The whole point: <em>offload</em> the work, the time, the effort &mdash; and put everything into the <em>message.</em></p>
      <div class="scenario">
        <p class="sc-problem">&ldquo;Here&rsquo;s my problem: I want people to cut single-use plastic &mdash; but spreading that today means a reel: scripting, filming, editing&hellip; and I freeze on camera.&rdquo;</p>
      </div>
      <h2 class="payoff-lead">Your challenge: a finished awareness reel &mdash; <em>without filming a thing.</em></h2>
      <a class="hero-tool" href="https://www.heygen.com" target="_blank" rel="noopener">
        <div class="ht-tag">Use it to say something you&rsquo;d otherwise have to film yourself</div>
        <div class="ht-name">HeyGen <span class="ht-arrow">&#8599;</span></div>
        <div class="ht-url">heygen.com</div>
        <p class="ht-line">Record yourself once for two minutes. After that, type your message and <em>&ldquo;you&rdquo; deliver it on camera</em>.</p>
      </a>
      <p class="cue-note">I&rsquo;ll demo the HeyGen basics &mdash; then you&rsquo;ve got <em>5 minutes max</em> (about 2 of those to build your AI replica). Go.</p>
      <button class="next-btn">Next: This is you, with AI <span class="arrow">&darr;</span></button>
    </section>

    <!-- 07 This is you, with AI -->
    <section class="section" id="s_withai">
      <div class="sec-eyebrow"><span class="num">07</span><span class="dot"></span><span>This is you, with AI</span><span class="rule"></span></div>
      <h2 class="spoken">This is you, <em>with AI</em>&hellip;</h2>
      <div class="story-photo">
        <svg viewBox="0 0 480 270" xmlns="http://www.w3.org/2000/svg" preserveAspectRatio="xMidYMid meet" role="img" aria-label="A person standing tall with arms raised, sparkles around them">
          <line x1="36" y1="244" x2="444" y2="244" stroke="#1B1714" stroke-width="2"/>
          <ellipse cx="240" cy="248" rx="44" ry="7" fill="#1B1714" opacity="0.14"/>
          <g fill="none" stroke="#1B1714" stroke-width="6" stroke-linecap="round" stroke-linejoin="round">
            <circle cx="240" cy="80" r="22" fill="#F2ECDE"/>
            <path d="M240 102 L240 184"/>
            <path d="M240 124 L196 70"/>
            <path d="M240 124 L284 70"/>
            <path d="M240 184 L216 234"/>
            <path d="M240 184 L264 234"/>
          </g>
          <text x="170" y="60" font-family="Fraunces" font-size="22" fill="#D63E2A" font-weight="700">+</text>
          <text x="304" y="60" font-family="Fraunces" font-size="22" fill="#D63E2A" font-weight="700">+</text>
          <circle cx="150" cy="118" r="4" fill="#D63E2A"/>
          <circle cx="334" cy="118" r="4" fill="#D63E2A"/>
          <circle cx="120" cy="170" r="3" fill="#D63E2A"/>
          <circle cx="362" cy="170" r="3" fill="#D63E2A"/>
          <circle cx="240" cy="34" r="5" fill="#D63E2A"/>
        </svg>
      </div>
      <button class="next-btn">Next: The expectation <span class="arrow">&darr;</span></button>
    </section>

    <!-- 10 The expectation (the case) -->
    <section class="section" id="s_expect">
      <div class="sec-eyebrow"><span class="num">10</span><span class="dot"></span><span>The expectation</span><span class="rule"></span></div>
      <div class="thesis-wrap">
        <h2 class="thesis">These weren&rsquo;t party tricks.</h2>
        <p class="thesis-sub">This is the <em>baseline</em> now &mdash; for anyone who does anything, not just &ldquo;work.&rdquo;</p>
      </div>
      <p class="cue-note">Make them picture the gap: someone who <em>hasn&rsquo;t</em> learned AI is doing research with pen and paper &mdash; reading books in a library. Someone who <em>has</em> is using the internet and a computer. Same task &mdash; not even close.</p>
      <button class="next-btn">Next: What&rsquo;s next <span class="arrow">&darr;</span></button>
    </section>

    <!-- 11 Close -->
    <section class="section s-closing" id="s_close">
      <div class="closing-frame">
        <div class="closing-meta">Day Zero &middot; complete</div>
        <h2 class="closing-title">Now the <em>10 days.</em></h2>
        <ul class="closing-sub-bullets big-bullets lettered">
          <li>You just saw the whole map of AI in <em>one sitting.</em></li>
          <li>Next ten days: <em>build the things you keep meaning to build</em> &mdash; alongside a room of builders.</li>
        </ul>
        <div class="closing-actions">
          <a class="join-btn" href="#">Join the next cohort <span class="arrow">&rarr;</span></a>
          <button class="ghost" id="restart">&uarr; Back to top</button>
        </div>
      </div>
    </section>
"""

# strip illustrations — audience won't see the slides, so the sketches are dead weight
NEW_MAIN = re.sub(r' *<div class="story-photo">.*?</div>\n', '', NEW_MAIN, flags=re.S)

main_open = '<main class="main" id="main">'
main_close = '</main>'
mo = src.find(main_open) + len(main_open)
mc = src.find(main_close, mo)
# keep two-space indent before </main>
src = src[:mo] + NEW_MAIN + '\n  ' + src[mc:]

# auto-number eyebrows + nav by document order, so removing/adding slides never leaves a gap
def _renumber(html, cls):
    cnt = [0]
    def repl(m):
        v = '%02d' % cnt[0]; cnt[0] += 1
        return '<span class="%s">%s</span>' % (cls, v)
    return re.sub(r'<span class="' + cls + r'">\d+</span>', repl, html)
src = _renumber(src, 'num')
src = _renumber(src, 'dm-num')

open('index-new.html', 'w', encoding='utf-8').write(src)
print('wrote index-new.html, length', len(src))

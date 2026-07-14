const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const OUT = '/home/user/fbalfano/brand_assets';
const HTMLDIR = path.join(OUT, 'html');
fs.mkdirSync(HTMLDIR, { recursive: true });

// ---- Brand tokens ----
const C = {
  navy: '#0E2A47',
  navyDeep: '#081b30',
  navyMid: '#123a5e',
  gold: '#D4A94F',
  goldSoft: '#e3c078',
  cream: '#F6F1E7',
  mute: '#9db4c9',
  line: 'rgba(212,169,79,0.28)',
};

const houseSVG = (op = 0.10) => `
<svg class="motif" viewBox="0 0 200 200" fill="none" xmlns="http://www.w3.org/2000/svg" style="opacity:${op}">
  <path d="M20 96 L100 32 L180 96" stroke="${C.gold}" stroke-width="3" stroke-linejoin="round" stroke-linecap="round"/>
  <path d="M40 88 V172 H160 V88" stroke="${C.gold}" stroke-width="3" stroke-linejoin="round"/>
  <path d="M86 172 V126 H114 V172" stroke="${C.gold}" stroke-width="3" stroke-linejoin="round"/>
  <path d="M150 60 V44 H166 V74" stroke="${C.gold}" stroke-width="3" stroke-linejoin="round"/>
</svg>`;

const base = (n, inner, extraClass = '') => `<!doctype html><html><head><meta charset="utf-8">
<style>
  * { margin:0; padding:0; box-sizing:border-box; }
  :root{
    --navy:${C.navy}; --gold:${C.gold}; --cream:${C.cream}; --mute:${C.mute};
  }
  html,body{ width:1080px; height:1350px; }
  .slide{
    position:relative; width:1080px; height:1350px; overflow:hidden;
    background:
      radial-gradient(1200px 700px at 78% 8%, rgba(212,169,79,0.14), rgba(212,169,79,0) 60%),
      radial-gradient(900px 900px at 12% 100%, ${C.navyMid}, rgba(18,58,94,0) 55%),
      linear-gradient(160deg, ${C.navy} 0%, ${C.navyDeep} 100%);
    color:var(--cream);
    font-family:"Helvetica Neue","Liberation Sans",Arial,sans-serif;
    padding:96px 96px 84px;
    display:flex; flex-direction:column;
  }
  .serif{ font-family:Georgia,"Bitstream Charter","Liberation Serif",serif; }
  /* frame */
  .frameline{ position:absolute; inset:44px; border:1px solid ${C.line}; border-radius:14px; pointer-events:none; }
  .motif{ position:absolute; right:70px; bottom:70px; width:240px; height:240px; }
  .topbar{ display:flex; justify-content:space-between; align-items:center; position:relative; z-index:2; }
  .wordmark{ font-size:22px; letter-spacing:.28em; font-weight:700; text-transform:uppercase; color:var(--cream); display:flex; align-items:center; gap:12px;}
  .dot{ width:11px; height:11px; border-radius:50%; background:var(--gold); display:inline-block; }
  .count{ font-size:20px; letter-spacing:.18em; color:var(--mute); font-weight:600; }
  .count b{ color:var(--gold); }
  .body{ flex:1; display:flex; flex-direction:column; justify-content:center; position:relative; z-index:2; }
  .kicker{ text-transform:uppercase; letter-spacing:.34em; font-size:22px; font-weight:700; color:var(--gold); margin-bottom:34px; }
  h1{ font-size:104px; line-height:1.02; font-weight:700; letter-spacing:-.5px; }
  h1 em{ font-style:italic; color:var(--gold); }
  h2{ font-size:78px; line-height:1.05; font-weight:700; letter-spacing:-.5px; }
  .lede{ font-size:34px; line-height:1.5; color:#dfe7ef; max-width:800px; margin-top:38px; font-weight:300;}
  .rule{ width:120px; height:5px; background:var(--gold); border-radius:4px; margin:30px 0 0; }
  .footer{ display:flex; justify-content:space-between; align-items:center; position:relative; z-index:2; }
  .url{ font-size:26px; letter-spacing:.06em; color:var(--cream); font-weight:600; }
  .url span{ color:var(--gold); }
  .swipe{ font-size:24px; color:var(--mute); letter-spacing:.14em; text-transform:uppercase; font-weight:600; display:flex; align-items:center; gap:14px;}
  .dots{ display:flex; gap:10px; }
  .dots i{ width:9px; height:9px; border-radius:50%; background:rgba(255,255,255,0.22); }
  .dots i.on{ background:var(--gold); width:26px; border-radius:5px; }
  /* lists */
  ul.pain{ list-style:none; margin-top:20px; }
  ul.pain li{ font-size:37px; line-height:1.35; padding:22px 0; border-bottom:1px solid rgba(255,255,255,0.10); display:flex; gap:24px; align-items:flex-start; color:#e9eef4; font-weight:300;}
  ul.pain li .x{ color:var(--gold); font-size:34px; line-height:1.35; }
  ul.wins{ list-style:none; margin-top:26px; }
  ul.wins li{ font-size:38px; line-height:1.35; padding:20px 0; display:flex; gap:24px; align-items:flex-start; color:#eef2f7; font-weight:300;}
  ul.wins li .ck{ color:var(--gold); font-weight:700; font-size:36px; }
  ul.wins li b{ font-weight:700; color:var(--cream); }
  /* stats */
  .stats{ display:flex; flex-direction:column; gap:26px; margin-top:14px; }
  .stat{ border:1px solid ${C.line}; border-radius:16px; padding:34px 40px; background:rgba(255,255,255,0.03); display:flex; align-items:baseline; gap:28px;}
  .stat .num{ font-size:82px; font-weight:700; color:var(--gold); line-height:1; min-width:230px;}
  .stat .lab{ font-size:32px; color:#dfe7ef; font-weight:300; line-height:1.3;}
  /* CTA */
  .cta{ display:inline-flex; align-items:center; gap:18px; background:var(--gold); color:${C.navyDeep}; font-weight:700; font-size:34px; letter-spacing:.02em; padding:30px 52px; border-radius:60px; margin-top:44px; width:max-content;}
  .contact{ margin-top:52px; display:flex; flex-direction:column; gap:12px; font-size:30px; color:#dfe7ef; font-weight:300;}
  .contact b{ color:var(--cream); font-weight:700; }
  .note{ font-size:30px; color:var(--gold); font-weight:600; letter-spacing:.02em;}
</style></head><body>
<div class="slide ${extraClass}">
  <div class="frameline"></div>
  ${houseSVG(n === 1 ? 0.14 : 0.09)}
  <div class="topbar">
    <div class="wordmark"><span class="dot"></span>We Sell Your House</div>
    <div class="count"><b>${String(n).padStart(2,'0')}</b> / 07</div>
  </div>
  <div class="body">${inner}</div>
  <div class="footer">
    <div class="url">wesellyourhouse<span>.ca</span></div>
    <div class="dots">${[1,2,3,4,5,6,7].map(i=>`<i class="${i===n?'on':''}"></i>`).join('')}</div>
  </div>
</div></body></html>`;

const swipe = `<div class="swipe">Swipe <span style="color:var(--gold);font-size:30px">→</span></div>`;

// ---- Slides ----
const slides = [
  // 1 COVER
  base(1, `
    <div class="kicker">Home Sellers · Local Experts</div>
    <h1 class="serif">Thinking of<br>selling your <em>home?</em></h1>
    <div class="rule"></div>
    <div class="lede">Here's how the right team gets you sold faster, for more — without the stress.</div>
    <div style="height:40px"></div>
    ${swipe}
  `, 'cover'),

  // 2 PROBLEM
  base(2, `
    <div class="kicker">The old way</div>
    <h2 class="serif">Selling shouldn't<br>feel like this.</h2>
    <ul class="pain">
      <li><span class="x">✕</span><span>Endless showings that lead nowhere</span></li>
      <li><span class="x">✕</span><span>Lowball offers and second-guessing your price</span></li>
      <li><span class="x">✕</span><span>Surprise fees buried in the fine print</span></li>
      <li><span class="x">✕</span><span>Your listing sitting on the market for months</span></li>
    </ul>
  `),

  // 3 SOLD FASTER
  base(3, `
    <div class="kicker">Reason 01</div>
    <h2 class="serif">Sold faster.</h2>
    <div class="lede">Priced with real market data and marketed everywhere buyers are looking — so your home moves.</div>
    <ul class="wins">
      <li><span class="ck">✓</span><span><b>Data-driven pricing</b> that attracts serious offers</span></li>
      <li><span class="ck">✓</span><span><b>Pro photos &amp; listings</b> across every major portal</span></li>
      <li><span class="ck">✓</span><span><b>A ready buyer network</b> from day one</span></li>
    </ul>
  `),

  // 4 MORE MONEY
  base(4, `
    <div class="kicker">Reason 02</div>
    <h2 class="serif">More money<br>in your pocket.</h2>
    <div class="lede">Skilled negotiation and transparent, low fees mean more of the sale price stays with you.</div>
    <ul class="wins">
      <li><span class="ck">✓</span><span><b>Top-dollar negotiation</b> on every offer</span></li>
      <li><span class="ck">✓</span><span><b>Clear, upfront fees</b> — no surprises at closing</span></li>
      <li><span class="ck">✓</span><span><b>Strategic timing</b> to maximize your return</span></li>
    </ul>
  `),

  // 5 ZERO HASSLE
  base(5, `
    <div class="kicker">Reason 03</div>
    <h2 class="serif">Zero hassle.<br>Sell as-is.</h2>
    <div class="lede">We handle the heavy lifting from listing to keys — you just approve and sign.</div>
    <ul class="wins">
      <li><span class="ck">✓</span><span><b>Staging &amp; prep</b> handled for you</span></li>
      <li><span class="ck">✓</span><span><b>Showings &amp; paperwork</b> fully managed</span></li>
      <li><span class="ck">✓</span><span><b>Sell as-is</b> — no costly repairs required</span></li>
    </ul>
  `),

  // 6 PROOF / STATS
  base(6, `
    <div class="kicker">The results</div>
    <h2 class="serif">Homeowners<br>love the outcome.</h2>
    <div class="stats">
      <div class="stat"><div class="num">17</div><div class="lab">days average, list to sold*</div></div>
      <div class="stat"><div class="num">99%</div><div class="lab">of list price achieved on average*</div></div>
      <div class="stat"><div class="num">4.9★</div><div class="lab">from hundreds of local reviews*</div></div>
    </div>
  `),

  // 7 CTA
  base(7, `
    <div class="kicker">Your move</div>
    <h1 class="serif">Ready to<br>get <em>sold?</em></h1>
    <div class="lede">Start with a free, no-obligation home valuation. Find out exactly what your home is worth today.</div>
    <div class="cta">Book your free valuation →</div>
    <div class="contact">
      <div><b>Visit</b> &nbsp;wesellyourhouse.ca</div>
      <div><b>Call / Text</b> &nbsp;(000) 000-0000</div>
    </div>
  `, 'ctaSlide'),
];

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1080, height: 1350 }, deviceScaleFactor: 2 });
  for (let i = 0; i < slides.length; i++) {
    const n = i + 1;
    const html = slides[i];
    const htmlPath = path.join(HTMLDIR, `slide-${n}.html`);
    fs.writeFileSync(htmlPath, html);
    await page.setContent(html, { waitUntil: 'networkidle' });
    const pngPath = path.join(OUT, `slide-${n}.png`);
    await page.screenshot({ path: pngPath, clip: { x: 0, y: 0, width: 1080, height: 1350 } });
    console.log('rendered', pngPath);
  }
  await browser.close();
})().catch(e => { console.error(e); process.exit(1); });

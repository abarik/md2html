---
title: "Középértékek és szóródási mutatók"
subtitle: "Az eloszlás helyzete, alakja és szóródása"
author: "Abari Kálmán"
date: "2026. ősz"
lang: hu
footer: "Matematikai alapok II. · 4. Középértékek és szóródási mutatók"
---

## Három kérdés az eloszlásról

```{=html}
<div class="grid" style="--cols:3">
  <div class="stat"><b>Hol?</b><small style="font-size:20px"><strong>Középértékek:</strong> átlag, medián, módusz, trimmelt átlag</small></div>
  <div class="stat"><b>Milyen alakú?</b><small style="font-size:20px"><strong>Alakmutatók:</strong> ferdeség, csúcsosság</small></div>
  <div class="stat"><b>Mennyire szóródik?</b><small style="font-size:20px"><strong>Szóródási mutatók:</strong> terjedelem, IQR, átlagos eltérés, szórás, relatív szórás</small></div>
</div>
<script>
// közös segédfüggvények a diasor ábráihoz
window.Plot = {
  NS: 'http://www.w3.org/2000/svg',
  fmt: (v, d = 0) => v.toLocaleString('hu-HU', {minimumFractionDigits: d, maximumFractionDigits: d}),
  scale: (d0, d1, r0, r1) => v => r0 + (v - d0) / (d1 - d0) * (r1 - r0),
  el(parent, tag, a = {}, text) {
    const e = document.createElementNS(this.NS, tag);
    for (const k in a) e.setAttribute(k, a[k]);
    if (text != null) e.textContent = text;
    return parent.appendChild(e);
  },
  rng(seed) {  // determinisztikus álvéletlen-generátor (mulberry32)
    return () => { seed = seed + 0x6D2B79F5 | 0; let t = Math.imul(seed ^ seed >>> 15, 1 | seed); t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; };
  },
  normal(rnd) { return Math.sqrt(-2 * Math.log(1 - rnd())) * Math.cos(2 * Math.PI * rnd()); }
};
</script>
```

Egyetlen szám sosem írja le teljesen az adatokat: a mutatókat **együtt**, és mindig **ábrával** együtt értelmezzük.

# Középértékek

## Átlag (számtani közép)

Az $x_1, x_2, \ldots, x_n$ minta átlaga az értékek összege osztva az elemszámmal:

$$\bar{x} = \frac{1}{n}\sum_{i=1}^{n} x_i$$

- Az átlagtól mért eltérések összege **nulla**: $\sum_{i=1}^{n}(x_i - \bar{x}) = 0$ – az átlag a minta „súlypontja”
- Az átlag az a szám, amelytől mért **négyzetes** eltérések összege a legkisebb
- *Példa:* 3, 8, 6, 14, 0, −4, 0, 12, −7, 0, −10 → $\bar{x} = 22 / 11 = 2$

## Medián

Legalább **ordinális** skálájú változónál: rendezzük az adatokat ($x_{(1)} \le x_{(2)} \le \ldots \le x_{(n)}$), és válasszuk ki a **középsőt**; páros $n$ esetén a két középső átlagát.

| Minta | Rendezve | Medián |
|:--|:--|--:|
| 2, 8, 5, 4, 7 | 2 < 4 < **5** < 7 < 8 | 5 |
| 2, 8, 5, 4, 7, 4 | 2 < 4 = **4** < **5** < 7 < 8 | (4 + 5) / 2 = 4,5 |
| 3, 8, 6, 14, 0, −4, 2, 12, −7, −1, −10 | −10, −7, −4, −1, 0, **2**, 3, 6, 8, 12, 14 | 2 |

A medián az a szám, amelytől mért **abszolút** eltérések összege a legkisebb; kiugró értékekre nem érzékeny – **robusztus** mutató.

## Módusz

- A mintában **leggyakrabban** előforduló érték; nominális változónál is értelmezhető
- Nem mindig egyértelmű: lehet több módusz (**bimodális**, multimodális eloszlás)
- Megbízhatóan inkább nagyobb (50–100 elemű) mintáknál értelmezzük

*Példa:* 3, 5, 1, 4, 2, 9, 6, 10, 5, 3, 4, 3, 9, 3, 6, 1

| Érték | 3 | 1 | 4 | 5 | 6 | 9 | 2 | 10 |
|:--|--:|--:|--:|--:|--:|--:|--:|--:|
| Gyakoriság | **4** | 2 | 2 | 2 | 2 | 2 | 1 | 1 |

: A módusz a 3 (négyszer fordul elő).

## Melyik középértéket válasszuk? {.smaller}

| Mérési szint | Módusz | Medián | Átlag |
|:--|:-:|:-:|:-:|
| Nominális | ✓ | – | – |
| Ordinális | ✓ | ✓ | – |
| Intervallum, arány | ✓ | ✓ | ✓ |

- **Szimmetrikus**, kiugró értékek nélküli eloszlásnál az átlag a leghatékonyabb
- **Ferde** eloszlásnál vagy **kiugró** értékek esetén a medián vagy a **trimmelt átlag** (pl. a legkisebb és a legnagyobb 20% elhagyásával számolt átlag) jobb választás [(Wilcox, 2017)]{.cite}
- A pszichológiában tipikus példa a **reakcióidő**: jobbra ferde, alkalmanként nagyon hosszú értékekkel (figyelmi kihagyás) [(Ratcliff, 1993)]{.cite}

## Próbálja ki: átlag vagy medián?

Tíz reakcióidő (ms); az utolsó értéket – például egy figyelmi kihagyást – a csúszkával lehet változtatni:

```{=html}
<div class="widget"><svg id="mm-plot" viewBox="0 0 1000 190" role="img" aria-label="Reakcióidők, átlag, medián és trimmelt átlag"></svg></div>
<div class="controls" style="margin-top:12px">
  <label><span>A 10. reakcióidő: <output id="mm-v-o"></output> ms</span>
    <input id="mm-v" type="range" min="500" max="1500" step="10" value="580"></label>
</div>
<div class="grid" style="--cols:3;margin-top:12px">
  <div class="stat"><b id="mm-mean"></b><small>átlag</small></div>
  <div class="stat"><b id="mm-med"></b><small>medián</small></div>
  <div class="stat"><b id="mm-trim"></b><small>20%-os trimmelt átlag</small></div>
</div>
<script>
(() => {
  const P = window.Plot, $ = id => document.getElementById(id), svg = $('mm-plot');
  const base = [420, 445, 460, 475, 490, 505, 520, 540, 565];
  const x = P.scale(380, 1540, 30, 970), y = 130;
  function draw() {
    const v = +$('mm-v').value, d = [...base, v].sort((a, b) => a - b), n = d.length;
    const mean = d.reduce((a, b) => a + b) / n, med = (d[n / 2 - 1] + d[n / 2]) / 2;
    const trim = d.slice(2, n - 2).reduce((a, b) => a + b) / (n - 4);
    svg.replaceChildren();
    P.el(svg, 'line', {class: 'axis', x1: 30, x2: 970, y1: y, y2: y});
    for (let t = 400; t <= 1500; t += 100) P.el(svg, 'text', {class: 'tick', x: x(t), y: y + 28, 'text-anchor': 'middle'}, t);
    [[med, 'medián', 'var(--accent)', 22], [trim, 'trimmelt', 'var(--ok)', 48], [mean, 'átlag', 'var(--accent-2)', 74]].forEach(([m, t, c, ly]) => {
      P.el(svg, 'line', {x1: x(m), x2: x(m), y1: ly + 6, y2: y, style: `stroke:${c};stroke-width:3;stroke-dasharray:6 4`});
      P.el(svg, 'text', {class: 'label', x: x(m) + 6, y: ly, style: `fill:${c}`}, t);
    });
    d.forEach(t => P.el(svg, 'circle', {class: 'dot', cx: x(t), cy: y - 10, r: 9}));
    $('mm-v-o').value = v;
    $('mm-mean').textContent = P.fmt(mean, 1) + ' ms';
    $('mm-med').textContent = P.fmt(med, 1) + ' ms';
    $('mm-trim').textContent = P.fmt(trim, 1) + ' ms';
  }
  $('mm-v').oninput = draw;
  draw();
})();
</script>
```

::: {.notes}
Húzzuk a csúszkát 1500 ms-ig: az átlag kb. 100 ms-mal nő, a medián és a trimmelt átlag alig mozdul.
:::

# Az eloszlás alakja

## Ferdeség

- **Szimmetrikus** (egycsúcsú) eloszlásnál: átlag = medián = módusz
- **Ferde** eloszlásnál a módusz az egyik, az átlag a másik irányba húzódik; a medián általában a kettő közé esik
- **Jobbra** (pozitívan) ferde: hosszú jobb oldali „farok”, pl. reakcióidő, jövedelem; **balra** (negatívan) ferde: pl. egy könnyű teszt pontszámai
- A ferdeség mérőszáma a standardizált eltérések harmadik hatványának átlaga:

$$\gamma_1 = E\left[\left(\frac{X-\mu}{\sigma}\right)^3\right]$$

## Próbálja ki: ferdeség

:::: {.columns}
::: {.column width="62%"}
```{=html}
<div class="widget"><svg id="sk-plot" viewBox="0 0 720 380" role="img" aria-label="Ferde eloszlás módusszal, mediánnal és átlaggal"></svg></div>
```
:::

::: {.column width="38%"}
```{=html}
<div class="controls">
  <label><span>Ferdeség iránya és mértéke: <output id="sk-s-o"></output></span>
    <input id="sk-s" type="range" min="-1" max="1" step="0.05" value="0.6"></label>
</div>
<div class="stats">
  <div class="stat"><b id="sk-g"></b><small>ferdeségi együttható (γ₁)</small></div>
  <div class="stat"><b id="sk-ord" style="font-size:20px"></b><small>a három középérték sorrendje</small></div>
</div>
<script>
(() => {
  const P = window.Plot, $ = id => document.getElementById(id), svg = $('sk-plot');
  // lognormális eloszlás, standardizálva: X = (exp(σZ) − 1) / σ; σ → 0 esetén normális
  const sx = P.scale(-4, 4, 30, 700), sy = P.scale(0, 0.75, 340, 20);
  function draw() {
    const s = +$('sk-s').value, sg = Math.abs(s), sign = s < 0 ? -1 : 1;
    const f = x => {
      x *= sign;
      if (sg < 1e-6) return Math.exp(-x * x / 2) / Math.sqrt(2 * Math.PI);
      const yv = 1 + sg * x;
      return yv <= 0 ? 0 : sg * Math.exp(-(Math.log(yv) ** 2) / (2 * sg * sg)) / (yv * sg * Math.sqrt(2 * Math.PI));
    };
    const mode = sg < 1e-6 ? 0 : sign * (Math.exp(-sg * sg) - 1) / sg, mean = sg < 1e-6 ? 0 : sign * (Math.exp(sg * sg / 2) - 1) / sg;
    svg.replaceChildren();
    let d = '';
    for (let i = 0; i <= 300; i++) { const x = -4 + 8 * i / 300; d += (i ? 'L' : 'M') + sx(x).toFixed(1) + ',' + sy(f(x)).toFixed(1); }
    P.el(svg, 'path', {class: 'area', d: d + `L${sx(4)},${sy(0)}L${sx(-4)},${sy(0)}Z`});
    P.el(svg, 'path', {class: 'curve', d});
    P.el(svg, 'line', {class: 'axis', x1: 30, x2: 700, y1: sy(0), y2: sy(0)});
    [[mode, 'módusz', 'var(--ok)', 26], [0, 'medián', 'var(--accent)', 52], [mean, 'átlag', 'var(--accent-2)', 78]].forEach(([m, t, c, ly]) => {
      P.el(svg, 'line', {x1: sx(m), x2: sx(m), y1: ly + 6, y2: sy(0), style: `stroke:${c};stroke-width:3;stroke-dasharray:6 4`});
      P.el(svg, 'text', {class: 'label', x: sx(m) + 6, y: ly, style: `fill:${c}`}, t);
    });
    const g = sg < 1e-6 ? 0 : sign * (Math.exp(sg * sg) + 2) * Math.sqrt(Math.exp(sg * sg) - 1);
    $('sk-s-o').value = P.fmt(s, 2);
    $('sk-g').textContent = P.fmt(g, 2);
    $('sk-ord').textContent = sg < 1e-6 ? 'Mo = Me = átlag' : s > 0 ? 'Mo < Me < átlag' : 'átlag < Me < Mo';
  }
  $('sk-s').oninput = draw;
  draw();
})();
</script>
```

Pozitív érték: jobbra ferde; negatív: balra ferde; nulla: szimmetrikus (normális).
:::
::::

## Csúcsosság – egy tévhit korrekciója

:::: {.columns}
::: {.column width="55%"}
- A csúcsosság (kurtózis) a standardizált eltérések **negyedik** hatványának átlaga; a normális eloszlásé 3, ezért gyakran a „többletcsúcsosságot” közlik: $\gamma_2 = E\left[\left(\frac{X-\mu}{\sigma}\right)^4\right] - 3$
- **Régi értelmezés:** a csúcs „hegyességét” méri – ez **téves**
- **Mai értelmezés:** a **farkak** súlyát, a szélsőséges értékek valószínűségét méri [(DeCarlo, 1997; Westfall, 2014)]{.cite}
:::

::: {.column width="45%"}
```{=html}
<div class="widget">
  <svg id="ku-plot" viewBox="0 0 500 300" role="img" aria-label="Normális és Laplace-eloszlás azonos szórással"></svg>
  <div class="legend" style="margin-left:10px"><span><i class="dash"></i>normális (γ₂ = 0)</span><span><i></i>Laplace (γ₂ = 3)</span></div>
</div>
<script>
(() => {
  const P = window.Plot, svg = document.getElementById('ku-plot');
  const sx = P.scale(-4.5, 4.5, 15, 485), sy = P.scale(0, 0.75, 280, 15), b = 1 / Math.SQRT2;
  const path = f => Array.from({length: 301}, (_, i) => { const x = -4.5 + 9 * i / 300; return (i ? 'L' : 'M') + sx(x).toFixed(1) + ',' + sy(f(x)).toFixed(1); }).join('');
  P.el(svg, 'path', {class: 'ref', d: path(x => Math.exp(-x * x / 2) / Math.sqrt(2 * Math.PI)), style: 'opacity:1'});
  P.el(svg, 'path', {class: 'curve', d: path(x => Math.exp(-Math.abs(x) / b) / (2 * b))});
  P.el(svg, 'line', {class: 'axis', x1: 15, x2: 485, y1: sy(0), y2: sy(0)});
})();
</script>
```
:::
::::

::: {.callout-warning}
Ugyanakkora szórás mellett a nagyobb csúcsosságú eloszlás **több szélsőséges értéket** produkál – ez a kiugró értékek szempontjából fontos.
:::

## Próbálja ki: csúcsosság

:::: {.columns}
::: {.column width="62%"}
```{=html}
<div class="widget">
  <svg id="kt-plot" viewBox="0 0 720 360" role="img" aria-label="Eltérő csúcsosságú eloszlások azonos szórással"></svg>
  <div class="legend"><span><i class="dash"></i>normális (γ₂ = 0)</span><span><i></i>beállított eloszlás</span><span>satírozva: |z| &gt; 2</span></div>
</div>
```
:::

::: {.column width="38%"}
```{=html}
<div class="controls">
  <label><span>A farkak súlya: <output id="kt-t-o"></output></span>
    <input id="kt-t" type="range" min="-1" max="0.75" step="0.05" value="0.5"></label>
  <div>y-tengely:<span class="seg" id="kt-y"><button data-y="lin" class="on">lineáris</button><button data-y="log">logaritmikus</button></span></div>
</div>
<div class="stats">
  <div class="stat"><b id="kt-g"></b><small>többletcsúcsosság (γ₂)</small></div>
  <div class="stat"><b id="kt-p"></b><small>P(|z| &gt; 3); normálisnál 0,27%</small></div>
</div>
<div class="stat" style="margin-top:12px"><b id="kt-sh"></b><small>a γ₂ + 3 ennyi százaléka származik a |z| &gt; 1 tartományból</small></div>
<script>
(() => {
  const P = window.Plot, $ = id => document.getElementById(id), svg = $('kt-plot');
  // általánosított normális eloszlás egységnyi szórással: β = 2 normális, β = 1 Laplace, β → ∞ egyenletes
  const gamma = z => {  // Lanczos-közelítés
    if (z < 0.5) return Math.PI / (Math.sin(Math.PI * z) * gamma(1 - z));
    const c = [0.99999999999980993, 676.5203681218851, -1259.1392167224028, 771.32342877765313, -176.61502916214059,
      12.507343278686905, -0.13857109526572012, 9.9843695780195716e-6, 1.5056327351493116e-7];
    z -= 1;
    let x = c[0];
    for (let i = 1; i < 9; i++) x += c[i] / (z + i);
    const t = z + 7.5;
    return Math.sqrt(2 * Math.PI) * t ** (z + 0.5) * Math.exp(-t) * x;
  };
  const dens = beta => {
    const a = Math.sqrt(gamma(1 / beta) / gamma(3 / beta)), k = beta / (2 * a * gamma(1 / beta));
    return x => k * Math.exp(-((Math.abs(x) / a) ** beta));
  };
  const integ = (f, a, b, n = 2000) => {  // Simpson-szabály
    const h = (b - a) / n;
    let sum = f(a) + f(b);
    for (let i = 1; i < n; i++) sum += (i % 2 ? 4 : 2) * f(a + i * h);
    return sum * h / 3;
  };
  const norm = dens(2), sx = P.scale(-5, 5, 30, 705);
  let ylog = false;
  function draw() {
    const t = +$('kt-t').value, beta = 2 ** (1 - 2 * t), f = dens(beta);
    const g2 = gamma(5 / beta) * gamma(1 / beta) / gamma(3 / beta) ** 2 - 3;
    const ymax = Math.max(0.45, f(0) * 1.08);
    const sy = ylog ? (v => 320 - (Math.log10(Math.max(v, 1e-6)) + 6) / 6.3 * 300) : P.scale(0, ymax, 320, 20);
    const path = (g, a, b) => Array.from({length: 401}, (_, i) => {
      const x = a + (b - a) * i / 400;
      return (i ? 'L' : 'M') + sx(x).toFixed(1) + ',' + sy(g(x)).toFixed(1);
    }).join('');
    const area = (g, a, b) => path(g, a, b) + `L${sx(b)},${sy(ylog ? 1e-6 : 0)}L${sx(a)},${sy(ylog ? 1e-6 : 0)}Z`;
    svg.replaceChildren();
    const ticks = ylog ? [1e-6, 1e-4, 1e-2, 1] : [0, 0.2, 0.4, 0.6, 0.8, 1, 1.2].filter(v => v <= ymax);
    ticks.forEach(v => {
      P.el(svg, 'line', {class: 'grid', x1: 30, x2: 705, y1: sy(v), y2: sy(v)});
      P.el(svg, 'text', {class: 'tick', x: 34, y: sy(v) - 4}, ylog ? '10' + ['⁻⁶', '⁻⁴', '⁻²', '⁰'][ticks.indexOf(v)] : P.fmt(v, 1));
    });
    for (let x = -4; x <= 4; x += 2) P.el(svg, 'text', {class: 'tick', x: sx(x), y: 348, 'text-anchor': 'middle'}, P.fmt(x));
    P.el(svg, 'path', {class: 'area', d: area(f, -5, -2) + area(f, 2, 5)});
    P.el(svg, 'path', {class: 'ref', d: path(norm, -5, 5), style: 'opacity:1'});
    P.el(svg, 'path', {class: 'curve', d: path(f, -5, 5)});
    P.el(svg, 'line', {class: 'axis', x1: 30, x2: 705, y1: sy(ylog ? 1e-6 : 0), y2: sy(ylog ? 1e-6 : 0)});
    const pTail = 1 - 2 * integ(f, 0, 3), inner = 2 * integ(x => x ** 4 * f(x), 0, 1);
    $('kt-t-o').value = t < -0.05 ? 'könnyű' : t > 0.05 ? 'nehéz' : 'normális';
    $('kt-g').textContent = P.fmt(Math.abs(g2) < 0.005 ? 0 : g2, 2);
    $('kt-p').textContent = P.fmt(pTail * 100, 2) + '%';
    $('kt-sh').textContent = P.fmt((1 - inner / (g2 + 3)) * 100, 1) + '%';
  }
  $('kt-t').oninput = draw;
  $('kt-y').onclick = e => {
    const btn = e.target.closest('button');
    if (!btn) return;
    ylog = btn.dataset.y === 'log';
    for (const x of $('kt-y').children) x.classList.toggle('on', x === btn);
    draw();
  };
  draw();
})();
</script>
```
:::
::::

::: {.notes}
Logaritmikus tengelyen jól látszik: a nehéz farkú eloszlásnál a szélsőséges értékek nagyságrendekkel valószínűbbek. A γ₂ értékét szinte teljesen a ±1σ-n kívüli tartomány adja (Westfall, 2014) – ezért a farkak, nem a csúcs mutatója.
:::

# Szóródási mutatók

## Miért nem elég a középérték?

- A szóródási mutatók azt mérik, mennyire **koncentrálódnak** az értékek a középérték körül
- Két csoportnak lehet azonos a középértéke, miközben az eloszlásuk egészen más
- *Példa:* ha egy osztály matematikajegyei egyes és ötös között ingadoznak hármas átlaggal, az nem ugyanaz, mintha mindenki hármast kapott volna

```{=html}
<div class="grid" style="--cols:5;margin-top:10px">
  <div class="stat"><b>R</b><small>terjedelem</small></div>
  <div class="stat"><b>IQR</b><small>interkvartilis terjedelem</small></div>
  <div class="stat"><b>AE</b><small>átlagos abszolút eltérés</small></div>
  <div class="stat"><b>s</b><small>szórás (s² variancia)</small></div>
  <div class="stat"><b>V</b><small>relatív szórás</small></div>
</div>
```

## Terjedelem

A legnagyobb és a legkisebb érték különbsége:

$$R = x_{\max} - x_{\min}$$

*Példa:* 3, 8, 6, 14, 0, −4, 0, 12, −7, 0, −10 → $R = 14 - (-10) = 24$

::: {.callout-warning}
A terjedelem csak a **két legszélső** értéken múlik, ezért egyetlen kiugró érték is erősen megnöveli, és a mintanagysággal is nő. Tájékoztató jellegű mutató.
:::

## Kvartilisek és interkvartilis terjedelem

- A **kvartilisek** ($Q_1, Q_2, Q_3$) a rendezett mintát négy egyenlő részre osztják; $Q_2$ a medián
- $Q_1$ alatt az adatok negyede, $Q_3$ alatt háromnegyede található
- **Interkvartilis terjedelem:** $\mathrm{IQR} = Q_3 - Q_1$ – az adatok **középső 50%-ának** szélessége; **interkvartilis félterjedelem:** $(Q_3 - Q_1)/2$

::: {.callout-tip}
## Egy egyszerű eljárás
1. Rendezzük a mintát növekvő sorrendbe, és keressük meg a mediánt ($Q_2$)
2. $Q_1$ az alsó, $Q_3$ a felső fél mediánja
:::

## IQR: példa és egy fontos megjegyzés {.smaller}

Egy 10 pontos statisztikateszt eredményei ($n = 19$), rendezve:

0, 0, 0, 4, **5**, 6, 7, 7, 7, **8**, 8, 8, 9, 9, **9**, 9, 9, 9, 10

$Q_1 = 5$ (az alsó 9 adat mediánja), medián = 8, $Q_3 = 9$ (a felső 9 adat mediánja) → $\mathrm{IQR} = 9 - 5 = 4$

::: {.callout-important}
## A kvartilisnek nincs egyetlen „helyes” definíciója
A statisztikai programok **különböző módszerekkel** számolnak kvantilist: Hyndman és Fan (1996) kilenc elterjedt definíciót hasonlított össze. Ugyanerre a mintára egy másik, gyakori módszer $Q_1 = 5{,}5$ és $\mathrm{IQR} = 3{,}5$ értéket ad. Kis mintánál ez érezhető különbség – közléskor érdemes megadni a használt programot.
:::

## Kvantilisek, decilisek, percentilisek {.smaller}

- **$q$-adrendű kvantilis:** az az érték, amely a rendezett mintát $q : (1-q)$ arányban osztja ketté
- **Kvartilisek:** negyedelnek ($Q_1, Q_2, Q_3$); **decilisek:** tizedelnek ($D_1, \ldots, D_9$); **percentilisek:** századolnak ($P_1, \ldots, P_{99}$)

*Példa* (rendezve): 6, 7, 15, 36, 39, 40, 41, 42, 43, 47, 49

| | $Q_1$ | medián | $Q_3$ | $D_1$ | $D_9$ |
|:--|--:|--:|--:|--:|--:|
| Érték (lineáris interpolációval) | 25,5 | 40 | 42,5 | 7 | 47 |

A tesztnormák gyakran **percentilisrangot** adnak meg: a 84. percentilis azt jelenti, hogy a normaminta 84%-a ennél alacsonyabb pontszámot ért el.

## Dobozdiagram (boxplot)

```{=html}
<div class="widget"><svg id="bx-plot" viewBox="0 0 1000 200" role="img" aria-label="Dobozdiagram részei"></svg></div>
<script>
(() => {
  const P = window.Plot, svg = document.getElementById('bx-plot');
  const d = [6, 7, 15, 36, 39, 40, 41, 42, 43, 47, 49], q1 = 25.5, me = 40, q3 = 42.5;
  const x = P.scale(0, 55, 40, 960), y = 95;
  P.el(svg, 'line', {class: 'axis', x1: x(6), x2: x(q1), y1: y, y2: y});
  P.el(svg, 'line', {class: 'axis', x1: x(q3), x2: x(49), y1: y, y2: y});
  [6, 49].forEach(v => P.el(svg, 'line', {class: 'axis', x1: x(v), x2: x(v), y1: y - 18, y2: y + 18}));
  P.el(svg, 'rect', {class: 'bar', x: x(q1), y: y - 35, width: x(q3) - x(q1), height: 70, rx: 6});
  P.el(svg, 'line', {x1: x(me), x2: x(me), y1: y - 35, y2: y + 35, style: 'stroke:var(--accent-2);stroke-width:4'});
  d.forEach((v, i) => P.el(svg, 'circle', {class: 'dot', cx: x(v), cy: y + 62 + (i % 2) * 12, r: 6}));
  [[6, 'min'], [q1, 'Q₁'], [me, 'medián'], [q3, 'Q₃'], [49, 'max']].forEach(([v, t], i) =>
    P.el(svg, 'text', {class: 'label', x: x(v), y: i % 2 ? 22 : 45, 'text-anchor': 'middle'}, t));
  for (let t = 0; t <= 55; t += 5) P.el(svg, 'text', {class: 'tick', x: x(t), y: 196, 'text-anchor': 'middle'}, t);
})();
</script>
```

- **Doboz:** a középső 50% ($Q_1$ – $Q_3$), benne a **medián** [(Tukey, 1977)]{.cite}
- **Bajuszok:** a legszélső érték a $Q_1 - 1{,}5\,\mathrm{IQR}$ és $Q_3 + 1{,}5\,\mathrm{IQR}$ határon belül; ezen kívül: **kiugró** érték
- Látszik a helyzet, a szóródás és a ferdeség – itt: **balra ferde** eloszlás

## Próbálja ki: doboz, hegedű, pontok

:::: {.columns}
::: {.column width="62%"}
```{=html}
<div class="widget"><svg id="vi-plot" viewBox="0 0 720 400" role="img" aria-label="Két csoport dobozdiagramja, hegedűábrája és pontjai"></svg></div>
```
:::

::: {.column width="38%"}
Két csoport, $n = 60$ fő csoportonként.

```{=html}
<div class="controls">
  <div>Ábra:<span class="seg" id="vi-mode"><button data-m="box" class="on">doboz</button><button data-m="violin">hegedű</button><button data-m="dots">pontok</button><button data-m="all">mind</button></span></div>
</div>
<script>
(() => {
  const P = window.Plot, $ = id => document.getElementById(id), svg = $('vi-plot'), rnd = P.rng(1);
  const A = Array.from({length: 60}, () => 50 + 12 * P.normal(rnd));
  const B = Array.from({length: 60}, (_, i) => (i % 2 ? 33 : 67) + 5 * P.normal(rnd));
  const y = P.scale(0, 100, 370, 20);
  const q = (s, p) => { const i = (s.length - 1) * p, lo = Math.floor(i); return s[lo] + (s[Math.ceil(i)] - s[lo]) * (i - lo); };
  const kde = xs => {  // Gauss-magfüggvényes sűrűségbecslés, Silverman-féle sávszélességgel
    const n = xs.length, m = xs.reduce((a, b) => a + b) / n, sd = Math.sqrt(xs.reduce((a, b) => a + (b - m) ** 2, 0) / (n - 1));
    const s = [...xs].sort((a, b) => a - b), h = 0.9 * Math.min(sd, (q(s, 0.75) - q(s, 0.25)) / 1.34) * n ** -0.2;
    return t => xs.reduce((a, v) => a + Math.exp(-(((t - v) / h) ** 2) / 2), 0) / (n * h * Math.sqrt(2 * Math.PI));
  };
  let mode = 'box';
  function draw() {
    svg.replaceChildren();
    for (let v = 0; v <= 100; v += 20) {
      P.el(svg, 'line', {class: 'grid', x1: 50, x2: 710, y1: y(v), y2: y(v)});
      P.el(svg, 'text', {class: 'tick', x: 42, y: y(v) + 5, 'text-anchor': 'end'}, v);
    }
    [['A csoport', A, 230], ['B csoport', B, 530]].forEach(([name, xs, cx]) => {
      const s = [...xs].sort((a, b) => a - b), q1 = q(s, 0.25), me = q(s, 0.5), q3 = q(s, 0.75), iqr = q3 - q1;
      if (mode === 'violin' || mode === 'all') {
        const f = kde(xs), ts = Array.from({length: 121}, (_, i) => i * 100 / 120), w = t => f(t) * 2600;
        const d = ts.map((t, i) => (i ? 'L' : 'M') + (cx + w(t)).toFixed(1) + ',' + y(t).toFixed(1)).join('') +
          ts.slice().reverse().map(t => 'L' + (cx - w(t)).toFixed(1) + ',' + y(t).toFixed(1)).join('') + 'Z';
        P.el(svg, 'path', {class: 'area', d, style: 'stroke:var(--accent);stroke-width:2'});
      }
      if (mode === 'dots' || mode === 'all') {
        s.forEach((v, i) => P.el(svg, 'circle', {class: 'dot', cx: cx + ((i * 37) % 13 - 6) * 7, cy: y(v), r: 5}));
      }
      if (mode === 'box' || mode === 'all') {
        const lo = s.find(v => v >= q1 - 1.5 * iqr), hi = [...s].reverse().find(v => v <= q3 + 1.5 * iqr), bw = mode === 'all' ? 24 : 60;
        P.el(svg, 'line', {class: 'axis', x1: cx, x2: cx, y1: y(lo), y2: y(q1)});
        P.el(svg, 'line', {class: 'axis', x1: cx, x2: cx, y1: y(q3), y2: y(hi)});
        P.el(svg, 'rect', {class: 'bar', x: cx - bw, y: y(q3), width: 2 * bw, height: y(q1) - y(q3), style: 'stroke:var(--fg);stroke-width:1.5'});
        P.el(svg, 'line', {x1: cx - bw, x2: cx + bw, y1: y(me), y2: y(me), style: 'stroke:var(--accent-2);stroke-width:4'});
        s.filter(v => v < lo || v > hi).forEach(v => P.el(svg, 'circle', {cx, cy: y(v), r: 5, style: 'fill:none;stroke:var(--accent-2);stroke-width:2'}));
      }
      P.el(svg, 'text', {class: 'tick', x: cx, y: 395, 'text-anchor': 'middle'}, name);
    });
  }
  $('vi-mode').onclick = e => {
    const btn = e.target.closest('button');
    if (!btn) return;
    mode = btn.dataset.m;
    for (const x of $('vi-mode').children) x.classList.toggle('on', x === btn);
    draw();
  };
  draw();
})();
</script>
```

::: {.callout-warning}
A dobozdiagram elrejti, hogy a B csoport **kétcsúcsú**. A hegedűábra a dobozt egy simított sűrűségbecsléssel egészíti ki [(Hintze & Nelson, 1998)]{.cite}.
:::
:::
::::

## Átlagos abszolút eltérés {.smaller}

Az átlagtól mért eltérések **abszolút értékeinek** átlaga (középeltérés): $\mathrm{AE} = \frac{1}{n}\sum_{i=1}^{n} \left| x_i - \bar{x} \right|$

| $x_i$ | 3 | 8 | 6 | 12 | 0 | −4 | 10 | **Összesen** |
|:--|--:|--:|--:|--:|--:|--:|--:|--:|
| $x_i - \bar{x}$ | −2 | 3 | 1 | 7 | −5 | −9 | 5 | **0** |
| $\left\lvert x_i - \bar{x} \right\rvert$ | 2 | 3 | 1 | 7 | 5 | 9 | 5 | **32** |

Az átlag 5, így $\mathrm{AE} = 32 / 7 \approx 4{,}57$

::: {.callout-tip}
## Robusztus változat: medián abszolút eltérés (MAD)
$\mathrm{MAD} = 1{,}4826 \cdot \mathrm{med}\left| x_i - \mathrm{med}(x) \right|$. Kiugró értékek szűrésére az „átlag $\pm\ 3s$” helyett a „medián $\pm\ 2{,}5 \cdot \mathrm{MAD}$” ajánlott [(Leys és mtsai, 2013)]{.cite}.
:::

## Variancia és szórás – populáció

Az átlagos abszolút eltérésnél elterjedtebb az átlagos **négyzetes** eltérés, a **variancia**:

$$\sigma^2 = V(X) = E\left[(X - \mu)^2\right]$$

A **szórás** a variancia négyzetgyöke:

$$\sigma = \sqrt{V(X)}$$

- A négyzetre emelés miatt a nagy eltérések **nagyobb súlyt** kapnak
- A szórás mértékegysége megegyezik az adatokéval, a varianciáé annak négyzete

## Tapasztalati variancia és szórás {.smaller}

$$s^2 = \frac{Q}{n-1} = \frac{\sum_{i=1}^{n}(x_i - \bar{x})^2}{n-1}, \qquad s = \sqrt{s^2}$$

$Q$: eltérés-négyzetösszeg, $n - 1$: **szabadságfok**. *Példa* (átlag: 7):

| $x_i$ | 3 | 8 | 6 | 14 | 0 | 11 | **Összesen** |
|:--|--:|--:|--:|--:|--:|--:|--:|
| $x_i - \bar{x}$ | −4 | 1 | −1 | 7 | −7 | 4 | **0** |
| $(x_i - \bar{x})^2$ | 16 | 1 | 1 | 49 | 49 | 16 | **132** |

$s^2 = 132 / 5 = 26{,}4$, $\quad s = \sqrt{26{,}4} \approx 5{,}14$

::: {.notes}
Miért n − 1? A mintaátlag „közelebb van” a minta elemeihez, mint a valódi μ, ezért n-nel osztva alábecsülnénk a varianciát – a következő dia ezt szimulációval mutatja meg.
:::

## Próbálja ki: miért n − 1?

:::: {.columns}
::: {.column width="62%"}
```{=html}
<div class="widget">
  <svg id="nm-plot" viewBox="0 0 720 380" role="img" aria-label="A variancia becslése n-nel és n−1-gyel osztva"></svg>
  <div class="legend"><span><i class="dash"></i>valódi σ² = 225</span><span><i style="border-top-color:var(--accent-2)"></i>n-nel osztva (elmélet)</span><span><i></i>n − 1-gyel osztva</span></div>
</div>
```
:::

::: {.column width="38%"}
4000 véletlen minta egy $\sigma = 15$ szórású sokaságból (pl. IQ); minden mintából kétféleképpen becsüljük a varianciát, majd átlagoljuk a becsléseket.

```{=html}
<div class="controls">
  <label><span>Mintanagyság: n = <output id="nm-n-o"></output></span>
    <input id="nm-n" type="range" min="2" max="30" step="1" value="4"></label>
</div>
<div class="stats">
  <div class="stat"><b id="nm-a"></b><small>becslések átlaga, n − 1-gyel osztva</small></div>
  <div class="stat"><b id="nm-b"></b><small>becslések átlaga, n-nel osztva</small></div>
</div>
<script>
(() => {
  const P = window.Plot, $ = id => document.getElementById(id), svg = $('nm-plot'), rnd = P.rng(5);
  const x = P.scale(1, 31, 60, 705), y = P.scale(0, 260, 340, 20), V = 225;
  function draw() {
    const n = +$('nm-n').value;
    let sa = 0, sb = 0;
    for (let r = 0; r < 4000; r++) {
      const xs = Array.from({length: n}, () => 100 + 15 * P.normal(rnd)), m = xs.reduce((a, b) => a + b) / n;
      const qq = xs.reduce((a, b) => a + (b - m) ** 2, 0);
      sa += qq / (n - 1); sb += qq / n;
    }
    sa /= 4000; sb /= 4000;
    svg.replaceChildren();
    for (let v = 0; v <= 250; v += 50) {
      P.el(svg, 'line', {class: 'grid', x1: 60, x2: 705, y1: y(v), y2: y(v)});
      P.el(svg, 'text', {class: 'tick', x: 52, y: y(v) + 5, 'text-anchor': 'end'}, v);
    }
    for (let t = 2; t <= 30; t += 4) P.el(svg, 'text', {class: 'tick', x: x(t), y: 366, 'text-anchor': 'middle'}, t);
    P.el(svg, 'line', {class: 'ref', x1: 60, x2: 705, y1: y(V), y2: y(V), style: 'opacity:1'});
    let d = '';
    for (let t = 2; t <= 30; t++) d += (t > 2 ? 'L' : 'M') + x(t).toFixed(1) + ',' + y(V * (t - 1) / t).toFixed(1);
    P.el(svg, 'path', {d, style: 'fill:none;stroke:var(--accent-2);stroke-width:3'});
    P.el(svg, 'line', {class: 'mean', x1: x(n), x2: x(n), y1: y(0), y2: y(250)});
    P.el(svg, 'circle', {cx: x(n), cy: y(sb), r: 9, style: 'fill:var(--accent-2);stroke:var(--paper);stroke-width:2'});
    P.el(svg, 'circle', {class: 'dot', cx: x(n), cy: y(sa), r: 9});
    P.el(svg, 'line', {class: 'axis', x1: 60, x2: 705, y1: y(0), y2: y(0)});
    $('nm-n-o').value = n;
    $('nm-a').textContent = P.fmt(sa, 1);
    $('nm-b').textContent = P.fmt(sb, 1);
  }
  $('nm-n').oninput = draw;
  draw();
})();
</script>
```
:::
::::

::: {.notes}
n = 2-nél az n-nel osztott becslés átlagosan csak a valódi variancia fele; n − 1-gyel osztva a becslés átlagosan pontos (torzítatlan). Nagy mintánál a különbség elhanyagolható.
:::

## Relatív szórás (variációs együttható) {.smaller}

Különböző mértékegységű vagy eltérő átlagú változók szóródásának összehasonlítására: $V = s / \bar{x}$, gyakran százalékban.

:::: {.columns}
::: {.column}
*Példa: újszülöttek*

| | Átlag | Szórás | $V$ |
|:--|--:|--:|--:|
| Testhossz | 50,20 cm | 2,51 cm | 5,0% |
| Testsúly | 3226 g | 494 g | 15,3% |

A testsúly relatíve jóval változékonyabb.
:::

::: {.column}
*Azonos szórás, eltérő relatív szórás*

| Minta | $s$ | $V$ |
|:--|--:|--:|
| 1, 2, 3, 4 | 1,29 | 51,6% |
| 1001, 1002, 1003, 1004 | 1,29 | 0,13% |

:::
::::

::: {.callout-warning}
Csak **arányskálán**, pozitív értékekre értelmes: intervallumskálán (pl. °C) a nullpont önkényes.
:::

## Melyik mutatót mikor? {.smaller}

| Mutató | Legalább ilyen skála | Kiugró értékekre | Megjegyzés |
|:--|:--|:--|:--|
| Módusz | nominális | robusztus | több is lehet |
| Medián, kvartilisek, IQR | ordinális | **robusztus** | ferde eloszlásnál |
| Trimmelt átlag, MAD | intervallum | **robusztus** | modern alternatíva |
| Átlag, szórás, variancia | intervallum | érzékeny | szimmetrikus eloszlásnál |
| Terjedelem | ordinális | nagyon érzékeny | csak tájékoztató |
| Relatív szórás | arány | érzékeny | csak pozitív értékekre |

: Közléskor: átlag és szórás (vagy medián és IQR), valamint $n$ [(APA, 2020)]{.cite}.

## Összefoglalás {.inverse .center}

- **Középértékek:** átlag, medián, módusz – a mérési szint és az eloszlás alakja dönt
- **Alak:** a ferdeség az aszimmetriát, a csúcsosság a **farkak** súlyát méri
- **Szóródás:** terjedelem, IQR, átlagos eltérés, szórás, relatív szórás
- A medián, az IQR és a trimmelt átlag **robusztus**, az átlag és a szórás érzékeny a kiugró értékekre
- A mintavarianciában **$n - 1$**-gyel osztunk

## Irodalom {.smaller}

::: {.refs}
American Psychological Association. (2020). *Publication manual of the American Psychological Association* (7th ed.).

DeCarlo, L. T. (1997). On the meaning and use of kurtosis. *Psychological Methods, 2*(3), 292–307.

Hintze, J. L., & Nelson, R. D. (1998). Violin plots: A box plot–density trace synergism. *The American Statistician, 52*(2), 181–184.

Hyndman, R. J., & Fan, Y. (1996). Sample quantiles in statistical packages. *The American Statistician, 50*(4), 361–365.

Leys, C., Ley, C., Klein, O., Bernard, P., & Licata, L. (2013). Detecting outliers: Do not use standard deviation around the mean, use absolute deviation around the median. *Journal of Experimental Social Psychology, 49*(4), 764–766. https://doi.org/10.1016/j.jesp.2013.03.013

Ratcliff, R. (1993). Methods for dealing with reaction time outliers. *Psychological Bulletin, 114*(3), 510–532.

Tukey, J. W. (1977). *Exploratory data analysis.* Addison-Wesley.

Westfall, P. H. (2014). Kurtosis as peakedness, 1905–2014. R.I.P. *The American Statistician, 68*(3), 191–195. https://doi.org/10.1080/00031305.2014.917055

Wilcox, R. R. (2017). *Introduction to robust estimation and hypothesis testing* (4th ed.). Academic Press.

**Magyar nyelvű tankönyv:** Vargha A. (2000). *Matematikai statisztika pszichológiai, nyelvészeti és biológiai alkalmazásokkal.* Pólya Kiadó.
:::

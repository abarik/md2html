---
title: "Statisztikai alapfogalmak"
subtitle: "Leíró statisztika és a normális eloszlás"
author: "Abari Kálmán"
date: "2026. október 12."
lang: hu
footer: "Statisztikai alapfogalmak · MD2HTML példa"
format:
  revealjs:
    incremental: false
---

# Alapfogalmak

## Sokaság és minta

:::: {.columns}
::: {.column width="56%"}
- **Sokaság** (populáció): a vizsgálat összes lehetséges egysége
- **Minta**: a sokaság ténylegesen megfigyelt része, elemszáma $n$
- **Paraméter** ($\mu$, $\sigma$) a sokaságot, **statisztika** ($\bar{x}$, $s$) a mintát jellemzi
:::

::: {.column width="44%"}
::: {.callout-tip}
## Miért mintavétel?
A teljes sokaság megfigyelése többnyire drága vagy lehetetlen -- a mintából *következtetünk* a sokaságra.
:::

::: {.callout-warning}
A következtetés csak **reprezentatív** mintából megbízható.
:::
:::
::::

::: {.notes}
Példa: egy választás előtti közvélemény-kutatás ~1000 fős mintából becsül a teljes választói sokaságra.
:::

## A változók mérési szintje {.smaller}

| Mérési szint | Példa | Értelmezhető művelet | Jellemző mutató |
|:--|:--|:--|:--|
| Nominális | nem, vércsoport, lakóhely | $=,\ \neq$ | módusz |
| Ordinális | iskolai végzettség, helyezés | $+\ <,\ >$ | medián, kvartilisek |
| Intervallum | hőmérséklet (°C), IQ | $+\ -$ | átlag, szórás |
| Arány | testmagasság, jövedelem | $+\ \div$ | mértani átlag, relatív szórás |

: Minden szint örökli az alatta lévők műveleteit és mutatóit.

## Középértékek

::: {.incremental}
- **Számtani átlag:** $\bar{x} = \frac{1}{n}\sum_{i=1}^{n} x_i$
- **Medián:** a nagyság szerint rendezett adatsor középső eleme
- **Módusz:** a leggyakrabban előforduló érték
:::

. . .

::: {.callout-note}
Az átlag érzékeny a kiugró értékekre, a medián [robusztus]{.fragment}.
:::

::: {.notes}
Jövedelmeknél ezért gyakran a mediánt közlik: néhány nagyon magas jövedelem felfelé húzza az átlagot.
:::

## Szóródási mutatók

- **Terjedelem:** $R = x_{\max} - x_{\min}$
- **Korrigált tapasztalati szórás:**

$$s = \sqrt{\frac{1}{n-1}\sum_{i=1}^{n}\left(x_i-\bar{x}\right)^2}$$

. . .

- **Interkvartilis terjedelem:** $\mathrm{IQR} = Q_3 - Q_1$
- **Relatív szórás:** $V = s / \bar{x}$

## Egy kis számpélda

:::: {.columns}
::: {.column width="50%"}
Adatok: 4, 8, 6, 5, 3, 7

- $n = 6$, $\sum x_i = 33$
- $\bar{x} = 33/6 = 5{,}5$
- medián $= (5+6)/2 = 5{,}5$
- $s^2 = 17{,}5/5 = 3{,}5$, $s \approx 1{,}87$
:::

::: {.column width="50%"}
```python
import statistics as st

x = [4, 8, 6, 5, 3, 7]
print(st.mean(x))    # 5.5
print(st.median(x))  # 5.5
print(st.stdev(x))   # 1.8708...
```
:::
::::

# A normális eloszlás

## Sűrűségfüggvény -- próbálja ki!

:::: {.columns}
::: {.column width="62%"}
```{=html}
<div class="widget">
  <svg id="nd-plot" viewBox="0 0 720 400" role="img" aria-label="A normális eloszlás sűrűségfüggvénye"></svg>
  <div class="legend"><span><i></i>N(μ, σ²)</span><span><i class="dash"></i>standard normális N(0, 1)</span></div>
</div>
```
:::

::: {.column width="38%"}
$$f(x)=\frac{1}{\sigma\sqrt{2\pi}}\,e^{-\frac{(x-\mu)^2}{2\sigma^2}}$$

```{=html}
<div class="controls">
  <label><span>Várható érték: μ = <output id="nd-mu-o"></output></span>
    <input id="nd-mu" type="range" min="-3" max="3" step="0.1" value="0"></label>
  <label><span>Szórás: σ = <output id="nd-sd-o"></output></span>
    <input id="nd-sd" type="range" min="0.5" max="3" step="0.1" value="1"></label>
  <div>Sáv:<span class="seg" id="nd-k"><button data-k="1" class="on">±1σ</button><button data-k="2">±2σ</button><button data-k="3">±3σ</button></span></div>
</div>
<div class="stats">
  <div class="stat"><b id="nd-p"></b><small id="nd-int"></small></div>
  <div class="stat"><b id="nd-f"></b><small>csúcsmagasság f(μ)</small></div>
</div>
<script>
(() => {
  const $ = id => document.getElementById(id), svg = $('nd-plot'), NS = 'http://www.w3.org/2000/svg';
  const W = 720, H = 400, L = 46, R = 12, T = 14, B = 40, X0 = -8, X1 = 8, YM = 0.85;
  const sx = x => L + (x - X0) / (X1 - X0) * (W - L - R);
  const sy = y => H - B - y / YM * (H - T - B);
  const pdf = (x, m, s) => Math.exp(-((x - m) ** 2) / (2 * s * s)) / (s * Math.sqrt(2 * Math.PI));
  const fmt = (v, d) => v.toLocaleString('hu-HU', {minimumFractionDigits: d, maximumFractionDigits: d});
  const el = (tag, a, text) => {
    const e = document.createElementNS(NS, tag);
    for (const k in a) e.setAttribute(k, a[k]);
    if (text != null) e.textContent = text;
    return svg.appendChild(e);
  };
  for (let x = X0; x <= X1; x += 2) {
    el('line', {class: 'grid', x1: sx(x), x2: sx(x), y1: T, y2: sy(0)});
    el('text', {class: 'tick', x: sx(x), y: sy(0) + 26, 'text-anchor': 'middle'}, fmt(x, 0));
  }
  for (let i = 0; i <= 4; i++) {
    el('line', {class: 'grid', x1: L, x2: W - R, y1: sy(i * 0.2), y2: sy(i * 0.2)});
    el('text', {class: 'tick', x: L - 8, y: sy(i * 0.2) + 5, 'text-anchor': 'end'}, fmt(i * 0.2, 1));
  }
  el('line', {class: 'axis', x1: L, x2: W - R, y1: sy(0), y2: sy(0)});
  const area = el('path', {class: 'area'}), ref = el('path', {class: 'ref'}), curve = el('path', {class: 'curve'});
  const mean = el('line', {class: 'mean'}), lab = el('text', {class: 'label', 'text-anchor': 'middle'}, 'μ');
  const path = (m, s, a, b) => {
    let d = '';
    for (let i = 0; i <= 240; i++) {
      const x = a + (b - a) * i / 240;
      d += (i ? 'L' : 'M') + sx(x).toFixed(1) + ',' + sy(pdf(x, m, s)).toFixed(1);
    }
    return d;
  };
  const P = {1: 68.27, 2: 95.45, 3: 99.73};
  let k = 1;
  ref.setAttribute('d', path(0, 1, X0, X1));

  function draw() {
    const m = +$('nd-mu').value, s = +$('nd-sd').value;
    const a = Math.max(X0, m - k * s), b = Math.min(X1, m + k * s), top = sy(pdf(m, m, s));
    curve.setAttribute('d', path(m, s, X0, X1));
    area.setAttribute('d', path(m, s, a, b) + `L${sx(b).toFixed(1)},${sy(0)}L${sx(a).toFixed(1)},${sy(0)}Z`);
    for (const [k2, v] of Object.entries({x1: sx(m), x2: sx(m), y1: sy(0), y2: top})) mean.setAttribute(k2, v);
    lab.setAttribute('x', sx(m)); lab.setAttribute('y', top - 10);
    $('nd-mu-o').value = fmt(m, 1);
    $('nd-sd-o').value = fmt(s, 1);
    $('nd-p').textContent = fmt(P[k], 2) + ' %';
    $('nd-int').textContent = `P(${fmt(m - k * s, 1)} < X < ${fmt(m + k * s, 1)})`;
    $('nd-f').textContent = fmt(pdf(m, m, s), 3);
  }
  $('nd-mu').oninput = $('nd-sd').oninput = draw;
  $('nd-k').onclick = e => {
    const btn = e.target.closest('button');
    if (!btn) return;
    k = +btn.dataset.k;
    for (const x of $('nd-k').children) x.classList.toggle('on', x === btn);
    draw();
  };
  draw();
})();
</script>
```
:::
::::

::: {.notes}
Mozgassuk a csúszkákat: μ eltolja a görbét, σ szélesíti és lapítja -- a görbe alatti terület mindig 1.
:::

## A 68–95–99,7 szabály

Ha $X \sim N(\mu, \sigma^2)$, akkor

::: {.incremental}
- $P(\mu - \sigma < X < \mu + \sigma) \approx 68{,}3\%$
- $P(\mu - 2\sigma < X < \mu + 2\sigma) \approx 95{,}4\%$
- $P(\mu - 3\sigma < X < \mu + 3\sigma) \approx 99{,}7\%$
:::

. . .

::: {.callout-important}
## Ökölszabály
A $\mu \pm 3\sigma$ sávon kívül eső megfigyelés ritka -- érdemes **kiugró értékként** megvizsgálni.
:::

## Standardizálás

Bármely normális eloszlású változó átváltható standard normálissá:

$$z = \frac{x-\mu}{\sigma}, \qquad Z \sim N(0,1)$$

. . .

> **Példa.** Az IQ-pontszám eloszlása közelítőleg $N(100,\ 15^2)$.
> A 130 pont $z = (130-100)/15 = 2$ szórásnyira van az átlag felett,
> így a népességnek csak kb. 2,3%-a ér el ennél magasabb értéket.

## Összefoglalás {.inverse .center}

- A **minta** statisztikái a **sokaság** paramétereit becsülik
- A mérési szint határozza meg, mely mutatók értelmesek
- Középérték **és** szóródás együtt írja le az eloszlást
- A normális eloszlást két paraméter, $\mu$ és $\sigma$ határozza meg

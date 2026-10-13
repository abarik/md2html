---
title: "Valószínűségi változók és nevezetes eloszlások"
subtitle: "Várható érték és szórás, binomiális, Poisson- és normális eloszlás, centrális határeloszlás-tétel"
author: "Abari Kálmán"
date: "2026. ősz"
lang: hu
footer: "Matematikai alapok · 6. Valószínűségi változók és eloszlások"
---

## Miről lesz szó?

```{=html}
<div class="grid" style="--cols:4">
  <div class="stat"><b>X</b><small style="font-size:19px"><strong>Valószínűségi változó:</strong> a véletlen kimenetelhez számot rendel</small></div>
  <div class="stat"><b>μ, σ</b><small style="font-size:19px"><strong>Várható érték és szórás:</strong> az eloszlás közepe és szóródása</small></div>
  <div class="stat"><b>B, Po, N</b><small style="font-size:19px"><strong>Nevezetes eloszlások:</strong> binomiális, Poisson, normális</small></div>
  <div class="stat"><b>CHT</b><small style="font-size:19px"><strong>Centrális határeloszlás-tétel:</strong> miért normális a mintaátlag?</small></div>
</div>
<script>
// közös segédfüggvények a diasor ábráihoz és számításaihoz
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
  seg(id, fn) {
    const box = document.getElementById(id);
    box.onclick = e => {
      const b = e.target.closest('button');
      if (!b) return;
      for (const x of box.children) x.classList.toggle('on', x === b);
      fn(b.dataset);
    };
  },
  path(f, a, b, sx, sy, n = 300) {
    let d = '';
    for (let i = 0; i <= n; i++) { const x = a + (b - a) * i / n; d += (i ? 'L' : 'M') + sx(x).toFixed(1) + ',' + sy(f(x)).toFixed(1); }
    return d;
  },
  phi: x => Math.exp(-x * x / 2) / Math.sqrt(2 * Math.PI),
  Phi(x) {  // standard normális eloszlásfüggvény (Abramowitz–Stegun 7.1.26)
    const t = 1 / (1 + 0.3275911 * Math.abs(x) / Math.SQRT2);
    const e = 1 - ((((1.061405429 * t - 1.453152027) * t + 1.421413741) * t - 0.284496736) * t + 0.254829592) * t * Math.exp(-x * x / 2);
    return x >= 0 ? (1 + e) / 2 : (1 - e) / 2;
  },
  invPhi(p) { let lo = -9, hi = 9; for (let i = 0; i < 80; i++) { const m = (lo + hi) / 2; this.Phi(m) < p ? lo = m : hi = m; } return (lo + hi) / 2; },
  C(n, k) { if (k < 0 || k > n) return 0; let r = 1; for (let i = 1; i <= k; i++) r = r * (n - k + i) / i; return r; },
  binom(n, k, p) { return this.C(n, k) * p ** k * (1 - p) ** (n - k); },
  pois(l, k) { let r = Math.exp(-l); for (let i = 1; i <= k; i++) r *= l / i; return r; },
  grid(svg, sy, x0, x1, ticks, d = 2) {
    ticks.forEach(v => {
      this.el(svg, 'line', {class: 'grid', x1: x0, x2: x1, y1: sy(v), y2: sy(v)});
      this.el(svg, 'text', {class: 'tick', x: x0 - 8, y: sy(v) + 5, 'text-anchor': 'end'}, this.fmt(v, d));
    });
  }
};
</script>
```

A pszichológiában mért mennyiségek – helyes válaszok száma, reakcióidő, tesztpontszám – **valószínűségi változók**; viselkedésüket eloszlásuk írja le.

# Valószínűségi változók

## Valószínűségi változó

Az eseménytéren értelmezett valós függvény: $X: \Omega \to \mathbb{R}$ – minden kimenetelhez egy **számot** rendel.

:::: {.columns}
::: {.column width="45%"}
*Példa:* egy érmét háromszor feldobunk, $X$ a **fejek száma**.

0 fej: 1, 1 fej: 3, 2 fej: 3, 3 fej: 1 kimenetel.

$X$ értéke a kísérlet kimenetelétől függ, ezért valószínűségi változó.
:::

::: {.column width="55%"}
```{=html}
<div class="widget"><svg id="rv-plot" viewBox="0 0 560 360" role="img" aria-label="A kimenetelek leképezése a fejek számára"></svg></div>
<script>
(() => {
  const P = window.Plot, svg = document.getElementById('rv-plot');
  const om = ['iii', 'fii', 'ifi', 'iif', 'ffi', 'fif', 'iff', 'fff'], val = s => [...s].filter(c => c === 'f').length;
  const yv = v => 60 + v * 85;
  P.el(svg, 'text', {class: 'title', x: 70, y: 22, 'text-anchor': 'middle'}, 'Ω');
  P.el(svg, 'text', {class: 'title', x: 470, y: 22, 'text-anchor': 'middle'}, 'X értéke');
  om.forEach((s, i) => {
    const y = 48 + i * 40;
    P.el(svg, 'line', {x1: 108, x2: 448, y1: y, y2: yv(val(s)), style: 'stroke:var(--accent);stroke-opacity:.45;stroke-width:2'});
    P.el(svg, 'rect', {x: 30, y: y - 15, width: 78, height: 30, rx: 8, style: 'fill:var(--paper);stroke:var(--line)'});
    P.el(svg, 'text', {class: 'tick', x: 69, y: y + 5, 'text-anchor': 'middle', style: 'font-family:var(--mono)'}, s);
  });
  [0, 1, 2, 3].forEach(v => {
    P.el(svg, 'circle', {cx: 470, cy: yv(v), r: 22, style: 'fill:var(--accent)'});
    P.el(svg, 'text', {class: 'title', x: 470, y: yv(v) + 6, 'text-anchor': 'middle', style: 'fill:var(--on-accent)'}, v);
  });
})();
</script>
```
:::
::::

## Az eloszlás

A valószínűségi változó **eloszlása** a lehetséges értékek és a hozzájuk tartozó valószínűségek összessége: $p_k = P(X = x_k)$.

:::: {.columns}
::: {.column width="40%"}
| Fejek száma ($x_k$) | 0 | 1 | 2 | 3 |
|:--|:-:|:-:|:-:|:-:|
| $p_k$ | 1/8 | 3/8 | 3/8 | 1/8 |

Tulajdonságai:

- $0 \le p_k \le 1$
- $\sum p_k = 1$
:::

::: {.column width="60%"}
```{=html}
<div class="widget"><svg id="d3-plot" viewBox="0 0 600 320" role="img" aria-label="A fejek számának eloszlása vonaldiagramon"></svg></div>
<script>
(() => {
  const P = window.Plot, svg = document.getElementById('d3-plot');
  const x = P.scale(-0.5, 3.5, 70, 580), y = P.scale(0, 0.5, 280, 20);
  P.grid(svg, y, 70, 580, [0, 0.125, 0.25, 0.375, 0.5], 3);
  [1, 3, 3, 1].forEach((c, k) => {
    P.el(svg, 'line', {x1: x(k), x2: x(k), y1: y(0), y2: y(c / 8), style: 'stroke:var(--accent);stroke-width:5'});
    P.el(svg, 'circle', {class: 'dot', cx: x(k), cy: y(c / 8), r: 9});
    P.el(svg, 'text', {class: 'tick', x: x(k), y: 306, 'text-anchor': 'middle'}, k);
  });
  P.el(svg, 'line', {class: 'axis', x1: 70, x2: 580, y1: y(0), y2: y(0)});
})();
</script>
```
:::
::::

## Diszkrét és folytonos valószínűségi változók

:::: {.columns}
::: {.column}
::: {.callout-note}
## Diszkrét
Lehetséges értékei **megszámlálhatók** (izolált pontok a számegyenesen). Eloszlását a $p_k = P(X = x_k)$ valószínűségek adják meg.

*Pszichológiai példák:* helyes válaszok száma egy teszten, hibák száma, pánikrohamok száma egy héten.
:::
:::

::: {.column}
::: {.callout-tip}
## Folytonos
Értékei egy **intervallumot** töltenek ki; egyetlen érték valószínűsége 0, csak **tartományoknak** van pozitív valószínűsége. Eloszlását a **sűrűségfüggvény** adja meg.

*Pszichológiai példák:* reakcióidő, testmagasság, szívfrekvencia.
:::
:::
::::

# Várható érték és szórás

## Várható érték

A várható érték a lehetséges értékek **valószínűségekkel súlyozott átlaga** – az eloszlás „közepe”:

$$M(X) = \mu_X = \sum_{k} x_k\,p_k$$

*Példa – kockadobás:* minden érték valószínűsége $1/6$, így

$$M(X) = 1 \cdot \tfrac{1}{6} + 2 \cdot \tfrac{1}{6} + \ldots + 6 \cdot \tfrac{1}{6} = \frac{21}{6} = 3{,}5$$

::: {.callout-warning}
A várható érték **átlagérték**, nem a leggyakoribb érték – a kockadobásnál nincs is a lehetséges értékek között. A nemzetközi szakirodalomban jele: $E(X)$.
:::

## Variancia és szórás {.smaller}

**Variancia:** $D^2(X) = \sigma_X^2 = \sum_k (x_k - \mu)^2\,p_k = M(X^2) - M(X)^2$; **szórás:** $D(X) = \sqrt{D^2(X)}$

*Példa:* egy autókölcsönzőből 20 hét alatt hetente kikölcsönzött autók száma

| Autók száma ($x_i$) | 10 | 11 | 12 | 13 | **Összesen** |
|:--|--:|--:|--:|--:|--:|
| Hetek száma | 5 | 6 | 7 | 2 | **20** |
| $p_i$ | 0,25 | 0,30 | 0,35 | 0,10 | **1** |
| $x_i\,p_i$ | 2,5 | 3,3 | 4,2 | 1,3 | **11,3** |
| $x_i^2\,p_i$ | 25 | 36,3 | 50,4 | 16,9 | **128,6** |

$\mu = 11{,}3$; $\quad \sigma^2 = 128{,}6 - 11{,}3^2 = 0{,}91$; $\quad \sigma = \sqrt{0{,}91} \approx 0{,}95$ autó

## Standardizálás és relatív szórás

A **standardizált** (normált) változó:

$$Z = \frac{X - \mu}{\sigma}, \qquad M(Z) = 0, \quad D^2(Z) = 1$$

$Z$ azt mutatja meg, hogy $X$ értéke **hány szórásnyira** van a várható értéktől – mértékegységtől függetlenül.

A **relatív szórás**: $\sigma / \mu$ (csak pozitív, arányskálájú változónál értelmes).

# Folytonos valószínűségi változók

## Sűrűségfüggvény

:::: {.columns}
::: {.column width="52%"}
Folytonos változónál egyetlen érték valószínűsége 0, ezért az eloszlást az $f(x)$ **sűrűségfüggvénnyel** adjuk meg:

1. $f(x) \ge 0$ – a görbe az $x$ tengely fölött van
2. a görbe alatti teljes terület 1
3. egy $[a;\ b]$ intervallumba esés valószínűsége a fölötte lévő **terület**:

$$P(a \le X \le b) = \int_a^b f(x)\,dx$$
:::

::: {.column width="48%"}
```{=html}
<div class="widget"><svg id="ds-plot" viewBox="0 0 520 330" role="img" aria-label="Reakcióidő-szerű ferde sűrűségfüggvény satírozott intervallummal"></svg></div>
<script>
(() => {
  const P = window.Plot, svg = document.getElementById('ds-plot');
  // lognormális „reakcióidő” sűrűség (ms)
  const f = x => x <= 0 ? 0 : Math.exp(-((Math.log(x) - Math.log(450)) ** 2) / (2 * 0.25 ** 2)) / (x * 0.25 * Math.sqrt(2 * Math.PI));
  const sx = P.scale(150, 1100, 20, 505), sy = P.scale(0, 0.0038, 285, 20), a = 400, b = 550;
  P.el(svg, 'path', {class: 'area', d: P.path(f, a, b, sx, sy) + `L${sx(b)},${sy(0)}L${sx(a)},${sy(0)}Z`});
  P.el(svg, 'path', {class: 'curve', d: P.path(f, 150, 1100, sx, sy)});
  P.el(svg, 'line', {class: 'axis', x1: 20, x2: 505, y1: sy(0), y2: sy(0)});
  [200, 400, 600, 800, 1000].forEach(v => P.el(svg, 'text', {class: 'tick', x: sx(v), y: 310, 'text-anchor': 'middle'}, v));
  P.el(svg, 'text', {class: 'label', x: sx(475), y: sy(0.0012), 'text-anchor': 'middle'}, 'P(400 ≤ X ≤ 550)');
  P.el(svg, 'text', {class: 'tick', x: 505, y: 326, 'text-anchor': 'end'}, 'reakcióidő (ms)');
})();
</script>
```
:::
::::

## Eloszlásfüggvény

Az **eloszlásfüggvény** megadja, mekkora valószínűséggel kisebb $X$ egy adott $x$ értéknél: $F(x) = P(X < x)$, és $P(a \le X < b) = F(b) - F(a)$.

```{=html}
<div class="grid" style="--cols:2">
  <div class="widget"><svg id="cdf1" viewBox="0 0 460 230" role="img" aria-label="Diszkrét változó lépcsős eloszlásfüggvénye"></svg></div>
  <div class="widget"><svg id="cdf2" viewBox="0 0 460 230" role="img" aria-label="Folytonos változó eloszlásfüggvénye"></svg></div>
</div>
<script>
(() => {
  const P = window.Plot;
  const s1 = document.getElementById('cdf1'), x1 = P.scale(-1, 4, 50, 445), y = P.scale(0, 1, 190, 20);
  P.grid(s1, y, 50, 445, [0, 0.5, 1], 1);
  const F = [0, 1 / 8, 4 / 8, 7 / 8, 1];
  for (let k = 0; k <= 4; k++) {
    const a = k === 0 ? -1 : k - 1, b = k === 4 ? 4 : k;
    P.el(s1, 'line', {x1: x1(a), x2: x1(b), y1: y(F[k]), y2: y(F[k]), style: 'stroke:var(--accent);stroke-width:4'});
    if (k < 4) P.el(s1, 'circle', {cx: x1(k), cy: y(F[k]), r: 5, style: 'fill:var(--paper);stroke:var(--accent);stroke-width:2'});
  }
  [0, 1, 2, 3].forEach(v => P.el(s1, 'text', {class: 'tick', x: x1(v), y: 215, 'text-anchor': 'middle'}, v));
  P.el(s1, 'text', {class: 'label', x: 445, y: 40, 'text-anchor': 'end'}, 'diszkrét: lépcsős');
  const s2 = document.getElementById('cdf2'), x2 = P.scale(-3.5, 3.5, 50, 445);
  P.grid(s2, y, 50, 445, [0, 0.5, 1], 1);
  P.el(s2, 'path', {class: 'curve', d: P.path(v => P.Phi(v), -3.5, 3.5, x2, y)});
  [-3, -2, -1, 0, 1, 2, 3].forEach(v => P.el(s2, 'text', {class: 'tick', x: x2(v), y: 215, 'text-anchor': 'middle'}, P.fmt(v)));
  P.el(s2, 'text', {class: 'label', x: 445, y: 160, 'text-anchor': 'end'}, 'folytonos: sima S-görbe');
})();
</script>
```

Diszkrét változónál **lépcsős**, folytonosnál **folytonos** (deriváltja a sűrűségfüggvény). A nemzetközi irodalom többnyire $F(x) = P(X \le x)$ alakban definiálja.

## Várható érték és szórás folytonos esetben

Az összegzés helyére **integrál** kerül:

$$M(X) = \int_{-\infty}^{\infty} x\,f(x)\,dx$$

$$D^2(X) = \int_{-\infty}^{\infty} (x - \mu)^2 f(x)\,dx, \qquad D(X) = \sqrt{D^2(X)}$$

::: {.callout-note}
A jelentés ugyanaz, mint diszkrét esetben: a várható érték az eloszlás „súlypontja”, a szórás a tőle mért tipikus eltérés.
:::

# Nevezetes eloszlások

## Nevezetes eloszlások áttekintése {.smaller}

| Eloszlás | Típus | Paraméter | Várható érték | Variancia | Pszichológiai példa |
|:--|:--|:--|:-:|:-:|:--|
| Binomiális $B(n, p)$ | diszkrét | $n, p$ | $np$ | $np(1-p)$ | helyes válaszok száma találgatásnál |
| Poisson $Po(\lambda)$ | diszkrét | $\lambda$ | $\lambda$ | $\lambda$ | ritka események száma egy időszakban |
| Normális $N(\mu, \sigma^2)$ | folytonos | $\mu, \sigma$ | $\mu$ | $\sigma^2$ | IQ-pontszám, mérési hiba |

: A **statisztikai eloszlásokat** ($\chi^2$, $t$, $F$) a hipotézisvizsgálatoknál használjuk – ezekről később lesz szó.

## Binomiális eloszlás

Egy $A$ esemény valószínűsége $p$. A kísérletet $n$-szer **egymástól függetlenül** megismételjük; $X$ = $A$ bekövetkezéseinek száma.

$$P(X = k) = \binom{n}{k} p^k (1-p)^{n-k}, \qquad k = 0, 1, \ldots, n$$

$$\mu = np, \qquad \sigma^2 = np(1-p)$$

::: {.callout-note}
## Példa: visszatevéses húzás
10 golyóból 3 piros; visszatevéssel 20-szor húzunk ($p = 0{,}3$). Annak valószínűsége, hogy pontosan 6 piros lesz:

$P(X = 6) = \binom{20}{6} \cdot 0{,}3^6 \cdot 0{,}7^{14} \approx 0{,}192$; $\quad \mu = 6$, $\sigma^2 = 4{,}2$
:::

## Próbálja ki: találgatás egy teszten

:::: {.columns}
::: {.column width="60%"}
```{=html}
<div class="widget"><svg id="bn-plot" viewBox="0 0 700 380" role="img" aria-label="Binomiális eloszlás oszlopdiagramja"></svg></div>
```
:::

::: {.column width="40%"}
Feleletválasztós teszt; aki **csak találgat**, minden kérdést $p$ valószínűséggel talál el.

```{=html}
<div class="controls" style="gap:8px">
  <label><span>Kérdések száma: n = <output id="bn-n-o"></output></span><input id="bn-n" type="range" min="1" max="40" step="1" value="20"></label>
  <label><span>Találati esély: p = <output id="bn-p-o"></output></span><input id="bn-p" type="range" min="0.05" max="0.95" step="0.05" value="0.25"></label>
  <label><span>Megfelelt, ha legalább <output id="bn-k-o"></output> helyes</span><input id="bn-k" type="range" min="0" max="40" step="1" value="10"></label>
</div>
<div class="grid" style="--cols:2;gap:8px;margin-top:10px">
  <div class="stat"><b id="bn-pk" style="font-size:24px"></b><small>P(X ≥ k) – „átmegy” találgatással</small></div>
  <div class="stat"><b id="bn-m" style="font-size:24px"></b><small>μ = np és σ</small></div>
</div>
<script>
(() => {
  const P = window.Plot, $ = id => document.getElementById(id), svg = $('bn-plot');
  function draw() {
    const n = +$('bn-n').value, p = +$('bn-p').value;
    $('bn-k').max = n;
    const k0 = Math.min(+$('bn-k').value, n), pr = Array.from({length: n + 1}, (_, k) => P.binom(n, k, p));
    const ymax = Math.max(...pr) * 1.15, x = P.scale(-0.5, n + 0.5, 60, 690), y = P.scale(0, ymax, 340, 20), w = Math.max(2, (x(1) - x(0)) * 0.75);
    svg.replaceChildren();
    const st = ymax > 0.5 ? 0.2 : ymax > 0.2 ? 0.1 : 0.05;
    P.grid(svg, y, 60, 690, Array.from({length: Math.floor(ymax / st) + 1}, (_, i) => i * st), 2);
    pr.forEach((v, k) => P.el(svg, 'rect', {class: k >= k0 ? 'bar' : '', x: x(k) - w / 2, width: w, y: y(v), height: y(0) - y(v),
      style: k >= k0 ? 'fill:var(--accent-2);fill-opacity:.75' : 'fill:var(--accent);fill-opacity:.45'}));
    const step = n > 20 ? 5 : n > 10 ? 2 : 1;
    for (let k = 0; k <= n; k += step) P.el(svg, 'text', {class: 'tick', x: x(k), y: 362, 'text-anchor': 'middle'}, k);
    P.el(svg, 'line', {class: 'axis', x1: 60, x2: 690, y1: y(0), y2: y(0)});
    const tail = pr.slice(k0).reduce((a, b) => a + b, 0);
    $('bn-n-o').value = n; $('bn-p-o').value = P.fmt(p, 2); $('bn-k-o').value = k0;
    $('bn-pk').textContent = P.fmt(tail * 100, tail < 0.01 ? 3 : 1) + '%';
    $('bn-m').textContent = P.fmt(n * p, 1) + ' és ' + P.fmt(Math.sqrt(n * p * (1 - p)), 2);
  }
  ['bn-n', 'bn-p', 'bn-k'].forEach(id => $(id).oninput = draw);
  draw();
})();
</script>
```
:::
::::

::: {.notes}
20 kérdés, 4 válaszlehetőség (p = 0,25): annak esélye, hogy valaki pusztán találgatással legalább 10 helyes választ ad, kb. 1,4%. Ez a tesztfejlesztésben és a „véletlen szint feletti” teljesítmény megítélésében is fontos.
:::

## Poisson-eloszlás {.smaller}

Ha $X$ értékei $k = 0, 1, 2, \ldots$ és

$$P(X = k) = \frac{\lambda^k}{k!}\,e^{-\lambda}, \qquad \lambda > 0,$$

akkor $X$ **$\lambda$ paraméterű Poisson-eloszlású**; $\mu = \sigma^2 = \lambda$ [(Poisson, 1837)]{.cite}.

- **Ritka események** száma egy időszakban: hívások 10 perc alatt, gépelési hibák oldalanként – a pszichológiában pl. **pánikrohamok** száma egy héten
- A binomiális eloszlás **határesete**: nagy $n$, kis $p$, $np \to \lambda$

::: {.callout-note}
## Példa
Naponta átlagosan 2,1 téves tűzriasztás: $P(X = 4) = \frac{2{,}1^4}{4!}\,e^{-2{,}1} \approx 0{,}099$
:::

## Próbálja ki: Poisson és binomiális

:::: {.columns}
::: {.column width="60%"}
```{=html}
<div class="widget">
  <svg id="po-plot" viewBox="0 0 700 360" role="img" aria-label="Poisson-eloszlás és binomiális közelítése"></svg>
  <div class="legend"><span><i style="border-top:10px solid var(--accent);opacity:.5;width:12px"></i>Poisson(λ)</span><span><i style="border-top-color:var(--accent-2)"></i>binomiális B(n, λ/n)</span></div>
</div>
```
:::

::: {.column width="40%"}
```{=html}
<div class="controls" style="gap:8px">
  <label><span>λ = <output id="po-l-o"></output></span><input id="po-l" type="range" min="0.5" max="10" step="0.1" value="2.1"></label>
  <label><span>Binomiális: n = <output id="po-n-o"></output>, p = λ/n = <output id="po-pp-o"></output></span><input id="po-n" type="range" min="5" max="200" step="1" value="10"></label>
</div>
<div class="grid" style="--cols:2;gap:8px;margin-top:10px">
  <div class="stat"><b id="po-4" style="font-size:24px"></b><small>Poisson: P(X = 4)</small></div>
  <div class="stat"><b id="po-d" style="font-size:24px"></b><small>legnagyobb eltérés a binomiálistól</small></div>
</div>
<p style="font-size:19px;margin-top:10px">Növelje n-et: a binomiális eloszlás egyre közelebb kerül a Poisson-eloszláshoz.</p>
<script>
(() => {
  const P = window.Plot, $ = id => document.getElementById(id), svg = $('po-plot');
  function draw() {
    const l = +$('po-l').value, n = +$('po-n').value, p = Math.min(1, l / n), K = 20;
    const po = Array.from({length: K + 1}, (_, k) => P.pois(l, k)), bi = Array.from({length: K + 1}, (_, k) => P.binom(n, k, p));
    const ymax = Math.max(...po, ...bi) * 1.15, x = P.scale(-0.5, K + 0.5, 60, 690), y = P.scale(0, ymax, 320, 20), w = (x(1) - x(0)) * 0.7;
    svg.replaceChildren();
    const st = ymax > 0.4 ? 0.1 : 0.05;
    P.grid(svg, y, 60, 690, Array.from({length: Math.floor(ymax / st) + 1}, (_, i) => i * st), 2);
    po.forEach((v, k) => P.el(svg, 'rect', {class: 'bar', x: x(k) - w / 2, width: w, y: y(v), height: y(0) - y(v)}));
    P.el(svg, 'path', {d: bi.map((v, k) => (k ? 'L' : 'M') + x(k).toFixed(1) + ',' + y(v).toFixed(1)).join(''), style: 'fill:none;stroke:var(--accent-2);stroke-width:2.5'});
    bi.forEach((v, k) => P.el(svg, 'circle', {cx: x(k), cy: y(v), r: 4.5, style: 'fill:var(--accent-2)'}));
    for (let k = 0; k <= K; k += 2) P.el(svg, 'text', {class: 'tick', x: x(k), y: 344, 'text-anchor': 'middle'}, k);
    P.el(svg, 'line', {class: 'axis', x1: 60, x2: 690, y1: y(0), y2: y(0)});
    $('po-l-o').value = P.fmt(l, 1); $('po-n-o').value = n; $('po-pp-o').value = P.fmt(p, 3);
    $('po-4').textContent = P.fmt(po[4], 4);
    $('po-d').textContent = P.fmt(Math.max(...po.map((v, k) => Math.abs(v - bi[k]))), 4);
  }
  ['po-l', 'po-n'].forEach(id => $(id).oninput = draw);
  draw();
})();
</script>
```
:::
::::

## Normális eloszlás {.smaller}

Sűrűségfüggvénye a **Gauss-féle haranggörbe** [(Gauss, 1809)]{.cite}:

$$f(x) = \frac{1}{\sigma\sqrt{2\pi}}\,e^{-\frac{(x-\mu)^2}{2\sigma^2}}$$

:::: {.columns}
::: {.column width="48%"}
- $\mu$: a középérték – a görbe szimmetriája miatt egybeesik a móduszszal és a mediánnal
- $\sigma$: a szórás – kis szórás a várható érték körül koncentrálódó eloszlást jelent
- Jelölés: $X \sim N(\mu, \sigma^2)$
:::

::: {.column width="52%"}
```{=html}
<div class="widget">
  <svg id="nf-plot" viewBox="0 0 520 200" role="img" aria-label="Normális eloszlások különböző paraméterekkel"></svg>
  <div class="legend" style="margin-left:10px;flex-wrap:wrap;gap:4px 14px">
    <span><i></i>N(0, 1)</span><span><i style="border-top-color:var(--accent-2)"></i>N(0, 2²)</span><span><i style="border-top-color:var(--ok)"></i>N(2, 0,5²)</span>
  </div>
</div>
<script>
(() => {
  const P = window.Plot, svg = document.getElementById('nf-plot');
  const sx = P.scale(-6, 6, 15, 505), sy = P.scale(0, 0.85, 175, 8), n = (m, s) => x => P.phi((x - m) / s) / s;
  [[0, 1, 'var(--accent)'], [0, 2, 'var(--accent-2)'], [2, 0.5, 'var(--ok)']].forEach(([m, s, c]) =>
    P.el(svg, 'path', {d: P.path(n(m, s), -6, 6, sx, sy), style: `fill:none;stroke:${c};stroke-width:3.5`}));
  P.el(svg, 'line', {class: 'axis', x1: 15, x2: 505, y1: sy(0), y2: sy(0)});
  [-4, -2, 0, 2, 4].forEach(v => P.el(svg, 'text', {class: 'tick', x: sx(v), y: 196, 'text-anchor': 'middle'}, P.fmt(v)));
})();
</script>
```
:::
::::

## Normális-e a pszichológiai adat? {.smaller}

- Az **IQ-tesztek** pontszámait úgy konstruálják, hogy közelítőleg $N(100, 15^2)$ eloszlásúak legyenek
- A valódi adatok azonban **ritkán** pontosan normálisak: 440 nagy mintás teljesítmény- és pszichometriai mérésből egy sem volt az [(Micceri, 1989)]{.cite}
- 693 kis mintás pszichológiai eloszlásnak csak 5,5%-a volt a normálishoz közeli ferdeségű és csúcsosságú [(Blanca és mtsai, 2013)]{.cite}
- A **reakcióidő** tipikusan jobbra ferde; kérdőíves pontszámoknál gyakori a plafon- vagy padlóhatás

A normális eloszlás ettől még központi jelentőségű: a **mintaátlag** eloszlása a centrális határeloszlás-tétel miatt jól közelíthető vele.

## A standard normális eloszlás

A $\mu = 0$, $\sigma = 1$ paraméterű tag a **standard normális eloszlás**: $Z \sim N(0, 1)$; eloszlásfüggvénye $\Phi(z)$.

:::: {.columns}
::: {.column width="55%"}
**Lineáris transzformáció:** ha $X \sim N(\mu, \sigma^2)$, akkor $Y = aX + b \sim N(a\mu + b,\ a^2\sigma^2)$, azaz $Y$ szórása $|a|\sigma$.

**Standardizálás** és visszafelé:

$$Z = \frac{X - \mu}{\sigma} \sim N(0, 1), \qquad X = \sigma Z + \mu$$
:::

::: {.column width="45%"}
| $Y$ | várható érték | szórás |
|:--|:-:|:-:|
| $2X + 3$ | $2\mu + 3$ | $2\sigma$ |
| $5X$ | $5\mu$ | $5\sigma$ |
| $0{,}1X - 2$ | $0{,}1\mu - 2$ | $0{,}1\sigma$ |
:::
::::

## Lineáris transzformáció egy mintán {.smaller}

Legyen a minta $x_1, \ldots, x_n$, átlaga $\bar{x}$, szórása $s$. Ha minden értékhez $b$-t adunk, illetve $a$-val szorzunk:

| Transzformált adatok | Átlag | Szórás | Variancia |
|:--|:-:|:-:|:-:|
| $x_i + b$ | $\bar{x} + b$ | $s$ | $s^2$ |
| $a \cdot x_i$ | $a\bar{x}$ | $\lvert a \rvert s$ | $a^2 s^2$ |
| $a \cdot x_i + b$ | $a\bar{x} + b$ | $\lvert a \rvert s$ | $a^2 s^2$ |

: Eltolás nem változtat a szóródáson; nyújtás a szórást $|a|$-szorosára változtatja.

*Példa:* New Mexicóban a június 20-i hőmérséklet átlaga 86 °F, szórása 12,6 °F → Celsiusban ($Y = (X - 32)/1{,}8$) 30 °C és 7 °C. Budapesten 25 °C és 5 °C → Fahrenheitben ($X = 1{,}8Y + 32$) [77 °F és 9 °F.]{.fragment}

## Próbálja ki: standard pontskálák

:::: {.columns}
::: {.column width="58%"}
```{=html}
<div class="widget"><svg id="ss-plot" viewBox="0 0 680 330" role="img" aria-label="Standard normális görbe a kiválasztott z-értékkel"></svg></div>
```
:::

::: {.column width="42%"}
A pszichológiai tesztek eredményeit gyakran **lineárisan transzformált** z-pontként közlik.

```{=html}
<div class="controls"><label><span>z = <output id="ss-z-o"></output></span><input id="ss-z" type="range" min="-3" max="3" step="0.05" value="1"></label></div>
<div class="grid" style="--cols:2;gap:8px;margin-top:10px">
  <div class="stat"><b id="ss-iq" style="font-size:24px"></b><small>IQ-skála: 100 + 15z</small></div>
  <div class="stat"><b id="ss-t" style="font-size:24px"></b><small>T-pont: 50 + 10z</small></div>
  <div class="stat"><b id="ss-st" style="font-size:24px"></b><small>sztenin (1–9): 5 + 2z</small></div>
  <div class="stat"><b id="ss-pr" style="font-size:24px"></b><small>percentilisrang: Φ(z)</small></div>
</div>
<script>
(() => {
  const P = window.Plot, $ = id => document.getElementById(id), svg = $('ss-plot');
  const sx = P.scale(-3.5, 3.5, 20, 665), sy = P.scale(0, 0.43, 270, 15);
  function draw() {
    const z = +$('ss-z').value;
    svg.replaceChildren();
    P.el(svg, 'path', {class: 'area', d: P.path(P.phi, -3.5, z, sx, sy) + `L${sx(z)},${sy(0)}L${sx(-3.5)},${sy(0)}Z`});
    P.el(svg, 'path', {class: 'curve', d: P.path(P.phi, -3.5, 3.5, sx, sy)});
    P.el(svg, 'line', {class: 'mean', x1: sx(z), x2: sx(z), y1: sy(0), y2: sy(P.phi(z)) - 10});
    P.el(svg, 'line', {class: 'axis', x1: 20, x2: 665, y1: sy(0), y2: sy(0)});
    [-3, -2, -1, 0, 1, 2, 3].forEach(v => {
      P.el(svg, 'text', {class: 'tick', x: sx(v), y: 290, 'text-anchor': 'middle'}, 'z ' + P.fmt(v));
      P.el(svg, 'text', {class: 'tick', x: sx(v), y: 310, 'text-anchor': 'middle'}, 'IQ ' + (100 + 15 * v));
      P.el(svg, 'text', {class: 'tick', x: sx(v), y: 328, 'text-anchor': 'middle'}, 'T ' + (50 + 10 * v));
    });
    $('ss-z-o').value = P.fmt(z, 2);
    $('ss-iq').textContent = P.fmt(100 + 15 * z, 1);
    $('ss-t').textContent = P.fmt(50 + 10 * z, 1);
    $('ss-st').textContent = Math.min(9, Math.max(1, Math.round(5 + 2 * z)));
    $('ss-pr').textContent = P.fmt(P.Phi(z) * 100, 1) + '.';
  }
  $('ss-z').oninput = draw;
  draw();
})();
</script>
```
:::
::::

## Néhány összefüggés a normális eloszlásra

:::: {.columns}
::: {.column width="58%"}
```{=html}
<div class="widget"><svg id="sr-plot" viewBox="0 0 640 330" role="img" aria-label="A 68–95–99,7 szabály szemléltetése"></svg></div>
<script>
(() => {
  const P = window.Plot, svg = document.getElementById('sr-plot');
  const sx = P.scale(-3.6, 3.6, 15, 625), sy = P.scale(0, 0.45, 285, 15);
  [[-3, 3, 0.12], [-2, 2, 0.2], [-1, 1, 0.3]].forEach(([a, b, o]) =>
    P.el(svg, 'path', {d: P.path(P.phi, a, b, sx, sy) + `L${sx(b)},${sy(0)}L${sx(a)},${sy(0)}Z`, style: `fill:var(--accent);fill-opacity:${o}`}));
  P.el(svg, 'path', {class: 'curve', d: P.path(P.phi, -3.6, 3.6, sx, sy)});
  P.el(svg, 'line', {class: 'axis', x1: 15, x2: 625, y1: sy(0), y2: sy(0)});
  [['34,1%', -0.5, 0.15], ['34,1%', 0.5, 0.15], ['13,6%', -1.5, 0.05], ['13,6%', 1.5, 0.05], ['2,1%', -2.45, 0.025], ['2,1%', 2.45, 0.025]].forEach(([t, x, y]) =>
    P.el(svg, 'text', {class: 'title', x: sx(x), y: sy(y), 'text-anchor': 'middle', style: 'font-size:16px'}, t));
  ['μ−3σ', 'μ−2σ', 'μ−σ', 'μ', 'μ+σ', 'μ+2σ', 'μ+3σ'].forEach((t, i) => P.el(svg, 'text', {class: 'tick', x: sx(i - 3), y: 310, 'text-anchor': 'middle'}, t));
})();
</script>
```
:::

::: {.column width="42%"}
| Intervallum | Valószínűség |
|:--|--:|
| $\mu \pm \sigma$ | 68,27% |
| $\mu \pm 2\sigma$ | 95,45% |
| $\mu \pm 3\sigma$ | 99,73% |

Szimmetria: $\Phi(-z) = 1 - \Phi(z)$, így $P(-1 < Z < 1)$ $= 2\Phi(1) - 1$ $= 0{,}6827$
:::
::::

## Próbálja ki: normáliseloszlás-kalkulátor

:::: {.columns}
::: {.column width="58%"}
```{=html}
<div class="widget"><svg id="nc-plot" viewBox="0 0 680 340" role="img" aria-label="Normális eloszlás a kiszámított terület satírozásával"></svg></div>
```
A nyomtatott táblázatok helyett ma programot használunk – ez a dia is egy ilyen kalkulátor.
:::

::: {.column width="42%"}
```{=html}
<div class="controls" style="gap:10px;font-size:19px">
  <div>Minta:<span class="seg" id="nc-pre"><button data-m="0" data-s="1" data-a="-1" data-b="1" class="on">N(0, 1)</button><button data-m="100" data-s="15" data-a="85" data-b="130">IQ</button><button data-m="2" data-s="0.03" data-a="1.95" data-b="1.98">kenyér</button></span></div>
  <div class="grid" style="--cols:2;gap:8px">
    <label>μ <input id="nc-m" type="number" step="any" value="0" style="width:100%;font-size:18px"></label>
    <label>σ <input id="nc-s" type="number" step="any" min="0" value="1" style="width:100%;font-size:18px"></label>
    <label>a (alsó határ) <input id="nc-a" type="number" step="any" value="-1" style="width:100%;font-size:18px"></label>
    <label>b (felső határ) <input id="nc-b" type="number" step="any" value="1" style="width:100%;font-size:18px"></label>
  </div>
  <div>Terület:<span class="seg" id="nc-mode"><button data-k="ab" class="on">a &lt; X &lt; b</button><button data-k="lb">X &lt; b</button><button data-k="ga">X &gt; a</button></span></div>
</div>
<div class="stat" style="margin-top:10px"><b id="nc-p"></b><small id="nc-z"></small></div>
<script>
(() => {
  const P = window.Plot, $ = id => document.getElementById(id), svg = $('nc-plot');
  let mode = 'ab';
  function draw() {
    const m = +$('nc-m').value, s = Math.max(1e-9, +$('nc-s').value), a = +$('nc-a').value, b = +$('nc-b').value;
    const za = (a - m) / s, zb = (b - m) / s, lo = mode === 'lb' ? -4 : za, hi = mode === 'ga' ? 4 : zb;
    const p = mode === 'ab' ? P.Phi(zb) - P.Phi(za) : mode === 'lb' ? P.Phi(zb) : 1 - P.Phi(za);
    const sx = P.scale(-4, 4, 20, 665), sy = P.scale(0, 0.43, 290, 15), L = Math.max(-4, Math.min(4, lo)), H = Math.max(-4, Math.min(4, hi));
    svg.replaceChildren();
    if (H > L) P.el(svg, 'path', {class: 'area', d: P.path(P.phi, L, H, sx, sy) + `L${sx(H)},${sy(0)}L${sx(L)},${sy(0)}Z`, style: 'fill-opacity:.35'});
    P.el(svg, 'path', {class: 'curve', d: P.path(P.phi, -4, 4, sx, sy)});
    P.el(svg, 'line', {class: 'axis', x1: 20, x2: 665, y1: sy(0), y2: sy(0)});
    [-3, -2, -1, 0, 1, 2, 3].forEach(v => {
      P.el(svg, 'text', {class: 'tick', x: sx(v), y: 312, 'text-anchor': 'middle'}, P.fmt(m + v * s, s < 0.1 ? 2 : s < 1 ? 1 : 0));
      P.el(svg, 'text', {class: 'tick', x: sx(v), y: 332, 'text-anchor': 'middle', style: 'opacity:.7'}, 'z ' + P.fmt(v));
    });
    $('nc-p').textContent = 'P = ' + P.fmt(p, 4);
    $('nc-z').textContent = (mode !== 'lb' ? `z(a) = ${P.fmt(za, 2)}  ` : '') + (mode !== 'ga' ? `z(b) = ${P.fmt(zb, 2)}` : '');
  }
  ['nc-m', 'nc-s', 'nc-a', 'nc-b'].forEach(id => $(id).oninput = draw);
  P.seg('nc-mode', ds => { mode = ds.k; draw(); });
  P.seg('nc-pre', ds => { $('nc-m').value = ds.m; $('nc-s').value = ds.s; $('nc-a').value = ds.a; $('nc-b').value = ds.b; draw(); });
  draw();
})();
</script>
```
:::
::::

## Példa: kenyerek tömege {.smaller}

A 2 kg-os kenyerek tömege $X \sim N(2;\ 0{,}03^2)$ kg. Standardizálás: $Z = (X - 2)/0{,}03$.

a) $P(X < 1{,}95) = P\left(Z < \frac{1{,}95 - 2}{0{,}03}\right) = P(Z < -1{,}67) = 1 - \Phi(1{,}67) = 1 - 0{,}9525 = 0{,}0475$

b) $P(X > 1{,}98) = P(Z > -0{,}67) = \Phi(0{,}67) = 0{,}7486$

c) Milyen, 2 kg-ra szimmetrikus határok közé esik a kenyerek 90%-a? $P(Z > v) = 0{,}05$-ből $v = 1{,}645$, így $h = 1{,}645 \cdot 0{,}03 \approx 0{,}049$ kg: a kenyerek kb. 90%-a **1,951 és 2,049 kg** közé esik.

::: {.callout-note}
A táblázat kerekített z-értékekkel dolgozik; kalkulátorral pontosan: a) $0{,}0478$, b) $0{,}7475$.
:::

# Mintaátlag és centrális határeloszlás-tétel

## A minta mint valószínűségi változók együttese

- **$n$ elemű minta:** $n$ darab **azonos eloszlású**, egymástól **független** valószínűségi változó: $X_1, X_2, \ldots, X_n$
- Mindegyik $X_i$ eloszlása (várható értéke, szórása) megegyezik a populációban megfigyelt $X$ változóéval
- **Statisztika:** a mintaelemek függvénye – így maga is valószínűségi változó. Például a **mintaátlag**:

$$\bar{X} = \frac{1}{n}\sum_{i=1}^{n} X_i$$

Ezért van **eloszlása** a mintaátlagnak, a szórásnak, a mediánnak is: mintáról mintára ingadoznak.

## A mintaátlag eloszlása

Ha a populáció várható értéke $\mu$, szórása $\sigma$, akkor

$$M(\bar{X}) = \mu, \qquad D(\bar{X}) = \frac{\sigma}{\sqrt{n}}$$

- A mintaátlag **torzítatlanul** becsüli $\mu$-t
- Szórása – az **átlag standard hibája** – a mintanagyság négyzetgyökével csökken
- Minél nagyobb $n$, a mintaátlag eloszlása annál inkább hasonlít a **normális eloszláshoz** – akkor is, ha a populáció nem normális

## Centrális határeloszlás-tétel

**Független**, azonos eloszlású valószínűségi változók összege – és így átlaga is – a tagok számának növekedésével **normális eloszláshoz** tart [(Fischer, 2011)]{.cite}:

$$\bar{X} \approx N\left(\mu,\ \frac{\sigma^2}{n}\right) \quad \text{elég nagy } n \text{ esetén}$$

- Ezért közelíthető sok jelenség normális eloszlással: sok független hatás **eredője** (pl. mérési hiba, biológiai jellemzők)
- Hagyományos ökölszabály: $n \ge 30$ – erősen ferde vagy nehéz farkú populációnál ennél **jóval nagyobb** minta kellhet [(Wilcox, 2017)]{.cite}

## Próbálja ki: centrális határeloszlás-tétel

:::: {.columns}
::: {.column width="62%"}
```{=html}
<div class="widget"><svg id="ct-plot" viewBox="0 0 720 420" role="img" aria-label="Populáció eloszlása és a mintaátlagok hisztogramja"></svg></div>
```
:::

::: {.column width="38%"}
```{=html}
<div class="controls" style="gap:10px">
  <div class="grid" id="ct-pop" style="--cols:2;gap:6px">
    <button class="btn on" data-p="norm">normális</button><button class="btn" data-p="exp">jobbra ferde</button>
    <button class="btn" data-p="unif">egyenletes</button><button class="btn" data-p="bim">kétcsúcsú</button>
  </div>
  <label><span>Mintanagyság: n = <output id="ct-n-o"></output></span><input id="ct-n" type="range" min="1" max="50" step="1" value="1"></label>
  <div><button class="btn" id="ct-new">Új 3000 minta</button></div>
</div>
<div class="stats">
  <div class="stat"><b id="ct-se"></b><small>σ/√n (elméleti standard hiba)</small></div>
  <div class="stat"><b id="ct-emp"></b><small>az átlagok tényleges szórása</small></div>
</div>
<p style="font-size:18px;margin-top:8px">Fent a populáció, lent 3000 mintaátlag hisztogramja és az N(μ, σ²/n) közelítés.</p>
<script>
(() => {
  const P = window.Plot, $ = id => document.getElementById(id), svg = $('ct-plot');
  const rn = () => Math.sqrt(-2 * Math.log(1 - Math.random())) * Math.cos(2 * Math.PI * Math.random());
  const pops = {
    norm: {m: 0, s: 1, r: [-4, 4], f: P.phi, g: rn},
    exp: {m: 1, s: 1, r: [-0.3, 6], f: x => x < 0 ? 0 : Math.exp(-x), g: () => -Math.log(1 - Math.random())},
    unif: {m: 0.5, s: Math.sqrt(1 / 12), r: [-0.2, 1.2], f: x => x >= 0 && x <= 1 ? 1 : 0, g: Math.random},
    bim: {m: 2.1, s: Math.sqrt(0.49 + 4), r: [-2, 6.2], f: x => 0.5 * (P.phi((x - 0.1) / 0.7) + P.phi((x - 4.1) / 0.7)) / 0.7, g: () => (Math.random() < 0.5 ? 0.1 : 4.1) + 0.7 * rn()}
  };
  let pop = pops.norm;
  function draw() {
    const n = +$('ct-n').value, [a, b] = pop.r, sx = P.scale(a, b, 40, 705), B = 60, bw = (b - a) / B;
    const bins = new Array(B).fill(0), means = [];
    for (let j = 0; j < 3000; j++) {
      let s = 0;
      for (let i = 0; i < n; i++) s += pop.g();
      const m = s / n, k = Math.floor((m - a) / bw);
      means.push(m);
      if (k >= 0 && k < B) bins[k]++;
    }
    const se = pop.s / Math.sqrt(n), mm = means.reduce((x, y) => x + y) / 3000;
    const emp = Math.sqrt(means.reduce((x, y) => x + (y - mm) ** 2, 0) / 2999);
    svg.replaceChildren();
    // populáció (felső panel)
    const fmax = Math.max(...Array.from({length: 200}, (_, i) => pop.f(a + (b - a) * i / 199))) * 1.1, sy1 = P.scale(0, fmax, 120, 18);
    P.el(svg, 'text', {class: 'label', x: 40, y: 14}, 'populáció');
    P.el(svg, 'path', {class: 'area', d: P.path(pop.f, a, b, sx, sy1, 400) + `L${sx(b)},${sy1(0)}L${sx(a)},${sy1(0)}Z`});
    P.el(svg, 'path', {class: 'curve', d: P.path(pop.f, a, b, sx, sy1, 400), style: 'stroke-width:2.5'});
    P.el(svg, 'line', {class: 'axis', x1: 40, x2: 705, y1: sy1(0), y2: sy1(0)});
    // mintaátlagok (alsó panel), sűrűségskálán
    const dens = bins.map(c => c / (3000 * bw)), nd = x => P.phi((x - pop.m) / se) / se;
    const ymax = Math.max(...dens, nd(pop.m)) * 1.08, sy2 = P.scale(0, ymax, 385, 150);
    P.el(svg, 'text', {class: 'label', x: 40, y: 146}, `${n} elemű minták átlagai`);
    dens.forEach((d, k) => { if (d) P.el(svg, 'rect', {class: 'bar', x: sx(a + k * bw) + 0.5, width: Math.max(1, sx(a + bw) - sx(a) - 1), y: sy2(d), height: sy2(0) - sy2(d)}); });
    P.el(svg, 'path', {d: P.path(nd, a, b, sx, sy2, 400), style: 'fill:none;stroke:var(--accent-2);stroke-width:3'});
    P.el(svg, 'line', {class: 'axis', x1: 40, x2: 705, y1: sy2(0), y2: sy2(0)});
    const step = (b - a) > 5 ? 1 : 0.2;
    for (let t = Math.ceil(a / step) * step; t <= b + 1e-9; t += step) P.el(svg, 'text', {class: 'tick', x: sx(t), y: 408, 'text-anchor': 'middle'}, P.fmt(t, step < 1 ? 1 : 0));
    $('ct-n-o').value = n;
    $('ct-se').textContent = P.fmt(se, 3);
    $('ct-emp').textContent = P.fmt(emp, 3);
  }
  $('ct-n').oninput = $('ct-new').onclick = draw;
  P.seg('ct-pop', ds => { pop = pops[ds.p]; draw(); });
  draw();
})();
</script>
```
:::
::::

::: {.notes}
Kezdjük n = 1-gyel (a mintaátlag eloszlása maga a populáció), majd növeljük: a kétcsúcsú és a ferde populációnál is kialakul a haranggörbe, és a hisztogram szűkül (σ/√n). A ferde populációnál kis n mellett még látszik a ferdeség.
:::

## Kitekintés: statisztikai eloszlások

A hipotézisvizsgálatokban a normális eloszlásból **származtatott** eloszlásokat használjuk:

| Eloszlás | Honnan származik? | Mire használjuk? |
|:--|:--|:--|
| $t$-eloszlás | standardizált átlag **becsült** szórással | átlagok összehasonlítása kis mintán [(Student, 1908)]{.cite} |
| $\chi^2$-eloszlás | standard normális változók négyzetösszege | gyakoriságok elemzése, illeszkedésvizsgálat |
| $F$-eloszlás | két $\chi^2$ változó (normált) hányadosa | varianciaelemzés (ANOVA) |

: Ezek részletes tárgyalása a következő témákban következik.

## Összefoglalás {.inverse .center}

- A **valószínűségi változó** számot rendel a kimenetelekhez; **eloszlása** írja le
- **Várható érték** = súlyozott átlag, **szórás** = tipikus eltérés; $Z = (X - \mu)/\sigma$
- **Binomiális:** sikerek száma $n$ független kísérletben; **Poisson:** ritka események száma
- **Normális:** szimmetrikus haranggörbe; 68–95–99,7%-os szabály; táblázat helyett program
- **Centrális határeloszlás-tétel:** a mintaátlag eloszlása közel normális, szórása $\sigma/\sqrt{n}$

## Irodalom {.smaller}

::: {.refs}
Blanca, M. J., Arnau, J., López-Montiel, D., Bono, R., & Bendayan, R. (2013). Skewness and kurtosis in real data samples. *Methodology, 9*(2), 78–84. https://doi.org/10.1027/1614-2241/a000057

Fischer, H. (2011). *A history of the central limit theorem: From classical to modern probability theory.* Springer.

Gauss, C. F. (1809). *Theoria motus corporum coelestium in sectionibus conicis solem ambientium.* Perthes & Besser.

Micceri, T. (1989). The unicorn, the normal curve, and other improbable creatures. *Psychological Bulletin, 105*(1), 156–166. https://doi.org/10.1037/0033-2909.105.1.156

Poisson, S. D. (1837). *Recherches sur la probabilité des jugements en matière criminelle et en matière civile.* Bachelier.

Student. (1908). The probable error of a mean. *Biometrika, 6*(1), 1–25.

Wilcox, R. R. (2017). *Introduction to robust estimation and hypothesis testing* (4th ed.). Academic Press.

**Magyar nyelvű tankönyv:** Vargha A. (2000). *Matematikai statisztika pszichológiai, nyelvészeti és biológiai alkalmazásokkal.* Pólya Kiadó.
:::

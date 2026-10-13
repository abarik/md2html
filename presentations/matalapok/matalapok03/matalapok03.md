---
title: "Eloszlások és ábrázolásuk"
subtitle: "Gyakorisági táblázatok és ábrák a leíró statisztikában"
author: "Abari Kálmán"
date: "2026. ősz"
lang: hu
footer: "Matematikai alapok II. · 3. Eloszlások és ábrázolásuk"
---

## Az eloszlások fontosabb jellemzői {.smaller}

| | Populáció (elméleti) | Minta (tapasztalati) |
|:--|:--|:--|
| **Eloszlás** | elméleti eloszlás | tapasztalati (empirikus) eloszlás |
| **Középértékek** | átlag, trimmelt átlag, medián, módusz | mintaátlag, trimmelt átlag, medián, módusz |
| **Szóródási mutatók** | elméleti szórás, variancia, relatív szórás, középeltérés, IQR | korrigált tapasztalati szórás és variancia, relatív szórás, középeltérés, IQR |
| **Alakmutatók** | ferdeség, csúcsosság | mintabeli ferdeség és csúcsosság |

: Ebben a részben az eloszlással és ábrázolásával foglalkozunk; a mutatók a következő részek témái.

```{=html}
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
  }
};
</script>
```

# Elméleti és tapasztalati eloszlás

## Elméleti eloszlás (populáció)

:::: {.columns}
::: {.column width="56%"}
Az eloszlás megmutatja, **milyen valószínűséggel** fordulnak elő a változó egyes értékei a populációban.

- **Diszkrét** változó: $P(X = x_i) = p_i$, ahol $\sum p_i = 1$
- **Folytonos** változó: sűrűségfüggvénnyel adjuk meg; a görbe alatti **terület** a valószínűség:

$$P(a \le X \le b) = \int_a^b f(x)\,dx$$
:::

::: {.column width="44%"}
```{=html}
<div class="widget"><svg id="th-plot" viewBox="0 0 520 330" role="img" aria-label="Sűrűségfüggvény, a görbe alatti terület a valószínűség"></svg></div>
<script>
(() => {
  const P = window.Plot, svg = document.getElementById('th-plot');
  const sx = P.scale(-3.5, 3.5, 20, 500), sy = P.scale(0, 0.42, 280, 20);
  const f = x => Math.exp(-x * x / 2) / Math.sqrt(2 * Math.PI), a = -0.6, b = 1.3;
  const path = (x0, x1) => Array.from({length: 121}, (_, i) => {
    const x = x0 + (x1 - x0) * i / 120;
    return (i ? 'L' : 'M') + sx(x).toFixed(1) + ',' + sy(f(x)).toFixed(1);
  }).join('');
  P.el(svg, 'path', {class: 'area', d: path(a, b) + `L${sx(b)},${sy(0)}L${sx(a)},${sy(0)}Z`});
  P.el(svg, 'path', {class: 'curve', d: path(-3.5, 3.5)});
  P.el(svg, 'line', {class: 'axis', x1: 20, x2: 500, y1: sy(0), y2: sy(0)});
  [[a, 'a'], [b, 'b']].forEach(([x, t]) => {
    P.el(svg, 'line', {class: 'mean', x1: sx(x), x2: sx(x), y1: sy(0), y2: sy(f(x))});
    P.el(svg, 'text', {class: 'label', x: sx(x), y: sy(0) + 28, 'text-anchor': 'middle'}, t);
  });
  P.el(svg, 'text', {class: 'tick', x: sx((a + b) / 2), y: sy(0.12), 'text-anchor': 'middle'}, 'P(a ≤ X ≤ b)');
  P.el(svg, 'text', {class: 'tick', x: sx(2.2), y: sy(0.2), 'text-anchor': 'middle'}, 'f(x)');
})();
</script>
```
:::
::::

## Tapasztalati eloszlás (minta)

- A populációbeli eloszlást **sosem ismerjük pontosan** – a minta alapján következtetünk rá
- A változó értékeinek **mintabeli** megoszlása a **tapasztalati** (empirikus) eloszlás
- Ezt **gyakorisági táblázatokkal** és **ábrákkal** írjuk le
- A minta növelésével a tapasztalati eloszlás egyre pontosabban közelíti az elméletit (*Glivenko–Cantelli-tétel*)

::: {.callout-tip}
Mielőtt bármit kiszámolnánk, **nézzük meg az adatokat**: a táblázat és az ábra az elemzés első lépése, nem díszítése. [(Tukey, 1977)]{.cite}
:::

# Gyakorisági táblázatok

## Gyakorisági eloszlás

A tapasztalati eloszlás a minta **gyakorisági eloszlása**: hány megfigyelés tartozik az egyes értékekhez vagy értékcsoportokhoz. Ezek alkotják a **gyakorisági táblázatot**.

```{=html}
<div class="grid" style="--cols:3">
  <div class="stat"><b>1.</b><small style="font-size:20px">kategorikus változó<br>(pl. vércsoport)</small></div>
  <div class="stat"><b>2.</b><small style="font-size:20px">nem csoportosított kvantitatív változó<br>(kevés különböző érték)</small></div>
  <div class="stat"><b>3.</b><small style="font-size:20px">csoportosított kvantitatív változó<br>(sok különböző érték)</small></div>
</div>
```

Jelölés: $f_i$ – gyakoriság, $n = \sum f_i$ – mintaelemszám, $p_i = f_i / n$ – relatív gyakoriság.

## Kategorikus változó: vércsoport

:::: {.columns}
::: {.column width="55%"}
25 véradó vércsoportja:

[AB, B, A, 0, B, 0, B, 0, A, 0, B, 0, B, B, B, A, 0, AB, AB, 0, A, B, AB, 0, A]{.muted}

A kategóriák sorrendje nominális változónál tetszőleges – célszerű **gyakoriság szerint** rendezni, vagy egy megszokott sorrendet követni.
:::

::: {.column width="45%"}
| Vércsoport | Gyakoriság ($f$) | % |
|:--|--:|--:|
| A | 5 | 20 |
| B | 8 | 32 |
| 0 | 8 | 32 |
| AB | 4 | 16 |
| **Összesen** | **25** | **100** |
:::
::::

## Nem csoportosított kvantitatív változó

Egy figyelmi feladatban elkövetett **hibák száma** 25 résztvevőnél (példaadatok):

[10, 10, 6, 12, 6, 9, 16, 20, 11, 10, 11, 11, 9, 12, 11, 7, 10, 11, 14, 21, 12, 6, 10, 11, 6]{.muted}

Kevés különböző érték van, ezért **minden értéknek** külön oszlopot adunk – csoportosításra nincs szükség:

| Hibák | 6 | 7 | 9 | 10 | 11 | 12 | 14 | 16 | 20 | 21 | **Összesen** |
|:--|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| Gyakoriság ($f$) | 4 | 1 | 2 | 5 | 6 | 3 | 1 | 1 | 1 | 1 | **25** |

## Relatív és kumulatív gyakoriság {.smaller}

| Hibák ($x_i$) | 6 | 7 | 9 | 10 | 11 | 12 | 14 | 16 | 20 | 21 |
|:--|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| Gyakoriság ($f_i$) | 4 | 1 | 2 | 5 | 6 | 3 | 1 | 1 | 1 | 1 |
| Relatív gyakoriság ($p_i$) | 0,16 | 0,04 | 0,08 | 0,20 | 0,24 | 0,12 | 0,04 | 0,04 | 0,04 | 0,04 |
| Kumulatív gyakoriság ($F_i$) | 4 | 5 | 7 | 12 | 18 | 21 | 22 | 23 | 24 | 25 |
| Kumulatív relatív gyakoriság | 0,16 | 0,20 | 0,28 | 0,48 | 0,72 | 0,84 | 0,88 | 0,92 | 0,96 | 1,00 |

- **Relatív gyakoriság:** $p_i = f_i / n$, összege 1 (100%)
- **Kumulatív gyakoriság:** az adott értéknél **kisebb vagy egyenlő** értékek gyakoriságainak összege, $F_i = \sum_{j \le i} f_j$; relatív változata $F_i / n$

::: {.notes}
Olvassuk le együtt: a résztvevők 48%-a legfeljebb 10, 72%-a legfeljebb 11 hibát vétett.
:::

## Osztályok kialakítása {.smaller}

Sok különböző értéknél az adatokat **osztályokba** soroljuk:

:::: {.columns}
::: {.column width="50%"}
1. Az adatokat **nagyság szerint rendezzük**
2. Eldöntjük az osztályok **számát** vagy **szélességét**
3. Kijelöljük a határokat: az osztályok **diszjunktak**, az alsó határ beletartozik, a felső nem: $[85;\ 95)$
4. Megszámoljuk a **gyakoriságokat**, kiszámoljuk a relatív gyakoriságokat
:::

::: {.column width="50%"}
::: {.callout-tip}
## Hány osztály legyen?
- Ökölszabály: 5–15 osztály
- **Sturges:** $k \approx 1 + \log_2 n$ [(Sturges, 1926)]{.cite}
- **Freedman–Diaconis:** $h = 2 \cdot \mathrm{IQR} / \sqrt[3]{n}$ – kevésbé érzékeny a kiugró értékekre [(Freedman & Diaconis, 1981)]{.cite}

A választás **befolyásolja, mit látunk**!
:::
:::
::::

## Csoportosított kvantitatív változó {.smaller}

:::: {.columns}
::: {.column width="50%"}
A Kincskereső programban részt vevő 30 óvodás és tanuló testmagassága (cm):

[143, 151, 136, 127, 132, 132, 126, 138, 119, 104, 113, 90, 126, 123, 121, 133, 104, 99, 112, 129, 107, 139, 122, 137, 112, 121, 140, 134, 133, 123]{.muted}

Sturges szerint $k \approx 1 + \log_2 30 \approx 5{,}9$, azaz kb. 6–7 osztály – itt 10 cm-es osztályokat használunk.
:::

::: {.column width="50%"}
| Magasság (cm) | $f$ | $p$ | % |
|:--|--:|--:|--:|
| [85; 95) | 1 | 0,03 | 3 |
| [95; 105) | 3 | 0,10 | 10 |
| [105; 115) | 4 | 0,13 | 13 |
| [115; 125) | 6 | 0,20 | 20 |
| [125; 135) | 9 | 0,30 | 30 |
| [135; 145) | 6 | 0,20 | 20 |
| [145; 155) | 1 | 0,03 | 3 |
| **Összesen** | **30** | **1** | **100** |
:::
::::

# Ábrázolás

## Melyik ábra mire való?

| Változó | Ajánlott ábra | Kerülendő |
|:--|:--|:--|
| Kategorikus (nominális, ordinális) | **oszlopdiagram** | 3D-s és sok szeletű kördiagram |
| Kvantitatív, kevés érték vagy kis minta | **pontdiagram**, oszlopdiagram | csak átlag oszloppal |
| Kvantitatív, sok érték | **hisztogram**, sűrűségbecslés, kumulatív eloszlásfüggvény | túl kevés vagy túl sok osztály |
| Csoportok összehasonlítása | egyedi adatpontok + összegzés (pl. *raincloud* ábra) | „dinamitábra”: oszlop ± hibasáv |

: A dobozábrát (boxplot) a szóródási mutatókkal együtt tárgyaljuk.

## Pontdiagram {.smaller}

Minden adatot egy, a mért érték fölé rajzolt **pont** jelenít meg (hibák száma, $n = 25$):

```{=html}
<div class="widget"><svg id="dot-plot" viewBox="0 0 900 200" role="img" aria-label="Pontdiagram a hibák számáról"></svg></div>
<script>
(() => {
  const P = window.Plot, svg = document.getElementById('dot-plot');
  const data = [10, 10, 6, 12, 6, 9, 16, 20, 11, 10, 11, 11, 9, 12, 11, 7, 10, 11, 14, 21, 12, 6, 10, 11, 6];
  const x = P.scale(5, 22, 40, 870), base = 165, cnt = {};
  P.el(svg, 'line', {class: 'axis', x1: 30, x2: 880, y1: base, y2: base});
  for (let v = 5; v <= 22; v++) P.el(svg, 'text', {class: 'tick', x: x(v), y: base + 26, 'text-anchor': 'middle'}, v);
  data.forEach(v => {
    const c = cnt[v] = (cnt[v] || 0) + 1;
    P.el(svg, 'circle', {class: 'dot', cx: x(v), cy: base - 13 - (c - 1) * 24, r: 10});
  });
})();
</script>
```

:::: {.columns}
::: {.column}
- **Előnye:** kevés adatnál könnyen elkészíthető; látszik, hol tömörülnek az adatok, és vannak-e **kiugró** értékek
:::

::: {.column}
- **Hátránya:** nagy mintánál a gyakoriságok nehezen olvashatók le
:::
::::

## Oszlopdiagram és kördiagram

```{=html}
<div class="grid" style="--cols:2">
  <div class="widget"><svg id="bar-plot" viewBox="0 0 460 290" role="img" aria-label="Vércsoportok oszlopdiagramon"></svg></div>
  <div class="widget"><svg id="pie-plot" viewBox="0 0 460 290" role="img" aria-label="Vércsoportok kördiagramon"></svg></div>
</div>
<script>
(() => {
  const P = window.Plot, data = [['B', 8], ['0', 8], ['A', 5], ['AB', 4]], n = 25;
  const colors = ['var(--accent)', 'var(--accent-2)', 'var(--ok)', 'var(--warn)'];
  const bar = document.getElementById('bar-plot'), y = P.scale(0, 10, 245, 25);
  for (let v = 0; v <= 10; v += 2) {
    P.el(bar, 'line', {class: 'grid', x1: 50, x2: 445, y1: y(v), y2: y(v)});
    P.el(bar, 'text', {class: 'tick', x: 42, y: y(v) + 5, 'text-anchor': 'end'}, v);
  }
  data.forEach(([k, f], i) => {
    const x0 = 70 + i * 95;
    P.el(bar, 'rect', {x: x0, width: 70, y: y(f), height: y(0) - y(f), style: `fill:${colors[0]}`});
    P.el(bar, 'text', {class: 'label', x: x0 + 35, y: y(f) - 8, 'text-anchor': 'middle'}, f);
    P.el(bar, 'text', {class: 'tick', x: x0 + 35, y: 270, 'text-anchor': 'middle'}, k);
  });
  P.el(bar, 'line', {class: 'axis', x1: 50, x2: 445, y1: y(0), y2: y(0)});
  const pie = document.getElementById('pie-plot'), cx = 150, cy = 145, R = 115;
  let a0 = -Math.PI / 2;
  data.forEach(([k, f], i) => {
    const a1 = a0 + f / n * 2 * Math.PI, big = a1 - a0 > Math.PI ? 1 : 0, m = (a0 + a1) / 2;
    P.el(pie, 'path', {d: `M${cx},${cy}L${cx + R * Math.cos(a0)},${cy + R * Math.sin(a0)}A${R},${R} 0 ${big} 1 ${cx + R * Math.cos(a1)},${cy + R * Math.sin(a1)}Z`,
      style: `fill:${colors[i]};stroke:var(--paper);stroke-width:2`});
    P.el(pie, 'text', {class: 'title', x: cx + R * 0.62 * Math.cos(m), y: cy + R * 0.62 * Math.sin(m) + 6, 'text-anchor': 'middle', style: 'fill:#fff'}, P.fmt(f / n * 100) + '%');
    P.el(pie, 'rect', {x: 300, y: 80 + i * 36, width: 18, height: 18, rx: 4, style: `fill:${colors[i]}`});
    P.el(pie, 'text', {class: 'tick', x: 326, y: 95 + i * 36}, `${k} (${f})`);
    a0 = a1;
  });
})();
</script>
```

Oszlopdiagramnál minden kategóriának egy **oszlop** felel meg, amelynek **magassága** a gyakoriságot (vagy arányt) mutatja; a tengely **nullától** induljon. A kördiagramon a **szög** és a **terület** hordozza az arányt.

## Kör vagy oszlop? Amit a kutatások mutatnak

- Az emberi észlelés a **közös skálán elhelyezett pozíciót** és a **hosszt** ítéli meg legpontosabban; a **szöget** és a **területet** kevésbé pontosan [(Cleveland & McGill, 1984)]{.cite}
- **Rész–egész** viszony becslésénél a kördiagram nem rosszabb az oszlopdiagramnál [(Spence & Lewandowsky, 1991)]{.cite}
- A **3D-s** hatás, a sok szelet és a díszítés torzít, és nem ad információt [(Tufte, 1983)]{.cite}

::: {.callout-tip}
## Gyakorlati ajánlás
Kategóriák **összehasonlítására** oszlopdiagram; kördiagram legfeljebb néhány kategóriánál, ha a **részek aránya az egészhez** a lényeg.
:::

## Hisztogram

- A vízszintes tengelyen az **osztályintervallumok**, fölöttük téglalapok, amelyek **területe** a relatív gyakorisággal arányos: magasságuk $p_i / h$, ahol $h$ az osztályszélesség – így a teljes terület 1
- Diszkrét változónál az értékek az intervallumok **közepére** kerülnek
- A minta növelésével a hisztogram az elméleti **sűrűségfüggvényt** közelíti
- Sok módszer feltételezi, hogy a hisztogram nagyjából **haranggörbe** (normális eloszlás) alakú – az ábrán ezt is ellenőrizzük

::: {.callout-warning}
A hisztogram alakja függ az **osztályszélességtől** és az osztályok **kezdőpontjától** – ugyanazok az adatok különböző képet mutathatnak. Próbálja ki!
:::

## Próbálja ki: hisztogram

:::: {.columns}
::: {.column width="62%"}
```{=html}
<div class="widget">
  <svg id="hi-plot" viewBox="0 0 720 400" role="img" aria-label="Hisztogram állítható osztályszélességgel"></svg>
  <div class="legend"><span><i></i>gyakorisági poligon / elméleti sűrűség</span></div>
</div>
```
:::

::: {.column width="38%"}
```{=html}
<div class="controls">
  <div>Adatok:<span class="seg" id="hi-data"><button data-d="kk" class="on">Kincskereső (n = 30)</button><button data-d="sim">szimulált (n = 1000)</button></span></div>
  <label><span>Osztályszélesség: h = <output id="hi-w-o"></output> cm</span>
    <input id="hi-w" type="range" min="2" max="20" step="1" value="10"></label>
  <label><span>Kezdőpont eltolása: <output id="hi-o-o"></output> cm</span>
    <input id="hi-o" type="range" min="0" max="9" step="1" value="0"></label>
  <label style="display:flex;gap:10px;align-items:center"><input type="checkbox" id="hi-poly"> gyakorisági poligon</label>
</div>
<div class="stats">
  <div class="stat"><b id="hi-k"></b><small>osztály ezzel a szélességgel</small></div>
  <div class="stat"><b id="hi-fd"></b><small>Sturges / Freedman–Diaconis szerinti szélesség (cm)</small></div>
</div>
<script>
(() => {
  const P = window.Plot, $ = id => document.getElementById(id), svg = $('hi-plot');
  const kk = [143, 151, 136, 127, 132, 132, 126, 138, 119, 104, 113, 90, 126, 123, 121, 133, 104, 99, 112, 129, 107, 139, 122, 137, 112, 121, 140, 134, 133, 123];
  let seed = 7;  // determinisztikus álvéletlen-generátor (mulberry32), hogy mindig ugyanaz a minta legyen
  const rnd = () => { seed = seed + 0x6D2B79F5 | 0; let t = Math.imul(seed ^ seed >>> 15, 1 | seed); t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; };
  const sim = Array.from({length: 1000}, () => 124.2 + 14.2 * Math.sqrt(-2 * Math.log(1 - rnd())) * Math.cos(2 * Math.PI * rnd()));
  const sets = {kk, sim};
  let which = 'kk';
  const W = 720, H = 400, L = 54, R = 12, T = 16, B = 42, X0 = 70, X1 = 180;
  const sx = P.scale(X0, X1, L, W - R);
  const quart = (s, q) => { const i = (s.length - 1) * q, lo = Math.floor(i); return s[lo] + (s[Math.ceil(i)] - s[lo]) * (i - lo); };
  function draw() {
    const data = sets[which], n = data.length, w = +$('hi-w').value;
    $('hi-o').max = w - 1;
    const off = Math.min(+$('hi-o').value, w - 1), s = [...data].sort((a, b) => a - b);
    const k0 = Math.floor((s[0] - 85 - off) / w), k1 = Math.floor((s[n - 1] - 85 - off) / w);
    const bins = [];
    for (let k = k0; k <= k1; k++) bins.push({a: 85 + off + k * w, f: 0});
    data.forEach(v => bins[Math.floor((v - 85 - off) / w) - k0].f++);
    const fmax = Math.max(...bins.map(b => b.f)), step = [1, 2, 5, 10, 20, 50, 100, 200].find(st => fmax * 1.15 / st <= 6);
    const ymax = Math.ceil(fmax * 1.15 / step) * step, sy = P.scale(0, ymax, H - B, T);
    svg.replaceChildren();
    for (let v = 0; v <= ymax; v += step) {
      P.el(svg, 'line', {class: 'grid', x1: L, x2: W - R, y1: sy(v), y2: sy(v)});
      P.el(svg, 'text', {class: 'tick', x: L - 8, y: sy(v) + 5, 'text-anchor': 'end'}, v);
    }
    for (let x = 80; x <= X1; x += 20) P.el(svg, 'text', {class: 'tick', x: sx(x), y: H - B + 26, 'text-anchor': 'middle'}, x);
    bins.forEach(b => {
      if (b.f) P.el(svg, 'rect', {class: 'bar', x: sx(b.a) + 0.5, width: Math.max(1, sx(b.a + w) - sx(b.a) - 1), y: sy(b.f), height: sy(0) - sy(b.f)});
    });
    if ($('hi-poly').checked) {
      const pts = [[bins[0].a - w / 2, 0], ...bins.map(b => [b.a + w / 2, b.f]), [bins[bins.length - 1].a + w * 1.5, 0]];
      P.el(svg, 'path', {class: 'curve', d: pts.map(([x, f], i) => (i ? 'L' : 'M') + sx(x).toFixed(1) + ',' + sy(f).toFixed(1)).join('')});
    }
    if (which === 'sim') {
      let d = '';
      for (let i = 0; i <= 200; i++) {
        const x = X0 + (X1 - X0) * i / 200, z = (x - 124.2) / 14.2;
        d += (i ? 'L' : 'M') + sx(x).toFixed(1) + ',' + sy(n * w * Math.exp(-z * z / 2) / (14.2 * Math.sqrt(2 * Math.PI))).toFixed(1);
      }
      P.el(svg, 'path', {class: 'ref', d});
    }
    P.el(svg, 'line', {class: 'axis', x1: L, x2: W - R, y1: sy(0), y2: sy(0)});
    const sturges = (s[n - 1] - s[0]) / (1 + Math.log2(n)), fd = 2 * (quart(s, 0.75) - quart(s, 0.25)) / Math.cbrt(n);
    $('hi-w-o').value = w;
    $('hi-o-o').value = off;
    $('hi-k').textContent = bins.length;
    $('hi-fd').textContent = P.fmt(sturges, 1) + ' / ' + P.fmt(fd, 1);
  }
  $('hi-w').oninput = $('hi-o').oninput = $('hi-poly').onchange = draw;
  $('hi-data').onclick = e => {
    const btn = e.target.closest('button');
    if (!btn) return;
    which = btn.dataset.d;
    for (const x of $('hi-data').children) x.classList.toggle('on', x === btn);
    draw();
  };
  draw();
})();
</script>
```
:::
::::

::: {.notes}
Mutassuk meg: 10 cm-es osztályoknál a Kincskereső-adatok egycsúcsúnak látszanak; 4–5 cm-nél „fogazott” lesz a kép. A szimulált 1000 elemű mintánál a hisztogram szépen követi az elméleti sűrűségfüggvényt.
:::

## A kumulatív eloszlás ábrája

:::: {.columns}
::: {.column width="50%"}
```{=html}
<div class="widget"><svg id="ecdf-plot" viewBox="0 0 640 380" role="img" aria-label="A hibák számának tapasztalati eloszlásfüggvénye"></svg></div>
<script>
(() => {
  const P = window.Plot, svg = document.getElementById('ecdf-plot');
  const tab = [[6, 4], [7, 1], [9, 2], [10, 5], [11, 6], [12, 3], [14, 1], [16, 1], [20, 1], [21, 1]], n = 25;
  const x = P.scale(4, 23, 56, 625), y = P.scale(0, 1, 335, 20);
  for (let v = 0; v <= 1.001; v += 0.25) {
    P.el(svg, 'line', {class: 'grid', x1: 56, x2: 625, y1: y(v), y2: y(v)});
    P.el(svg, 'text', {class: 'tick', x: 48, y: y(v) + 5, 'text-anchor': 'end'}, P.fmt(v, 2));
  }
  for (let v = 4; v <= 22; v += 2) P.el(svg, 'text', {class: 'tick', x: x(v), y: 360, 'text-anchor': 'middle'}, v);
  P.el(svg, 'line', {class: 'axis', x1: 56, x2: 625, y1: y(0), y2: y(0)});
  P.el(svg, 'line', {class: 'mean', x1: 56, x2: x(11), y1: y(0.5), y2: y(0.5)});
  P.el(svg, 'line', {class: 'mean', x1: x(11), x2: x(11), y1: y(0.5), y2: y(0)});
  P.el(svg, 'text', {class: 'label', x: x(11) + 8, y: y(0.08)}, 'medián = 11');
  let F = 0, d = `M${x(4)},${y(0)}`;
  tab.forEach(([v, f]) => {
    d += `L${x(v)},${y(F / n)}`;
    F += f;
    d += `L${x(v)},${y(F / n)}`;
  });
  d += `L${x(23)},${y(1)}`;
  P.el(svg, 'path', {class: 'curve', d});
  F = 0;
  tab.forEach(([v, f]) => { F += f; P.el(svg, 'circle', {class: 'dot', cx: x(v), cy: y(F / n), r: 5}); });
})();
</script>
```
:::

::: {.column width="50%"}
- A **tapasztalati eloszlásfüggvény** minden $x$-hez megadja, hogy az adatok hányad része **legfeljebb** $x$
- Lépcsős függvény: minden mért értéknél a relatív gyakorisággal ugrik
- Osztályozás nélkül, **minden adatot** felhasznál
- Leolvasható róla a **medián** (0,5-ös szint) és bármely percentilis
:::
::::

## Mutasd az adatokat!

:::: {.columns}
::: {.column width="58%"}
```{=html}
<div class="widget"><svg id="sd-plot" viewBox="0 0 640 380" role="img" aria-label="Két csoport: oszlopdiagram vagy egyedi adatok"></svg></div>
```
:::

::: {.column width="42%"}
Két csoport pontszáma, $n = 20$ fő csoportonként. Az átlag mindkettőben **50,1**.

```{=html}
<div class="controls">
  <div>Ábra:<span class="seg" id="sd-mode"><button data-m="bar" class="on">átlag ± SE</button><button data-m="dots">adatok</button><button data-m="both">mindkettő</button></span></div>
</div>
<script>
(() => {
  const P = window.Plot, $ = id => document.getElementById(id), svg = $('sd-plot');
  const groups = [
    ['Kontroll', [50, 28, 62, 45, 71, 38, 55, 49, 33, 66, 52, 41, 58, 47, 74, 36, 53, 44, 60, 40]],
    ['Kísérleti', [34, 36, 31, 38, 35, 33, 37, 32, 36, 39, 64, 66, 61, 68, 65, 63, 67, 62, 66, 69]]
  ];
  const y = P.scale(0, 80, 340, 20);
  let mode = 'bar';
  function draw() {
    svg.replaceChildren();
    for (let v = 0; v <= 80; v += 20) {
      P.el(svg, 'line', {class: 'grid', x1: 50, x2: 630, y1: y(v), y2: y(v)});
      P.el(svg, 'text', {class: 'tick', x: 42, y: y(v) + 5, 'text-anchor': 'end'}, v);
    }
    groups.forEach(([name, xs], g) => {
      const cx = 200 + g * 280, n = xs.length, m = xs.reduce((a, b) => a + b) / n;
      const se = Math.sqrt(xs.reduce((a, b) => a + (b - m) ** 2, 0) / (n - 1) / n);
      if (mode !== 'dots') {
        P.el(svg, 'rect', {class: 'bar', x: cx - 70, width: 140, y: y(m), height: y(0) - y(m)});
        P.el(svg, 'line', {class: 'axis', x1: cx, x2: cx, y1: y(m - se), y2: y(m + se)});
        P.el(svg, 'line', {class: 'axis', x1: cx - 18, x2: cx + 18, y1: y(m + se), y2: y(m + se)});
      }
      if (mode !== 'bar') {
        const seen = {};
        xs.forEach(v => {
          const b = Math.round(v / 3), c = seen[b] = (seen[b] || 0) + 1;
          P.el(svg, 'circle', {class: 'dot', cx: cx + (c % 2 ? 1 : -1) * Math.floor(c / 2) * 18, cy: y(v), r: 7});
        });
        P.el(svg, 'line', {class: 'mean', x1: cx - 80, x2: cx + 80, y1: y(m), y2: y(m)});
      }
      P.el(svg, 'text', {class: 'tick', x: cx, y: 365, 'text-anchor': 'middle'}, name);
    });
    P.el(svg, 'line', {class: 'axis', x1: 50, x2: 630, y1: y(0), y2: y(0)});
  }
  $('sd-mode').onclick = e => {
    const btn = e.target.closest('button');
    if (!btn) return;
    mode = btn.dataset.m;
    for (const x of $('sd-mode').children) x.classList.toggle('on', x === btn);
    draw();
  };
  draw();
})();
</script>
```

::: {.callout-warning}
Az átlagot mutató oszlopdiagram („dinamitábra”) elrejti az eloszlást: itt a kísérleti csoport valójában **két alcsoportból** áll. [(Weissgerber és mtsai, 2015)]{.cite}
:::
:::
::::

## A jó ábra ismérvei {.smaller}

:::: {.columns}
::: {.column}
- **Mutassa az adatokat**: az egyedi pontokat is, pl. *raincloud* ábrával [(Allen és mtsai, 2021)]{.cite}
- Az **összegző statisztikák** nem helyettesítik az ábrát: azonos mutatók mellett is gyökeresen eltérhetnek az adatok [(Anscombe, 1973; Matejka & Fitzmaurice, 2017)]{.cite}
- Oszlopdiagramnál a tengely **nullától** induljon; ne legyen 3D, árnyék, díszítés [(Tufte, 1983)]{.cite}
:::

::: {.column}
- **Színek**: színtévesztők számára is megkülönböztethető paletta, „szivárvány” és piros–zöld skála nélkül [(Crameri és mtsai, 2020)]{.cite}
- **Feliratok**: tengelynév mértékegységgel, $n$ megadása, beszédes cím [(APA, 2020)]{.cite}
- **Eszközök**: JASP és jamovi (ingyenes, grafikus felület); R és Python
:::
::::

## Összefoglalás {.inverse .center}

- Az **elméleti** eloszlás a populációt, a **tapasztalati** a mintát írja le
- Gyakorisági táblázat: **gyakoriság**, **relatív** és **kumulatív** gyakoriság
- Sok különböző értéknél **osztályokba** soroljuk az adatokat – a választás befolyásolja a képet
- Kategorikus változóhoz **oszlopdiagram**, kvantitatív változóhoz **pontdiagram**, **hisztogram**, **eloszlásfüggvény**
- **Mutassuk az adatokat**, ne csak az átlagot!

## Irodalom (1/2) {.smaller}

::: {.refs}
Allen, M., Poggiali, D., Whitaker, K., Marshall, T. R., van Langen, J., & Kievit, R. A. (2021). Raincloud plots: A multi-platform tool for robust data visualization [version 2]. *Wellcome Open Research, 4*, 63. https://doi.org/10.12688/wellcomeopenres.15191.2

American Psychological Association. (2020). *Publication manual of the American Psychological Association* (7th ed.).

Anscombe, F. J. (1973). Graphs in statistical analysis. *The American Statistician, 27*(1), 17–21.

Cleveland, W. S., & McGill, R. (1984). Graphical perception: Theory, experimentation, and application to the development of graphical methods. *Journal of the American Statistical Association, 79*(387), 531–554.

Crameri, F., Shephard, G. E., & Heron, P. J. (2020). The misuse of colour in science communication. *Nature Communications, 11*, 5444. https://doi.org/10.1038/s41467-020-19160-7

Freedman, D., & Diaconis, P. (1981). On the histogram as a density estimator: L₂ theory. *Zeitschrift für Wahrscheinlichkeitstheorie und verwandte Gebiete, 57*(4), 453–476.

Matejka, J., & Fitzmaurice, G. (2017). Same stats, different graphs: Generating datasets with varied appearance and identical statistics through simulated annealing. In *Proceedings of the 2017 CHI Conference on Human Factors in Computing Systems*. ACM. https://doi.org/10.1145/3025453.3025912
:::

## Irodalom (2/2) {.smaller}

::: {.refs}
Spence, I., & Lewandowsky, S. (1991). Displaying proportions and percentages. *Applied Cognitive Psychology, 5*(1), 61–77. https://doi.org/10.1002/acp.2350050106

Sturges, H. A. (1926). The choice of a class interval. *Journal of the American Statistical Association, 21*(153), 65–66.

Tufte, E. R. (1983). *The visual display of quantitative information.* Graphics Press.

Tukey, J. W. (1977). *Exploratory data analysis.* Addison-Wesley.

Weissgerber, T. L., Milic, N. M., Winham, S. J., & Garovic, V. D. (2015). Beyond bar and line graphs: Time for a new data presentation paradigm. *PLoS Biology, 13*(4), e1002128. https://doi.org/10.1371/journal.pbio.1002128

**Magyar nyelvű tankönyv:** Vargha A. (2000). *Matematikai statisztika pszichológiai, nyelvészeti és biológiai alkalmazásokkal.* Pólya Kiadó.
:::

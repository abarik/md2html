---
title: "Valószínűség-számítás"
subtitle: "Események, valószínűség, feltételes valószínűség és a Bayes-tétel"
author: "Abari Kálmán"
date: "2026. ősz"
lang: hu
footer: "Matematikai alapok · 5. Valószínűség-számítás"
---

## Miért kell a pszichológusnak valószínűség-számítás?

- A pszichológiai jelenségek **sztochasztikusak**: ugyanarra az ingerre sem reagálunk kétszer ugyanúgy
- A **statisztikai következtetés** ($p$-érték, becslés) a valószínűség-számításra épül
- A **diagnosztikai döntések** (szűrőtesztek) feltételes valószínűségek
- A valószínűségi **ítéletalkotás** maga is kutatási terület: intuíciónk a véletlenről gyakran téved [(Tversky & Kahneman, 1974)]{.cite}
- Egyre elterjedtebbek a **bayesi** módszerek is [(Etz & Vandekerckhove, 2018)]{.cite}

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
  },
  seg(id, fn) {  // kapcsológomb-csoport: a kattintott gomb lesz aktív
    const box = document.getElementById(id);
    box.onclick = e => {
      const b = e.target.closest('button');
      if (!b) return;
      for (const x of box.children) x.classList.toggle('on', x === b);
      fn(b.dataset);
    };
  }
};
</script>
```

# Véletlen jelenségek és események

## Determinisztikus és véletlen jelenségek {.smaller}

:::: {.columns}
::: {.column}
### Determinisztikus
Azonos körülmények között mindig **ugyanúgy** zajlik le; a feltételekből a kimenetel egyértelműen következik.

*Példa:* a szabadesés törvénye, Ohm törvénye.
:::

::: {.column}
### Sztochasztikus (véletlen)
A kimenetel lényegében azonos körülmények között sem egyértelmű.

*Példa:* pénzfeldobás, kockadobás, lottóhúzás – vagy egy személy **reakcióideje** egymást követő próbákban.
:::
::::

A **valószínűség-számítás** a **véletlen tömegjelenségek** – sokszor megismételhető véletlen jelenségek – törvényszerűségeit vizsgálja.

## Kísérlet, elemi esemény, eseménytér

- **Kísérlet:** ellenőrzött feltételek mellett végzett, megismételhető vizsgálat vagy megfigyelés, amelynek eredményét véletlen tényezők is befolyásolják
- Egy kísérletnek több lehetséges kimenetele van; egyszeri végrehajtáskor **pontosan egy** következik be – de előre nem tudjuk, melyik
- **Elemi esemény:** a kísérlet egy lehetséges kimenetele
- **Eseménytér** ($\Omega$): a kísérlet összes elemi eseményének halmaza

## Példák eseménytérre {.smaller}

| Kísérlet | Eseménytér | Típusa |
|:--|:--|:--|
| Egy érme egyszeri feldobása | $\Omega_1 = \{f, i\}$ | véges |
| Két feldobás | $\Omega_2 = \{ff, fi, if, ii\}$ | véges |
| Három feldobás | $\Omega_3 = \{fff, ffi, fif, iff, fii, ifi, iif, iii\}$ | véges, $2^3 = 8$ elem |
| Dobálás az első fejig | $\Omega_4 = \{f, if, iif, iiif, \ldots\}$ | megszámlálhatóan végtelen |
| Egyszerű reakcióidő mérése (ms) | a nemnegatív valós számok, $[0;\ \infty)$ | nem megszámlálható (kontinuum) |

: $f$ = fej, $i$ = írás.

## Események

- **Esemény:** az $\Omega$ eseménytér tetszőleges részhalmaza; jelölése $A, B, C, \ldots$
- Az $A$ esemény **bekövetkezik**, ha a kísérlet kimenetele eleme az $A$ halmaznak
- **Összetett esemény:** legalább két elemi eseményből áll
- **Biztos esemény:** az összes elemi eseményt tartalmazza, mindig bekövetkezik: $I = \Omega$
- **Lehetetlen esemény:** egyetlen elemi eseményt sem tartalmaz, sosem következik be: $O = \emptyset$

*Példa – kockadobás:* $A$ = „páratlan számot dobunk” $= \{1, 3, 5\}$, $B$ = „3-nál kisebbet dobunk” $= \{1, 2\}$

## Viszonyok események között

- $A_1$ **maga után vonja** $A_2$-t ($A_1 \subseteq A_2$), ha valahányszor $A_1$ bekövetkezik, $A_2$ is bekövetkezik
- Az $A$ **ellentett eseménye** ($\overline{A}$) pontosan akkor következik be, ha $A$ nem
- Események **kölcsönösen kizárják** egymást, ha egyszerre legfeljebb egyikük következhet be

::: {.callout-note}
## Példa – kockadobás
$\Omega = \{1, 2, 3, 4, 5, 6\}$. „Nem dobunk ötöst”: $\overline{\{5\}} = \{1, 2, 3, 4, 6\}$. $A$ = páratlan, $B$ = páros: ekkor $\overline{A} = B$, és $A$, $B$ kizárják egymást. Továbbá $\{1\} \subseteq A$.
:::

# Eseményalgebra

## Műveletek eseményekkel {.smaller}

| Művelet | Hagyományos jelölés | Halmazjelölés | Mikor következik be? |
|:--|:-:|:-:|:--|
| összeg | $A + B$ | $A \cup B$ | **legalább az egyik** bekövetkezik |
| szorzat | $AB$ | $A \cap B$ | **mindkettő** bekövetkezik |
| különbség | $A - B$ | $A \setminus B$ | $A$ bekövetkezik, de $B$ nem |
| ellentett | $\overline{A}$ | $\overline{A}$ (vagy $A^c$) | $A$ nem következik be |

: A magyar tankönyvek gyakran a „+” és a szorzásjelölést használják; a nemzetközi szakirodalomban a halmazjelölés az elterjedt.

- Az összeg és a szorzat **kommutatív** és **asszociatív**: $A \cup B = B \cup A$, $A \cap (B \cap C) = (A \cap B) \cap C$
- $A$ és $B$ pontosan akkor zárja ki egymást, ha $A \cap B = \emptyset$

## Azonosságok

:::: {.columns}
::: {.column}
- $A \cup A = A$, $\quad A \cap A = A$
- $A \cup \emptyset = A$, $\quad A \cap \emptyset = \emptyset$
- $A \cup \Omega = \Omega$, $\quad A \cap \Omega = A$
- $A \cup \overline{A} = \Omega$, $\quad A \cap \overline{A} = \emptyset$
:::

::: {.column}
**Disztributivitás:**

- $A \cap (B \cup C) = (A \cap B) \cup (A \cap C)$
- $A \cup (B \cap C) = (A \cup B) \cap (A \cup C)$

**De Morgan-azonosságok:**

- $\overline{A \cup B} = \overline{A} \cap \overline{B}$
- $\overline{A \cap B} = \overline{A} \cup \overline{B}$
:::
::::

## Próbálja ki: eseményalgebra

:::: {.columns}
::: {.column width="58%"}
```{=html}
<div class="widget"><svg id="vn-plot" viewBox="0 0 560 360" role="img" aria-label="Venn-diagram a kiválasztott eseménnyel"></svg></div>
```
:::

::: {.column width="42%"}
```{=html}
<div class="controls">
  <div class="grid" id="vn-ops" style="--cols:2;gap:8px">
    <button class="btn on" data-o="u">A ∪ B</button><button class="btn" data-o="i">A ∩ B</button>
    <button class="btn" data-o="ab">A ∖ B</button><button class="btn" data-o="ba">B ∖ A</button>
    <button class="btn" data-o="ca">Ā</button><button class="btn" data-o="cu">Ā ∩ B̄</button>
  </div>
</div>
<div class="callout callout-note" style="margin-top:12px"><p class="callout-title" id="vn-t"></p><p id="vn-d"></p></div>
<script>
(() => {
  const P = window.Plot, $ = id => document.getElementById(id);
  const ops = {
    u: ['A ∪ B (A + B)', 'Legalább az egyik bekövetkezik.', '<circle cx="210" cy="185" r="115" class="hl"/><circle cx="350" cy="185" r="115" class="hl"/>'],
    i: ['A ∩ B (AB)', 'Mindkettő bekövetkezik.', '<circle cx="210" cy="185" r="115" class="hl" clip-path="url(#vn-cB)"/>'],
    ab: ['A ∖ B (A − B)', 'A bekövetkezik, de B nem.', '<circle cx="210" cy="185" r="115" class="hl" mask="url(#vn-nB)"/>'],
    ba: ['B ∖ A (B − A)', 'B bekövetkezik, de A nem.', '<circle cx="350" cy="185" r="115" class="hl" mask="url(#vn-nA)"/>'],
    ca: ['Ā', 'A nem következik be (ellentett esemény).', '<rect x="20" y="20" width="520" height="320" rx="14" class="hl" mask="url(#vn-nA)"/>'],
    cu: ['Ā ∩ B̄ = A ∪ B ellentettje', 'Egyik sem következik be – de Morgan-azonosság.', '<rect x="20" y="20" width="520" height="320" rx="14" class="hl" mask="url(#vn-nAB)"/>']
  };
  const defs = '<defs><clipPath id="vn-cB"><circle cx="350" cy="185" r="115"/></clipPath>' +
    '<mask id="vn-nA"><rect width="560" height="360" fill="#fff"/><circle cx="210" cy="185" r="115" fill="#000"/></mask>' +
    '<mask id="vn-nB"><rect width="560" height="360" fill="#fff"/><circle cx="350" cy="185" r="115" fill="#000"/></mask>' +
    '<mask id="vn-nAB"><rect width="560" height="360" fill="#fff"/><circle cx="210" cy="185" r="115" fill="#000"/><circle cx="350" cy="185" r="115" fill="#000"/></mask></defs>' +
    '<style>#vn-plot .hl{fill:var(--accent);fill-opacity:.4}#vn-plot .o{fill:none;stroke:var(--fg);stroke-width:2.5}</style>';
  function draw(o) {
    const [t, d, shape] = ops[o];
    $('vn-plot').innerHTML = defs + shape +
      '<rect x="20" y="20" width="520" height="320" rx="14" class="o"/><circle cx="210" cy="185" r="115" class="o"/><circle cx="350" cy="185" r="115" class="o"/>' +
      '<text class="title" x="40" y="52">Ω</text><text class="title" x="140" y="110">A</text><text class="title" x="410" y="110">B</text>';
    $('vn-t').textContent = t;
    $('vn-d').textContent = d;
  }
  P.seg('vn-ops', ds => draw(ds.o));
  draw('u');
})();
</script>
```
:::
::::

## Teljes eseményrendszer

A $B_1, B_2, \ldots, B_n$ események **teljes eseményrendszert** alkotnak, ha

1. együtt kiadják a biztos eseményt: $B_1 \cup B_2 \cup \ldots \cup B_n = \Omega$, és
2. páronként kizárják egymást: $B_i \cap B_j = \emptyset$, ha $i \neq j$

Vagyis a kísérlet minden kimenetelekor **pontosan egy** $B_i$ következik be.

::: {.callout-note}
## Példák
Kockadobás: $\{1\}, \{2\}, \ldots, \{6\}$; vagy: páros / páratlan. Pszichológia: egy diagnosztikai rendszer kategóriái akkor alkotnak teljes eseményrendszert, ha mindenki **pontosan egy** kategóriába sorolható.
:::

## Feladatok {.smaller}

1. Egy érmét ötször feldobunk. Hány elemi esemény van? [$2^5 = 32$]{.fragment} Hányban van pontosan két fej? [$\binom{5}{2} = 10$]{.fragment}
2. Egy egész számot választunk; $A$: a szám 5-tel osztható, $B$: a szám 0-ra végződik.
   - $A \cup B$ = [5-tel osztható, mert $B \subseteq A$]{.fragment}
   - $A \cap B$ = [0-ra végződik ($A \cap B = B$)]{.fragment}
   - $A \setminus B$ = [5-re végződik]{.fragment}
3. Egyszerű reakcióidőt mérünk ($X$, ms); $A$: $X < 200$, $B$: $X > 180$.
   - $A \cap B$ = [$180 < X < 200$]{.fragment}
   - $A \cup B$ = [biztos esemény]{.fragment}
   - $\overline{A}$ = [$X \geq 200$]{.fragment}

# A valószínűség fogalma

## Valószínűség

- Egy kísérlet minden eseményéhez egy **számot** rendelünk: az esemény **valószínűségét**
- Ez 0 és 1 közötti szám, amely kifejezi, mennyire várható, hogy az esemény bekövetkezik
- 0-hoz közeli érték: alig elképzelhető; 1-hez közeli érték: szinte biztos
- Gyakran százalékban adjuk meg: $0{,}7 = 70\%$

::: {.callout-tip}
## Gyakoriság és relatív gyakoriság
Ha $n$ kísérletből az $A$ esemény $k$-szor következik be, akkor $k$ az $A$ **gyakorisága**, $k/n$ pedig a **relatív gyakorisága**. A kísérletszám növelésével a relatív gyakoriság egyre kisebb ingadozással egy rögzített szám körül stabilizálódik: ez a szám $P(A)$.
:::

## Próbálja ki: a relatív gyakoriság stabilizálódása

:::: {.columns}
::: {.column width="62%"}
```{=html}
<div class="widget"><svg id="lln-plot" viewBox="0 0 720 380" role="img" aria-label="A relatív gyakoriság alakulása a kísérletek számának függvényében"></svg></div>
```
:::

::: {.column width="38%"}
```{=html}
<div class="controls">
  <div>Esemény:<span class="seg" id="lln-ev"><button data-p="0.5" class="on">fej (1/2)</button><button data-p="0.1666667">hatos (1/6)</button></span></div>
  <div style="display:flex;gap:8px;flex-wrap:wrap">
    <button class="btn" data-k="10" id="lln-10">+10</button><button class="btn" data-k="100" id="lln-100">+100</button>
    <button class="btn" data-k="1000" id="lln-1000">+1000</button><button class="btn" id="lln-reset">Újra</button>
  </div>
</div>
<div class="stats">
  <div class="stat"><b id="lln-n"></b><small>kísérletek száma (n)</small></div>
  <div class="stat"><b id="lln-f"></b><small>relatív gyakoriság (k/n)</small></div>
</div>
<script>
(() => {
  const P = window.Plot, $ = id => document.getElementById(id), svg = $('lln-plot');
  let p = 0.5, k = 0, hist = [];
  const x = v => P.scale(0, 4, 60, 705)(Math.log10(v)), y = P.scale(0, 1, 340, 20);
  function draw() {
    svg.replaceChildren();
    for (let v = 0; v <= 1.001; v += 0.25) {
      P.el(svg, 'line', {class: 'grid', x1: 60, x2: 705, y1: y(v), y2: y(v)});
      P.el(svg, 'text', {class: 'tick', x: 52, y: y(v) + 5, 'text-anchor': 'end'}, P.fmt(v, 2));
    }
    [1, 10, 100, 1000, 10000].forEach(v => P.el(svg, 'text', {class: 'tick', x: x(v), y: 366, 'text-anchor': 'middle'}, P.fmt(v)));
    P.el(svg, 'line', {class: 'ref', x1: 60, x2: 705, y1: y(p), y2: y(p), style: 'opacity:1'});
    P.el(svg, 'text', {class: 'label', x: 700, y: y(p) - 8, 'text-anchor': 'end'}, 'P(A) = ' + P.fmt(p, 3));
    if (hist.length) {
      const step = Math.max(1, Math.floor(hist.length / 800));
      let d = '';
      for (let i = 0; i < hist.length; i += step) d += (i ? 'L' : 'M') + x(i + 1).toFixed(1) + ',' + y(hist[i]).toFixed(1);
      d += 'L' + x(hist.length).toFixed(1) + ',' + y(hist[hist.length - 1]).toFixed(1);
      P.el(svg, 'path', {class: 'curve', d});
    }
    P.el(svg, 'line', {class: 'axis', x1: 60, x2: 705, y1: y(0), y2: y(0)});
    $('lln-n').textContent = P.fmt(hist.length);
    $('lln-f').textContent = hist.length ? P.fmt(hist[hist.length - 1], 3) : '–';
  }
  function add(m) {
    for (let i = 0; i < m && hist.length < 10000; i++) {
      if (Math.random() < p) k++;
      hist.push(k / (hist.length + 1));
    }
    draw();
  }
  ['10', '100', '1000'].forEach(m => $('lln-' + m).onclick = () => add(+m));
  $('lln-reset').onclick = () => { k = 0; hist = []; draw(); };
  P.seg('lln-ev', ds => { p = +ds.p; k = 0; hist = []; draw(); });
  draw();
})();
</script>
```

A vízszintes tengely logaritmikus. Legfeljebb 10 000 kísérlet.
:::
::::

::: {.notes}
Az első néhány dobásnál a relatív gyakoriság nagyon ingadozik – ezt mutatja a kis számok törvénye is (1. rész). Több ezer kísérlet után már alig tér el a valószínűségtől: ez a nagy számok törvénye.
:::

## A Kolmogorov-féle axiómák

A valószínűség elmélete néhány **axiómára** épül [(Kolmogorov, 1933)]{.cite}:

1. $0 \le P(A) \le 1$
2. $P(\emptyset) = 0$ és $P(\Omega) = 1$
3. Ha $A \cap B = \emptyset$, akkor $P(A \cup B) = P(A) + P(B)$
4. Általánosabban: páronként kizáró $A_1, A_2, \ldots, A_n$ eseményekre $P(A_1 \cup \ldots \cup A_n) = P(A_1) + \ldots + P(A_n)$

::: {.callout-note}
Az axiómák nem mondják meg, **mit jelent** a valószínűség – csak azt, hogyan számoljunk vele.
:::

## Az axiómák következményei {.smaller}

a) Ha $A \subseteq B$, akkor $P(A) \le P(B)$

b) **Összeadási tétel** két eseményre: $P(A \cup B) = P(A) + P(B) - P(A \cap B)$

c) Három eseményre: $P(A \cup B \cup C) = P(A) + P(B) + P(C) - P(A \cap B) - P(A \cap C) - P(B \cap C) + P(A \cap B \cap C)$

d) Teljes eseményrendszerre: $P(B_1) + P(B_2) + \ldots + P(B_n) = 1$

e) Ellentett eseményre: $P(A) + P(\overline{A}) = 1$, azaz $P(\overline{A}) = 1 - P(A)$

::: {.callout-tip}
Az (a) pontból: $P(A \cap B) \le P(A)$ – az együttes bekövetkezés sosem valószínűbb. Az intuíció ezt gyakran megsérti (konjunkciós hiba).
:::

## A valószínűség értelmezései {.smaller}

| Értelmezés | Mit jelent $P(A)$? | Példa |
|:--|:--|:--|
| **Klasszikus** (Laplace) | kedvező / összes eset, egyenlően valószínű kimenetelek mellett | kockadobás, kártyahúzás |
| **Gyakorisági** (frekventista) | a relatív gyakoriság határértéke sok ismétlés esetén | hibaarány, $p$-érték, konfidenciaintervallum |
| **Szubjektív, bayesi** | egy állítás hihetőségének mértéke a rendelkezésre álló információ alapján | diagnózis valószínűsége, Bayes-faktor |

- A pszichológiai statisztika hagyományosan **gyakorisági** szemléletű ($p$-érték, szignifikancia)
- A **bayesi** megközelítés a hipotézisek valószínűségét az adatok fényében frissíti; ingyenes programokban (pl. JASP) is elérhető [(Etz & Vandekerckhove, 2018)]{.cite}

## Példa: megjelenés egy vizsgálaton {.smaller}

:::: {.columns}
::: {.column width="40%"}
Egy laborvizsgálat 1000 időpontjának kimenetele (példaadatok):

| Érkezés | Gyakoriság |
|:--|--:|
| korábban | 100 |
| időben | 800 |
| később | 75 |
| nem jelent meg | 25 |
| **Összesen** | **1000** |
:::

::: {.column width="60%"}
- $A$: korábban érkezik, $P(A) = 100/1000 = 0{,}1$
- $B$: később érkezik, $P(B) = 75/1000 = 0{,}075$
- $A$ és $B$ kizárják egymást, ezért annak valószínűsége, hogy **nem pontosan** érkezik (de megjelenik):

$$P(A \cup B) = 0{,}1 + 0{,}075 = 0{,}175$$

- Ellentett eseménnyel: $C$ = időben, $D$ = nem jelent meg; $A \cup B = \overline{C \cup D}$, így $P(A \cup B) = 1 - (0{,}8 + 0{,}025) = 0{,}175$
:::
::::

# Valószínűségi mezők

## Valószínűségi mező

- Legyen $\Omega = \{A_1, A_2, \ldots, A_n\}$ teljes eseményrendszer, és ismerjük a $p_i = P(A_i)$ valószínűségeket
- Az események a hozzájuk tartozó valószínűségekkel együtt a **valószínűségi mező**
- Egy összetett esemény valószínűsége az őt alkotó elemi események valószínűségeinek **összege**

::: {.callout-note}
## Példa: három érme, a fejek száma
$\Omega = \{0, 1, 2, 3\}$, $\quad p_0 = 1/8$, $p_1 = 3/8$, $p_2 = 3/8$, $p_3 = 1/8$

Legalább egy fej: $3/8 + 3/8 + 1/8 = 7/8$, vagy egyszerűbben $1 - p_0 = 7/8$
:::

## Klasszikus valószínűségi mező

Ha a véges $\Omega$ eseménytér $n$ elemi eseménye **egyenlően valószínű** (mindegyik $1/n$), akkor egy $k$ elemi eseményből álló $A$ esemény valószínűsége:

$$P(A) = \frac{k}{n} = \frac{\text{kedvező esetek száma}}{\text{összes eset száma}}$$

::: {.callout-tip}
## Kombinatorikai segédeszköz
$n$ elemből $k$ elem **sorrend nélküli** kiválasztásainak száma a binomiális együttható:

$$\binom{n}{k} = \frac{n!}{k!\,(n-k)!}, \qquad \text{pl. } \binom{20}{3} = \frac{20 \cdot 19 \cdot 18}{3 \cdot 2 \cdot 1} = 1140$$
:::

## Példa: magyar kártya

A 32 lapos magyar kártyából egy lapot húzunk. $A$: piros lapot húzunk; $B$: számos lapot (VII–X) húzunk.

:::: {.columns}
::: {.column}
- $P(A) = \dfrac{8}{32} = \dfrac{1}{4}$
- $P(B) = \dfrac{16}{32} = \dfrac{1}{2}$
- $P(A \cap B) = \dfrac{4}{32} = \dfrac{1}{8}$
:::

::: {.column}
::: {.callout-note}
Vegyük észre: $P(A \cap B) = \frac{1}{8} = \frac{1}{4} \cdot \frac{1}{2} = P(A)\,P(B)$. A két esemény tehát **független** – erről később lesz szó.
:::
:::
::::

## Példa: visszatevés nélküli mintavétel {.smaller}

Egy dobozban 20 csavar van, közülük 6 hibás. Hármat véletlenszerűen kiválasztunk. Mennyi a valószínűsége, hogy **mindhárom** hibás ($A$), illetve hogy **egyik sem** ($B$)?

- Az összes eset: $\binom{20}{3} = 1140$
- $A$ kedvező esetei: $\binom{6}{3} = 20$ $\quad\Rightarrow\quad P(A) = \dfrac{20}{1140} = \dfrac{1}{57} \approx 0{,}018$
- $B$ kedvező esetei: $\binom{14}{3} = 364$ $\quad\Rightarrow\quad P(B) = \dfrac{364}{1140} = \dfrac{91}{285} \approx 0{,}319$

::: {.callout-tip}
Pszichológiai megfelelő: egy 20 fős csoportból, amelyben 6 fő szorongásos tüneteket mutat, 3 főt választunk ki egy interjúra. Ugyanez a számítás adja meg, mennyi az esélye, hogy egyikük sem, illetve mindegyikük tünetes.
:::

## Próbálja ki: visszatevés nélküli mintavétel

:::: {.columns}
::: {.column width="58%"}
```{=html}
<div class="widget"><svg id="hg-plot" viewBox="0 0 680 380" role="img" aria-label="A kiválasztott hibás elemek számának valószínűségei"></svg></div>
```
:::

::: {.column width="42%"}
```{=html}
<div class="controls">
  <label><span>Összes elem: N = <output id="hg-N-o"></output></span><input id="hg-N" type="range" min="5" max="40" step="1" value="20"></label>
  <label><span>Ebből hibás: K = <output id="hg-K-o"></output></span><input id="hg-K" type="range" min="0" max="40" step="1" value="6"></label>
  <label><span>Kiválasztott: n = <output id="hg-n-o"></output></span><input id="hg-n" type="range" min="1" max="10" step="1" value="3"></label>
</div>
<div class="grid" style="--cols:3;gap:8px;margin-top:12px">
  <div class="stat"><b id="hg-0" style="font-size:22px"></b><small>egyik sem hibás</small></div>
  <div class="stat"><b id="hg-1" style="font-size:22px"></b><small>legalább egy hibás</small></div>
  <div class="stat"><b id="hg-a" style="font-size:22px"></b><small>mind hibás</small></div>
</div>
<script>
(() => {
  const P = window.Plot, $ = id => document.getElementById(id), svg = $('hg-plot');
  const C = (n, k) => { if (k < 0 || k > n) return 0; let r = 1; for (let i = 1; i <= k; i++) r = r * (n - k + i) / i; return r; };
  function draw() {
    const N = +$('hg-N').value;
    $('hg-K').max = N; $('hg-n').max = Math.min(10, N);
    const K = Math.min(+$('hg-K').value, N), n = Math.min(+$('hg-n').value, N);
    const p = Array.from({length: n + 1}, (_, k) => C(K, k) * C(N - K, n - k) / C(N, n));
    const x = P.scale(-0.5, 10.5, 60, 670), y = P.scale(0, 1, 330, 20), w = (x(1) - x(0)) * 0.7;
    svg.replaceChildren();
    for (let v = 0; v <= 1.001; v += 0.25) {
      P.el(svg, 'line', {class: 'grid', x1: 60, x2: 670, y1: y(v), y2: y(v)});
      P.el(svg, 'text', {class: 'tick', x: 52, y: y(v) + 5, 'text-anchor': 'end'}, P.fmt(v, 2));
    }
    p.forEach((v, k) => {
      P.el(svg, 'rect', {class: 'bar', x: x(k) - w / 2, width: w, y: y(v), height: y(0) - y(v)});
      if (v > 0.0005) P.el(svg, 'text', {class: 'tick', x: x(k), y: y(v) - 6, 'text-anchor': 'middle'}, P.fmt(v, 3));
      P.el(svg, 'text', {class: 'tick', x: x(k), y: 352, 'text-anchor': 'middle'}, k);
    });
    P.el(svg, 'text', {class: 'tick', x: 365, y: 376, 'text-anchor': 'middle'}, 'hibás elemek száma a kiválasztottak között');
    P.el(svg, 'line', {class: 'axis', x1: 60, x2: 670, y1: y(0), y2: y(0)});
    $('hg-N-o').value = N; $('hg-K-o').value = K; $('hg-n-o').value = n;
    $('hg-0').textContent = P.fmt(p[0], 3);
    $('hg-1').textContent = P.fmt(1 - p[0], 3);
    $('hg-a').textContent = P.fmt(p[n], 3);
  }
  ['hg-N', 'hg-K', 'hg-n'].forEach(id => $(id).oninput = draw);
  draw();
})();
</script>
```

$P(X = k) = \dfrac{\binom{K}{k}\binom{N-K}{n-k}}{\binom{N}{n}}$
:::
::::

## Feladatok (1) {.smaller}

1. Egy dobozban 12 tranzisztor van, közülük 4 hibás. Kettőt kiveszünk. Mennyi a valószínűsége, hogy
   - mindkettő hibás? [$\binom{4}{2} / \binom{12}{2} = 6/66 = 1/11$]{.fragment}
   - egyik sem hibás? [$\binom{8}{2} / \binom{12}{2} = 28/66 = 14/33$]{.fragment}
   - legalább az egyik hibás? [$1 - 14/33 = 19/33$]{.fragment}
2. Egy rekeszben 20 nő és 10 férfi adatlapja van; mindkét nemnél a személyek fele pszichológus. Egy lapot kiveszünk. Mennyi a valószínűsége, hogy
   - férfié ($A$)? [$10/30 = 1/3$]{.fragment}
   - pszichológusé ($B$)? [$15/30 = 1/2$]{.fragment}
   - férfié vagy pszichológusé? [$P(A) + P(B) - P(A \cap B) = 1/3 + 1/2 - 5/30 = 2/3$]{.fragment}

## Feladatok (2) {.smaller}

3. Egy úszómedencénél 8 rajtkő van, 6 úszó indul, a rajtköveket kisorsolják. Mennyi a valószínűsége, hogy a 3-as kőről nem indul senki? [$\binom{7}{6} / \binom{8}{6} = 7/28 = 1/4$]{.fragment}
4. Egy 52 lapos kártyacsomagból 13 lapot húzunk. Mennyi a valószínűsége, hogy a treff király köztük van? [$\binom{51}{12} / \binom{52}{13} = 13/52 = 1/4$]{.fragment}
5. Két szabályos kockával dobunk. Mennyi a valószínűsége, hogy a pontok összege legalább 10, ha
   - az első kockán ötös van? [a második kockán 5 vagy 6 kell: $2/6 = 1/3$]{.fragment}
   - legalább az egyik kockán ötös van? [11 ilyen kimenetel van, ebből 3 jó: $(5,5), (5,6), (6,5)$, így $3/11$]{.fragment}

::: {.notes}
Az 5. feladat már feltételes valószínűség – átvezet a következő témához.
:::

# Feltételes valószínűség

## Feltételes valószínűség

Annak valószínűsége, hogy $A$ bekövetkezik, **ha tudjuk**, hogy $B$ bekövetkezett:

$$P(A \mid B) = \frac{P(A \cap B)}{P(B)}, \qquad P(B) \neq 0$$

::: {.callout-note}
## Példa: felhős és esős napok
$A$: esik, $B$: felhős. A napok 30%-a felhős, 10%-a felhős és esős: $P(B) = 0{,}3$, $P(A \cap B) = 0{,}1$. Ha reggel felhős az ég:

$$P(A \mid B) = \frac{0{,}1}{0{,}3} = \frac{1}{3}$$

– a józan ész is ezt mondja: a felhős napok harmada esős.
:::

## Példa: hallgatók egy karon {.smaller}

:::: {.columns}
::: {.column width="52%"}
| Szak | Férfi | Nő | Összes |
|:--|--:|--:|--:|
| Könyvelés | 120 | 80 | 200 |
| Pénzügy | 110 | 70 | 180 |
| Marketing | 70 | 50 | 120 |
| Vezetéstudomány | 110 | 100 | 210 |
| Statisztika | 50 | 10 | 60 |
| Informatika | 140 | 90 | 230 |
| **Összesen** | **600** | **400** | **1000** |
:::

::: {.column width="48%"}
$K$: könyvelés szakos, $N$: nő.

- Könyvelés szakos nő: $P(K \cap N) = 80/1000 = 0{,}08$
- Nő: $P(N) = 400/1000 = 0{,}4$
- Ha tudjuk, hogy nőt választottunk, mennyi a valószínűsége, hogy könyvelés szakos?

$$P(K \mid N) = \frac{0{,}08}{0{,}4} = 0{,}2$$

Ez egyszerűen: 80 nő a 400-ból.
:::
::::

## Példa: két kocka

Két szabályos kockával dobunk. $B$: a pontok összege 6; $A$: legalább az egyik kockán kettes van.

- $B = \{(1,5), (2,4), (3,3), (4,2), (5,1)\}$, tehát $P(B) = 5/36$
- $A \cap B = \{(2,4), (4,2)\}$, tehát $P(A \cap B) = 2/36$

$$P(A \mid B) = \frac{2/36}{5/36} = \frac{2}{5}$$

::: {.callout-tip}
A feltétel **leszűkíti az eseményteret**: $B$ bekövetkezése után már csak $B$ öt kimenetele lehetséges, ezekből kettő kedvező.
:::

## Szorzási tétel

A definíció átrendezésével:

$$P(A \cap B) = P(A \mid B)\,P(B)$$

Több eseményre (láncszabály):

$$P(A_1 \cap \ldots \cap A_n) = P(A_1)\,P(A_2 \mid A_1) \cdots P(A_n \mid A_1 \cap \ldots \cap A_{n-1})$$

::: {.callout-note}
## Példa: golyók visszatevés nélkül
5 fehér és 5 piros golyóból kétszer fehéret húztunk. Annak valószínűsége, hogy harmadikra is fehéret húzunk: a dobozban 3 fehér és 5 piros maradt, így $P = 3/8$.
:::

## Példa: érkezési sorrend {.smaller}

Egy fogadásra 5 lengyel, 8 román és 3 bolgár diplomata érkezik egyenként, véletlen sorrendben. Mennyi a valószínűsége, hogy elsőnek lengyel ($A_1$), másodiknak román ($A_2$), harmadiknak bolgár ($A_3$) érkezik?

- $P(A_1) = 5/16$ (16 vendégből 5 lengyel)
- $P(A_2 \mid A_1) = 8/15$ (a maradék 15-ből 8 román)
- $P(A_3 \mid A_1 \cap A_2) = 3/14$ (a maradék 14-ből 3 bolgár)

$$P(A_1 \cap A_2 \cap A_3) = \frac{5}{16} \cdot \frac{8}{15} \cdot \frac{3}{14} = \frac{1}{28} \approx 0{,}036$$

## Vigyázat: P(A | B) ≠ P(B | A)

- A feltételes valószínűség **nem szimmetrikus**: $P(A \mid B)$ és $P(B \mid A)$ általában különbözik
- *Példa:* a hallgatói táblázatban $P(K \mid N) = 0{,}2$, de $P(N \mid K) = 80/200 = 0{,}4$
- Diagnosztika: $P(\text{pozitív teszt} \mid \text{depresszió})$ – a teszt érzékenysége – **nem azonos** $P(\text{depresszió} \mid \text{pozitív teszt})$-tel

::: {.callout-important}
## A $p$-érték is feltételes valószínűség
$p = P(\text{legalább ilyen szélsőséges adat} \mid H_0)$ – ez **nem** $P(H_0 \mid \text{adat})$. A kettő összekeverése a statisztika egyik leggyakoribb félreértése [(Cohen, 1994)]{.cite}.
:::

# Teljes valószínűség és Bayes-tétel

## A teljes valószínűség tétele

Ha $B_1, B_2, \ldots, B_n$ teljes eseményrendszer és $P(B_i) \neq 0$, akkor bármely $A$ eseményre:

$$P(A) = \sum_{i=1}^{n} P(A \mid B_i)\,P(B_i)$$

- Alapja: $A = (A \cap B_1) \cup \ldots \cup (A \cap B_n)$, és ezek páronként kizárják egymást
- Szemléletesen: $A$ valószínűsége a különböző „utak” valószínűségeinek **súlyozott átlaga**

## Bayes tétele

Ha $B_1, \ldots, B_n$ teljes eseményrendszer, $P(B_i) \neq 0$ és $P(A) \neq 0$, akkor:

$$P(B_k \mid A) = \frac{P(A \mid B_k)\,P(B_k)}{\sum_{i=1}^{n} P(A \mid B_i)\,P(B_i)}$$

:::: {.columns}
::: {.column}
- $P(B_k)$: **előzetes** (a priori) valószínűség
- $P(A \mid B_k)$: az adat **valószínűsége** az egyes feltevések mellett
- $P(B_k \mid A)$: **utólagos** (a posteriori) valószínűség
:::

::: {.column}
::: {.callout-note}
Thomas Bayes tiszteletes eredménye halála után, 1763-ban jelent meg [(Bayes, 1763)]{.cite}. A tétel azt írja le, hogyan **frissítsük** meggyőződésünket új adatok fényében.
:::
:::
::::

## Példa: selejtes alkatrész {.smaller}

| Gép | Termelési arány $P(G_i)$ | Selejtarány $P(S \mid G_i)$ | $P(S \mid G_i)\,P(G_i)$ |
|:--|--:|--:|--:|
| $G_1$ | 0,50 | 0,03 | 0,015 |
| $G_2$ | 0,30 | 0,04 | 0,012 |
| $G_3$ | 0,20 | 0,05 | 0,010 |
| **Összesen** | **1** | | **0,037** |

a) Mennyi a valószínűsége, hogy egy véletlenül kiválasztott alkatrész selejtes? [Teljes valószínűség tétele: $P(S) = 0{,}015 + 0{,}012 + 0{,}010 = 0{,}037$]{.fragment}

b) Ha az alkatrész selejtes, mennyi a valószínűsége, hogy a $G_1$ gépen készült? [Bayes-tétel: $P(G_1 \mid S) = 0{,}015 / 0{,}037 \approx 0{,}405$]{.fragment}

::: {.notes}
Bár a G1 gép selejtaránya a legkisebb, a selejtes alkatrészek 40%-a mégis tőle származik – mert ő gyártja a legtöbbet. Az előzetes valószínűség (alapgyakoriság) számít!
:::

## Példa: alultöltött palackok

Egy borászat két üzemben palackoz. Az **A** üzem adja a termelés 55%-át 3%-os alultöltési aránnyal, a **B** üzem 45%-át 4%-kal. Egy reklamált palack alultöltött ($U$). Mennyi a valószínűsége, hogy az A üzemben töltötték?

$$P(A \mid U) = \frac{0{,}55 \cdot 0{,}03}{0{,}55 \cdot 0{,}03 + 0{,}45 \cdot 0{,}04} = \frac{0{,}0165}{0{,}0345} \approx 0{,}478$$

::: {.callout-tip}
A Bayes-tételt **döntési fával** is levezethetjük: az első elágazás az üzem (55% / 45%), a második az alultöltés. Az alultöltött ágak valószínűségeit összeadjuk, és a kérdéses ág arányát vesszük.
:::

## Bayes a pszichológiában: az alapgyakoriság {.smaller}

- **Alapgyakoriság elhanyagolása:** ítéleteinkben gyakran figyelmen kívül hagyjuk az előzetes valószínűséget [(Kahneman & Tversky, 1973)]{.cite}
- Orvosok és orvostanhallgatók többsége **súlyosan túlbecsülte** egy pozitív laboreredmény jelentőségét [(Casscells és mtsai, 1978)]{.cite}
- **Természetes gyakoriságokkal** („1000 emberből 50…”) a bayesi következtetés sokkal könnyebb [(Gigerenzer & Hoffrage, 1995)]{.cite}

::: {.callout-important}
## Szűrőteszt példa
A PHQ-9 depressziókérdőív 10 pontos határértéknél kb. 88%-os **érzékenységű** és **specificitású** [(Kroenke és mtsai, 2001)]{.cite}. Ha a depresszió gyakorisága 5%, mennyi az esélye, hogy egy pozitív eredményű személy valóban depressziós? [Csak kb. **28%**!]{.fragment}
:::

## Próbálja ki: pozitív szűrőteszt

:::: {.columns}
::: {.column width="58%"}
```{=html}
<div class="widget">
  <svg id="by-plot" viewBox="0 0 680 430" role="img" aria-label="1000 személy ikonos ábrája a szűrőteszt eredménye szerint"></svg>
  <div class="legend" style="flex-wrap:wrap;gap:6px 16px;margin-left:8px">
    <span><i style="border-top:10px solid var(--accent-2);width:12px"></i>depressziós, pozitív</span>
    <span><i style="border-top:10px solid var(--warn);width:12px"></i>depressziós, negatív</span>
    <span><i style="border-top:10px solid var(--accent);width:12px"></i>nem depressziós, pozitív</span>
    <span><i style="border-top:10px solid var(--line);width:12px"></i>nem depressziós, negatív</span>
  </div>
</div>
```
:::

::: {.column width="42%"}
```{=html}
<div class="controls" style="gap:8px;font-size:19px">
  <label><span>Gyakoriság (alapráta): <output id="by-p-o"></output></span><input id="by-p" type="range" min="1" max="50" step="1" value="5"></label>
  <label><span>Érzékenység: <output id="by-se-o"></output></span><input id="by-se" type="range" min="50" max="99" step="1" value="88"></label>
  <label><span>Specificitás: <output id="by-sp-o"></output></span><input id="by-sp" type="range" min="50" max="99" step="1" value="88"></label>
</div>
<div class="stats" style="margin-top:10px">
  <div class="stat"><b id="by-ppv"></b><small>P(depressziós | pozitív)</small></div>
  <div class="stat"><b id="by-npv"></b><small>P(nem depressziós | negatív)</small></div>
</div>
<p id="by-txt" style="font-size:17px;line-height:1.35;margin-top:10px"></p>
<script>
(() => {
  const P = window.Plot, $ = id => document.getElementById(id), svg = $('by-plot');
  function draw() {
    const prev = +$('by-p').value / 100, se = +$('by-se').value / 100, sp = +$('by-sp').value / 100;
    const sick = Math.round(1000 * prev), tp = Math.round(sick * se), fn = sick - tp;
    const healthy = 1000 - sick, fp = Math.round(healthy * (1 - sp)), tn = healthy - fp;
    const cols = ['var(--accent-2)', 'var(--warn)', 'var(--accent)', 'var(--line)'], counts = [tp, fn, fp, tn];
    svg.replaceChildren();
    let i = 0;
    counts.forEach((c, g) => {
      for (let j = 0; j < c; j++, i++) {
        const r = Math.floor(i / 40), q = i % 40;
        P.el(svg, 'circle', {cx: 12 + q * 16.7, cy: 12 + r * 16.7, r: 6.3, style: `fill:${cols[g]}`});
      }
    });
    const ppv = prev * se / (prev * se + (1 - prev) * (1 - sp)), npv = (1 - prev) * sp / ((1 - prev) * sp + prev * (1 - se));
    $('by-p-o').value = P.fmt(prev * 100) + '%';
    $('by-se-o').value = P.fmt(se * 100) + '%';
    $('by-sp-o').value = P.fmt(sp * 100) + '%';
    $('by-ppv').textContent = P.fmt(ppv * 100, 1) + '%';
    $('by-npv').textContent = P.fmt(npv * 100, 1) + '%';
    $('by-txt').textContent = `1000 főből ${sick} depressziós, közülük ${tp} pozitív. ${healthy} nem depressziós, közülük ${fp} mégis pozitív. ` +
      `A ${tp + fp} pozitív eredményből tehát csak ${tp} valódi: ${tp}/${tp + fp}.`;
  }
  ['by-p', 'by-se', 'by-sp'].forEach(id => $(id).oninput = draw);
  draw();
})();
</script>
```
:::
::::

::: {.notes}
Állítsuk az alaprátát 30%-ra (pl. pszichiátriai járóbeteg-ellátás): ugyanaz a teszt ekkor sokkal megbízhatóbb pozitív eredményt ad. A teszt „jósága” a populációtól függ!
:::

# Függetlenség

## Események függetlensége

$A$ és $B$ **független**, ha egyikük bekövetkezése nem befolyásolja a másik valószínűségét:

$$P(A \cap B) = P(A)\,P(B)$$

Ha $P(B) \neq 0$, ez azzal egyenértékű, hogy $P(A \mid B) = P(A)$.

::: {.callout-note}
## Példa
A 10 évnél fiatalabb gyermeket nevelő anyák 60%-a teljes munkaidőben dolgozik. Két anyát függetlenül kiválasztva:

- mindkettő teljes munkaidős: $0{,}6 \cdot 0{,}6 = 0{,}36$
- legalább az egyik: $1 - 0{,}4 \cdot 0{,}4 = 0{,}84$
:::

## Kizáró vagy független? {.smaller}

:::: {.columns}
::: {.column}
::: {.callout-tip}
## Kölcsönösen kizáró
Az egyik bekövetkezése **lehetetlenné teszi** a másikat: $A \cap B = \emptyset$.

**Összeadási szabály** – *legalább az egyik* bekövetkezésére:

$P(A \cup B) = P(A) + P(B)$
:::
:::

::: {.column}
::: {.callout-note}
## Független
Az egyik bekövetkezése **nem változtat** a másik esélyén.

**Szorzási szabály** – *mindkettő* bekövetkezésére:

$P(A \cap B) = P(A)\,P(B)$
:::
:::
::::

::: {.callout-warning}
A kettő **nem** ugyanaz: két pozitív valószínűségű kizáró esemény sosem független, hiszen $P(A \cap B) = 0 \neq P(A)\,P(B)$.
:::

## Példák: összeadni vagy szorozni? {.smaller}

Hatszor dobunk egy kockával; megkeverünk egy 52 lapos kártyacsomagot.

a) Az első **vagy** az utolsó dobás 1-es. [Nem kizáró események, ezért az általános összeadási tétel kell: $1/6 + 1/6 - 1/36 = 11/36$]{.fragment}

b) Az első **és** az utolsó dobás is 1-es. [Független események, szorozhatunk: $1/6 \cdot 1/6 = 1/36$]{.fragment}

c) A felső **vagy** az alsó kártya a pikk ász. [Kizáró események, összeadhatunk: $1/52 + 1/52 = 2/52$]{.fragment}

d) A felső **és** az alsó kártya is a pikk ász. [Kizáró, tehát nem független események – nem szorozhatunk: $P = 1/52 \cdot 0 = 0$]{.fragment}

# A véletlen és az intuíció

## Valószínűségi ítéletek és torzítások {.smaller}

- **Szerencsejátékos-tévedés:** sok „piros” után a „fekete” esélyét nagyobbnak gondoljuk – pedig a pörgetések függetlenek [(Tversky & Kahneman, 1974)]{.cite}
- **Konjunkciós hiba:** a „Linda-problémában” a többség valószínűbbnek ítélte, hogy Linda „banki ügyintéző **és** feminista”, mint hogy „banki ügyintéző” – pedig $P(A \cap B) \le P(A)$ [(Tversky & Kahneman, 1983)]{.cite}
- **Alapgyakoriság elhanyagolása:** lásd a szűrőteszt példáját
- **Monty Hall-probléma:** a legtöbben nem váltanak ajtót, pedig váltással kétszer akkora a nyerési esély [(Krauss & Wang, 2003)]{.cite}

::: {.notes}
A valószínűség-számítás nemcsak a statisztika eszköze, hanem mérce is: ehhez viszonyítva vizsgálja a kognitív pszichológia az emberi ítéletalkotást.
:::

## Próbálja ki: Monty Hall

:::: {.columns}
::: {.column width="55%"}
Három ajtó közül az egyik mögött autó, a másik kettő mögött kecske van. Ön választ egy ajtót; a műsorvezető – aki tudja, hol az autó – kinyit egy **másik**, kecskés ajtót. Vált vagy marad?

```{=html}
<div class="widget">
  <div class="grid" style="--cols:3" id="mh-doors">
    <button class="btn" data-d="0" style="height:110px;font-size:28px;border-radius:14px">1</button>
    <button class="btn" data-d="1" style="height:110px;font-size:28px;border-radius:14px">2</button>
    <button class="btn" data-d="2" style="height:110px;font-size:28px;border-radius:14px">3</button>
  </div>
  <p id="mh-msg" style="margin:6px 0 4px;font-size:21px"></p>
  <div style="display:flex;gap:8px"><button class="btn" id="mh-stay" hidden>Maradok</button><button class="btn" id="mh-switch" hidden>Váltok</button><button class="btn" id="mh-again" hidden>Új játék</button></div>
</div>
```
:::

::: {.column width="45%"}
```{=html}
<div class="stats">
  <div class="stat"><b id="mh-s"></b><small>nyerési arány maradással</small></div>
  <div class="stat"><b id="mh-w"></b><small>nyerési arány váltással</small></div>
</div>
<p style="margin-top:12px"><button class="btn" id="mh-sim">+1000 szimulált játék mindkét stratégiával</button></p>
<script>
(() => {
  const $ = id => document.getElementById(id), P = window.Plot, doors = [...$('mh-doors').children];
  const st = {stay: [0, 0], sw: [0, 0]};
  let car, pick, opened, phase;
  const label = (d, t) => { doors[d].textContent = t; };
  function reset() {
    car = Math.floor(Math.random() * 3); pick = opened = null; phase = 'pick';
    doors.forEach((b, i) => { b.disabled = false; b.classList.remove('on'); label(i, i + 1); });
    $('mh-msg').textContent = 'Válasszon egy ajtót!';
    ['mh-stay', 'mh-switch', 'mh-again'].forEach(id => $(id).hidden = true);
  }
  function stats() {
    const f = ([w, n]) => n ? P.fmt(w / n * 100, 1) + '% (' + n + ')' : '–';
    $('mh-s').textContent = f(st.stay);
    $('mh-w').textContent = f(st.sw);
  }
  $('mh-doors').onclick = e => {
    const b = e.target.closest('button');
    if (!b || phase !== 'pick') return;
    pick = +b.dataset.d;
    const goats = [0, 1, 2].filter(d => d !== pick && d !== car);
    opened = goats[Math.floor(Math.random() * goats.length)];
    doors[pick].classList.add('on');
    doors[opened].disabled = true; label(opened, '🐐');
    $('mh-msg').textContent = `A műsorvezető kinyitotta a(z) ${opened + 1}. ajtót: kecske. Marad a(z) ${pick + 1}. ajtónál, vagy vált?`;
    $('mh-stay').hidden = $('mh-switch').hidden = false;
    phase = 'decide';
  };
  function finish(sw) {
    const final = sw ? [0, 1, 2].find(d => d !== pick && d !== opened) : pick, win = final === car;
    const s = sw ? st.sw : st.stay;
    s[0] += win; s[1]++;
    doors.forEach((b, i) => { b.disabled = true; label(i, i === car ? '🚗' : '🐐'); b.classList.toggle('on', i === final); });
    $('mh-msg').textContent = win ? 'Nyert! 🚗' : 'Kecske… 🐐';
    $('mh-stay').hidden = $('mh-switch').hidden = true; $('mh-again').hidden = false;
    phase = 'done'; stats();
  }
  $('mh-stay').onclick = () => finish(false);
  $('mh-switch').onclick = () => finish(true);
  $('mh-again').onclick = reset;
  $('mh-sim').onclick = () => {
    for (let i = 0; i < 1000; i++) {
      const c = Math.floor(Math.random() * 3), p = Math.floor(Math.random() * 3);
      st.stay[0] += c === p; st.stay[1]++;
      st.sw[0] += c !== p; st.sw[1]++;
    }
    stats();
  };
  reset(); stats();
})();
</script>
```

::: {.callout-note}
Maradással csak akkor nyerünk, ha elsőre eltaláltuk az autót: $1/3$. Váltással minden más esetben: $2/3$.
:::
:::
::::

## Összefoglalás {.inverse .center}

- Az **eseménytér** a lehetséges kimenetelek halmaza, az **esemény** ennek részhalmaza
- Eseményműveletek: **unió** (legalább egyik), **metszet** (mindkettő), különbség, ellentett
- A valószínűség **Kolmogorov axiómáira** épül; értelmezése lehet klasszikus, gyakorisági vagy bayesi
- **Feltételes valószínűség:** $P(A \mid B) = P(A \cap B) / P(B)$ – és $P(A \mid B) \neq P(B \mid A)$
- A **Bayes-tétel** az alapgyakoriságot is figyelembe veszi – az intuíció gyakran nem
- **Kizáró** esemény: összeadunk; **független** esemény: szorzunk

## Irodalom (1/2) {.smaller}

::: {.refs}
Bayes, T. (1763). An essay towards solving a problem in the doctrine of chances. *Philosophical Transactions of the Royal Society of London, 53*, 370–418.

Casscells, W., Schoenberger, A., & Graboys, T. B. (1978). Interpretation by physicians of clinical laboratory results. *New England Journal of Medicine, 299*(18), 999–1001. https://doi.org/10.1056/NEJM197811022991808

Cohen, J. (1994). The earth is round (p < .05). *American Psychologist, 49*(12), 997–1003.

Etz, A., & Vandekerckhove, J. (2018). Introduction to Bayesian inference for psychology. *Psychonomic Bulletin & Review, 25*(1), 5–34. https://doi.org/10.3758/s13423-017-1262-3

Gigerenzer, G., & Hoffrage, U. (1995). How to improve Bayesian reasoning without instruction: Frequency formats. *Psychological Review, 102*(4), 684–704.

Kahneman, D., & Tversky, A. (1973). On the psychology of prediction. *Psychological Review, 80*(4), 237–251.

Kolmogorov, A. N. (1933). *Grundbegriffe der Wahrscheinlichkeitsrechnung.* Springer.
:::

## Irodalom (2/2) {.smaller}

::: {.refs}
Krauss, S., & Wang, X. T. (2003). The psychology of the Monty Hall problem: Discovering psychological mechanisms for solving a tenacious brain teaser. *Journal of Experimental Psychology: General, 132*(1), 3–22. https://doi.org/10.1037/0096-3445.132.1.3

Kroenke, K., Spitzer, R. L., & Williams, J. B. W. (2001). The PHQ-9: Validity of a brief depression severity measure. *Journal of General Internal Medicine, 16*(9), 606–613.

Tversky, A., & Kahneman, D. (1974). Judgment under uncertainty: Heuristics and biases. *Science, 185*(4157), 1124–1131.

Tversky, A., & Kahneman, D. (1983). Extensional versus intuitive reasoning: The conjunction fallacy in probability judgment. *Psychological Review, 90*(4), 293–315.

**Magyar nyelvű tankönyv:** Vargha A. (2000). *Matematikai statisztika pszichológiai, nyelvészeti és biológiai alkalmazásokkal.* Pólya Kiadó.
:::

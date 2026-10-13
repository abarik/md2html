---
title: "Statisztikai alapfogalmak"
subtitle: "Populáció és minta, változók, mérési skálák"
author: "Abari Kálmán"
date: "2026. ősz"
lang: hu
footer: "Matematikai alapok II. · 2. Statisztikai alapfogalmak"
---

## Mi a statisztika?

A statisztika az a tudomány, amely **adatok** gyűjtésével, rendszerezésével, összegzésével, elemzésével és értelmezésével foglalkozik, hogy a valós életben felmerülő **kérdésekre** választ találjon.

:::: {.columns}
::: {.column}
### Általános kérdések

- Okoz-e tüdőrákot a dohányzás?
- Melyik tanítási módszer a leghatékonyabb?
- Magasabbak-e 10 évesen a lányok, mint a fiúk?
:::

::: {.column}
### Pszichológiai kérdések

- Hatásosabb-e a kognitív terápia a várólistánál?
- Romlik-e a figyelem alvásmegvonás után?
- Különbözik-e a vizsgaszorongás a szakok között?
:::
::::

## Leíró és induktív statisztika

:::: {.columns}
::: {.column}
::: {.callout-note}
## Leíró statisztika
Az összegyűjtött adatok **tömör leírása**: táblázatok, grafikonok, átlagok, szórások. A vizsgált csoporton túl **nem általánosít**.

*Példa:* a népszámlálás 10 millió adatát grafikonok és mutatók teszik áttekinthetővé.
:::
:::

::: {.column}
::: {.callout-tip}
## Induktív (következtető) statisztika
Egy **minta** alapján következtet a **populáció** tulajdonságaira; más néven matematikai statisztika.

*Példa:* tévéműsorok nézettségmérése, választás előtti közvélemény-kutatás.
:::
:::
::::

A következtetés előtt mindig **le kell írni** és **ábrázolni** kell az adatokat – emlékezzünk Anscombe négy adatsorára!

# Populáció és minta

## Populáció és minta {.smaller}

:::: {.columns}
::: {.column width="52%"}
- **Populáció** (alapsokaság): a vizsgálat tárgyát képező egyedek összessége – **paraméterek** jellemzik
- **Minta**: a populációból a vizsgálat céljára kiválasztott egyedek összessége – **statisztikák** írják le
:::

::: {.column width="48%"}
| | Populáció: paraméter | Minta: statisztika |
|:--|:-:|:-:|
| elemszám | $N$ | $n$ |
| átlag | $\mu$ | $\bar{x}$ |
| szórás | $\sigma$ | $s$ |
| korreláció | $\rho$ | $r$ |
| arány | $\pi$ | $\hat{p}$ |

: Görög betű a populáció, latin betű a minta jellemzőire.
:::
::::

## Miért minta? {.smaller}

:::: {.columns}
::: {.column width="50%"}
A teljes populáció vizsgálata

- túl **költséges** és **időigényes**,
- gyakran **nem is érhető el** minden egyed,
- a vizsgálat **károsíthatja** vagy megsemmisítheti az egyedeket.

A mintától elvárjuk, hogy **hűen reprezentálja** a populációt – csak így vonhatunk le helyes következtetést.
:::

::: {.column width="50%"}
::: {.callout-warning}
## A Literary Digest kudarca (1936)
A lap kb. 2,4 millió visszaküldött szavazólap alapján Landon győzelmét jósolta, ám Roosevelt nagy fölénnyel nyert. A torzítást a mintavételi keret (telefon- és autótulajdonosok) és a szelektív válaszadás együtt okozta; Gallup jóval kisebb mintával helyesen jósolt. [(Squire, 1988)]{.cite}
:::

**A minta nagysága nem pótolja a reprezentativitást.**
:::
::::

## Az adatmátrix {.smaller}

Az elemzést az egyedeket leíró **adatmátrixon** (adatmintán) végezzük:

| Azonosító | Nem | Életkor | Végzettség | Szorongás (pont) | Reakcióidő (ms) |
|:--|:--|--:|:--|--:|--:|
| 001 | nő | 21 | középfokú | 42 | 512 |
| 002 | férfi | 23 | felsőfokú | 35 | 468 |
| 003 | nő | 20 | középfokú | 51 | 547 |
| … | … | … | … | … | … |

**Sor** = egy megfigyelési egység (személy), **oszlop** = egy változó, **cella** = egy érték. [(Wickham, 2014)]{.cite}

::: {.notes}
A személyeket név helyett azonosító jelöli – a kutatási adatok védelme alapkövetelmény.
Hívjuk fel a figyelmet: az oszlopok mérési szintje különböző (nem: nominális, végzettség: ordinális, reakcióidő: arányskála) – erről szól a következő rész.
:::

## Változók

- **Statisztikai változó** (ismérv): az egyedeket jellemző, egyedről egyedre változó tulajdonság
- Példák: vérnyomás, IQ, életkor, nem, diagnózis, a percenként kiejtett szótagok száma, reakcióidő
- A pszichológiában a vizsgált tulajdonság gyakran **konstruktum** (pl. szorongás), a változó pedig ennek **operacionalizált** mérése (pl. egy kérdőív összpontszáma)

::: {.callout-note}
Ugyanaz a konstruktum többféleképpen mérhető: a szorongás lehet kérdőívpontszám, szívfrekvencia vagy klinikai besorolás – és ezek **mérési szintje is különbözhet**.
:::

# Mérés és mérési skálák

## Mérés

- A **statisztikai adat** mérés vagy számlálás útján keletkező tapasztalati érték
- **Mérés**: számok hozzárendelése tárgyakhoz vagy eseményekhez meghatározott **szabályok** szerint; a szabályok határozzák meg a **mérési skálát** [(Stevens, 1946)]{.cite}

:::: {.columns}
::: {.column}
::: {.callout-note}
## Mérhető (kvantitatív) adatok
Valamilyen skálán mért számok. **Eloszlásuk:** hol és milyen sűrűn helyezkednek el az értékek a skálán.
:::
:::

::: {.column}
::: {.callout-tip}
## Kategorizált (kvalitatív) adatok
Címkék, kategórianevek. **Eloszlásuk:** az egyes kategóriákba hány megfigyelés esik.
:::
:::
::::

## A változók csoportosítása

:::: {.columns}
::: {.column}
### Mérési szint szerint

- **Kvalitatív** (minőségi, kategorikus): nominális és ordinális skála
- **Kvantitatív** (mennyiségi, metrikus): intervallum- és arányskála
:::

::: {.column}
### Értékkészlet szerint

- **Diszkrét**: jól elkülönülő, megszámlálható értékek
- **Folytonos**: egy összefüggő tartomány bármely értéke
:::
::::

::: {.callout-important}
A két szempont független egymástól: egy arányskálájú változó lehet diszkrét (gyerekek száma) és folytonos (testsúly) is.
:::

## Mérési skálák és értékkészlet {.smaller}

Legyen $A$ és $B$ két egyed, $x_A$ és $x_B$ az $x$ változó értéke náluk.

| Skála | Mit állapíthatunk meg? | Diszkrét példa | Folytonos példa |
|:--|:--|:--|:--|
| Nominális | $x_A = x_B$ vagy $x_A \neq x_B$ | nem, születési hely, diagnózis | – |
| Ordinális | + $x_A < x_B$ vagy $x_A > x_B$ | végzettség, rendfokozat | szubjektív intenzitásítélet (fényesség, hangerő) |
| Intervallum | + $A$ értéke $x_A - x_B$ egységgel nagyobb | naptári év | hőmérséklet (°C, °F) |
| Arány | + $A$ értéke $x_A / x_B$-szer nagyobb | gyerekek száma, hibák száma | reakcióidő, testsúly, hőmérséklet (K) |

: Minden skála örökli az alatta lévők összehasonlítási lehetőségeit („+”).

## Nominális skála

- Egyszerű **kategorizálás**: a tulajdonságoknak nevet adunk, és minden egyedet egy kategóriába sorolunk
- Nincs értelmes sorrend, különbség vagy hányados – csak **azonosság** és **különbözőség**
- Példák: nem, családi állapot, vércsoport, pszichiátriai diagnózis (pl. depresszió, szorongásos zavar, szkizofrénia)

::: {.callout-tip}
## Értelmes mutatók
Gyakoriság, arány, **módusz**. A számkód (1 = nő, 2 = férfi) csak címke: az átlaga értelmetlen. [(Stevens, 1946)]{.cite}
:::

## Ordinális skála

- Az értékek **sorba rendezhetők**, de az egymást követő fokozatok közti „távolság” nem feltétlenül egyenlő
- Példák: iskolai végzettség, osztályzat (1–5), katonai rendfokozat, helyezés egy versenyen
- Az elégtelen és az elégséges közti különbség nem feltétlenül akkora, mint a jó és a jeles közötti

::: {.callout-tip}
## Értelmes mutatók
Az előzők, valamint **medián**, kvartilisek, percentilisek, rangkorreláció.
:::

## Intervallumskála

- A **különbségek** értelmesek és egyenlő egységűek, de a nullpont **önkényes**
- Példák: hőmérséklet °C-ban vagy °F-ben, IQ-pontszám, naptári év
- 35 és 38 °C között ugyanakkora a különbség, mint 42 és 45 °C között – de a 20 °C **nem** „kétszer olyan meleg”, mint a 10 °C (Kelvinben: $293{,}15 / 283{,}15 \approx 1{,}035$)

::: {.callout-tip}
## Értelmes mutatók
Az előzők, valamint **átlag**, **szórás**, Pearson-féle korreláció.
:::

## Arányskála

- Intervallumskála **természetes nullponttal**: a **hányados** is értelmes
- Példák: testsúly, életkor, reakcióidő, naponta elszívott cigaretták száma, hőmérséklet kelvinben (0 K = −273,15 °C)
- A 600 ms-os reakcióidő valóban kétszer olyan hosszú, mint a 300 ms-os

::: {.callout-tip}
## Értelmes mutatók
Az előzők, valamint **mértani átlag** és **relatív szórás** ($V = s/\bar{x}$).
:::

## Mennyire szigorúak a szabályok? {.smaller}

- Stevens (1946) szerint a mérési szint megszabja, mely statisztikák **megengedettek**
- Lord (1953) tanmeséjében a futballmezek *számait* átlagolják – és ez az adott kérdésre értelmes választ ad: a számok „nem tudják, honnan származnak”
- Velleman és Wilkinson (1993): a skálatipológia félrevezető, ha gépiesen alkalmazzuk – a **kutatási kérdés** és az adatok jelentése dönt
- **Likert-skála** [(Likert, 1932)]{.cite}: egyetlen tétel ordinális; több tétel összpontszámát a gyakorlatban rendszerint intervallumskálaként kezelik

::: {.callout-important}
A mérési szint jó kiindulópont, de mindig gondoljuk végig, **mit jelentenek a számok**.
:::

## Próbálja ki: melyik mérési szint?

```{=html}
<div class="widget" id="qz">
  <p class="muted" id="qz-count"></p>
  <h3 id="qz-item"></h3>
  <div class="grid" style="--cols:4" id="qz-opts">
    <button class="btn" data-v="0">nominális</button>
    <button class="btn" data-v="1">ordinális</button>
    <button class="btn" data-v="2">intervallum</button>
    <button class="btn" data-v="3">arány</button>
  </div>
  <div id="qz-fb"></div>
  <p><button class="btn" id="qz-next">Következő ›</button> <span class="muted" id="qz-score"></span></p>
</div>
<script>
(() => {
  const $ = id => document.getElementById(id);
  const names = ['nominális', 'ordinális', 'intervallum', 'arány'];
  const items = [
    ['Vércsoport (A, B, AB, 0)', 0, 'Csak azonosság és különbözőség állapítható meg, a kategóriák nem rendezhetők.'],
    ['Iskolai végzettség (alap-, közép-, felsőfok)', 1, 'Sorba rendezhető, de a fokozatok közti „távolság” nem egyenlő.'],
    ['Reakcióidő ezredmásodpercben', 3, 'Van természetes nullpont: a 600 ms valóban kétszer 300 ms.'],
    ['Hőmérséklet Celsius-fokban', 2, 'A különbségek egyenlők, de a 0 °C önkényesen választott nullpont.'],
    ['Pszichiátriai diagnózis', 0, 'Kategóriák, amelyek között nincs sorrend.'],
    ['Helyezés egy versenyen (1., 2., 3.)', 1, 'A sorrend értelmes, a helyezések közti különbség viszont nem feltétlenül egyenlő.'],
    ['Naponta elszívott cigaretták száma', 3, 'Számlálás: van valódi nulla, a hányados is értelmes.'],
    ['IQ-pontszám', 2, 'Egyenlő egységű skála, de a 0 pont nem jelenti az intelligencia hiányát.'],
    ['Osztályzat (1–5)', 1, 'Rangsor: az elégtelen és az elégséges között más a különbség, mint a jó és a jeles között.'],
    ['Testsúly kilogrammban', 3, 'Természetes nullpont, értelmes hányados.'],
    ['Családi állapot', 0, 'Kategóriák, amelyek között nincs sorrend.'],
    ['Naptári év (pl. 1946)', 2, 'A különbség értelmes (eltelt évek), de a 0. év önkényes kezdőpont.']
  ];
  const btns = [...$('qz-opts').children];
  let i = 0, ok = 0;
  function show() {
    if (i === items.length) {
      $('qz-count').textContent = 'Vége a kvíznek';
      $('qz-item').textContent = `Eredmény: ${ok} / ${items.length}`;
      $('qz-opts').hidden = true;
      $('qz-fb').className = ''; $('qz-fb').textContent = '';
      $('qz-next').textContent = 'Újrakezdés';
      return;
    }
    $('qz-opts').hidden = false;
    $('qz-count').textContent = `${i + 1}. változó a ${items.length}-ból`;
    $('qz-item').textContent = items[i][0];
    btns.forEach(b => { b.disabled = false; b.classList.remove('on'); });
    $('qz-fb').className = ''; $('qz-fb').textContent = '';
    $('qz-next').disabled = true;
    $('qz-next').textContent = 'Következő ›';
    $('qz-score').textContent = `Helyes válaszok: ${ok}`;
  }
  $('qz-opts').onclick = e => {
    const b = e.target.closest('button');
    if (!b || b.disabled) return;
    const [, right, why] = items[i], hit = +b.dataset.v === right;
    if (hit) ok++;
    btns.forEach(x => { x.disabled = true; x.classList.toggle('on', +x.dataset.v === right); });
    $('qz-fb').className = 'callout ' + (hit ? 'callout-tip' : 'callout-important');
    $('qz-fb').innerHTML = `<p class="callout-title">${hit ? 'Helyes!' : 'Nem egészen.'} A helyes válasz: ${names[right]}.</p><p>${why}</p>`;
    $('qz-score').textContent = `Helyes válaszok: ${ok}`;
    $('qz-next').disabled = false;
  };
  $('qz-next').onclick = () => {
    if (i === items.length) { i = 0; ok = 0; } else i++;
    show();
  };
  show();
})();
</script>
```

# Diszkrét és folytonos változók

## Diszkrét változók

- Értékei **jól elkülönülnek** egymástól; értékkészlete **megszámlálható** (véges vagy megszámlálhatóan végtelen)
- Minden nominális és csaknem minden ordinális változó diszkrét
- **Dichotóm** (kétértékű) változó: nem, dohányzik / nem dohányzik, helyes / helytelen válasz
- Példák: a fájdalom erőssége (enyhe, közepes, erős), a visszaesésig eltelt hónapok száma, a hibák száma egy teszten

## Folytonos változók

- Lehetséges értékei egy **összefüggő tartományt** töltenek ki – az értékskálán nincsenek „lyukak”
- Két érték között elméletileg végtelen sok köztes érték lehet; az értékek számossága **kontinuum**
- Az intervallum- és arányskálájú változók gyakran folytonosak
- Példák: testhőmérséklet, testmagasság, reakcióidő, egy nap alatt lehullott csapadék mennyisége

## Minden mérés közelítés

A folytonos változó mért értéke csak **közelíti** a valódi értéket: az egy tizedesre pontos 165,2 cm azt jelenti, hogy a valódi érték a $[165{,}15;\ 165{,}25)$ intervallumba esik.

```{=html}
<div class="widget">
  <svg id="pr-plot" viewBox="0 0 1000 150" role="img" aria-label="A mért érték és a valódi érték intervalluma a számegyenesen"></svg>
</div>
<div class="controls" style="margin-top:14px">
  <div>Mérési pontosság:<span class="seg" id="pr-k"><button data-k="0">egész cm</button><button data-k="1" class="on">1 tizedes</button><button data-k="2">2 tizedes</button><button data-k="3">3 tizedes</button></span></div>
</div>
<div class="grid" style="--cols:3;margin-top:14px">
  <div class="stat"><b id="pr-r"></b><small>mért (kerekített) érték</small></div>
  <div class="stat"><b id="pr-i"></b><small>itt van a valódi érték</small></div>
  <div class="stat"><b id="pr-e"></b><small>legnagyobb kerekítési hiba</small></div>
</div>
<script>
(() => {
  const $ = id => document.getElementById(id), TRUE = 165.1952344358;
  const fmt = (v, d) => v.toLocaleString('hu-HU', {minimumFractionDigits: d, maximumFractionDigits: d});
  let k = 1;
  function draw() {
    const u = 10 ** -k, r = Math.round(TRUE / u) * u, a = r - u / 2, b = r + u / 2;
    const X0 = r - 1.5 * u, sx = x => 40 + (x - X0) / (3 * u) * 920, y = 90;
    const tick = (x, label, cls = 'tick') =>
      `<line class="axis" x1="${sx(x)}" x2="${sx(x)}" y1="${y - 8}" y2="${y + 8}"/><text class="${cls}" x="${sx(x)}" y="${y + 32}" text-anchor="middle">${label}</text>`;
    $('pr-plot').innerHTML =
      `<rect class="area" x="${sx(a)}" y="${y - 30}" width="${sx(b) - sx(a)}" height="30"/>` +
      `<line class="axis" x1="40" x2="960" y1="${y}" y2="${y}"/>` +
      tick(r - u, fmt(r - u, k)) + tick(r + u, fmt(r + u, k)) +
      tick(a, fmt(a, k + 1)) + tick(b, fmt(b, k + 1)) +
      `<circle class="dot" cx="${sx(r)}" cy="${y}" r="8"/>` +
      `<text class="label" x="${sx(r)}" y="${y + 32}" text-anchor="middle" style="fill:var(--accent)">mért: ${fmt(r, k)}</text>` +
      `<line class="mean" x1="${sx(TRUE)}" x2="${sx(TRUE)}" y1="${y - 70}" y2="${y}"/>` +
      `<text class="label" x="${sx(TRUE)}" y="${y - 76}" text-anchor="middle">valódi: ${fmt(TRUE, 7)}…</text>`;
    $('pr-r').textContent = fmt(r, k) + ' cm';
    $('pr-i').textContent = `[${fmt(a, k + 1)}; ${fmt(b, k + 1)})`;
    $('pr-e').textContent = '± ' + fmt(u / 2, k + 1) + ' cm';
  }
  $('pr-k').onclick = e => {
    const btn = e.target.closest('button');
    if (!btn) return;
    k = +btn.dataset.k;
    for (const x of $('pr-k').children) x.classList.toggle('on', x === btn);
    draw();
  };
  draw();
})();
</script>
```

::: {.notes}
A folytonos változót a gyakorlatban mindig kerekítve, azaz diszkrét értékekként rögzítjük – a folytonosság a változó elméleti tulajdonsága.
:::

## Összefoglalás {.inverse .center}

- A **leíró** statisztika összegez, az **induktív** a mintából a populációra következtet
- A populációt **paraméterek**, a mintát **statisztikák** jellemzik; a minta legyen **reprezentatív**
- Az adatmátrix sorai az egyedek, oszlopai a **változók**
- Mérési szintek: **nominális → ordinális → intervallum → arány**
- Értékkészlet szerint a változó **diszkrét** vagy **folytonos**

## Irodalom {.smaller}

::: {.refs}
Likert, R. (1932). A technique for the measurement of attitudes. *Archives of Psychology, 140*, 1–55.

Lord, F. M. (1953). On the statistical treatment of football numbers. *American Psychologist, 8*(12), 750–751.

Squire, P. (1988). Why the 1936 *Literary Digest* poll failed. *Public Opinion Quarterly, 52*(1), 125–133.

Stevens, S. S. (1946). On the theory of scales of measurement. *Science, 103*(2684), 677–680.

Velleman, P. F., & Wilkinson, L. (1993). Nominal, ordinal, interval, and ratio typologies are misleading. *The American Statistician, 47*(1), 65–72.

Wickham, H. (2014). Tidy data. *Journal of Statistical Software, 59*(10), 1–23.

**Magyar nyelvű tankönyv:** Vargha A. (2000). *Matematikai statisztika pszichológiai, nyelvészeti és biológiai alkalmazásokkal.* Pólya Kiadó.
:::

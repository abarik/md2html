---
title: "Miért kell a pszichológusnak statisztika?"
subtitle: "Bevezetés a statisztikai gondolkodásba – pszichológia BA"
author: "Abari Kálmán"
date: "2026. ősz"
lang: hu
footer: "Matematikai alapok II. · 1. Bevezetés a statisztikai gondolkodásba"
---

## A pszichológia tapasztalati tudomány

- Kérdéseink empirikusak: *Csökkenti-e a rendszeres mozgás a szorongást?*
- Az emberek **különböznek** egymástól, és ugyanaz az ember sem viselkedik mindig egyformán: ez a **variabilitás**
- A statisztika a változékonyság tudománya: leírja azt, és elválasztja a **jelet** a **zajtól**

::: {.callout-note}
## A tudományos pszichológia két diszciplínája
A **kísérleti** hagyomány a feltételek hatását keresi, az egyéni különbség számára zaj. A **korrelációs** hagyomány számára éppen az egyéni különbség a vizsgálat tárgya. Mindkettő statisztikára épül. [(Cronbach, 1957)]{.cite}
:::

::: {.notes}
Kérdezzük meg a hallgatókat: ki jelentkezett pszichológiára azért, mert „nem kell matekozni”? A statisztika a pszichológus egyik alapvető munkaeszköze.
:::

# Közös gyökerek

## Az átlagember és a mérhető lélek

- **Adolphe Quetelet** (1835): az *átlagember* (*l’homme moyen*) – az emberi jellemzők a normális eloszlást követik
- **Gustav Theodor Fechner** (1860): pszichofizika – az érzet erőssége az inger logaritmusával arányos: $S = k \log I$
- **Wilhelm Wundt** (1879): az első pszichológiai laboratórium Lipcsében

::: {.callout-tip}
A pszichológia akkor vált önálló tudománnyá, amikor **mérni** kezdett.
:::

## Regresszió, korreláció, faktor {.smaller}

| Év | Ki | Mit adott a tudománynak |
|:--|:--|:--|
| 1886 | Francis Galton | **regresszió a középhez** (szülők és gyermekeik testmagassága) |
| 1888 | Francis Galton | a *co-relation*, azaz az együttjárás fogalma |
| 1896 | Karl Pearson | a **korrelációs együttható** ($r$) matematikai formája |
| 1904 | Charles Spearman | az **általános intelligencia** ($g$), a faktoranalízis kezdete |

::: {.callout-important}
A korreláció és a faktoranalízis **pszichológiai kérdésekre** – öröklődés, képességek, intelligencia – adott válaszként született.
:::

::: {.notes}
Érdemes megemlíteni: Galton és Pearson eugenikai céljai ma joggal elítéltek; a módszerek értéke ettől független, de a történet része.
:::

## A következtető statisztika megszületése

- **„Student”** (W. S. Gosset, 1908): kis minták, $t$-eloszlás – a Guinness sörgyár munkatársaként álnéven publikált
- **Ronald A. Fisher** (1925, 1935): szignifikanciavizsgálat, randomizálás, varianciaanalízis
- **Jerzy Neyman és Egon S. Pearson** (1933): $H_0$ és $H_1$, első- és másodfajú hiba

::: {.callout-note}
## A teakóstoló hölgy [(Fisher, 1935)]{.cite}
Nyolc csésze teából négybe először a tejet, négybe először a teát öntik. Ha a hölgy csak találgat, mind a nyolcat $1/70 \approx 1{,}4\%$ eséllyel sorolja be helyesen.
:::

# Az intuíció csapdái

## A kis számok törvénye

Egy városban két kórház van. A nagyobbikban naponta kb. 45, a kisebbikben kb. 15 csecsemő születik. Egy év alatt melyik kórházban volt több olyan nap, amikor a születettek **több mint 60%-a fiú** volt?

. . .

- A legtöbb megkérdezett szerint: *„nagyjából ugyanannyi”*
- A helyes válasz: a **kisebbikben** – a kis minta jobban ingadozik [(Tversky & Kahneman, 1974)]{.cite}

::: {.callout-warning}
A kutatók is túl sokat várnak a kis mintáktól: elvárják, hogy a minta a sokaság „kicsinyített mása” legyen. [(Tversky & Kahneman, 1971)]{.cite}
:::

## Próbálja ki: mintanagyság és mintaátlag

:::: {.columns}
::: {.column width="62%"}
```{=html}
<div class="widget">
  <svg id="sm-plot" viewBox="0 0 720 400" role="img" aria-label="1000 mintaátlag hisztogramja"></svg>
  <div class="legend"><span><i></i>a mintaátlag elméleti eloszlása</span><span><i class="dash"></i>sokasági átlag, μ = 100</span></div>
</div>
```
:::

::: {.column width="38%"}
1000 véletlen minta egy $N(100;\ 15^2)$ eloszlású sokaságból (pl. IQ). Minden minta átlaga egy adat a hisztogramon.

```{=html}
<div class="controls">
  <label><span>Mintanagyság: n = <output id="sm-n-o"></output></span>
    <input id="sm-n" type="range" min="2" max="50" step="1" value="5"></label>
  <div><button class="btn" id="sm-new">Új 1000 minta</button></div>
</div>
<div class="stats">
  <div class="stat"><b id="sm-se"></b><small>az átlagok szórása (standard hiba)</small></div>
  <div class="stat"><b id="sm-far"></b><small>az átlagok ennyi százaléka tér el 5 pontnál többel</small></div>
</div>
<script>
(() => {
  const $ = id => document.getElementById(id), svg = $('sm-plot'), NS = 'http://www.w3.org/2000/svg';
  const W = 720, H = 400, L = 52, R = 12, T = 14, B = 40, X0 = 70, X1 = 130, BW = 2, YM = 0.2, M = 1000;
  const sx = x => L + (x - X0) / (X1 - X0) * (W - L - R);
  const sy = y => H - B - Math.min(y, YM) / YM * (H - T - B);
  const fmt = (v, d) => v.toLocaleString('hu-HU', {minimumFractionDigits: d, maximumFractionDigits: d});
  const el = (tag, a, text, parent = svg) => {
    const e = document.createElementNS(NS, tag);
    for (const k in a) e.setAttribute(k, a[k]);
    if (text != null) e.textContent = text;
    return parent.appendChild(e);
  };
  const randn = () => {
    let u = 0;
    while (!u) u = Math.random();
    return Math.sqrt(-2 * Math.log(u)) * Math.cos(2 * Math.PI * Math.random());
  };
  for (let x = X0; x <= X1; x += 10) {
    el('line', {class: 'grid', x1: sx(x), x2: sx(x), y1: T, y2: sy(0)});
    el('text', {class: 'tick', x: sx(x), y: sy(0) + 26, 'text-anchor': 'middle'}, x);
  }
  for (let i = 0; i <= 4; i++) {
    el('line', {class: 'grid', x1: L, x2: W - R, y1: sy(i / 20), y2: sy(i / 20)});
    el('text', {class: 'tick', x: L - 8, y: sy(i / 20) + 5, 'text-anchor': 'end'}, fmt(i / 20, 2));
  }
  const bars = el('g', {}), curve = el('path', {class: 'curve'});
  el('line', {class: 'ref', x1: sx(100), x2: sx(100), y1: T, y2: sy(0)});
  el('line', {class: 'axis', x1: L, x2: W - R, y1: sy(0), y2: sy(0)});

  function draw() {
    const n = +$('sm-n').value, se = 15 / Math.sqrt(n), bins = new Array((X1 - X0) / BW).fill(0);
    let far = 0, s1 = 0, s2 = 0;
    for (let j = 0; j < M; j++) {
      let s = 0;
      for (let i = 0; i < n; i++) s += 100 + 15 * randn();
      const m = s / n, b = Math.floor((m - X0) / BW);
      if (b >= 0 && b < bins.length) bins[b]++;
      if (Math.abs(m - 100) > 5) far++;
      s1 += m; s2 += m * m;
    }
    bars.replaceChildren();
    bins.forEach((c, b) => {
      if (!c) return;
      const y = sy(c / (M * BW));
      el('rect', {class: 'bar', x: sx(X0 + b * BW) + 0.5, width: sx(X0 + BW) - sx(X0) - 1, y, height: sy(0) - y}, null, bars);
    });
    let d = '';
    for (let i = 0; i <= 240; i++) {
      const x = X0 + (X1 - X0) * i / 240, f = Math.exp(-((x - 100) ** 2) / (2 * se * se)) / (se * Math.sqrt(2 * Math.PI));
      d += (i ? 'L' : 'M') + sx(x).toFixed(1) + ',' + sy(f).toFixed(1);
    }
    curve.setAttribute('d', d);
    $('sm-n-o').value = n;
    $('sm-se').textContent = fmt(Math.sqrt(s2 / M - (s1 / M) ** 2), 2);
    $('sm-far').textContent = fmt(far / M * 100, 1) + ' %';
  }
  $('sm-n').oninput = $('sm-new').onclick = draw;
  draw();
})();
</script>
```
:::
::::

::: {.notes}
Kis n mellett az átlagok szélesen szóródnak; n növelésével a hisztogram összeszűkül. Elméletileg a standard hiba 15/√n: n = 4-nél 7,5, n = 25-nél 3, n = 50-nél kb. 2,1.
:::

## Regresszió a középhez {.smaller}

- Repülőoktatók tapasztalata: dicséret után a teljesítmény **romlik**, szidás után **javul** – tehát a büntetés hatásosabb? [(Tversky & Kahneman, 1974)]{.cite}

. . .

- Valójában a kiugró teljesítmény részben **véletlen**, ezért legközelebb várhatóan közelebb lesz az átlaghoz – beavatkozás nélkül is
- Galton (1886) is ezt látta: a nagyon magas szülők gyermekei átlagosan alacsonyabbak náluk

::: {.callout-important}
## Klinikai jelentőség
Terápiára akkor jelentkeznek, amikor a tünetek a **legsúlyosabbak** – a javulás egy része regresszió a középhez, ezért kell **kontrollcsoport**.
:::

# A kutatás alapfogalmai

## A kutatási folyamat {.smaller}

::: {.incremental}
1. **Kutatási kérdés** – csökkenti-e a mindfulness a vizsgaszorongást?
2. **Hipotézis** – a tréning után alacsonyabb a szorongáspontszám
3. **Operacionalizálás** – mivel mérjük a szorongást? (pl. kérdőív)
4. **Elrendezés és mintavétel** – kiket, hányakat, milyen csoportokban?
5. **Elemzés** – leíró és következtető statisztika
6. **Következtetés** – mit állíthatunk, és mit nem?
:::

::: {.callout-tip}
A statisztika nem az utolsó lépés: a jó elemzést már a kérdés megfogalmazásakor el kell kezdeni tervezni.
:::

## Mérés a pszichológiában

- A pszichológiai **konstruktumok** (intelligencia, szorongás, extraverzió) közvetlenül nem figyelhetők meg: **látens változók**
- Mérés: számok hozzárendelése tárgyakhoz vagy eseményekhez szabályok szerint [(Stevens, 1946)]{.cite}
- Négy mérési szint: **nominális** (diagnózis), **ordinális** (rangsor), **intervallum** (IQ), **arány** (reakcióidő)
- **Likert-skála** [(Likert, 1932)]{.cite}: „egyáltalán nem értek egyet” … „teljesen egyetértek” – ordinális vagy intervallumskála? Máig vitatott.

## A mérés minősége {.smaller}

:::: {.columns}
::: {.column}
### Megbízhatóság (reliabilitás)

- Mennyire mentes a mérés a véletlen hibától?
- Klasszikus tesztelmélet: $X = T + E$ (mért = valódi + hiba)
- Cronbach-alfa [(Cronbach, 1951)]{.cite}:

$$\alpha = \frac{k}{k-1}\left(1-\frac{\sum \sigma_i^2}{\sigma_X^2}\right)$$
:::

::: {.column}
### Érvényesség (validitás)

- Azt méri-e a teszt, amit mérni szeretnénk?
- Tartalmi, kritérium- és **konstruktumvaliditás** [(Cronbach & Meehl, 1955)]{.cite}

::: {.callout-tip}
Megbízhatóság érvényesség nélkül is lehetséges, érvényesség megbízhatóság nélkül nem.
:::
:::
::::

## Sokaság, minta, mintavételi ingadozás {.smaller}

- **Sokaság**: akikre a következtetést vonatkoztatni szeretnénk (pl. a magyar egyetemisták)
- **Minta**: akiket ténylegesen megvizsgálunk – gyakran éppen pszichológushallgatók
- A mintából számolt érték mintáról mintára **ingadozik**; az átlag standard hibája $\mathrm{SE} = \sigma / \sqrt{n}$ – négyszer akkora minta, fele akkora hiba

::: {.callout-warning}
## WEIRD minták
A pszichológiai vizsgálatok résztvevői túlnyomórészt nyugati, iskolázott, iparosodott, gazdag és demokratikus társadalmakból származnak. [(Henrich, Heine & Norenzayan, 2010)]{.cite}
:::

## Mindig ábrázolja az adatokat!

A **leíró** statisztika összegzi a mintát, a **következtető** a sokaságra általánosít. Az összegzés azonban információt veszít:

```{=html}
<div class="grid" id="ans" style="--cols:4"></div>
<script>
(() => {
  const NS = 'http://www.w3.org/2000/svg', box = document.getElementById('ans');
  const x1 = [10, 8, 13, 9, 11, 14, 6, 4, 12, 7, 5];
  const sets = [
    [x1, [8.04, 6.95, 7.58, 8.81, 8.33, 9.96, 7.24, 4.26, 10.84, 4.82, 5.68]],
    [x1, [9.14, 8.14, 8.74, 8.77, 9.26, 8.10, 6.13, 3.10, 9.13, 7.26, 4.74]],
    [x1, [7.46, 6.77, 12.74, 7.11, 7.81, 8.84, 6.08, 5.39, 8.15, 6.42, 5.73]],
    [[8, 8, 8, 8, 8, 8, 8, 19, 8, 8, 8], [6.58, 5.76, 7.71, 8.84, 8.47, 7.04, 5.25, 12.50, 5.56, 7.91, 6.89]]
  ];
  const sx = x => 26 + (x - 2) / 18 * 224, sy = y => 186 - (y - 2) / 12 * 160;
  sets.forEach(([xs, ys], k) => {
    const card = document.createElement('div'), svg = document.createElementNS(NS, 'svg');
    card.className = 'widget';
    svg.setAttribute('viewBox', '0 0 260 200');
    const el = (tag, a, text) => {
      const e = document.createElementNS(NS, tag);
      for (const key in a) e.setAttribute(key, a[key]);
      if (text != null) e.textContent = text;
      return svg.appendChild(e);
    };
    el('line', {class: 'axis', x1: sx(2), x2: sx(20), y1: sy(2), y2: sy(2)});
    el('line', {class: 'axis', x1: sx(2), x2: sx(2), y1: sy(2), y2: sy(14)});
    el('line', {class: 'ref', x1: sx(2), x2: sx(20), y1: sy(4), y2: sy(13)});
    xs.forEach((x, i) => el('circle', {class: 'dot', cx: sx(x), cy: sy(ys[i]), r: 5}));
    el('text', {class: 'title', x: sx(3), y: sy(13.2)}, ['I.', 'II.', 'III.', 'IV.'][k]);
    card.appendChild(svg);
    box.appendChild(card);
  });
})();
</script>
```

Mind a négy adatsorban $\bar{x} = 9$, $\bar{y} \approx 7{,}5$, $r \approx 0{,}82$ és $\hat{y} = 3 + 0{,}5x$. [(Anscombe, 1973)]{.cite}

## Korreláció és ok-okozat {.smaller}

:::: {.columns}
::: {.column width="52%"}
- A korreláció **nem** bizonyít oksági kapcsolatot: lehet fordított az irány, vagy egy harmadik tényező állhat a háttérben
- Oksági következtetéshez **kísérlet** kell: manipuláció és **véletlen besorolás**
- A belső érvényességet veszélyeztető tényezők [(Campbell & Stanley, 1963)]{.cite}: előzmények, érés, tesztelési hatás, a mérőeszköz változása, statisztikai regresszió, szelekció, lemorzsolódás
:::

::: {.column width="48%"}
::: {.callout-caution}
## Simpson-paradoxon: Berkeley, 1973

| | Jelentkezők | Felvettek |
|:--|--:|--:|
| Férfiak | 8442 | 44% |
| Nők | 4321 | 35% |

Szakonként vizsgálva a nők nem voltak hátrányban: többen jelentkeztek a nehezen bejutható szakokra. [(Bickel, Hammel & O’Connell, 1975)]{.cite}
:::
:::
::::

# Kritikus statisztikai gondolkodás

## Mit jelent a p-érték – és mit nem? {.smaller}

A $p$-érték annak valószínűsége, hogy **legalább ilyen szélsőséges** eredményt kapunk, *ha a nullhipotézis igaz*: $p = P(T \geq t \mid H_0)$

. . .

:::: {.columns}
::: {.column width="55%"}
**Nem** jelenti:

- annak valószínűségét, hogy $H_0$ igaz
- hogy $1-p$ eséllyel megismételhető az eredmény
- hogy nem szignifikáns eredménynél nincs hatás
- hogy a szignifikáns hatás fontos is
:::

::: {.column width="45%"}
::: {.callout-warning}
A következtetés nem múlhat azon, hogy a $p$ átlépi-e a 0,05-os határt – a gépies „rituálé” helyett gondolkodni kell. [(Cohen, 1994; Gigerenzer, 2004; Wasserstein & Lazar, 2016)]{.cite}
:::
:::
::::

## Hatásnagyság és statisztikai erő {.smaller}

- **Hatásnagyság**: mekkora a különbség? Cohen-féle $d = (\bar{x}_1 - \bar{x}_2) / s$
- **Statisztikai erő** ($1-\beta$): annak valószínűsége, hogy egy *létező* hatást ki is mutatunk
- A tanulmányok átlagosan kb. **48%** eséllyel mutattak volna ki közepes hatást [(Cohen, 1962)]{.cite}
- Két évtizeddel később: medián **37%** [(Sedlmeier & Gigerenzer, 1989)]{.cite}

::: {.callout-tip}
Legalább 80%-os erő ajánlott: közepes hatásnál ($d = 0{,}5$) ehhez csoportonként kb. 64 fő kell. [(Cohen, 1988)]{.cite}
:::

## Próbálja ki: statisztikai erő

:::: {.columns}
::: {.column width="62%"}
```{=html}
<div class="widget">
  <svg id="pw-plot" viewBox="0 0 720 400" role="img" aria-label="A próbastatisztika eloszlása a nullhipotézis és az alternatív hipotézis mellett"></svg>
  <div class="legend"><span><i class="dash"></i>H₀ igaz</span><span><i></i>H₁ igaz (van hatás)</span><span>satírozva: erő és α</span></div>
</div>
```
:::

::: {.column width="38%"}
Két független csoport, kétoldali próba.

```{=html}
<div class="controls">
  <label><span>Hatásnagyság: d = <output id="pw-d-o"></output></span>
    <input id="pw-d" type="range" min="0" max="1.2" step="0.05" value="0.5"></label>
  <label><span>Csoportonkénti létszám: n = <output id="pw-n-o"></output></span>
    <input id="pw-n" type="range" min="5" max="150" step="1" value="30"></label>
  <div>α:<span class="seg" id="pw-a"><button data-z="1.959964" class="on">0,05</button><button data-z="2.575829">0,01</button></span></div>
</div>
<div class="stats">
  <div class="stat"><b id="pw-pow"></b><small>statisztikai erő (1 − β)</small></div>
  <div class="stat"><b id="pw-n80"></b><small>létszám csoportonként 80%-os erőhöz</small></div>
</div>
<script>
(() => {
  const $ = id => document.getElementById(id), svg = $('pw-plot'), NS = 'http://www.w3.org/2000/svg';
  const W = 720, H = 400, L = 46, R = 12, T = 30, B = 40, X0 = -4, X1 = 9, YM = 0.42;
  const sx = x => L + (x - X0) / (X1 - X0) * (W - L - R);
  const sy = y => H - B - y / YM * (H - T - B);
  const fmt = (v, d) => v.toLocaleString('hu-HU', {minimumFractionDigits: d, maximumFractionDigits: d});
  const phi = x => Math.exp(-x * x / 2) / Math.sqrt(2 * Math.PI);
  const Phi = x => {  // standard normális eloszlásfüggvény (Abramowitz–Stegun 7.1.26)
    const t = 1 / (1 + 0.3275911 * Math.abs(x) / Math.SQRT2);
    const e = 1 - ((((1.061405429 * t - 1.453152027) * t + 1.421413741) * t - 0.284496736) * t + 0.254829592) * t * Math.exp(-x * x / 2);
    return x >= 0 ? (1 + e) / 2 : (1 - e) / 2;
  };
  const el = (tag, a, text) => {
    const e = document.createElementNS(NS, tag);
    for (const k in a) e.setAttribute(k, a[k]);
    if (text != null) e.textContent = text;
    return svg.appendChild(e);
  };
  const path = (f, a, b) => {
    let d = '';
    for (let i = 0; i <= 200; i++) {
      const x = a + (b - a) * i / 200;
      d += (i ? 'L' : 'M') + sx(x).toFixed(1) + ',' + sy(f(x)).toFixed(1);
    }
    return d;
  };
  const area = (f, a, b) => b <= a ? '' : path(f, a, b) + `L${sx(b).toFixed(1)},${sy(0)}L${sx(a).toFixed(1)},${sy(0)}Z`;
  for (let x = X0; x <= X1; x += 1) {
    el('line', {class: 'grid', x1: sx(x), x2: sx(x), y1: T, y2: sy(0)});
    el('text', {class: 'tick', x: sx(x), y: sy(0) + 26, 'text-anchor': 'middle'}, fmt(x, 0));
  }
  el('line', {class: 'axis', x1: L, x2: W - R, y1: sy(0), y2: sy(0)});
  const aPow = el('path', {class: 'area'}), aAlpha = el('path', {class: 'area-2'});
  const c0 = el('path', {class: 'ref'}), c1 = el('path', {class: 'curve'});
  const k1 = el('line', {class: 'mean'}), k2 = el('line', {class: 'mean'});
  const l0 = el('text', {class: 'label', 'text-anchor': 'middle'}, 'H₀'), l1 = el('text', {class: 'label', 'text-anchor': 'middle'}, 'H₁');
  let z = 1.959964;

  function draw() {
    const d = +$('pw-d').value, n = +$('pw-n').value, delta = d * Math.sqrt(n / 2);
    const f0 = phi, f1 = x => phi(x - delta);
    c0.setAttribute('d', path(f0, X0, X1));
    c1.setAttribute('d', path(f1, X0, X1));
    aAlpha.setAttribute('d', area(f0, z, X1) + area(f0, X0, -z));
    aPow.setAttribute('d', area(f1, z, X1) + area(f1, X0, -z));
    [[k1, z], [k2, -z]].forEach(([k, x]) => {
      for (const [a, v] of Object.entries({x1: sx(x), x2: sx(x), y1: T, y2: sy(0)})) k.setAttribute(a, v);
    });
    l0.setAttribute('x', sx(0)); l0.setAttribute('y', sy(phi(0)) - 10);
    l1.setAttribute('x', sx(Math.min(delta, X1 - 0.3))); l1.setAttribute('y', sy(phi(0)) - 10);
    l1.style.display = delta < 0.4 ? 'none' : '';
    const power = Phi(delta - z) + Phi(-delta - z);
    $('pw-d-o').value = fmt(d, 2);
    $('pw-n-o').value = n;
    $('pw-pow').textContent = fmt(power * 100, 1) + ' %';
    $('pw-n80').textContent = d > 0 ? Math.ceil(2 * ((z + 0.841621) / d) ** 2) : '∞';
  }
  $('pw-d').oninput = $('pw-n').oninput = draw;
  $('pw-a').onclick = e => {
    const btn = e.target.closest('button');
    if (!btn) return;
    z = +btn.dataset.z;
    for (const b of $('pw-a').children) b.classList.toggle('on', b === btn);
    draw();
  };
  draw();
})();
</script>
```

[Cohen (1988): $d = 0{,}2$ kicsi, $0{,}5$ közepes, $0{,}8$ nagy hatás.]{.cite}
:::
::::

::: {.notes}
Az alapbeállítás (d = 0,5; n = 30) kb. 49%-os erőt ad – éppen Cohen 1962-es átlaga. A létszámot a normális közelítés adja; a pontos t-próbás érték egy-két fővel nagyobb (d = 0,5-nél 64).
:::

## Replikációs válság {.smaller}

- **Ioannidis (2005)**: kis minták és rugalmas elemzés mellett a publikált eredmények jelentős része hamis lehet
- **Asztalfiók-probléma** [(Rosenthal, 1979)]{.cite}: a nem szignifikáns eredmények rejtve maradnak
- **Hamis pozitív pszichológia** [(Simmons és mtsai, 2011)]{.cite}: rugalmas adatgyűjtéssel és elemzéssel szinte bármi szignifikánssá tehető
- **Open Science Collaboration (2015)**: 100 vizsgálat megismétlése – a 97%-ban szignifikáns eredményekből **36%** lett ismét szignifikáns, a hatások feleakkorák lettek

::: {.notes}
Hangsúlyozzuk: a válság nem a statisztika kudarca, hanem a rossz statisztikai gyakorlaté – és a megoldás is statisztikai.
:::

## Statisztika a gyakorlatban

:::: {.columns}
::: {.column}
### A gyakorló pszichológusnak

- A statisztikai (mechanikus) előrejelzés legalább olyan pontos, mint a klinikai megítélés [(Meehl, 1954; Grove és mtsai, 2000)]{.cite}
- A szakirodalom kritikus olvasása: mintanagyság, hatásnagyság, konfidenciaintervallum
:::

::: {.column}
### A kutatónak

- Hatásnagyság és konfidenciaintervallum közlése [(Wilkinson & TFSI, 1999)]{.cite}
- Erőelemzés az adatgyűjtés előtt
- **Előzetes regisztráció**
- **Nyílt adatok** és elemzőkód
:::
::::

## Összefoglalás {.inverse .center}

- A pszichológia és a statisztika **közös gyökerű**: Galton, Pearson, Spearman
- A véletlenről alkotott intuíciónk **megbízhatatlan** – ezért van szükség statisztikára
- Jó elemzés csak jó **méréssel** és jó **kutatási elrendezéssel** lehetséges
- A $p$-érték önmagában kevés: **hatásnagyság**, **erő**, **replikáció**

## Irodalom (1/4) {.smaller}

::: {.refs}
Anscombe, F. J. (1973). Graphs in statistical analysis. *The American Statistician, 27*(1), 17–21.

Bickel, P. J., Hammel, E. A., & O’Connell, J. W. (1975). Sex bias in graduate admissions: Data from Berkeley. *Science, 187*(4175), 398–404.

Campbell, D. T., & Stanley, J. C. (1963). *Experimental and quasi-experimental designs for research.* Rand McNally.

Cohen, J. (1962). The statistical power of abnormal-social psychological research: A review. *Journal of Abnormal and Social Psychology, 65*(3), 145–153.

Cohen, J. (1988). *Statistical power analysis for the behavioral sciences* (2nd ed.). Erlbaum.

Cohen, J. (1994). The earth is round (p < .05). *American Psychologist, 49*(12), 997–1003.

Cronbach, L. J. (1951). Coefficient alpha and the internal structure of tests. *Psychometrika, 16*(3), 297–334.

Cronbach, L. J. (1957). The two disciplines of scientific psychology. *American Psychologist, 12*(11), 671–684.

Cronbach, L. J., & Meehl, P. E. (1955). Construct validity in psychological tests. *Psychological Bulletin, 52*(4), 281–302.
:::

## Irodalom (2/4) {.smaller}

::: {.refs}
Fechner, G. T. (1860). *Elemente der Psychophysik.* Breitkopf & Härtel.

Fisher, R. A. (1925). *Statistical methods for research workers.* Oliver & Boyd.

Fisher, R. A. (1935). *The design of experiments.* Oliver & Boyd.

Galton, F. (1886). Regression towards mediocrity in hereditary stature. *Journal of the Anthropological Institute of Great Britain and Ireland, 15*, 246–263.

Galton, F. (1888). Co-relations and their measurement, chiefly from anthropometric data. *Proceedings of the Royal Society of London, 45*, 135–145.

Gigerenzer, G. (2004). Mindless statistics. *The Journal of Socio-Economics, 33*(5), 587–606.

Grove, W. M., Zald, D. H., Lebow, B. S., Snitz, B. E., & Nelson, C. (2000). Clinical versus mechanical prediction: A meta-analysis. *Psychological Assessment, 12*(1), 19–30.

Henrich, J., Heine, S. J., & Norenzayan, A. (2010). The weirdest people in the world? *Behavioral and Brain Sciences, 33*(2–3), 61–83.

Ioannidis, J. P. A. (2005). Why most published research findings are false. *PLoS Medicine, 2*(8), e124.
:::

## Irodalom (3/4) {.smaller}

::: {.refs}
Likert, R. (1932). A technique for the measurement of attitudes. *Archives of Psychology, 140*, 1–55.

Meehl, P. E. (1954). *Clinical versus statistical prediction.* University of Minnesota Press.

Neyman, J., & Pearson, E. S. (1933). On the problem of the most efficient tests of statistical hypotheses. *Philosophical Transactions of the Royal Society of London, Series A, 231*, 289–337.

Open Science Collaboration. (2015). Estimating the reproducibility of psychological science. *Science, 349*(6251), aac4716.

Pearson, K. (1896). Mathematical contributions to the theory of evolution. III. Regression, heredity, and panmixia. *Philosophical Transactions of the Royal Society of London, Series A, 187*, 253–318.

Quetelet, A. (1835). *Sur l’homme et le développement de ses facultés, ou essai de physique sociale.* Bachelier.

Rosenthal, R. (1979). The file drawer problem and tolerance for null results. *Psychological Bulletin, 86*(3), 638–641.

Sedlmeier, P., & Gigerenzer, G. (1989). Do studies of statistical power have an effect on the power of studies? *Psychological Bulletin, 105*(2), 309–316.

Simmons, J. P., Nelson, L. D., & Simonsohn, U. (2011). False-positive psychology: Undisclosed flexibility in data collection and analysis allows presenting anything as significant. *Psychological Science, 22*(11), 1359–1366.
:::

## Irodalom (4/4) {.smaller}

::: {.refs}
Spearman, C. (1904). „General intelligence,” objectively determined and measured. *The American Journal of Psychology, 15*(2), 201–292.

Stevens, S. S. (1946). On the theory of scales of measurement. *Science, 103*(2684), 677–680.

Student. (1908). The probable error of a mean. *Biometrika, 6*(1), 1–25.

Tversky, A., & Kahneman, D. (1971). Belief in the law of small numbers. *Psychological Bulletin, 76*(2), 105–110.

Tversky, A., & Kahneman, D. (1974). Judgment under uncertainty: Heuristics and biases. *Science, 185*(4157), 1124–1131.

Wasserstein, R. L., & Lazar, N. A. (2016). The ASA statement on p-values: Context, process, and purpose. *The American Statistician, 70*(2), 129–133.

Wilkinson, L., & Task Force on Statistical Inference. (1999). Statistical methods in psychology journals: Guidelines and explanations. *American Psychologist, 54*(8), 594–604.

**Magyar nyelvű tankönyv:** Vargha A. (2000). *Matematikai statisztika pszichológiai, nyelvészeti és biológiai alkalmazásokkal.* Pólya Kiadó.
:::

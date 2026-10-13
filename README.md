# MD2HTML

Egyszerű Markdown → HTML diasor-konverter Pythonban. A bemenet a **Quarto reveal.js** markdown-szintaxisának
egy részhalmaza. A kimenet **egyetlen, kis méretű, önálló HTML fájl** (a példa kb. 24 KiB), amely
internetkapcsolat nélkül is működik. A beépített JavaScript-blokkoknak köszönhetően interaktív elemeket is
tartalmazhat.

- Csak a Python standard könyvtárát használja (Python 3.8+), semmit nem kell telepíteni.
- A megjelenést egyetlen téma-CSS adja (világos vagy sötét), ezt a program beágyazza a HTML-be.
- A képletek natív **MathML**-ként jelennek meg, ezért nincs szükség KaTeX-re vagy MathJaxra.
- A helyi képek data-URI-ként a HTML-be kerülnek.

## Könyvtárszerkezet

```
MD2HTML/
├── README.md
├── md2html/                  ← a program
│   ├── md2html.py
│   └── themes/               ← témák
│       ├── light.css         (alapértelmezett)
│       └── dark.css
└── presentations/            ← minden előadás saját mappában: .md forrás + kész .html
    ├── matalapok/            (sorozat: Matematikai alapok II., pszichológia BA)
    │   ├── matalapok01/      1. Bevezetés a statisztikai gondolkodásba
    │   │   ├── matalapok01.md
    │   │   └── matalapok01.html
    │   ├── matalapok02/      2. Statisztikai alapfogalmak
    │   │   ├── matalapok02.md
    │   │   └── matalapok02.html
    │   ├── matalapok03/      3. Eloszlások és ábrázolásuk
    │   │   ├── matalapok03.md
    │   │   └── matalapok03.html
    │   ├── matalapok04/      4. Középértékek és szóródási mutatók
    │   │   ├── matalapok04.md
    │   │   └── matalapok04.html
    │   ├── matalapok05/      5. Valószínűség-számítás
    │   │   ├── matalapok05.md
    │   │   └── matalapok05.html
    │   └── matalapok06/      6. Valószínűségi változók és eloszlások
    │       ├── matalapok06.md
    │       └── matalapok06.html
    └── statisztika/          (rövid bemutató példa)
        ├── statisztika.md
        └── statisztika.html
```

## Használat

**Egy egész könyvtár átalakítása.** A program az alkönyvtárakat is bejárja, és minden `.md` fájlból HTML-t
készít, a `README.md` kivételével:

```bash
python3 md2html/md2html.py presentations
```

**Egyetlen fájl átalakítása:**

```bash
python3 md2html/md2html.py presentations/statisztika/statisztika.md
```

A HTML mindig a forrás `.md` mellé kerül, azonos néven (`statisztika.md` → `statisztika.html`).
A meglévő HTML felülíródik. Egyszerre több bemenet is megadható, akár vegyesen fájlok és könyvtárak.

| Kapcsoló | Jelentés |
|---|---|
| `-t`, `--theme NÉV` | `light`, `dark` vagy egy saját `.css` útvonala (az `.md`-hez képest). Felülírja a YAML `theme:` mezőt. |
| `-o`, `--output FÁJL` | Más kimeneti fájlnév. Csak egyetlen `.md` bemenetnél használható. |
| `--no-embed` | A helyi képek ne kerüljenek a HTML-be, csak hivatkozás maradjon rájuk. |

A program minden elkészült fájlt kiír a méretével együtt. Ha egy fájl hibás (pl. ismeretlen téma), arról
`HIBA` sort ír, a többit ettől függetlenül feldolgozza, a végén pedig 1-es kilépési kóddal áll le.

## A forrásfájl felépítése

```markdown
---
title: "Statisztikai alapfogalmak"
subtitle: "Leíró statisztika és a normális eloszlás"
author: "Abari Kálmán"
date: today
lang: hu
theme: dark
footer: "Lábléc minden dián"
---

# Fejezetcím

## Első dia

- Felsorolás **kiemeléssel** és képlettel: $\bar{x} = \frac{1}{n}\sum x_i$

. . .

Ez csak a következő lépésre jelenik meg.
```

### YAML fejléc

| Mező | Hatás |
|---|---|
| `title`, `subtitle`, `author`, `institute`, `date` | Ezekből készül a címdia. A `date: today` a mai dátumot adja. |
| `lang` | A dokumentum nyelve. `hu` esetén a dobozfeliratok és a gombok magyarok. |
| `theme` | `light`, `dark` vagy saját `.css`. |
| `footer` | Lábléc a tartalmi diákon. |
| `incremental: true` | Minden felsorolás pontonként jelenik meg. |

### Diák

| Szintaxis | Eredmény |
|---|---|
| `# Cím` | Fejezetcím-dia (színes háttér) |
| `## Cím` | Normál dia |
| `---` (üres sor után) | Cím nélküli új dia |
| `## Cím {.smaller}` | Kisebb betűméret |
| `## Cím {.scrollable}` | Görgethető tartalom |
| `## Cím {.center}` | Függőlegesen középre igazított tartalom |
| `## Cím {.inverse}` | Ellentétes színű (kiemelő) dia |
| `## Cím {background-color="#123456"}` | Egyedi háttérszín |
| `## Cím {background-image="kep.jpg"}` | Háttérkép |

### Tartalom

| Szintaxis | Eredmény |
|---|---|
| `. . .` | Szünet: a további tartalom a következő lépésre jelenik meg |
| `::: {.incremental}` … `:::` | A felsorolás pontonként jelenik meg |
| `::: {.fragment}` … `:::`, `[szöveg]{.fragment}` | Lépésenként megjelenő blokk vagy szövegrész |
| `::: {.notes}` … `:::` | Előadói jegyzet (vetítés közben az **N** billentyűvel jelenik meg) |
| `:::: {.columns}` + `::: {.column width="40%"}` | Hasábok |
| `::: {.callout-note}` (`tip`, `warning`, `important`, `caution`) | Kiemelő doboz. A címe a `title="…"` attribútum vagy a doboz első `##` címsora. |
| `$…$`, `$$…$$` | Soron belüli és kiemelt képlet (tizedesvessző: `5{,}5`; `\binom`, halmazjelek is) |
| `\| a \| b \|` + `: felirat` | Táblázat felirattal, igazítással (`:--`, `:-:`, `--:`) |
| `![felirat](kep.png){width=50%}` | Kép. Ha önálló bekezdésben áll, a felirata is megjelenik. |
| ```` ```python ```` | Kódblokk egyszerű szintaxisszínezéssel |
| ```` ```{=html} ```` | Nyers HTML/JavaScript, változatlanul kerül a kimenetbe |
| `[(Szerző, 2020)]{.cite}` | Halványabb, kisebb betűs hivatkozás a dián |
| `::: {.refs}` … `:::` | Irodalomjegyzék függő behúzással (minden tétel külön bekezdés) |
| `**félkövér**`, `*dőlt*`, `` `kód` ``, `~~áthúzott~~`, `x^2^`, `H~2~O`, `[link](url)` | Szokásos soron belüli formázás |

## Interaktív elemek

Az interaktív részeket ```` ```{=html} ```` blokkba kell írni, a HTML-t és a `<script>`-et együtt.
A megjelenésüket a téma CSS-osztályai adják, így világos és sötét témában is jól néznek ki:

| Osztály | Szerep |
|---|---|
| `.widget` | Keretes kártya (pl. egy SVG ábra köré) |
| `.widget .grid`, `.axis`, `.tick`, `.curve`, `.ref`, `.area`, `.area-2`, `.mean`, `.label`, `.title` | SVG-elemek: rácsvonal, tengely, feliratok, görbe, referenciagörbe, két satírszín, jelölővonal, címke, cím |
| `.widget .bar`, `.widget .dot` | Hisztogramoszlop, adatpont |
| `.legend` | Jelmagyarázat |
| `.controls` | Csúszkák és címkék oszlopa |
| `.seg` | Kapcsológomb-csoport (az aktív gomb osztálya `on`) |
| `.btn` | Önálló gomb |
| `.stats` / `.stat` | Számértékek kártyákon |
| `.grid` | Rács-elrendezés; az oszlopszám a `--cols` változóval állítható (`style="--cols:4"`) |

Minimális példa:

````markdown
## Interaktív dia

```{=html}
<div class="controls">
  <label>Érték: <output id="o">5</output>
    <input id="r" type="range" min="0" max="10" value="5"></label>
</div>
<script>
  r.oninput = () => o.value = r.value;
</script>
```
````

Teljes példák:

- `presentations/statisztika/statisztika.md`, 9. dia: a normális eloszlás sűrűségfüggvénye, állítható
  várható értékkel és szórással.
- `presentations/matalapok/matalapok01/matalapok01.md`: a mintaátlag eloszlása a mintanagyság függvényében
  (szimulációval), statisztikai erő hatásnagyság, létszám és α szerint, valamint Anscombe négy adatsora
  (`.grid`).
- `presentations/matalapok/matalapok02/matalapok02.md`: kvíz a mérési szintekről (`.btn`, `.btn.on`) és a
  mérési pontosság szemléltetése számegyenesen.
- `presentations/matalapok/matalapok03/matalapok03.md`: hisztogram állítható osztályszélességgel és
  kezdőponttal, pont-, oszlop-, kör- és eloszlásfüggvény-ábra, valamint egy váltható „átlag ± SE vagy
  egyedi adatok” ábra. Itt az első dia egy közös `window.Plot` segédobjektumot definiál, amelyet a
  későbbi diák szkriptjei használnak (a szkriptek a dokumentum sorrendjében futnak le).
- `presentations/matalapok/matalapok04/matalapok04.md`: átlag, medián és trimmelt átlag egy mozgatható
  kiugró értékkel; ferdeség a három középértékkel; csúcsosság (a farkak súlya, logaritmikus nézettel); doboz-, hegedű- és pontábra (sűrűségbecsléssel);
  szimuláció arról, miért n − 1-gyel osztunk a mintavarianciában.
- `presentations/matalapok/matalapok05/matalapok05.md`: Venn-diagram az eseményműveletekhez (SVG maszkokkal),
  a relatív gyakoriság stabilizálódása, visszatevés nélküli mintavétel, Bayes-tétel szűrőteszten
  1000 fős ikonos ábrával, és egy játszható Monty Hall-feladvány szimulációval.
- `presentations/matalapok/matalapok06/matalapok06.md`: binomiális és Poisson-eloszlás (a közelítéssel),
  standard pontskálák (z, T, IQ, sztenin), normáliseloszlás-kalkulátor számbeviteli mezőkkel, és a
  centrális határeloszlás-tétel szimulációja négy különböző populációval. A közös `window.Plot`
  segédobjektum itt statisztikai függvényeket is tartalmaz (Φ, inverz Φ, binomiális, Poisson).

Ha egy elemnek tudnia kell, mikor jelenik meg a diája, figyelheti a dia `slideenter` eseményét.

## Vetítés

| Billentyű | Művelet |
|---|---|
| → ↓ PageDown Szóköz | Következő lépés vagy dia |
| ← ↑ PageUp Backspace | Előző lépés vagy dia |
| Home / End | Első / utolsó dia |
| F | Teljes képernyő |
| N (vagy S) | Előadói jegyzetek be/ki |
| Esc | Kilépés a csúszkából (a nyilak ezután ismét lapoznak) |

- Érintőképernyőn a diák vízszintes húzással lapozhatók.
- A jobb alsó sarokban a dia sorszáma és lapozógombok vannak.
- A cím a dia számát tartalmazza (`…html#/9`), így egy adott diára közvetlenül lehet hivatkozni.
- A diák 1280×720-as logikai méretűek, és bármilyen ablakmérethez arányosan igazodnak.
- **PDF:** a böngésző nyomtatás funkciójával (Ctrl+P → Mentés PDF-ként) minden dia egy-egy oldalra kerül, és a
  lépésenként megjelenő elemek is mind látszanak.

## Témák

Mindkét téma önálló, teljes CSS fájl, és **csak a `:root` színváltozóiban térnek el** egymástól.
Új téma készítéséhez másold le a `md2html/themes/light.css` fájlt pl. `sepia.css` néven, és írd át
a `:root` blokk változóit. Ezután a téma `--theme sepia` kapcsolóval vagy `theme: sepia` fejléccel használható.

A program a CSS-t beágyazás előtt tömöríti (megjegyzések és felesleges szóközök nélkül).

## Hogyan működik

1. **Fejléc:** a YAML fejlécet egy egyszerű elemző olvassa be. A beágyazott kulcsokat (pl.
   `format: revealjs: incremental:`) egyetlen szintre lapítja.
2. **Diákra bontás:** a dokumentum a felső szintű `#` és `##` címsoroknál, illetve a `---` soroknál diákra
   bomlik. A kódblokkokon és a `:::` blokkokon belüli címsorok nem bontanak.
3. **Blokkelemzés:** minden dia tartalmát egy rekurzív elemző dolgozza fel (`:::` blokkok, listák, táblázatok,
   kódblokkok, képletek, idézetek, bekezdések), majd a soron belüli formázás következik.
4. **Képletek:** a LaTeX-képleteket egy beépített átalakító alakítja MathML-lé (törtek, gyökök, indexek,
   görög betűk, műveleti jelek, ékezetek, `\left…\right`, `\text`, `\mathrm`, `\mathbb`).
5. **Összeállítás:** a HTML-be a diák mellé bekerül a tömörített téma-CSS és egy kb. 2 KiB-os navigációs
   szkript.

## Korlátok

- A képlet-átalakító a LaTeX-nek csak egy részét ismeri. Nincsenek többsoros környezetek
  (`\begin{aligned}`, mátrixok).
- A Quarto végrehajtható kódblokkjai (```` ```{python} ````, ```` ```{r} ````) **nem futnak le**, csak kódként
  jelennek meg. Számított eredményeket a szövegbe vagy egy ```` ```{=html} ```` blokkba kell írni.
- A reveal.js-ből hiányzik a diaáttekintő nézet, a külön ablakos előadói nézet, a függőleges diák és az
  automatikus betűméret-igazítás (`.r-fit-text`).

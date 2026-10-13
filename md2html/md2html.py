#!/usr/bin/env python3
"""md2html — Quarto reveal.js-szerű Markdownból kis méretű, egyfájlos HTML diasor.

Használat:
    python3 md2html.py BEMENET [BEMENET ...] [-o kimenet.html] [--theme light|dark|út/fájl.css] [--no-embed]

BEMENET lehet egy .md fájl vagy egy könyvtár; könyvtárnál az összes benne (és
alkönyvtáraiban) lévő .md fájl átalakul (a README.md kivételével). Minden
HTML a forrás .md mellé kerül, azonos néven.

Csak a Python standard könyvtárát használja. A kimenet egyetlen HTML fájl:
a téma CSS-e (themes/*.css) és a navigációs JavaScript beágyazva, a helyi képek
data-URI-ként, a matematikai képletek natív MathML-ként (nincs KaTeX/MathJax).

Támogatott Quarto/reveal.js szintaxis (részhalmaz):
  * YAML fejléc: title, subtitle, author, institute, date, lang, footer, incremental,
    theme (light | dark | saját .css; a parancssori --theme felülírja)
  * `# Fejezet` → fejezetcím-dia, `## Cím {.class}` → dia, `---` → cím nélküli dia
  * `. . .` szünet (töredék), `::: {.incremental}`, `::: {.fragment}`, `[szöveg]{.fragment}`
  * `::: {.notes}` előadói jegyzet (N billentyű), `:::: {.columns}` / `::: {.column width="40%"}`
  * `::: {.callout-note|tip|warning|important|caution}`
  * dia-attribútumok: `.smaller .scrollable .center .inverse`, `background-color`, `background-image`
  * `$...$`, `$$...$$` (LaTeX-részhalmaz → MathML), csőtáblázat (`: felirat`), képek `{width=..}`
  * ```` ```{=html} ```` nyers HTML/JS blokk — ezzel készülnek az interaktív elemek
"""
import argparse
import base64
import datetime
import html
import mimetypes
import re
import sys
from pathlib import Path

THEMES = Path(__file__).resolve().parent / 'themes'
CFG = {'base': Path('.'), 'embed': True, 'hu': False}


def esc(s, quote=True):
    return html.escape(str(s), quote)


# ---------------------------------------------------------------- YAML, attribútumok

def unq(v):
    v = v.strip()
    if len(v) > 1 and v[0] == v[-1] and v[0] in '"\'':
        return v[1:-1]
    return {'true': True, 'false': False}.get(v, v)


def front_matter(text):
    m = re.match(r'---[ \t]*\n(.*?)\n---[ \t]*\n', text, re.S)
    if not m:
        return {}, text
    meta, key = {}, None
    for line in m.group(1).splitlines():
        if not line.strip() or line.lstrip().startswith('#'):
            continue
        li = re.match(r'\s*-\s+(?:name:\s*)?(.*)', line)
        if li and key:
            prev = meta.get(key)
            meta[key] = (prev if isinstance(prev, list) else []) + [unq(li.group(1))]
            continue
        kv = re.match(r'\s*([\w-]+):\s*(.*)', line)
        if kv:  # beágyazott kulcsokat laposan kezelünk (format: revealjs: incremental: …)
            key = kv.group(1)
            meta[key] = unq(kv.group(2)) if kv.group(2) else ''
    if meta.get('date') == 'today':
        meta['date'] = datetime.date.today().isoformat()
    return meta, text[m.end():]


ATTR = re.compile(r'''([#.][\w:-]+)|([\w-]+)=("[^"]*"|'[^']*'|[^\s}]+)''')


def attrs(s):
    id_, cls, kv = '', [], {}
    for m in ATTR.finditer(s.strip().strip('{}')):
        if m.group(1):
            if m.group(1)[0] == '#':
                id_ = m.group(1)[1:]
            else:
                cls.append(m.group(1)[1:])
        else:
            kv[m.group(2)] = str(unq(m.group(3)))
    return id_, cls, kv


def attr_html(id_='', cls=(), kv=None):
    out = f' id="{esc(id_)}"' if id_ else ''
    if cls:
        out += f' class="{esc(" ".join(cls))}"'
    for k, v in (kv or {}).items():
        out += f' {k}="{esc(v)}"'
    return out


def to_style(kv):
    """width=…, top=… stb. → style; a puszta szám px."""
    st = [kv.pop('style')] if 'style' in kv else []
    for k in ('width', 'height', 'top', 'left', 'right', 'bottom'):
        if k in kv:
            v = kv.pop(k)
            unit = 'px' if re.fullmatch(r'[\d.]+', v) else ''
            st.append(f'{k}:{v}{unit}')
    if st:
        kv['style'] = ';'.join(st)
    return kv


def data_uri(src):
    p = CFG['base'] / src
    if not CFG['embed'] or re.match(r'[a-z]+:', src) or not p.is_file():
        return src
    mime = mimetypes.guess_type(p.name)[0] or 'application/octet-stream'
    return f'data:{mime};base64,' + base64.b64encode(p.read_bytes()).decode()


# ---------------------------------------------------------------- LaTeX → MathML

GREEK = dict(zip(*[iter(
    'alpha α beta β gamma γ delta δ epsilon ε varepsilon ε zeta ζ eta η theta θ vartheta ϑ iota ι '
    'kappa κ lambda λ mu μ nu ν xi ξ pi π rho ρ sigma σ tau τ upsilon υ phi φ varphi φ chi χ psi ψ '
    'omega ω Gamma Γ Delta Δ Theta Θ Lambda Λ Xi Ξ Pi Π Sigma Σ Phi Φ Psi Ψ Omega Ω'.split())] * 2))
OPS = dict(zip(*[iter(
    'cdot · times × div ÷ pm ± mp ∓ leq ≤ le ≤ geq ≥ ge ≥ neq ≠ ne ≠ approx ≈ sim ∼ equiv ≡ propto ∝ '
    'infty ∞ to → rightarrow → leftarrow ← Rightarrow ⇒ iff ⇔ in ∈ notin ∉ subset ⊂ cup ∪ cap ∩ '
    'forall ∀ exists ∃ partial ∂ nabla ∇ ldots … dots … cdots ⋯ sum ∑ prod ∏ int ∫ mid ∣ ast ∗ '
    'circ ∘ lt < gt > ll ≪ gg ≫ langle ⟨ rangle ⟩ setminus ∖ subseteq ⊆ supseteq ⊇ supset ⊃ '
    'emptyset ∅ varnothing ∅ neg ¬ land ∧ lor ∨ lvert | rvert | vert | Vert ‖'.split())] * 2))
FUNCS = set('exp ln log lg sin cos tan max min lim det sup inf arg Pr'.split())
ACCENT = {'bar': '¯', 'overline': '¯', 'hat': '^', 'widehat': '^', 'tilde': '~',
          'widetilde': '~', 'vec': '→', 'dot': '˙', 'ddot': '¨'}
SPACE = {',': '0.167em', ':': '0.222em', ';': '0.278em', ' ': '0.25em',
         'quad': '1em', 'qquad': '2em', '!': '', '\\': ''}
BB = {'R': 'ℝ', 'N': 'ℕ', 'Z': 'ℤ', 'Q': 'ℚ', 'C': 'ℂ', 'E': '𝔼', 'P': 'ℙ'}
DELIM = {'\\{': '{', '\\}': '}', '\\langle': '⟨', '\\rangle': '⟩', '\\lvert': '|',
         '\\rvert': '|', '\\|': '‖', '\\lbrace': '{', '\\rbrace': '}'}
TEXTOK = re.compile(r'\\[A-Za-z]+|\\.|\d+(?:(?:\.|\{,\})\d+)?|\s+|.', re.S)


def tex(src, display=False):
    toks, p = TEXTOK.findall(src), [0]

    def peek():
        while p[0] < len(toks) and toks[p[0]].isspace():
            p[0] += 1
        return toks[p[0]] if p[0] < len(toks) else None

    def take():
        t = peek()
        if t is not None:
            p[0] += 1
        return t

    def text_arg():
        if take() != '{':
            return ''
        out, depth = '', 1
        while p[0] < len(toks):
            t = toks[p[0]]
            p[0] += 1
            depth += (t == '{') - (t == '}')
            if not depth:
                break
            out += t[1:] if t[0] == '\\' and len(t) == 2 else t
        return out

    def arg():
        return atom(take())

    def script(a, sub, sup):
        big = display and re.match(r'<m[oi]>(∑|∏|lim|max|min)<', a)
        if sub and sup:
            tag, kids = ('munderover' if big else 'msubsup'), a + sub + sup
        elif sub:
            tag, kids = ('munder' if big else 'msub'), a + sub
        else:
            tag, kids = ('mover' if big else 'msup'), a + sup
        return f'<{tag}>{kids}</{tag}>'

    def seq(end):
        out, prev = '', ''
        while True:
            t = take()
            if t is None or t == end:
                return out
            if t in '^_':
                p[0] -= 1
                a = '<mrow></mrow>'
            elif t in ('-', '+', '\\pm') and (not prev or prev.startswith('<mo') and not re.match(r'<mo[^>]*>[)\]}|⟩]', prev)):
                a = atom(t).replace('<mo>', '<mo form="prefix">', 1)  # előjel, nem kivonás
            else:
                a = atom(t)
            prev = a
            sub = sup = None
            while peek() in ('^', '_', "'"):
                op = take()
                if op == "'":
                    sup = '<mo>′</mo>'
                elif op == '^':
                    sup = arg()
                else:
                    sub = arg()
            out += script(a, sub, sup) if sub or sup else a

    def delim(d):
        if d in (None, '.'):
            return ''
        return f'<mo stretchy="true">{esc(DELIM.get(d, d), False)}</mo>'

    def atom(t):
        if t is None:
            return ''
        if t == '{':
            return '<mrow>' + seq('}') + '</mrow>'
        if t[0] == '\\' and len(t) > 1:
            c = t[1:]
            if c in ('frac', 'dfrac', 'tfrac'):
                return f'<mfrac>{arg()}{arg()}</mfrac>'
            if c == 'binom':
                return f'<mrow><mo>(</mo><mfrac linethickness="0">{arg()}{arg()}</mfrac><mo>)</mo></mrow>'
            if c == 'sqrt':
                if peek() == '[':
                    take()
                    idx = seq(']')
                    return f'<mroot>{arg()}<mrow>{idx}</mrow></mroot>'
                return f'<msqrt>{arg()}</msqrt>'
            if c in ('text', 'mbox', 'textrm'):
                return '<mtext>' + esc(text_arg(), False).replace(' ', ' ') + '</mtext>'
            if c in ('mathrm', 'operatorname'):
                return f'<mi mathvariant="normal">{esc(text_arg(), False)}</mi>'
            if c == 'mathbb':
                return '<mi mathvariant="normal">' + ''.join(BB.get(ch, ch) for ch in text_arg()) + '</mi>'
            if c in ('mathbf', 'boldsymbol'):
                return f'<mrow style="font-weight:bold">{arg()}</mrow>'
            if c in ACCENT:
                return f'<mover accent="true">{arg()}<mo>{ACCENT[c]}</mo></mover>'
            if c == 'left':
                d1 = take()
                inner = seq('\\right')
                return f'<mrow>{delim(d1)}{inner}{delim(take())}</mrow>'
            if c in SPACE:
                return f'<mspace width="{SPACE[c]}"></mspace>' if SPACE[c] else ''
            if c in GREEK:
                g = GREEK[c]
                return f'<mi mathvariant="normal">{g}</mi>' if g.isupper() else f'<mi>{g}</mi>'
            if c in OPS:
                return f'<mo>{esc(OPS[c], False)}</mo>'
            if c in FUNCS:
                return f'<mi>{c}</mi>'
            if len(c) == 1:  # \{ \% \_ …
                return f'<mo>{esc(c, False)}</mo>'
            return f'<mi>{esc(c, False)}</mi>'
        if t[0].isdigit():
            return '<mn>' + t.replace('{,}', ',') + '</mn>'
        if t.isalpha():
            return f'<mi>{t}</mi>'
        return f'<mo>{esc({"-": "−", "*": "∗"}.get(t, t), False)}</mo>'

    body = seq(None)
    disp = ' display="block"' if display else ''
    return f'<math{disp}>{body}</math>'


# ---------------------------------------------------------------- soron belüli elemek

IMG = r'!\[([^\]]*)\]\(([^)\s]+)(?:\s+"([^"]*)")?\)(\{[^}]*\})?'


def img(alt, src, title=None, a=None):
    id_, cls, kv = attrs(a or '')
    t = f' title="{esc(title)}"' if title else ''
    return f'<img src="{esc(data_uri(src))}" alt="{esc(alt)}"{t}{attr_html(id_, cls, to_style(kv))}>'


def inline(s, stash=None):
    top = stash is None  # a beágyazott hívások (link-, span-szöveg) a külső tárolót használják
    if top:
        stash = []

    def keep(h):
        stash.append(h)
        return f'\x00{len(stash) - 1}\x00'

    def link(m):
        id_, cls, kv = attrs(m.group(4) or '')
        t = f' title="{esc(m.group(3))}"' if m.group(3) else ''
        return keep(f'<a href="{esc(m.group(2))}"{t}{attr_html(id_, cls, kv)}>{inline(m.group(1), stash)}</a>')

    def span(m):
        id_, cls, kv = attrs(m.group(2))
        return keep(f'<span{attr_html(id_, cls, to_style(kv))}>{inline(m.group(1), stash)}</span>')

    s = re.sub(r'(`+)(.+?)\1', lambda m: keep(f'<code>{esc(m.group(2).strip(), False)}</code>'), s)
    s = re.sub(r'\$\$(.+?)\$\$', lambda m: keep(tex(m.group(1), True)), s, flags=re.S)
    s = re.sub(r'(?<![\\$\w])\$(?!\s)([^$\n]+?)(?<!\s)\$(?![\w$])', lambda m: keep(tex(m.group(1))), s)
    s = re.sub(r'\\([\\`*_{}\[\]()#+\-.!$|~^<>"])', lambda m: keep(esc(m.group(1), False)), s)
    s = re.sub(r'<(https?://[^>\s]+)>', lambda m: keep(f'<a href="{esc(m.group(1))}">{esc(m.group(1), False)}</a>'), s)
    s = re.sub(r'</?[A-Za-z][^<>]*>|<!--.*?-->|&#?\w+;', lambda m: keep(m.group(0)), s)
    s = re.sub(IMG, lambda m: keep(img(*m.groups())), s)
    s = re.sub(r'\[([^\]]+)\]\(([^)\s]+)(?:\s+"([^"]*)")?\)(\{[^}]*\})?', link, s)
    s = re.sub(r'\[([^\]]+)\]\{([^}]*)\}', span, s)
    s = esc(s, False)
    s = re.sub(r'\*\*(?!\s)(.+?)(?<!\s)\*\*|__(.+?)__', lambda m: f'<strong>{m.group(1) or m.group(2)}</strong>', s)
    s = re.sub(r'\*(?!\s)(.+?)(?<!\s)\*|(?<!\w)_(?!\s)(.+?)(?<!\s)_(?!\w)', lambda m: f'<em>{m.group(1) or m.group(2)}</em>', s)
    s = re.sub(r'~~(.+?)~~', r'<del>\1</del>', s)
    s = re.sub(r'\^([^\s^]+)\^', r'<sup>\1</sup>', s)
    s = re.sub(r'~([^\s~]+)~', r'<sub>\1</sub>', s)
    s = s.replace('---', '—').replace('--', '–').replace('...', '…')
    s = re.sub(r'(?: {2,}|\\)\n', '<br>', s)
    while top and '\x00' in s:
        s = re.sub(r'\x00(\d+)\x00', lambda m: stash[int(m.group(1))], s)
    return s


# ---------------------------------------------------------------- blokkok

FENCE = re.compile(r'^(\s*)(`{3,}|~{3,})\s*(.*)$')
DIV = re.compile(r'^(:{3,})\s*(\{.*\}|[\w-]+)\s*$')
DIVEND = re.compile(r'^:{3,}\s*$')
HEAD = re.compile(r'^(#{1,6})\s+(.*?)\s*(\{[^}]*\})?\s*$')
LIST = re.compile(r'^(\s*)([-*+]|\d+[.)])\s+(.*)$')
SEP = re.compile(r'^(?=.*\|)\s*\|?\s*:?-+:?\s*(\|\s*:?-+:?\s*)*\|?\s*$')  # legalább egy | kell
CALLOUT = {'note': ('Note', 'Megjegyzés'), 'tip': ('Tip', 'Tipp'), 'warning': ('Warning', 'Figyelem'),
           'important': ('Important', 'Fontos'), 'caution': ('Caution', 'Vigyázat')}
TOK = re.compile(r'(?P<c>#[^\n]*|//[^\n]*)|(?P<s>"(?:\\.|[^"\\\n])*"|\'(?:\\.|[^\'\\\n])*\')'
                 r'|(?P<n>\b\d+(?:\.\d+)?\b)|(?P<k>\b(?:def|return|if|else|elif|for|while|in|import|from|as|'
                 r'class|function|const|let|var|new|true|false|True|False|None|null|NULL|and|or|not|lambda|library)\b)')


def indent(l):
    return len(l) - len(l.lstrip(' '))


def dedent(l, k):
    return l[min(k, indent(l)):]


def closes(mark, l):
    return re.match(r'\s*' + re.escape(mark[0]) + '{%d,}\\s*$' % len(mark), l)


def fence_end(lines, i, mark):
    j = i + 1
    while j < len(lines) and not closes(mark, lines[j]):
        j += 1
    return j


def div_end(lines, i):
    depth, j = 1, i + 1
    while j < len(lines):
        s = lines[j].strip()
        f = FENCE.match(lines[j])
        if f:
            j = fence_end(lines, j, f.group(2))
        elif DIVEND.match(s):
            depth -= 1
            if not depth:
                break
        elif DIV.match(s):
            depth += 1
        j += 1
    return j


def starts_block(l):
    s = l.strip()
    return bool(FENCE.match(l) or DIV.match(s) or DIVEND.match(s) or HEAD.match(s)
                or s.startswith(('$$', '>')) or LIST.match(l) or s == '. . .')


def highlight(code):
    out, pos = [], 0
    for m in TOK.finditer(code):
        out += [esc(code[pos:m.start()], False), f'<span class="t{m.lastgroup}">{esc(m.group(), False)}</span>']
        pos = m.end()
    return ''.join(out) + esc(code[pos:], False)


def code_block(info, body):
    info = info.strip()
    if info.replace(' ', '') in ('{=html}', '{=html5}'):
        return body
    if info.startswith('{'):
        _, cls, _ = attrs(info)
        words = info.strip('{} ').split()
        lang = cls[0] if cls else (words[0] if words and '=' not in words[0] else '')
    else:
        lang = info.split()[0] if info else ''
    code = highlight(body) if lang and lang not in ('html', 'css', 'text', 'md', 'markdown') else esc(body, False)
    cls = f' class="language-{esc(lang)}"' if lang else ''
    return f'<pre><code{cls}>{code}</code></pre>'


def table(rows, cap):
    def cells(r):
        return [c.strip() for c in re.split(r'(?<!\\)\|', r.strip().strip('|'))]

    def sty(a):
        return f' style="text-align:{a}"' if a else ''

    al = ['center' if c[:1] == ':' and c[-1:] == ':' else 'right' if c[-1:] == ':' else ''
          for c in cells(rows[1])] + [''] * 50
    head = ''.join(f'<th{sty(a)}>{inline(c)}</th>' for c, a in zip(cells(rows[0]), al))
    body = ''.join('<tr>' + ''.join(f'<td{sty(a)}>{inline(c)}</td>' for c, a in zip(cells(r), al)) + '</tr>'
                   for r in rows[2:])
    cap = f'<caption>{inline(cap)}</caption>' if cap else ''
    return f'<table>{cap}<thead><tr>{head}</tr></thead><tbody>{body}</tbody></table>'


def parse_list(lines, i, ctx):
    n, m = len(lines), LIST.match(lines[i])
    ind, ordered = len(m.group(1)), m.group(2)[0].isdigit()
    start = int(m.group(2)[:-1]) if ordered else 1
    items, loose, cind = [], False, 0

    def sibling(l):
        mm = LIST.match(l)
        return mm and len(mm.group(1)) == ind and mm.group(2)[0].isdigit() == ordered

    while i < n:
        l = lines[i]
        if sibling(l):
            mm = LIST.match(l)
            cind = mm.start(3)
            items.append([mm.group(3)])
        elif not l.strip():
            j = i
            while j < n and not lines[j].strip():
                j += 1
            if j < n and (indent(lines[j]) > ind or sibling(lines[j])):
                loose = True
                items[-1] += [''] * (j - i)
                i = j
                continue
            break
        elif indent(l) > ind:
            items[-1].append(dedent(l, cind))
        elif lines[i - 1].strip() and not starts_block(l):
            items[-1].append(l.strip())  # „lusta” folytatósor
        else:
            break
        i += 1

    li = ' class="fragment"' if ctx.get('inc') else ''
    body = ''
    for it in items:
        while it and not it[-1].strip():
            it.pop()
        h = blocks(it, ctx)
        if not loose:
            h = re.sub(r'^<p>(.*?)</p>', r'\1', h, count=1, flags=re.S)
        body += f'<li{li}>{h}</li>'
    tag = 'ol' if ordered else 'ul'
    st = f' start="{start}"' if start != 1 else ''
    return f'<{tag}{st}>{body}</{tag}>', i


def div(spec, inner, ctx):
    id_, cls, kv = attrs(spec) if spec.startswith('{') else ('', [spec], {})
    c2 = dict(ctx, inc='incremental' in cls or (ctx.get('inc') and 'nonincremental' not in cls))
    if 'notes' in cls:
        return f'<aside class="notes">{blocks(inner, c2)}</aside>'
    co = next((c[8:] for c in cls if c.startswith('callout-')), None)
    if co is not None:
        title = kv.get('title', '')
        k = next((x for x, l in enumerate(inner) if l.strip()), None)
        if not title and k is not None and HEAD.match(inner[k].strip()):
            title, inner = HEAD.match(inner[k].strip()).group(2), inner[k + 1:]
        title = title or CALLOUT.get(co, (co.title(),) * 2)[CFG['hu']]
        return (f'<div{attr_html(id_, ["callout"] + cls)}><p class="callout-title">{inline(title)}</p>'
                f'{blocks(inner, c2)}</div>')
    return f'<div{attr_html(id_, cls, to_style(kv))}>{blocks(inner, c2)}</div>'


def split_pause(lines):
    parts, fence, depth = [[]], None, 0
    for l in lines:
        s = l.strip()
        if fence:
            if closes(fence, l):
                fence = None
        elif FENCE.match(l):
            fence = FENCE.match(l).group(2)
        elif DIV.match(s):
            depth += 1
        elif DIVEND.match(s):
            depth -= 1
        elif s == '. . .' and depth == 0:
            parts.append([])
            continue
        parts[-1].append(l)
    return parts


def blocks(lines, ctx):
    parts = split_pause(lines)
    return block_seq(parts[0], ctx) + ''.join(
        f'<div class="fragment">{block_seq(p, ctx)}</div>' for p in parts[1:])


def block_seq(lines, ctx):
    out, i, n = [], 0, len(lines)
    while i < n:
        l = lines[i]
        s = l.strip()
        if not s:
            i += 1
            continue
        m = FENCE.match(l)
        if m:
            j = fence_end(lines, i, m.group(2))
            ind = len(m.group(1))
            out.append(code_block(m.group(3), '\n'.join(dedent(x, ind) for x in lines[i + 1:j])))
            i = j + 1
            continue
        m = DIV.match(s)
        if m:
            j = div_end(lines, i)
            out.append(div(m.group(2), lines[i + 1:j], ctx))
            i = j + 1
            continue
        if DIVEND.match(s):
            i += 1
            continue
        m = HEAD.match(s)
        if m:
            lv = len(m.group(1))
            id_, cls, kv = attrs(m.group(3) or '')
            out.append(f'<h{lv}{attr_html(id_, cls, kv)}>{inline(m.group(2))}</h{lv}>')
            i += 1
            continue
        if s.startswith('$$'):
            end = re.compile(r'\$\$\s*(\{[^}]*\})?\s*$')
            text, j = s[2:], i
            while not end.search(text) and j + 1 < n:
                j += 1
                text += '\n' + lines[j].strip()
            out.append(tex(end.sub('', text), True))
            i = j + 1
            continue
        if s.startswith('>'):
            j = i
            while j < n and lines[j].strip():
                j += 1
            quoted = [re.sub(r'^\s*> ?', '', x) for x in lines[i:j]]
            out.append(f'<blockquote>{blocks(quoted, ctx)}</blockquote>')
            i = j
            continue
        if s.startswith('|') and i + 1 < n and SEP.match(lines[i + 1]):
            j = i + 2
            while j < n and lines[j].strip().startswith('|'):
                j += 1
            k, cap = j, ''
            while k < n and not lines[k].strip():
                k += 1
            if k < n and lines[k].strip().startswith(': '):
                cap, j = re.sub(r'\s*\{[^}]*\}\s*$', '', lines[k].strip()[2:]), k + 1
            out.append(table(lines[i:j] if not cap else [x for x in lines[i:k] if x.strip()], cap))
            i = j
            continue
        if re.fullmatch(r'(\*\s*){3,}|(-\s*){3,}|(_\s*){3,}', s):
            out.append('<hr>')
            i += 1
            continue
        if LIST.match(l):
            h, i = parse_list(lines, i, ctx)
            out.append(h)
            continue
        if re.match(r'</?[A-Za-z][\w-]*[\s>/]|<!--', s):
            j = i
            while j < n and lines[j].strip():
                j += 1
            out.append('\n'.join(lines[i:j]))
            i = j
            continue
        j = i + 1
        while j < n and lines[j].strip() and not starts_block(lines[j]):
            j += 1
        text = '\n'.join(x.lstrip() for x in lines[i:j]).rstrip()
        m = re.fullmatch(IMG, text)
        if m and m.group(1):
            out.append(f'<figure>{img(*m.groups())}<figcaption>{inline(m.group(1))}</figcaption></figure>')
        else:
            out.append(f'<p>{inline(text)}</p>')
        i = j
    return ''.join(out)


# ---------------------------------------------------------------- diák

def split_slides(body):
    slides, cur, fence, depth = [], None, None, 0
    lines = body.split('\n')
    for k, l in enumerate(lines):
        s = l.strip()
        if fence:
            if closes(fence, l):
                fence = None
        elif FENCE.match(l):
            fence = FENCE.match(l).group(2)
        elif DIV.match(s):
            depth += 1
        elif DIVEND.match(s):
            depth -= 1
        elif depth == 0:
            m = HEAD.match(l)
            if m and len(m.group(1)) <= 2:
                cur = {'lvl': len(m.group(1)), 'title': m.group(2), 'attr': m.group(3) or '', 'lines': []}
                slides.append(cur)
                continue
            if s == '---' and (k == 0 or not lines[k - 1].strip()):
                cur = {'lvl': 2, 'title': '', 'attr': '', 'lines': []}
                slides.append(cur)
                continue
        if cur is None:
            if not s:
                continue
            cur = {'lvl': 2, 'title': '', 'attr': '', 'lines': []}
            slides.append(cur)
        cur['lines'].append(l)
    return slides


def slide_html(sl, ctx):
    id_, cls, kv = attrs(sl['attr'])
    body = blocks(sl['lines'], ctx)
    if not (sl['title'] or body.strip() or kv):
        return ''
    if sl['lvl'] == 1:
        cls = ['part'] + cls
    st = []
    if 'background-color' in kv:
        st.append('background-color:' + kv['background-color'])
    if 'background-image' in kv:
        size = kv.get('background-size', 'cover')
        st.append(f'background:url("{data_uri(kv["background-image"])}") center/{size} no-repeat')
    lv = sl['lvl']
    h = f'<h{lv}>{inline(sl["title"])}</h{lv}>' if sl['title'] else ''
    return f'<section{attr_html(id_, cls, {"style": ";".join(st)} if st else None)}>{h}{body}</section>'


def title_slide(meta):
    au = meta.get('author', '')
    meta = dict(meta, author=', '.join(au) if isinstance(au, list) else au)
    out = f'<h1 class="title">{inline(str(meta["title"]))}</h1>'
    for k in ('subtitle', 'author', 'institute', 'date'):
        if meta.get(k):
            out += f'<p class="{k}">{inline(str(meta[k]))}</p>'
    return f'<section class="title-slide">{out}</section>'


# ---------------------------------------------------------------- futtatókörnyezet (navigáció)

RUNTIME = r"""
(()=>{const d=document,b=d.body,deck=d.querySelector('.deck'),S=[...deck.querySelectorAll(':scope>section')],
bar=d.querySelector('.progress i'),num=d.querySelector('.num');let c=-1;
const fit=()=>deck.style.transform=`translate(-50%,-50%) scale(${Math.min(innerWidth/1280,innerHeight/720)})`;
const F=s=>[...s.querySelectorAll('.fragment')];
function go(n,back){n=Math.max(0,Math.min(S.length-1,n|0));if(n===c)return;c=n;
S.forEach((s,i)=>{s.classList.toggle('past',i<n);s.classList.toggle('present',i==n);s.classList.toggle('future',i>n)});
const s=S[n],bg=getComputedStyle(s).backgroundColor;F(s).forEach(f=>f.classList.toggle('visible',!!back));
b.style.backgroundColor=/^rgba\(.*, 0\)$|transparent/.test(bg)?'':bg;
bar.style.width=(S.length>1?n/(S.length-1)*100:100)+'%';num.textContent=n+1+' / '+S.length;
history.replaceState(null,'','#/'+(n+1));s.dispatchEvent(new Event('slideenter',{bubbles:true}))}
function next(){const f=F(S[c]).find(f=>!f.classList.contains('visible'));f?f.classList.add('visible'):go(c+1)}
function prev(){const f=F(S[c]).filter(f=>f.classList.contains('visible')).pop();f?f.classList.remove('visible'):go(c-1,1)}
d.addEventListener('keydown',e=>{const t=e.target,k=e.key;
if(e.ctrlKey||e.metaKey||e.altKey||t.closest('input,textarea,select,[contenteditable]')&&k!='Escape'||t.closest('button')&&(k==' '||k=='Enter'))return;
if(['ArrowRight','ArrowDown','PageDown',' '].includes(k))next();
else if(['ArrowLeft','ArrowUp','PageUp','Backspace'].includes(k))prev();
else if(k=='Home')go(0);else if(k=='End')go(S.length-1);
else if(k=='f')d.fullscreenElement?d.exitFullscreen():d.documentElement.requestFullscreen();
else if(k=='n'||k=='s')b.classList.toggle('show-notes');
else if(k=='Escape')t.blur&&t.blur();else return;e.preventDefault()});
d.querySelector('.next').onclick=e=>{next();e.currentTarget.blur()};
d.querySelector('.prev').onclick=e=>{prev();e.currentTarget.blur()};
let x0=null;deck.addEventListener('pointerdown',e=>{x0=e.pointerType=='touch'&&!e.target.closest('input')?e.clientX:null});
deck.addEventListener('pointerup',e=>{if(x0==null)return;const dx=e.clientX-x0;x0=null;if(Math.abs(dx)>50)dx<0?next():prev()});
const h=()=>+(/\d+/.exec(location.hash)||[1])[0]-1;
addEventListener('resize',fit);addEventListener('hashchange',()=>go(h()));fit();go(h())})();
"""


def min_css(s):
    s = re.sub(r'/\*.*?\*/', '', s, flags=re.S)
    s = re.sub(r'\s+', ' ', s)
    s = re.sub(r'\s*([{};,>])\s*', r'\1', s)
    s = re.sub(r':\s+', ':', s)
    return s.replace(';}', '}').strip()


def min_js(s):
    return '\n'.join(l.strip() for l in s.splitlines() if l.strip() and not l.strip().startswith('//'))


def theme_css(name, base):
    """Beépített téma neve (themes/<név>.css) vagy egy .css fájl útvonala (az .md-hez képest)."""
    p = THEMES / f'{name}.css'
    if not p.is_file():
        p = base / name
    if not p.is_file():
        avail = ', '.join(sorted(x.stem for x in THEMES.glob('*.css')))
        raise ValueError(f'ismeretlen téma: {name} (beépített: {avail})')
    return p.read_text(encoding='utf-8')


def convert(md, theme=None, base=Path('.'), embed=True):
    md = md.replace('\r\n', '\n').expandtabs(4)
    meta, body = front_matter(md)
    css = theme_css(str(theme or meta.get('theme') or 'light'), base)
    lang = str(meta.get('lang', 'en'))
    CFG.update(base=base, embed=embed, hu=lang.startswith('hu'))
    ctx = {'inc': meta.get('incremental') is True}
    secs = [title_slide(meta)] if meta.get('title') else []
    secs += [h for h in (slide_html(sl, ctx) for sl in split_slides(body)) if h]
    footer = f'<footer>{inline(str(meta["footer"]))}</footer>' if meta.get('footer') else ''
    title = re.sub(r'<[^>]+>', '', inline(str(meta.get('pagetitle') or meta.get('title') or 'Slides')))
    prev, nxt = ('Előző', 'Következő') if CFG['hu'] else ('Previous', 'Next')
    return (f'<!doctype html><html lang="{esc(lang)}"><meta charset="utf-8">'
            f'<meta name="viewport" content="width=device-width,initial-scale=1"><title>{title}</title>'
            f'<style>{min_css(css)}</style><div class="deck">{"".join(secs)}{footer}</div>'
            f'<div class="progress"><i></i></div><nav class="ctl"><button class="prev" aria-label="{prev}">‹</button>'
            f'<span class="num"></span><button class="next" aria-label="{nxt}">›</button></nav>'
            f'<script>{min_js(RUNTIME)}</script></html>\n')


def find_md(paths):
    """A megadott fájlok, illetve a könyvtárakban (rekurzívan) talált .md fájlok, README.md nélkül."""
    files = []
    for p in paths:
        if p.is_dir():
            files += sorted(f for f in p.rglob('*.md') if f.name.lower() != 'readme.md')
        elif p.is_file():
            files.append(p)
        else:
            sys.exit(f'Nem található: {p}')
    return files


def main():
    ap = argparse.ArgumentParser(description='Quarto reveal.js-szerű Markdown → egyfájlos HTML diasor')
    ap.add_argument('input', type=Path, nargs='+', help='.md fájl vagy könyvtár (az összes .md-t átalakítja)')
    ap.add_argument('-o', '--output', type=Path, help='kimeneti fájl (csak egyetlen .md bemenetnél)')
    ap.add_argument('-t', '--theme', help='light | dark | saját .css útvonala (alapértelmezés: a YAML theme, különben light)')
    ap.add_argument('--no-embed', action='store_true', help='helyi képek ne kerüljenek data-URI-ként a fájlba')
    a = ap.parse_args()
    files = find_md(a.input)
    if not files:
        sys.exit('Nincs átalakítható .md fájl.')
    if a.output and (len(files) > 1 or a.input[0].is_dir()):
        sys.exit('Az -o csak egyetlen .md fájl bemenetnél használható.')
    failed = 0
    for f in files:
        out = a.output or f.with_suffix('.html')
        try:
            doc = convert(f.read_text(encoding='utf-8'), a.theme, f.resolve().parent, not a.no_embed)
        except (ValueError, OSError) as e:
            failed += 1
            print(f'HIBA  {f}: {e}', file=sys.stderr)
            continue
        out.write_text(doc, encoding='utf-8')
        print(f'{out}  ({len(doc.encode()) / 1024:.1f} KiB)', file=sys.stderr)
    sys.exit(1 if failed else 0)


if __name__ == '__main__':
    main()

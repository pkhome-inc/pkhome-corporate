"""FUNDIA 表示切替（2026-11-26）
使い方: python3 tools/fundia_toggle.py off   # 非表示
        python3 tools/fundia_toggle.py on    # 表示（元どおり）
GitHub の Actions「FUNDIA 表示切替」から実行すると、コミットと公開まで自動で行う。
初回だけ、FUNDIA 部分に data-fundia の目印を付ける。文言は消さない。
"""
import pathlib
import re
import sys

MODE = sys.argv[1] if len(sys.argv) > 1 else ""
assert MODE in ("on", "off"), "on か off を指定"
ROOT = pathlib.Path(__file__).resolve().parent.parent

DESC_ON = "PKHOME株式会社 — 最新のAIで住まいの当たり前を更新する不動産テック企業。賃貸管理のAI運営「すむすむ」、不動産クラウドファンディング「FUNDIA」。"
DESC_OFF = "PKHOME株式会社 — 最新のAIで住まいの当たり前を更新する不動産テック企業。賃貸管理のAI運営「すむすむ」。"

NOTE = """<!-- FUNDIA 表示スイッチ（2026-11-26）
     <html data-fundia="off"> = FUNDIA 部分を非表示 / "on" = 表示
     切替: GitHub の Actions「FUNDIA 表示切替」で off / on を選んで実行（tools/fundia_toggle.py）
     確認用: URL に ?fundia=1 を付けると、その場だけ表示される -->
"""
SCRIPT = """<script>(function(){try{if(/[?&]fundia=1(&|$)/.test(location.search))document.documentElement.setAttribute('data-fundia','on')}catch(e){}})();</script>
"""
CSS_INDEX = """<style>
html[data-fundia="off"] [data-fundia]{display:none!important}
html:not([data-fundia="off"]) [data-fundia-alt]{display:none!important}
html[data-fundia="off"] .pillars{grid-template-columns:1fr}
</style>
"""
CSS_SUB = """<style>
html[data-fundia="off"] [data-fundia]{display:none!important}
</style>
"""
LI = '<li><a href="https://fundia.net" target="_blank" rel="noopener">FUNDIA</a></li>'
BIZ = '<div><h2 class="h2 mask reveal-h"><span>ふたつの事業</span></h2><p class="lead reveal">運営する側と、投資する側。不動産の両端に、PKHOMEは立ちます。</p></div>'
BIZ_ALT = '<div data-fundia-alt><h2 class="h2 mask reveal-h"><span>私たちの事業</span></h2><p class="lead reveal">管理会社を引き継ぎ、AIで運営する。住まいの現場から、当たり前を更新します。</p></div>'

MARKS = {
    "index.html": [
        ('<html lang="ja">', '<html lang="ja" data-fundia="off">', 1),
        ('<meta name="description"', '<!-- FUNDIA ON時の description: ' + DESC_ON + ' -->\n<meta name="description"', 1),
        ("</head>", NOTE + CSS_INDEX + SCRIPT + "</head>", 1),
        (LI, LI.replace("<li>", "<li data-fundia>"), 2),
        ("「すむすむ」と、一口五万円からの不動産投資「FUNDIA」。", "「すむすむ」<span data-fundia>と、一口五万円からの不動産投資「FUNDIA」</span>。", 1),
        ('<a class="en" href="https://fundia.net"', '<a class="en" data-fundia href="https://fundia.net"', 1),
        ("<span>FUNDIA — <em>from ¥50,000</em></span>", "<span data-fundia>FUNDIA — <em>from ¥50,000</em></span>", 1),
        (BIZ, BIZ.replace("<div>", "<div data-fundia>", 1) + BIZ_ALT, 1),
        ('<a class="pillar" href="https://fundia.net"', '<a class="pillar" data-fundia href="https://fundia.net"', 1),
        ('<section class="light" id="fundia">', '<section class="light" id="fundia" data-fundia>', 1),
        ("（管理会社の事業承継・AI運営）／不動産クラウドファンディング「FUNDIA」の運営／", "（管理会社の事業承継・AI運営）<span data-fundia>／不動産クラウドファンディング「FUNDIA」の運営</span>／", 1),
        ("賃貸住宅管理業登録・不動産特定共同事業許可　いずれも", "賃貸住宅管理業登録<span data-fundia>・不動産特定共同事業許可</span>　いずれも", 1),
    ],
    "sumusumu/index.html": [
        ('<html lang="ja">', '<html lang="ja" data-fundia="off">', 1),
        ("</head>", NOTE + CSS_SUB + SCRIPT + "</head>", 1),
        (LI, LI.replace("<li>", "<li data-fundia>"), 1),
    ],
}


def run(rel, marks):
    p = ROOT / rel
    raw = p.read_bytes()
    crlf = b"\r\n" in raw
    s = raw.decode("utf-8").replace("\r\n", "\n")
    if "data-fundia" not in s:
        for old, new, n in marks:
            c = s.count(old)
            assert c == n, f"{rel}: {n} 箇所のはずが {c} 箇所: {old[:50]!r}"
            s = s.replace(old, new)
    s, n = re.subn(r'<html lang="ja" data-fundia="(?:on|off)">', f'<html lang="ja" data-fundia="{MODE}">', s)
    assert n == 1, f"{rel}: html タグが見つからない"
    if rel == "index.html":
        desc = DESC_OFF if MODE == "off" else DESC_ON
        s, n = re.subn(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{desc}">', s)
        assert n == 1, "meta description が見つからない"
    if crlf:
        s = s.replace("\n", "\r\n")
    p.write_bytes(s.encode("utf-8"))
    print(rel, "->", MODE)


for rel, marks in MARKS.items():
    run(rel, marks)

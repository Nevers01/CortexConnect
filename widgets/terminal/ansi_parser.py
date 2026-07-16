import re
import html

ANSI_SGR_RE = re.compile(r"\x1b\[([0-9;]*)m")
ANSI_OTHER_RE = re.compile(r"\x1b(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")

FG_COLORS = {
    30: "#484f58",
    31: "#ff7b72",
    32: "#3fb950",
    33: "#d29922",
    34: "#58a6ff",
    35: "#bc8cff",
    36: "#39c5cf",
    37: "#d0d7de",
    90: "#6e7681",
    91: "#ff7b72",
    92: "#56d364",
    93: "#e3b341",
    94: "#79c0ff",
    95: "#d2a8ff",
    96: "#56d4dd",
    97: "#f0f6fc",
}


def ansi_to_html(text: str) -> str:
    result = []
    pos = 0

    current_color = "#d0d7de"
    bold = False

    for match in ANSI_SGR_RE.finditer(text):
        raw = text[pos:match.start()]
        result.append(_span(raw, current_color, bold))

        codes = match.group(1)
        if not codes:
            codes = "0"

        for code in codes.split(";"):
            if not code:
                continue

            try:
                value = int(code)
            except ValueError:
                continue

            if value == 0:
                current_color = "#d0d7de"
                bold = False
            elif value == 1:
                bold = True
            elif value == 22:
                bold = False
            elif value in FG_COLORS:
                current_color = FG_COLORS[value]

        pos = match.end()

    result.append(_span(text[pos:], current_color, bold))

    html_text = "".join(result)
    html_text = ANSI_OTHER_RE.sub("", html_text)

    return html_text


def _span(text: str, color: str, bold: bool) -> str:
    if not text:
        return ""

    safe = html.escape(text)
    safe = safe.replace(" ", "&nbsp;")
    safe = safe.replace("\n", "<br>")

    weight = "bold" if bold else "normal"

    return f'<span style="color:{color}; font-weight:{weight};">{safe}</span>'
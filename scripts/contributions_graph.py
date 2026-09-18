#!/usr/bin/env python3
"""Render the last 12 months of GitHub contributions as a static SVG line chart.

Stdlib only. Reads GITHUB_TOKEN (any token works for public contribution data),
queries the GraphQL contribution calendar, aggregates by week and writes one SVG
per colour scheme so the README can pick via <picture>.

    GITHUB_TOKEN=... python3 scripts/contributions_graph.py [--user PSheon] [--out assets/images]
"""

import argparse
import json
import os
import sys
import urllib.request
from datetime import date

QUERY = """
query($login: String!) {
  user(login: $login) {
    contributionsCollection {
      contributionCalendar {
        totalContributions
        weeks { contributionDays { date contributionCount } }
      }
    }
  }
}
"""

THEMES = {
    # dracula-ish, matches the other stat cards in dark mode
    "dark": dict(bg="#282a36", grid="#3d4052", axis="#6272a4", ink="#f8f8f2", muted="#9aa0c2",
                 line="#ff6e96", fill_top="#ff6e96", fill_alpha_top=0.32, fill_alpha_bottom=0.02,
                 dot_ring="#282a36"),
    "light": dict(bg="#fffefe", grid="#eceef3", axis="#c5c9d6", ink="#24292f", muted="#6e7781",
                  line="#ff6e96", fill_top="#ff6e96", fill_alpha_top=0.28, fill_alpha_bottom=0.02,
                  dot_ring="#fffefe"),
}

W, H = 900, 240
PAD_L, PAD_R, PAD_T, PAD_B = 44, 24, 44, 34


def fetch_calendar(login: str, token: str) -> dict:
    body = json.dumps({"query": QUERY, "variables": {"login": login}}).encode()
    req = urllib.request.Request(
        "https://api.github.com/graphql", data=body,
        headers={"Authorization": f"bearer {token}", "Content-Type": "application/json",
                 "User-Agent": "contributions-graph"},
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        payload = json.load(resp)
    if "errors" in payload:
        raise SystemExit(f"GraphQL error: {payload['errors']}")
    return payload["data"]["user"]["contributionsCollection"]["contributionCalendar"]


def weekly_series(calendar: dict):
    """One point per week: (first day of week, total contributions)."""
    out = []
    for week in calendar["weeks"]:
        days = week["contributionDays"]
        if not days:
            continue
        out.append((date.fromisoformat(days[0]["date"]), sum(d["contributionCount"] for d in days)))
    return out


def nice_ceiling(v: int) -> int:
    """Round up to a tidy axis maximum: 1-2-5 progression."""
    if v <= 0:
        return 10
    mag = 10 ** (len(str(v)) - 1)
    for m in (1, 2, 2.5, 5, 10):
        if v <= m * mag:
            return int(m * mag)
    return v


def smooth_path(points, y_min: float, y_max: float):
    """Catmull-Rom to cubic Bezier, so the curve passes through every data point.

    Control points are clamped to the plot's vertical range so a run of zeros
    never dips below the baseline.
    """
    if len(points) < 2:
        return ""
    clamp = lambda y: min(max(y, y_min), y_max)
    d = [f"M{points[0][0]:.1f},{points[0][1]:.1f}"]
    for i in range(len(points) - 1):
        p0 = points[i - 1] if i > 0 else points[i]
        p1, p2 = points[i], points[i + 1]
        p3 = points[i + 2] if i + 2 < len(points) else p2
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, clamp(p1[1] + (p2[1] - p0[1]) / 6))
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, clamp(p2[1] - (p3[1] - p1[1]) / 6))
        d.append(f"C{c1[0]:.1f},{c1[1]:.1f} {c2[0]:.1f},{c2[1]:.1f} {p2[0]:.1f},{p2[1]:.1f}")
    return " ".join(d)


def render(series, total: int, theme: dict, label: str) -> str:
    n = len(series)
    y_max = nice_ceiling(max(v for _, v in series))
    plot_w, plot_h = W - PAD_L - PAD_R, H - PAD_T - PAD_B
    x_at = lambda i: PAD_L + plot_w * i / (n - 1)
    y_at = lambda v: PAD_T + plot_h * (1 - v / y_max)
    pts = [(x_at(i), y_at(v)) for i, (_, v) in enumerate(series)]
    line_d = smooth_path(pts, PAD_T, PAD_T + plot_h)
    area_d = f"{line_d} L{pts[-1][0]:.1f},{PAD_T + plot_h:.1f} L{pts[0][0]:.1f},{PAD_T + plot_h:.1f} Z"

    # Y gridlines: 4 steps, labels in muted ink
    grid, ylabels = [], []
    for k in range(0, 5):
        v = y_max * k / 4
        y = y_at(v)
        grid.append(f'<line x1="{PAD_L}" y1="{y:.1f}" x2="{W - PAD_R}" y2="{y:.1f}" stroke="{theme["grid"]}" stroke-width="1"/>')
        ylabels.append(f'<text x="{PAD_L - 8}" y="{y + 4:.1f}" text-anchor="end" fill="{theme["muted"]}" font-size="11">{int(v)}</text>')

    # X labels: the first week that starts a new month
    xlabels, seen = [], set()
    for i, (d, _) in enumerate(series):
        key = (d.year, d.month)
        if key in seen or i == 0 and d.day > 7:
            continue
        seen.add(key)
        xlabels.append(f'<text x="{x_at(i):.1f}" y="{H - 12}" text-anchor="middle" fill="{theme["muted"]}" font-size="11">{d.strftime("%b")}</text>')

    # Selective direct labels: the peak week and the latest week
    peak_i = max(range(n), key=lambda i: series[i][1])
    last_i = n - 1
    marks = []
    for i, anchor in ((peak_i, "middle"), (last_i, "end")):
        x, y = pts[i]
        v = series[i][1]
        marks.append(
            f'<circle cx="{x:.1f}" cy="{y:.1f}" r="5" fill="{theme["line"]}" stroke="{theme["dot_ring"]}" stroke-width="2"/>'
        )
        ty = y - 12 if y - 12 > PAD_T + 8 else y + 20
        marks.append(f'<text x="{x:.1f}" y="{ty:.1f}" text-anchor="{anchor}" fill="{theme["ink"]}" font-size="11" font-weight="600">{v}</text>')

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{label}">
  <defs>
    <linearGradient id="area" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="{theme["fill_top"]}" stop-opacity="{theme["fill_alpha_top"]}"/>
      <stop offset="1" stop-color="{theme["fill_top"]}" stop-opacity="{theme["fill_alpha_bottom"]}"/>
    </linearGradient>
  </defs>
  <rect width="{W}" height="{H}" rx="6" fill="{theme["bg"]}"/>
  <g font-family="-apple-system, 'Segoe UI', Helvetica, Arial, sans-serif">
    <text x="{PAD_L}" y="24" fill="{theme["ink"]}" font-size="14" font-weight="600">Contributions · last 12 months</text>
    <text x="{W - PAD_R}" y="24" text-anchor="end" fill="{theme["muted"]}" font-size="12">{total:,} total · weekly</text>
    {"".join(grid)}
    {"".join(ylabels)}
    <path d="{area_d}" fill="url(#area)"/>
    <path d="{line_d}" fill="none" stroke="{theme["line"]}" stroke-width="2" stroke-linejoin="round" stroke-linecap="round"/>
    {"".join(marks)}
    {"".join(xlabels)}
  </g>
</svg>
"""


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--user", default="PSheon")
    ap.add_argument("--out", default="assets/images")
    ap.add_argument("--from-json", help="use a saved GraphQL response instead of calling the API")
    args = ap.parse_args()

    if args.from_json:
        calendar = json.load(open(args.from_json))["data"]["user"]["contributionsCollection"]["contributionCalendar"]
    else:
        token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
        if not token:
            print("GITHUB_TOKEN is required", file=sys.stderr)
            return 2
        calendar = fetch_calendar(args.user, token)

    series = weekly_series(calendar)
    total = calendar["totalContributions"]
    os.makedirs(args.out, exist_ok=True)
    for name, theme in THEMES.items():
        path = os.path.join(args.out, f"contributions-{name}.svg")
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(render(series, total, theme, f"{args.user} contributions, last 12 months, weekly totals"))
        print("wrote", path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

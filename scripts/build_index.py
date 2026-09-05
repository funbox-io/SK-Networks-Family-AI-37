#!/usr/bin/env python3
"""days/ · weekly/ 를 훑어 루트 README.md 진도표와 docs/data.json 을 다시 만듭니다.

    python3 scripts/build_index.py
"""
import datetime
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import ROOT, load_schedule, scan_days, scan_weekly  # noqa: E402

PAGES_URL = "https://funbox-io.github.io/SK-Networks-Family-AI-37/"
REPO = "funbox-io/SK-Networks-Family-AI-37"


def bar(done, total, length=20):
    filled = round(done / total * length) if total else 0
    return "█" * filled + "░" * (length - filled)


def build():
    sched = load_schedule()
    found = scan_days()
    weeks_found = scan_weekly()
    today = datetime.date.today().isoformat()

    rows = []
    for d in sched["days"]:
        info = found.get(d["date"]) or {}
        rows.append({**d,
                     "title": info.get("title", ""),
                     "tags": info.get("tags", []),
                     "lecture": info.get("lecture", 0),
                     "review": info.get("review", 0),
                     "exists": d["date"] in found})

    total = len(rows)
    done = [r for r in rows if r["lecture"] or r["review"]]
    pct = round(len(done) / total * 100) if total else 0
    passed = [r for r in rows if r["date"] <= today]

    out = []
    A = out.append
    A(f"# {sched['course']}\n")
    A("> 6개월 과정의 **수업 자료**와 **복습 자료**를 하루 단위로 기록합니다.\n")
    A("| | |")
    A("|:--|:--|")
    A(f"| 📅 **교육기간** | {sched['start']} ~ {sched['end']} · **{total}일 / {sched['totalHours']}시간** |")
    A(f"| ⏰ **교육시간** | {sched['dailyHours']} |")
    A(f"| 📈 **기록 진행률** | `{bar(len(done), total)}` **{len(done)} / {total}일 ({pct}%)** |")
    A(f"| 🌐 **웹으로 보기** | [{PAGES_URL}]({PAGES_URL}) — 검색 · 교과목 필터 |")
    A("| 📖 **설정 · 사용법** | [SETUP.md](SETUP.md) |")
    A("")
    A("---\n")

    # ── 커리큘럼 ────────────────────────────────
    A("## 🗂 커리큘럼\n")
    A("| # | 교과목 | 주요 내용 | 기간 | 일수 | 기록 |")
    A("|:-:|:--|:--|:--|:-:|:--|")
    for i, p in enumerate(sched["phases"], 1):
        pdone = sum(1 for r in rows if r["phaseKey"] == p["key"] and (r["lecture"] or r["review"]))
        A(f"| {i} | **{p['name']}** | {p['topics']} | {p['startDate'][5:]} ~ {p['endDate'][5:]} "
          f"| {p['days']}일 | `{bar(pdone, p['days'], 10)}` {pdone}/{p['days']} |")
    A("")
    A("<sub>교과목별 시작·종료일은 OT 자료의 일수 배분을 순서대로 적용한 <b>예상치</b>입니다. "
      "실제 일정이 다르면 <code>schedule.json</code> 의 <code>phases</code> 를 고쳐주세요.</sub>\n")

    # ── 최근 기록 ───────────────────────────────
    recent = [r for r in reversed(rows) if r["exists"]][:5]
    if recent:
        A("## 🕘 최근 기록\n")
        for r in recent:
            t = r["title"] or "_(제목 작성 전)_"
            A(f"- **Day {r['no']:03d}** · [{r['date']} ({r['weekday']})](days/{r['date']}/) — {t}")
        A("")

    # ── 진도표 ─────────────────────────────────
    A("---\n")
    A("## 📅 진도표\n")
    A("각 날짜를 누르면 그날의 **수업 자료**와 **복습 자료**로 바로 갈 수 있습니다. "
      "📄 = 수업 자료 개수, 📝 = 복습 자료 개수\n")

    cur_key = next((r["phaseKey"] for r in rows if r["date"] >= today), rows[-1]["phaseKey"])
    for p in sched["phases"]:
        prows = [r for r in rows if r["phaseKey"] == p["key"]]
        pdone = sum(1 for r in prows if r["lecture"] or r["review"])
        openattr = " open" if p["key"] == cur_key else ""
        A(f"<details{openattr}>")
        A(f"<summary><b>{p['name']}</b> · {p['startDate']} ~ {p['endDate']} "
          f"· {pdone}/{len(prows)}일 기록됨</summary>\n")
        A("| Day | 주차 | 날짜 | 주제 | 수업 | 복습 |")
        A("|:-:|:-:|:--|:--|:-:|:-:|")
        for r in prows:
            label = f"{r['date'][5:]} ({r['weekday']})"
            if r["exists"]:
                cell = f"[{label}](days/{r['date']}/)"
                lec = f"📄 {r['lecture']}" if r["lecture"] else "–"
                rev = f"📝 {r['review']}" if r["review"] else "–"
                title = r["title"] or "_(작성 전)_"
            else:
                cell, lec, rev, title = label, "", "", ""
            A(f"| {r['no']:03d} | {r['week']}주 | {cell} | {title} | {lec} | {rev} |")
        A("\n</details>\n")

    # ── 주차별 회고 ─────────────────────────────
    weeks = {}
    for r in rows:
        weeks.setdefault(r["week"], []).append(r)
    wdone = sum(1 for n in weeks if weeks_found.get(n, {}).get("written"))
    A("<details>")
    A(f"<summary><b>📝 주차별 회고</b> · {wdone}/{len(weeks)}주 작성됨</summary>\n")
    A("| 주차 | 기간 | 회고 |")
    A("|:-:|:--|:--|")
    for n, wrows in sorted(weeks.items()):
        rng = f"{wrows[0]['date']} ~ {wrows[-1]['date']}"
        w = weeks_found.get(n)
        if w:
            mark = "✅" if w["written"] else "✏️ 작성 중"
            A(f"| {n}주 | {rng} | [{w['title'] or mark}](weekly/{w['file']}) |")
        else:
            A(f"| {n}주 | {rng} | – |")
    A("\n</details>\n")

    # ── 쉬는 날 ────────────────────────────────
    hol = sched.get("holidays", [])
    if hol:
        A("<details>")
        A(f"<summary><b>🏖 쉬는 날 (공휴일 {len(hol)}일)</b></summary>\n")
        A("| 날짜 | 이름 |")
        A("|:--|:--|")
        for h in hol:
            A(f"| {h['date']} | {h['name']} |")
        A("\n</details>\n")

    # ── 사용법 ─────────────────────────────────
    A("---\n")
    A("## 🛠 이 저장소 쓰는 법\n")
    A("```bash")
    A("python3 scripts/new_day.py              # 오늘 수업일 폴더 만들기")
    A("python3 scripts/new_day.py 2026-09-07   # 특정 날짜로 만들기")
    A("python3 scripts/new_day.py --next       # 아직 안 만든 가장 이른 수업일")
    A("python3 scripts/new_day.py --weekly     # 이번 주 회고 파일 만들기")
    A("python3 scripts/build_index.py          # 진도표만 다시 만들기")
    A("```\n")
    A("1. `new_day.py` 로 그날 폴더를 만듭니다.")
    A("2. `days/<날짜>/lecture/` 에 **수업 자료**, `days/<날짜>/review/` 에 **복습 자료**를 넣습니다.")
    A("3. `days/<날짜>/README.md` 맨 위 `title:` 에 그날 주제를 한 줄 적습니다. → 진도표에 그대로 표시됩니다.")
    A("4. push 하면 GitHub Actions 가 진도표와 웹사이트를 알아서 갱신합니다.\n")
    A(f"<sub>이 문서는 <code>scripts/build_index.py</code> 가 자동으로 만듭니다. "
      f"직접 고치지 마세요. (마지막 갱신 {today})</sub>")

    (ROOT / "README.md").write_text("\n".join(out) + "\n", encoding="utf-8")

    docs = ROOT / "docs"
    docs.mkdir(exist_ok=True)
    (docs / "data.json").write_text(json.dumps({
        "course": sched["course"], "repo": REPO,
        "start": sched["start"], "end": sched["end"],
        "totalHours": sched["totalHours"], "dailyHours": sched["dailyHours"],
        "generated": today, "total": total, "done": len(done), "passed": len(passed),
        "phases": sched["phases"], "days": rows,
        "weeks": [{"week": n,
                   "start": w[0]["date"], "end": w[-1]["date"],
                   "file": weeks_found.get(n, {}).get("file"),
                   "title": weeks_found.get(n, {}).get("title", ""),
                   "written": bool(weeks_found.get(n, {}).get("written"))}
                  for n, w in sorted(weeks.items())],
        "holidays": hol,
    }, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"README.md · docs/data.json 갱신 완료 — {len(done)}/{total}일 기록됨")


if __name__ == "__main__":
    build()

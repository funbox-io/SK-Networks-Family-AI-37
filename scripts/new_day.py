#!/usr/bin/env python3
"""새 수업일(또는 주차 회고) 파일을 만들고 진도표를 갱신합니다.

    python3 scripts/new_day.py             # 오늘
    python3 scripts/new_day.py 2026-09-07  # 특정 날짜
    python3 scripts/new_day.py --next      # 아직 안 만든 가장 이른 수업일
    python3 scripts/new_day.py --weekly    # 해당 주차 회고 파일도 만들기
    python3 scripts/new_day.py 2026-09-05 --force   # 일정에 없는 날도 강제 생성
"""
import argparse
import datetime
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import DAYS, WEEKLY, TEMPLATES, WD, load_schedule  # noqa: E402
import build_index  # noqa: E402


def make_weekly(sched, week):
    wrows = [d for d in sched["days"] if d["week"] == week]
    if not wrows:
        print(f"{week}주차는 일정에 없습니다.")
        return
    WEEKLY.mkdir(exist_ok=True)
    f = WEEKLY / f"week-{week:02d}.md"
    if f.exists():
        print(f"이미 있습니다: weekly/{f.name}")
        return
    rng = f"{wrows[0]['date']} ~ {wrows[-1]['date']}"
    tpl = (TEMPLATES / "weekly-README.md").read_text(encoding="utf-8")
    f.write_text(tpl.replace("{{WEEK}}", str(week)).replace("{{RANGE}}", rng), encoding="utf-8")
    print(f"만들었습니다: weekly/{f.name}  ({week}주차 · {rng})")


def main():
    ap = argparse.ArgumentParser(description="새 수업일 폴더 생성")
    ap.add_argument("date", nargs="?", help="YYYY-MM-DD (기본: 오늘)")
    ap.add_argument("--next", action="store_true", help="아직 안 만든 가장 이른 수업일")
    ap.add_argument("--weekly", action="store_true", help="해당 주차 회고 파일도 생성")
    ap.add_argument("--force", action="store_true", help="일정에 없는 날짜도 생성")
    args = ap.parse_args()

    sched = load_schedule()
    by_date = {d["date"]: d for d in sched["days"]}

    if args.next:
        target = next((d["date"] for d in sched["days"] if not (DAYS / d["date"]).is_dir()), None)
        if target is None:
            sys.exit("모든 수업일 폴더가 이미 만들어져 있습니다.")
    else:
        target = args.date or datetime.date.today().isoformat()

    try:
        dt = datetime.date.fromisoformat(target)
    except ValueError:
        sys.exit(f"날짜 형식이 잘못됐습니다: {target} (YYYY-MM-DD 로 적어주세요)")

    if target not in by_date and not args.force:
        why = "주말" if dt.weekday() >= 5 else "공휴일이거나 교육기간 밖"
        sys.exit(f"{target} 은(는) 수업일이 아닙니다 ({why}).\n"
                 f"그래도 만들려면 뒤에 --force 를 붙이세요.")

    info = by_date.get(target, {"no": 0, "week": 0, "phase": "-"})
    folder = DAYS / target
    if folder.is_dir():
        print(f"이미 있습니다: days/{target}/")
    else:
        (folder / "lecture").mkdir(parents=True)
        (folder / "review").mkdir(parents=True)
        tpl = (TEMPLATES / "day-README.md").read_text(encoding="utf-8")
        for k, v in {"{{DAY}}": f"{info['no']:03d}", "{{DATE}}": target,
                     "{{WEEKDAY}}": WD[dt.weekday()], "{{WEEK}}": str(info["week"]),
                     "{{PHASE}}": info["phase"]}.items():
            tpl = tpl.replace(k, v)
        (folder / "README.md").write_text(tpl, encoding="utf-8")
        for sub in ("lecture", "review"):
            src = TEMPLATES / f"{sub}-GUIDE.md"
            if src.is_file():
                (folder / sub / "GUIDE.md").write_text(src.read_text(encoding="utf-8"),
                                                       encoding="utf-8")
        print(f"만들었습니다: days/{target}/   Day {info['no']:03d} · "
              f"{WD[dt.weekday()]}요일 · {info['week']}주차 · {info['phase']}")
        print("  ├─ README.md   ← 오늘 주제와 요약을 적으세요 (title: 칸이 진도표에 표시됩니다)")
        print("  ├─ lecture/    ← 수업 자료를 넣으세요")
        print("  └─ review/     ← 복습 자료를 넣으세요")

    if args.weekly and info["week"]:
        make_weekly(sched, info["week"])

    build_index.build()


if __name__ == "__main__":
    main()

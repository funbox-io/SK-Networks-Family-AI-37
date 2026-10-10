#!/usr/bin/env python3
"""새 수업일(또는 주차 회고) 파일을 만들고 진도표를 갱신합니다.

    python3 .setup/scripts/new_day.py             # 오늘
    python3 .setup/scripts/new_day.py 2026-09-07  # 특정 날짜
    python3 .setup/scripts/new_day.py --next      # 아직 안 만든 가장 이른 수업일
    python3 .setup/scripts/new_day.py --weekly    # 해당 주차 회고 파일도 만들기
    python3 .setup/scripts/new_day.py 2026-09-05 --force   # 일정에 없는 날도 강제 생성
"""
import argparse
import datetime
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import DAYS, WEEKLY, TEMPLATES, WD, load_schedule  # noqa: E402
import build_index  # noqa: E402


# 요일별 PCCE 연습 주제 (월=0 … 금=4)
PCCE_TOPICS = ["입출력·연산자", "조건문", "반복문", "리스트·문자열", "함수·딕셔너리"]

# ADsP 제51회(2026-10-31)까지 날짜별 주제 — 시험이 끝나면 비워도 됩니다
ADSP_TOPICS = {
    "2026-10-12": "1과목: 데이터와 정보, DIKW, 데이터베이스 특징",
    "2026-10-13": "1과목: 빅데이터 특징·가치·위기 요인",
    "2026-10-14": "1과목: 데이터 사이언스, 데이터 사이언티스트 역량",
    "2026-10-15": "2과목: 분석 기획, 분석 방법론(KDD·CRISP-DM)",
    "2026-10-16": "2과목: 분석 과제 발굴(하향식·상향식)",
    "2026-10-19": "3과목: 통계 기초(표본추출·척도·확률분포)",
    "2026-10-20": "3과목: 추정과 가설검정",
    "2026-10-21": "3과목: 회귀분석",
    "2026-10-22": "3과목: 시계열·주성분분석·다차원척도",
    "2026-10-23": "3과목: 분류(로지스틱·의사결정나무·앙상블)",
    "2026-10-26": "기출: 1과목",
    "2026-10-27": "기출: 2과목",
    "2026-10-28": "기출: 3과목",
    "2026-10-29": "전범위 모의고사 1회",
    "2026-10-30": "오답만 다시 + 헷갈리는 것 요약 1장",
}


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
                     "{{PHASE}}": info["phase"],
                     "{{PCCE_TOPIC}}": PCCE_TOPICS[dt.weekday()] if dt.weekday() < 5 else "자유",
                     "{{ADSP_LINE}}": (f"오늘 주제: **{ADSP_TOPICS[target]}** · 5문제, 틀린 것만 내 말로 한 줄"
                                       if target in ADSP_TOPICS else "틀린 문제만 내 말로 한 줄")}.items():
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

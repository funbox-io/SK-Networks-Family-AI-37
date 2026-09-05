"""공용 유틸 — 표준 라이브러리만 사용합니다."""
from pathlib import Path
import json

_HERE = Path(__file__).resolve()
ROOT = _HERE.parents[2]          # 저장소 루트
SETUP = _HERE.parents[1]         # .setup
DAYS = ROOT / "days"             # 수업일 기록 (사람이 채우는 곳)
WEEKLY = ROOT / "weekly"         # 주차별 회고
TEMPLATES = SETUP / "templates"
SCHEDULE = SETUP / "schedule.json"
SITE = SETUP / "site"            # GitHub Pages 로 배포되는 폴더
SKIP_NAMES = {".gitkeep", "GUIDE.md", ".DS_Store"}
WD = "월화수목금토일"


def load_schedule():
    return json.loads(SCHEDULE.read_text(encoding="utf-8"))


def parse_front_matter(text):
    """--- ... --- 블록을 key: value 로 파싱합니다 (외부 의존성 없음)."""
    meta = {}
    if not text.startswith("---"):
        return meta, text
    end = text.find("\n---", 3)
    if end == -1:
        return meta, text
    for line in text[3:end].strip("\n").splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            meta[k.strip()] = v.strip()
    return meta, text[end + 4:]


def count_files(folder: Path):
    if not folder.is_dir():
        return 0
    return sum(1 for p in folder.rglob("*")
               if p.is_file() and p.name not in SKIP_NAMES and not p.name.startswith("."))


def scan_days():
    """days/ 를 훑어 날짜별 상태를 dict 로 돌려줍니다."""
    found = {}
    if not DAYS.is_dir():
        return found
    for folder in sorted(DAYS.iterdir()):
        if not folder.is_dir():
            continue
        readme = folder / "README.md"
        meta = {}
        if readme.is_file():
            meta, _ = parse_front_matter(readme.read_text(encoding="utf-8"))
        tags = [t.strip() for t in meta.get("tags", "").strip("[]").split(",") if t.strip()]
        found[folder.name] = {
            "title": meta.get("title", "").strip(),
            "tags": tags,
            "lecture": count_files(folder / "lecture"),
            "review": count_files(folder / "review"),
        }
    return found


def scan_weekly():
    """weekly/week-NN.md 를 훑어 주차별 회고 상태를 돌려줍니다."""
    found = {}
    if not WEEKLY.is_dir():
        return found
    for f in sorted(WEEKLY.glob("week-*.md")):
        meta, body = parse_front_matter(f.read_text(encoding="utf-8"))
        try:
            n = int(meta.get("week") or f.stem.split("-")[1])
        except (ValueError, IndexError):
            continue
        # 템플릿 그대로면 '작성 전'으로 봅니다.
        written = len([l for l in body.splitlines()
                       if l.strip().startswith("- ") and l.strip() != "-"]) > 0
        found[n] = {"file": f.name, "title": meta.get("title", "").strip(), "written": written}
    return found

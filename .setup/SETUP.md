# 처음 한 번만 하는 설정

## 폴더 구조

```
.github/     자동화 워크플로 (건드릴 일 없음)
.setup/      스크립트 · 템플릿 · 일정표 · 웹사이트 소스
days/        ← 수업/복습 자료를 넣는 곳
weekly/      주차별 회고
README.md    자동 생성되는 진도표
```

평소에 열 폴더는 `days/` 하나입니다.

## 1. 파일 올리기

### 방법 A — 로컬에서 (권장)
```bash
git clone https://github.com/funbox-io/SK-Networks-Family-AI-37.git
cd SK-Networks-Family-AI-37
# 받은 zip 의 내용물을 이 폴더에 전부 복사한 뒤
git add .
git commit -m "feat: 수업/복습 기록 구조 · 진도표 자동화 · GitHub Pages"
git push
```

### 방법 B — 웹에서
저장소 화면 → `Add file` → `Upload files` → zip 을 푼 **폴더 안의 항목들**을 드래그 → Commit.
> `.github/workflows/pages.yml` 은 숨김 폴더라 드래그가 안 될 수 있습니다.
> 그럴 땐 `Add file` → `Create new file` → 파일명에 `.github/workflows/pages.yml` 을 그대로 입력하고 내용을 붙여넣으세요.

## 2. GitHub Pages 켜기

저장소 → **Settings** → 왼쪽 **Pages** → **Source** 를 **GitHub Actions** 로 선택 → 저장.

몇 분 뒤 아래 주소로 열립니다.
<https://funbox-io.github.io/SK-Networks-Family-AI-37/>

## 3. Actions 쓰기 권한 확인

저장소 → **Settings** → **Actions** → **General** → 맨 아래 **Workflow permissions** 에서
**Read and write permissions** 선택 → 저장.
(진도표를 자동으로 커밋하려면 필요합니다.)

---

# 매일 하는 일

```bash
python3 .setup/scripts/new_day.py        # 오늘 폴더 만들기
```

1. `days/<오늘날짜>/lecture/` 에 **수업 자료**를 넣습니다.
2. 집에 와서 `days/<오늘날짜>/review/` 에 **복습 자료**를 넣습니다.
3. `days/<오늘날짜>/README.md` 맨 위 `title:` 칸에 그날 주제를 한 줄 적습니다.
   ```yaml
   title: 파이썬 리스트 · 딕셔너리
   tags: [Python, 자료구조]
   ```
4. `git add . && git commit -m "day 007" && git push`

push 하면 진도표(README)와 웹사이트가 자동으로 갱신됩니다.

## 주말에 하는 일

```bash
python3 .setup/scripts/new_day.py --weekly   # 이번 주 회고 파일 만들기
```
`weekly/week-NN.md` 를 채우고 블로그 링크를 남겨두면 진도표에 ✅ 로 표시됩니다.

---

# 일정이 바뀌면

`.setup/schedule.json` 하나만 고치면 README 와 웹사이트가 같이 바뀝니다.

- **휴강/임시공휴일**: `days` 배열에서 그 날짜 항목을 지웁니다.
- **교과목 기간**: `phases` 의 `startDate` / `endDate` / `days` 를 실제 일정에 맞게 고칩니다.
  (지금 값은 OT 자료의 일수 배분 — 14 / 23 / 29 / 16 / 38일 — 을 순서대로 적용한 **예상치**입니다.)

고친 뒤 `python3 .setup/scripts/build_index.py` 를 한 번 실행하세요.

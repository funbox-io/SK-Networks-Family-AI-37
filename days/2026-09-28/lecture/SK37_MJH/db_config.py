"""MySQL 접속 정보 — 여기 값을 내 MySQL에 맞게 바꾸면 됩니다 (secrets.toml 없이 이 파일만 사용).

MySQL Workbench에서 접속할 때 쓰는 값과 같습니다.
    host     : 보통 "localhost" (또는 "127.0.0.1")
    port     : 보통 3306
    user     : 보통 "root"
    password : MySQL 설치할 때 정한 root 비밀번호
    database : db/holiday_db.sql 을 실행하면 생기는 "holiday_db"

※ 비밀번호가 그대로 적히는 파일이니, 깃허브 등 공개된 곳에 올릴 때는 비밀번호를 지우고 올리세요.
"""

MYSQL = {
    "host": "localhost",
    "port": 3306,
    "user": "root",
    "password": "",   # ← 내 MySQL root 비밀번호를 여기에 적으세요 (공개 저장소에는 비워 둡니다)
    "database": "holiday_db",
}

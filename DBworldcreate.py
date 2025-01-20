import sqlite3

# データベースの作成（ファイルとして保存される）
conn = sqlite3.connect("example.db")

# カーソルオブジェクトの作成
cursor = conn.cursor()

# テーブルの作成
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    age INTEGER NOT NULL
)
""")

# データの挿入
cursor.execute("INSERT INTO users (name, age) VALUES (?, ?)", ("Alice", 25))

# データの取得
cursor.execute("SELECT * FROM users")
rows = cursor.fetchall()
print(rows)

# コミットしてクローズ
conn.commit()
conn.close()
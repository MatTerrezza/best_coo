import sqlite3
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

DB_NAME = os.getenv("DB")


def init_db(): # определяем наличие бидэ если нет создаем

    with sqlite3.connect(DB_NAME) as conn:
        cur = conn.cursor()
        # Таблица пользователей
        cur.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        # Таблица активности (для логгирования команд)
        cur.execute('''
            CREATE TABLE IF NOT EXISTS user_activity (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                command TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(user_id) REFERENCES users(user_id)
            )
        ''')
        conn.commit()

def log_command(user_id, command): #логи
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute('''
            INSERT INTO user_activity (user_id, command) 
            VALUES (?, ?)
        ''', (user_id, command))
        conn.commit()

def add_user_if_not_exists(user_id, username=None): #добавление нового пользователя
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute('''
            INSERT OR IGNORE INTO users (user_id, username) 
            VALUES (?, ?)
        ''', (user_id, username))
        conn.commit()

def remove_user(user_id): #удаление пользователя из биде
  
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute('DELETE FROM users WHERE user_id = ?', (user_id,))
        conn.commit()

def get_all_users():  #получение всез пользоватлей
    with sqlite3.connect(DB_NAME) as conn:
        cur = conn.cursor()
        cur.execute('SELECT user_id FROM users')
        return [row[0] for row in cur.fetchall()]

def is_user_allowed(user_id): # проверка прав , у мужлан нет прав у меня получается тоже
 
    return True  # В реальном проекте заменить на проверку прав

def get_active_users(): # те самые с синдромом старосты 

    with sqlite3.connect(DB_NAME) as conn:
        cur = conn.cursor()
        cur.execute('''
            SELECT DISTINCT user_id FROM user_activity 
            WHERE date(timestamp) >= date('now', '-7 days')
        ''')
        return [row[0] for row in cur.fetchall()]

def get_top_commands(): # Топ комманд для статы

    with sqlite3.connect(DB_NAME) as conn:
        cur = conn.cursor()
        cur.execute('''
            SELECT command, COUNT(*) as count 
            FROM user_activity 
            GROUP BY command 
            ORDER BY count DESC 
            LIMIT 10
        ''')
        return cur.fetchall()

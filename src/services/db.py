import sqlite3
import pandas as pd
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class DatabaseManager:
    DB_NAME = "maintenance_logs.db"
    TIMEOUT = 30  # Seconds for SQLite busy timeout

    @staticmethod
    def _get_connection():
        """Creates a new database connection with proper configuration."""
        conn = sqlite3.connect(DatabaseManager.DB_NAME, timeout=DatabaseManager.TIMEOUT)
        conn.execute("PRAGMA journal_mode=WAL;")  # Enable Write-Ahead Logging for concurrency
        conn.execute("PRAGMA synchronous=NORMAL;") # Faster writes, safe enough for WAL
        return conn

    @staticmethod
    def init_db():
        try:
            with DatabaseManager._get_connection() as conn:
                c = conn.cursor()
                c.execute('''
                    CREATE TABLE IF NOT EXISTS logs (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        timestamp TEXT,
                        error_code TEXT,
                        ai_analysis TEXT
                    )
                ''')
                c.execute('''
                    CREATE TABLE IF NOT EXISTS error_solutions (
                        error_code TEXT PRIMARY KEY,
                        solution TEXT,
                        last_updated TEXT
                    )
                ''')
                conn.commit()
        except Exception as e:
            logger.critical(f"DB Init Error: {e}")

    @staticmethod
    def log_fault(error_code, ai_analysis):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        try:
            with DatabaseManager._get_connection() as conn:
                c = conn.cursor()
                
                # Check for duplicate in the very last entry to avoid spamming
                c.execute('SELECT error_code FROM logs ORDER BY id DESC LIMIT 1')
                row = c.fetchone()
                if row and str(row[0]) == str(error_code):
                    return

                c.execute('''
                    INSERT INTO logs (timestamp, error_code, ai_analysis)
                    VALUES (?, ?, ?)
                ''', (timestamp, error_code, ai_analysis))
                conn.commit()
                
        except sqlite3.OperationalError as e:
            logger.error(f"DB Operational Error (Locked?): {e}")
        except Exception as e:
            logger.error(f"DB General Error: {e}")

    @staticmethod
    def get_cached_solution(error_code: str) -> str | None:
        """Cache'den çözüm getirir."""
        try:
            with DatabaseManager._get_connection() as conn:
                c = conn.cursor()
                c.execute("SELECT solution FROM error_solutions WHERE error_code = ?", (error_code,))
                row = c.fetchone()
                return row[0] if row else None
        except Exception as e:
            logger.warning(f"Cache Read Error: {e}")
            return None

    @staticmethod
    def upsert_solution(error_code: str, solution: str):
        """Çözümü cache'e yazar veya günceller."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try:
            with DatabaseManager._get_connection() as conn:
                c = conn.cursor()
                c.execute('''
                    INSERT INTO error_solutions (error_code, solution, last_updated)
                    VALUES (?, ?, ?)
                    ON CONFLICT(error_code) DO UPDATE SET
                        solution=excluded.solution,
                        last_updated=excluded.last_updated
                ''', (error_code, solution, timestamp))
                conn.commit()
        except Exception as e:
            logger.error(f"Cache Write Error: {e}")

    @staticmethod
    def get_logs_as_df(limit: int = 0):
        try:
            with DatabaseManager._get_connection() as conn:
                query = "SELECT * FROM logs ORDER BY id DESC"
                if limit > 0:
                    query += f" LIMIT {limit}"
                return pd.read_sql_query(query, conn)
        except Exception as e:
            logger.error(f"Log Read Error: {e}")
            return pd.DataFrame()

    @staticmethod
    def get_daily_logs_as_df():
        """Bugüne ait logları getirir."""
        today = datetime.now().strftime("%Y-%m-%d")
        try:
            with DatabaseManager._get_connection() as conn:
                # SQLite timestamp stores as TEXT "YYYY-MM-DD HH:MM:SS"
                # We filter where timestamp starts with today's date
                return pd.read_sql_query(f"SELECT * FROM logs WHERE timestamp LIKE '{today}%' ORDER BY id DESC", conn)
        except Exception as e:
            logger.error(f"Daily Log Read Error: {e}")
            return pd.DataFrame()

# Initialize on module load
DatabaseManager.init_db()
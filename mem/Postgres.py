import psycopg2
from psycopg2.extras import RealDictCursor
from pathlib import Path
import os
from dotenv import load_dotenv

class Start_PG:
    def __init__(self):
        env_path = Path(__file__).resolve().parent.parent / "config" / ".env"
        load_dotenv(env_path)

        self.conn = psycopg2.connect(
            dbname=os.getenv('DBNAME_DB'),
            user=os.getenv('NAME_DB'),
            password=os.getenv('PASSWORD_DB'),
            host=os.getenv('HOST_DB'),
            port=os.getenv('PORT_DB'),
        )
        self.cur = self.conn.cursor(cursor_factory=RealDictCursor)

    def add_transaction(self, created_at: str, tx_type: str, category: str, amount: float):
        sql = """
        INSERT INTO transactions (type, category, amount, created_at)
        VALUES (%s, %s, %s, %s)
        RETURNING id, type, category, amount, created_at;
        """
        self.cur.execute(sql, (tx_type, category, amount, created_at))
        row = self.cur.fetchone()   # получаем вставленную строку
        self.conn.commit()
        return row
    
    def load_transaction(self):
        sql = """
        SELECT id, type, category, amount, created_at
        FROM transactions
        ORDER BY created_at DESC
        """
        self.cur.execute(sql)
        return self.cur.fetchall()
    
    def remove_transaction(self, tx_id):
        sql = "DELETE FROM transactions WHERE id = %s;"
        self.cur.execute(sql, (tx_id,))
        deleted = self.cur.rowcount  
        self.conn.commit()           
        return deleted > 0
    
    def get_balance_summary(self):
        self.cur.execute("""
        SELECT total_income, total_expense, balance
        FROM balance_summary;
        """)
        return self.cur.fetchone()
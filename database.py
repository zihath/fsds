import sqlite3

class DatabaseConnection:
    def __init__(self, db_name='users.db'):
        self.conn = sqlite3.connect(db_name, timeout=10)
        self.cur = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        # Create users table if it doesn't exist
        self.cur.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL
            )
        ''')

        # Create expenses table if it doesn't exist
        self.cur.execute('''
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                amount REAL,
                description TEXT,
                date TEXT,
                category TEXT,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        ''')
        
        self.cur.execute('''
            CREATE TABLE IF NOT EXISTS income (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                amount REAL NOT NULL,
                source TEXT,
                date TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES user(id) ON DELETE CASCADE
            )
        ''')

        
        self.conn.commit()

    def close(self):
        self.conn.close()

class User:
    def __init__(self, db_connection=None):
        self.db_connection = db_connection or DatabaseConnection()

    def register_user(self, username, password):
        try:
            self.db_connection.cur.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            self.db_connection.conn.commit()
            return "Registration successful."
        except sqlite3.IntegrityError:
            return "Username already exists."

    def verify_user(self, username, password):
        self.db_connection.cur.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        user = self.db_connection.cur.fetchone()
        if user:
            return "Login successful."
        else:
            return "Login failed."

    def get_user_id(self, username):
        self.db_connection.cur.execute("SELECT id FROM users WHERE username=?", (username,))
        user = self.db_connection.cur.fetchone()
        if user:
            return user[0]
        return None

class AddExpense:
    def __init__(self, db_connection=None):
        self.db_connection = db_connection or DatabaseConnection()

    def insert(self, user_id, amount, description, date, category):
        self.db_connection.cur.execute(
            "INSERT INTO expenses (user_id, amount, description, date, category) VALUES (?, ?, ?, ?, ?)",
            (user_id, amount, description, date, category)
        )
        self.db_connection.conn.commit()
    
    def fetch_by_date(self, user_id, date):
        self.db_connection.cur.execute(
            "SELECT date, amount, description, category FROM expenses WHERE user_id = ? AND date = ?",
            (user_id, date)
        )
        return self.db_connection.cur.fetchall()
        
    def fetch_between_date(self, user_id, start_date, end_date):
        self.db_connection.cur.execute(
            "SELECT id, amount, description, date, category FROM expenses WHERE user_id = ? AND date BETWEEN ? AND ?",
            (user_id, start_date, end_date)
        )
        return self.db_connection.cur.fetchall()


    def delete(self, expense_id):
        self.db_connection.cur.execute(
            "DELETE FROM expenses WHERE id = ?",
            (expense_id,)
        )
        self.db_connection.conn.commit()
        
class AddIncome:
    def __init__(self, db_connection=None):
        self.db_connection = db_connection or DatabaseConnection()

    def insert(self, user_id, amount, source, date):
        # Insert a new income into the table
        try:
            self.db_connection.cur.execute('''
                INSERT INTO income (user_id, amount, source, date)
                VALUES (?, ?, ?, ?)
            ''', (user_id, amount, source, date))
            self.db_connection.conn.commit()
        except sqlite3.OperationalError as e:
            print(f"Error while inserting income: {e}")
            
    
    

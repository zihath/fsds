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
   git             password TEXT NOT NULL
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
            "SELECT id, amount, description, date, category FROM expenses WHERE user_id = ? AND date = ?",
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
        # Insert or update income based on whether the source exists for the user
        try:
            # Check if the source already exists for the given user_id
            self.db_connection.cur.execute('''
                SELECT id FROM income WHERE user_id = ? AND source = ?
            ''', (user_id, source))
            
            existing_record = self.db_connection.cur.fetchone()

            if existing_record:
                # If record exists, perform an update
                self.db_connection.cur.execute('''
                    UPDATE income 
                    SET amount = ?, date = ?
                    WHERE user_id = ? AND source = ?
                ''', (amount, date, user_id, source))
                print(f"Updated existing income record for {source} with new amount and date.")
            else:
                # If no record exists, perform an insert
                self.db_connection.cur.execute('''
                    INSERT INTO income (user_id, amount, source, date)
                    VALUES (?, ?, ?, ?)
                ''', (user_id, amount, source, date))
                print(f"Inserted new income record for {source}.")
            
            self.db_connection.conn.commit()

        except sqlite3.OperationalError as e:
            print(f"Error while inserting/updating income: {e}")

            
    
    def fetch_by_user_id(self, user_id):
        # Fetch all income records for the given user_id
        try:
            self.db_connection.cur.execute('''
                SELECT id, amount, source, date FROM income WHERE user_id = ?
            ''', (user_id,))
            return self.db_connection.cur.fetchall()
        except sqlite3.OperationalError as e:
            print(f"Error while fetching income: {e}")
            return []
        
    def update_income(self, user_id, source, new_amount):
        # Update the income amount for the specified user_id and source (category)
        try:
            self.db_connection.cur.execute('''
                UPDATE income 
                SET amount = ?
                WHERE user_id = ? AND source = ?
            ''', (new_amount, user_id, source))
            self.db_connection.conn.commit()
            if self.db_connection.cur.rowcount > 0:
                print("Income updated successfully")
            else:
                print("No matching record found to update")
        except sqlite3.OperationalError as e:
            print(f"Error while updating income: {e}")       
    
    

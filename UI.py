import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow,QTextEdit, QTableWidgetItem,QTableWidget,QDialog, QPushButton, QMessageBox, QLabel, QLineEdit, QVBoxLayout, QHBoxLayout, QSpacerItem, QSizePolicy, QWidget, QComboBox, QDateEdit
)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt, QDate
from database import User, AddExpense, DatabaseConnection , AddIncome

class AddIncomeWindow(QMainWindow):
    def __init__(self, user_id, username):
        super().__init__()
        self.username = username
        self.user_id = user_id
        self.addincome = AddIncome()

        self.setWindowTitle("Add Income")
        self.setGeometry(100, 100, 400, 250)  # Adjusted height to fit all widgets

        layout = QVBoxLayout()

        # Amount
        amount_label = QLabel("Amount:")
        layout.addWidget(amount_label)
        self.amount_input = QLineEdit()
        self.amount_input.setPlaceholderText("Enter amount")
        layout.addWidget(self.amount_input)

        # Source of Income
        source_label = QLabel("Source of Income:")
        layout.addWidget(source_label)
        self.source_input = QComboBox()
        self.source_input.addItems(["Salary", "Business", "Investments", "Other"])
        layout.addWidget(self.source_input)

        # Date input
        date_label = QLabel("Date:")
        self.date_input = QDateEdit()
        self.date_input.setDate(QDate.currentDate())
        layout.addWidget(date_label)
        layout.addWidget(self.date_input)

        # Submit button
        submit_button = QPushButton("Add Income")
        submit_button.clicked.connect(self.add_income)
        layout.addWidget(submit_button)
        
        view_button = QPushButton("View Income sources")
        view_button.clicked.connect(self.load_income)
        layout.addWidget(view_button)
        
        self.income_display = QTextEdit()
        self.income_display.setReadOnly(True)
        layout.addWidget(self.income_display)
        
        amount_label = QLabel("New Amount:")
        layout.addWidget(amount_label)
        self.amount_input = QLineEdit()
        self.amount_input.setPlaceholderText("Enter new amount")
        layout.addWidget(self.amount_input)

        source_label = QLabel("Source of Income:")
        layout.addWidget(source_label)
        self.source_input = QComboBox()
        self.source_input.addItems(["Salary", "Business", "Investments", "Other"])
        layout.addWidget(self.source_input)

        update_button = QPushButton("Update Income")
        update_button.clicked.connect(self.update_income)
        layout.addWidget(update_button)

        # Return to Home button
        return_button = QPushButton("Return to Home")
        return_button.clicked.connect(self.return_to_welcome)
        layout.addWidget(return_button)

        # Central widget setup
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def add_income(self):
        amount = self.amount_input.text()
        source = self.source_input.currentText()
        date = self.date_input.date().toString('yyyy-MM-dd')

        if not amount or not date:
            QMessageBox.warning(self, "Input Error", "Please enter all the information.")
            return

        try:
            self.addincome.insert(self.user_id, amount, source, date)
            QMessageBox.information(self, "Success", "Income added successfully!")
            # Do not close the window, just clear inputs
            self.amount_input.clear()
            self.source_input.setCurrentIndex(0)
            self.date_input.setDate(QDate.currentDate())
        except Exception as e:
            QMessageBox.critical(self, "Database Error", str(e))
    
    def load_income(self):
        try:
            # Fetch income records for the logged-in user
            incomes = self.addincome.fetch_by_user_id(self.user_id)

            if not incomes:
                QMessageBox.information(self, "No Data", "No income records found for this user.")
                self.income_display.clear()
                return

            # Display the incomes in the text area
            self.income_display.clear()
            self.income_display.append(f"{'ID':<10}{'Amount':<15}{'Source':<20}{'Date':<15}")
            self.income_display.append("="*60)
            for income in incomes:
                self.income_display.append(f"{income[0]:<10}{income[1]:<15}{income[2]:<20}{income[3]:<15}")
        
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def update_income(self):
        source = self.source_input.currentText()  # The income category (e.g., "Salary")
        new_amount = self.amount_input.text()      # The new amount to update

        if not new_amount:
            QMessageBox.warning(self, "Input Error", "Please enter a new amount.")
            return

        try:
            # Update income using user_id, source, and the new amount
            self.addincome.update_income(self.user_id, source, new_amount)
            QMessageBox.information(self, "Success", f"Income for {source} updated successfully!")
            
            # Optionally, reload income data to reflect the updated values
            self.load_income()
            
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def return_to_welcome(self):
        self.Main_window = WelcomeWindow(self.username)
        self.Main_window.show()
        self.close()

class History(QMainWindow):
    def __init__(self ,user_id, username):
        super().__init__()
        self.user_id = user_id
        self.username = username
        self.addexpense = AddExpense()  # Initialize AddExpense class

        self.setWindowTitle("Expense History")
        self.setGeometry(100, 100, 600, 400)

        layout = QVBoxLayout()

        # Start Date
        start_date_label = QLabel("Start Date:")
        layout.addWidget(start_date_label)
        self.start_date_input = QDateEdit()
        self.start_date_input.setDate(QDate.currentDate())
        layout.addWidget(self.start_date_input)

        # End Date
        end_date_label = QLabel("End Date:")
        layout.addWidget(end_date_label)
        self.end_date_input = QDateEdit()
        self.end_date_input.setDate(QDate.currentDate())
        layout.addWidget(self.end_date_input)

        # Show Transactions button
        show_button = QPushButton("Show Transactions")
        show_button.clicked.connect(self.load_expenses)
        layout.addWidget(show_button)
        
        return_button = QPushButton("Return to Home page")
        return_button.clicked.connect(self.return_to_welcome)
        layout.addWidget(return_button)
        
        # Display area for expenses
        self.expense_display = QTextEdit()
        self.expense_display.setReadOnly(True)
        layout.addWidget(self.expense_display)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def load_expenses(self):
        start_date = self.start_date_input.date().toString('yyyy-MM-dd')
        end_date = self.end_date_input.date().toString('yyyy-MM-dd')

        # Fetch expenses from backend
        try:
            expenses = self.addexpense.fetch_between_date(self.user_id, start_date, end_date)

            if not expenses:
                QMessageBox.information(self, "No Data", "No expenses found for the selected date range.")
                self.expense_display.clear()
                return

            # Display the expenses in the text area
            self.expense_display.clear()
            self.expense_display.append(f"{'ID':<10}{'Amount':<15}{'Description':<20}{'Date':<15}{'Category'}")
            self.expense_display.append("="*65)
            for expense in expenses:
                if len(expense) == 5:
                    self.expense_display.append(f"{expense[0]:<10}{expense[1]:<15}{expense[2]:<20}{expense[3]:<15}{expense[4]}")
                else:
                    QMessageBox.warning(self, "Data Error", "Unexpected data format found in expenses.")
                    break
                
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
        
    def return_to_welcome(self):
        self.Main_window = WelcomeWindow(self.username)
        self.Main_window.show()
        self.close()
        
class DeleteExpenseWindow(QMainWindow):
    def __init__(self, user_id ,username):
        super().__init__()
        self.user_id = user_id
        self.addexpense = AddExpense()
        self.username = username
        self.setWindowTitle("Delete Expense")
        self.setGeometry(100, 100, 600, 400)

        layout = QVBoxLayout()

        # Date input
        date_label = QLabel("Select Date:")
        layout.addWidget(date_label)
        self.date_input = QDateEdit()
        self.date_input.setDate(QDate.currentDate())
        layout.addWidget(self.date_input)

        # Button to load expenses
        load_button = QPushButton("Load Expenses")
        load_button.clicked.connect(self.load_expenses)
        layout.addWidget(load_button)

        # Text area to display expenses
        self.expense_display = QTextEdit()
        self.expense_display.setReadOnly(True)
        layout.addWidget(self.expense_display)

        # Input to enter the ID for deletion
        id_label = QLabel("Enter ID of the expense to delete:")
        layout.addWidget(id_label)
        self.id_input = QLineEdit()
        layout.addWidget(self.id_input)

        # Delete button
        delete_button = QPushButton("Delete Selected Expense")
        delete_button.clicked.connect(self.delete_expense)
        layout.addWidget(delete_button)
        
        return_button = QPushButton("Return to Add Expense page")
        return_button.clicked.connect(self.return_to_expense)
        layout.addWidget(return_button)
        
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def load_expenses(self):
        date = self.date_input.date().toString('yyyy-MM-dd')
        expenses = self.addexpense.fetch_by_date(self.user_id, date)

        if not expenses:
            QMessageBox.information(self, "No Data", "No expenses found for the selected date.")
            self.expense_display.clear()
            return

        # Display the expenses in the text area
        self.expense_display.clear()
        self.expense_display.append(f"{'ID':<10}{'Amount':<15}{'Description':<20}{'Date':<15}{'Category'}")
        self.expense_display.append("="*65)
        for expense in expenses:
            self.expense_display.append(f"{expense[0]:<10}{expense[1]:<15}{expense[2]:<20}{expense[3]:<15}{expense[4]}")

    def delete_expense(self):
        expense_id = self.id_input.text()

        if not expense_id:
            QMessageBox.warning(self, "Input Error", "Please enter the ID of the expense to delete.")
            return

        confirmation = QMessageBox.question(self,"Confirm Delete",f"Are you sure you want to delete expense ID {expense_id}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if confirmation == QMessageBox.StandardButton.Yes:
            try:
                self.addexpense.delete(expense_id)
                QMessageBox.information(self, "Success", f"Expense ID {expense_id} deleted successfully.")
                self.load_expenses()  # Refresh the displayed expenses after deletion
            except Exception as e:
                QMessageBox.critical(self, "Database Error", str(e))

    def return_to_expense(self):
        self.Main_window = AddExpenseWindow(self.user_id,self.username)
        self.Main_window.show()
        self.close()
                
class AddExpenseWindow(QDialog):
    def __init__(self, user_id ,username):
        super().__init__()
        self.username=username
        self.addexpense = AddExpense()

        self.user_id = user_id
        self.setWindowTitle("Add Expense")
        self.setGeometry(200, 200, 300, 250)

        layout = QVBoxLayout()

        # Amount input
        amount_label = QLabel("Amount:")
        self.amount_input = QLineEdit()
        layout.addWidget(amount_label)
        layout.addWidget(self.amount_input)

        # Description input
        description_label = QLabel("Description:")
        self.description_input = QLineEdit()
        layout.addWidget(description_label)
        layout.addWidget(self.description_input)

        # Category input (dropdown)
        category_label = QLabel("Category:")
        self.category_dropdown = QComboBox()
        self.category_dropdown.addItems(["Food", "Transport", "Entertainment", "Utilities", "Others"])
        layout.addWidget(category_label)
        layout.addWidget(self.category_dropdown)

        # Date input
        date_label = QLabel("Date:")
        self.date_input = QDateEdit()
        self.date_input.setDate(QDate.currentDate())
        layout.addWidget(date_label)
        layout.addWidget(self.date_input)

        # Submit button
        submit_button = QPushButton("Add Expense")
        submit_button.clicked.connect(self.add_expense_to_db)
        layout.addWidget(submit_button)
        
        delete_button = QPushButton("Delete added expense")
        delete_button.clicked.connect(self.go_to_deleteexpense)
        layout.addWidget(delete_button)
        
        return_button = QPushButton("Return to home")
        return_button.clicked.connect(self.return_to_welcome)
        layout.addWidget(return_button)
        
        self.setLayout(layout)

    def add_expense_to_db(self):
        amount = self.amount_input.text()
        description = self.description_input.text()
        category = self.category_dropdown.currentText()
        date = self.date_input.date().toString('yyyy-MM-dd')

        if not amount or not description or not date or not category:
            QMessageBox.warning(self, "Input Error", "Please enter all information.")
            return

        try:
            self.addexpense.insert(self.user_id, amount, description, date, category)
            QMessageBox.information(self, "Success", "Expense added successfully!")
        except Exception as e:
            QMessageBox.critical(self, "Database Error", str(e))
    
    def go_to_deleteexpense(self):
        self.delete_expense_window = DeleteExpenseWindow(self.user_id ,self.username)
        self.delete_expense_window.show()
        self.close()
        
    def return_to_welcome(self):
        self.Main_window = WelcomeWindow(self.username)
        self.Main_window.show()
        self.close()
        
class WelcomeWindow(QMainWindow):
    def __init__(self, username):
        super().__init__()
        
        self.db = User()
        self.user_id = self.db.get_user_id(username)
        self.username=username
        self.setWindowTitle("Welcome")
        self.setGeometry(100, 100, 400, 300)

        layout = QVBoxLayout()

        welcome_label = QLabel(f"Welcome Back, {username}!")
        welcome_label.setFont(QFont('Arial', 18))
        welcome_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(welcome_label)

        layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        add_expense_button = QPushButton("Add Expense")
        add_expense_button.clicked.connect(self.show_add_expense_window)
        layout.addWidget(add_expense_button)

        analyze_button = QPushButton("Analyze")
        layout.addWidget(analyze_button)

        add_income_button = QPushButton("Add Income")
        add_income_button.clicked.connect(self.show_add_income_window)
        layout.addWidget(add_income_button)

        see_history_button = QPushButton("See History")
        see_history_button.clicked.connect(self.show_history)
        layout.addWidget(see_history_button)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def show_add_expense_window(self):
        self.addexpense_window = AddExpenseWindow(self.user_id,self.username)
        self.addexpense_window.show()
        self.close()
        
    def show_add_income_window(self):
        self.income_window = AddIncomeWindow(self.user_id,self.username)
        self.income_window.show()
        self.close()
        
    def show_history(self):
        self.history_window = History(self.user_id,self.username)
        self.history_window.show()
        self.close

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login & Registration")
        self.setGeometry(100, 100, 400, 300)
        self.connection = DatabaseConnection()
        self.db = User(self.connection)

        self.layout = QVBoxLayout()

        self.login_widget = self.create_login_widget()
        self.register_widget = self.create_register_widget()

        self.layout.addWidget(self.login_widget)
        self.layout.addWidget(self.register_widget)
        self.register_widget.hide()

        central_widget = QWidget()
        central_widget.setLayout(self.layout)
        self.setCentralWidget(central_widget)

    def create_login_widget(self):
        layout = QVBoxLayout()

        title_label = QLabel("Login")
        title_label.setFont(QFont('Arial', 18))
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)

        layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        username_label = QLabel("Username:")
        layout.addWidget(username_label)
        self.username_login_input = QLineEdit()
        self.username_login_input.setPlaceholderText("Enter your username")
        layout.addWidget(self.username_login_input)

        password_label = QLabel("Password:")
        layout.addWidget(password_label)
        self.password_login_input = QLineEdit()
        self.password_login_input.setPlaceholderText("Enter your password")
        self.password_login_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.password_login_input)

        login_button = QPushButton("Login")
        login_button.clicked.connect(self.login)
        layout.addWidget(login_button)

        register_link = QPushButton("No account? Register here.")
        register_link.clicked.connect(self.show_register_page)
        layout.addWidget(register_link)

        widget = QWidget()
        widget.setLayout(layout)

        return widget

    def create_register_widget(self):
        layout = QVBoxLayout()

        title_label = QLabel("Register")
        title_label.setFont(QFont('Arial', 18))
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)

        layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        username_label = QLabel("Username:")
        layout.addWidget(username_label)
        self.username_register_input = QLineEdit()
        self.username_register_input.setPlaceholderText("Enter your username")
        layout.addWidget(self.username_register_input)

        password_label = QLabel("Password:")
        layout.addWidget(password_label)
        self.password_register_input = QLineEdit()
        self.password_register_input.setPlaceholderText("Enter your password")
        self.password_register_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.password_register_input)

        register_button = QPushButton("Register")
        register_button.clicked.connect(self.register)
        layout.addWidget(register_button)

        login_link = QPushButton("Already have an account? Login here.")
        login_link.clicked.connect(self.show_login_page)
        layout.addWidget(login_link)

        widget = QWidget()
        widget.setLayout(layout)

        return widget

    def show_login_page(self):
        self.register_widget.hide()
        self.login_widget.show()

    def show_register_page(self):
        self.login_widget.hide()
        self.register_widget.show()

    def login(self):
        username = self.username_login_input.text()
        password = self.password_login_input.text()
        result = self.db.verify_user(username, password)

        if result == "Login successful.":
            QMessageBox.information(self, "Login", "Login successful!")
            self.Main_window = WelcomeWindow(username)
            self.Main_window.show()
            self.close()
        else:
            QMessageBox.warning(self, "Login Failed", "Invalid username or password.")

    def register(self):
        username = self.username_register_input.text()
        password = self.password_register_input.text()
        result = self.db.register_user(username, password)
        QMessageBox.information(self, "Registration", result)

        if result == "Registration successful.":
            self.show_login_page()
        
    def closeEvent(self, event):
        self.db.db_connection.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

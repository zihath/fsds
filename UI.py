import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QTableWidget,QDialog, QPushButton, QMessageBox, QLabel, QLineEdit, QVBoxLayout, QHBoxLayout, QSpacerItem, QSizePolicy, QWidget, QComboBox, QDateEdit
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

    def return_to_welcome(self):
        self.Main_window = WelcomeWindow(self.username)
        self.Main_window.show()
        self.close()


class deleteexpense(QDialog):
    def __init__(self,user_id):
        super().__init__()
        self.user_id = user_id
        self.setWindowTitle("Delete Expense")
        self.resize(400, 300)
        layout = QVBoxLayout()

        self.date_edit = QDateEdit(self)
        self.date_edit.setCalendarPopup(True)
        self.date_edit.setDate(QDate.currentDate())
        layout.addWidget(self.date_edit)

        self.table = QTableWidget(self)
        layout.addWidget(self.table)

        self.show_expenses_button = QPushButton("Show Expenses", self)
        self.show_expenses_button.clicked.connect(self.show_expenses)
        layout.addWidget(self.show_expenses_button)

        self.delete_button = QPushButton("Delete Selected Expense", self)
        self.delete_button.clicked.connect(self.delete_selected_expense)
        layout.addWidget(self.delete_button)

        self.setLayout(layout)

    def show_expenses(self):
        date = self.date_edit.date().toString("yyyy-MM-dd")
        expenses = AddExpense(self.db_connection).get_expenses_by_date(self.user_id, date)

        self.table.setRowCount(len(expenses))
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["ID", "Amount", "Description", "Date", "Category"])

        for row, expense in enumerate(expenses):
            for col, data in enumerate(expense):
                self.table.setItem(row, col, QTableWidgetItem(str(data)))

    def delete_selected_expense(self):
        selected_row = self.table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Error", "Please select a row to delete")
            return

        expense_id = self.table.item(selected_row, 0).text()  # Get the ID from the first column

        # Confirm the delete action
        confirm = QMessageBox.question(self, "Confirm Delete", "Are you sure you want to delete this expense?",
                                       QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

        if confirm == QMessageBox.StandardButton.Yes:
            AddExpense(self.db_connection).delete_expense(expense_id)
            QMessageBox.information(self, "Success", "Expense deleted successfully!")
            self.show_expenses()
            
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
        self.delete_expense_window = deleteexpense(self.user_id)
        self.delete_expense_window.show()
        self.close()
        
    def return_to_welcome(self):
        self.Main_window = WelcomeWindow(self.username)
        self.Main_window.show()
        
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

import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow,QStackedWidget,QSplitter,QTextEdit, QTableWidgetItem,QTableWidget,QDialog, QPushButton, QMessageBox, QLabel, QLineEdit, QVBoxLayout, QHBoxLayout, QSpacerItem, QSizePolicy, QWidget, QComboBox, QDateEdit
)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt, QDate
from database import User, AddExpense, DatabaseConnection , AddIncome

class AddIncomeWindow(QMainWindow):
    def __init__(self, user_id, username):
        super().__init__()
        self.username = username
        self.user_id = user_id
        self.addincome = AddIncome()  # Assuming AddIncome is a class you have defined for database interaction

        self.setWindowTitle("Manage Income")
        self.setGeometry(100, 100, 400, 300)

        layout = QVBoxLayout()

        # Horizontal layout for Add and Update buttons
        button_layout = QHBoxLayout()
        
        # Add Income button
        self.add_income_button = QPushButton("Add Income")
        self.add_income_button.clicked.connect(self.show_add_income_form)
        button_layout.addWidget(self.add_income_button)

        # Update Income button
        self.update_income_button = QPushButton("Update Income")
        self.update_income_button.clicked.connect(self.show_update_income_form)
        button_layout.addWidget(self.update_income_button)

        layout.addLayout(button_layout)

        # Add Income Form (Initially hidden)
        self.add_income_form = QWidget()
        add_income_layout = QVBoxLayout()

        amount_label = QLabel("Amount:")
        add_income_layout.addWidget(amount_label)
        self.amount_input = QLineEdit()
        self.amount_input.setPlaceholderText("Enter amount")
        add_income_layout.addWidget(self.amount_input)

        source_label = QLabel("Source of Income:")
        add_income_layout.addWidget(source_label)
        self.source_input = QComboBox()
        self.source_input.addItems(["Salary", "Business", "Investments", "Other"])
        add_income_layout.addWidget(self.source_input)

        date_label = QLabel("Date:")
        self.date_input = QDateEdit()
        self.date_input.setDate(QDate.currentDate())
        add_income_layout.addWidget(date_label)
        add_income_layout.addWidget(self.date_input)

        submit_button = QPushButton("Submit Income")
        submit_button.clicked.connect(self.add_income)
        add_income_layout.addWidget(submit_button)

        self.add_income_form.setLayout(add_income_layout)
        self.add_income_form.setVisible(True)  # Initially hidden
        layout.addWidget(self.add_income_form)

        # Update Income Form (Initially hidden)
        self.update_income_form = QWidget()
        update_income_layout = QVBoxLayout()

        update_amount_label = QLabel("New Amount:")
        update_income_layout.addWidget(update_amount_label)
        self.update_amount_input = QLineEdit()
        self.update_amount_input.setPlaceholderText("Enter new amount")
        update_income_layout.addWidget(self.update_amount_input)

        update_source_label = QLabel("New Source of Income:")
        update_income_layout.addWidget(update_source_label)
        self.update_source_input = QComboBox()
        self.update_source_input.addItems(["Salary", "Business", "Investments", "Other"])
        update_income_layout.addWidget(self.update_source_input)

        update_button = QPushButton("Update Income")
        update_button.clicked.connect(self.update_income)
        update_income_layout.addWidget(update_button)

        self.update_income_form.setLayout(update_income_layout)
        self.update_income_form.setVisible(False)  # Initially hidden
        layout.addWidget(self.update_income_form)

        # Central widget setup
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def show_add_income_form(self):
        """ Show the Add Income form and hide the Update Income form """
        self.add_income_form.setVisible(True)
        self.update_income_form.setVisible(False)

    def show_update_income_form(self):
        """ Show the Update Income form and hide the Add Income form """
        self.update_income_form.setVisible(True)
        self.add_income_form.setVisible(False)

    def add_income(self):
        """ Logic to add income """
        amount = self.amount_input.text()
        source = self.source_input.currentText()
        date = self.date_input.date().toString('yyyy-MM-dd')

        if not amount or not date:
            QMessageBox.warning(self, "Input Error", "Please enter all the information.")
            return

        try:
            self.addincome.insert(self.user_id, amount, source, date)
            QMessageBox.information(self, "Success", "Income added successfully!")
            self.amount_input.clear()
            self.source_input.setCurrentIndex(0)
            self.date_input.setDate(QDate.currentDate())
        except Exception as e:
            QMessageBox.critical(self, "Database Error", str(e))

    def update_income(self):
        """ Logic to update income """
        new_amount = self.update_amount_input.text()
        new_source = self.update_source_input.currentText()

        if not new_amount:
            QMessageBox.warning(self, "Input Error", "Please enter the new amount.")
            return

        try:
            self.addincome.update(self.user_id, new_amount, new_source)
            QMessageBox.information(self, "Success", "Income updated successfully!")
            self.update_amount_input.clear()
            self.update_source_input.setCurrentIndex(0)
        except Exception as e:
            QMessageBox.critical(self, "Database Error", str(e))

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
        
class AddExpenseWindow(QMainWindow):
    def __init__(self, user_id, username):
        super().__init__()
        self.username = username
        self.user_id = user_id
        self.addexpense = AddExpense()  # Assuming AddExpense is a class you have defined for database interaction

        self.setWindowTitle("Manage Expenses")
        self.setGeometry(100, 100, 500, 400)

        layout = QVBoxLayout()

        # Horizontal layout for Add and Delete buttons
        button_layout = QHBoxLayout()
        
        # Add Expense button
        self.add_expense_button = QPushButton("Add Expense")
        self.add_expense_button.clicked.connect(self.show_add_expense_form)
        button_layout.addWidget(self.add_expense_button)

        # Delete Expense button
        self.delete_expense_button = QPushButton("Delete Expense")
        self.delete_expense_button.clicked.connect(self.show_delete_expense_form)
        button_layout.addWidget(self.delete_expense_button)

        layout.addLayout(button_layout)

        # Add Expense Form (Initially hidden)
        self.add_expense_form = QWidget()
        add_expense_layout = QVBoxLayout()

        amount_label = QLabel("Amount:")
        add_expense_layout.addWidget(amount_label)
        self.amount_input = QLineEdit()
        add_expense_layout.addWidget(self.amount_input)

        description_label = QLabel("Description:")
        add_expense_layout.addWidget(description_label)
        self.description_input = QLineEdit()
        add_expense_layout.addWidget(self.description_input)

        category_label = QLabel("Category:")
        self.category_dropdown = QComboBox()
        self.category_dropdown.addItems(["Food", "Transport", "Entertainment", "Utilities", "Others"])
        add_expense_layout.addWidget(category_label)
        add_expense_layout.addWidget(self.category_dropdown)

        date_label = QLabel("Date:")
        self.date_input = QDateEdit()
        self.date_input.setDate(QDate.currentDate())
        add_expense_layout.addWidget(date_label)
        add_expense_layout.addWidget(self.date_input)

        submit_button = QPushButton("Submit Expense")
        submit_button.clicked.connect(self.add_expense_to_db)
        add_expense_layout.addWidget(submit_button)

        self.add_expense_form.setLayout(add_expense_layout)
        self.add_expense_form.setVisible(True)  # Initially visible
        layout.addWidget(self.add_expense_form)

        # Delete Expense Form (Initially hidden)
        self.delete_expense_form = QWidget()
        delete_expense_layout = QVBoxLayout()

        date_label = QLabel("Select Date:")
        delete_expense_layout.addWidget(date_label)
        self.date_input_delete = QDateEdit()
        self.date_input_delete.setDate(QDate.currentDate())
        delete_expense_layout.addWidget(self.date_input_delete)

        load_button = QPushButton("Load Expenses")
        load_button.clicked.connect(self.load_expenses)
        delete_expense_layout.addWidget(load_button)

        self.expense_display = QTextEdit()
        self.expense_display.setReadOnly(True)
        delete_expense_layout.addWidget(self.expense_display)

        id_label = QLabel("Enter ID of the expense to delete:")
        delete_expense_layout.addWidget(id_label)
        self.id_input = QLineEdit()
        delete_expense_layout.addWidget(self.id_input)

        delete_button = QPushButton("Delete Selected Expense")
        delete_button.clicked.connect(self.delete_expense)
        delete_expense_layout.addWidget(delete_button)

        self.delete_expense_form.setLayout(delete_expense_layout)
        self.delete_expense_form.setVisible(False)  # Initially hidden
        layout.addWidget(self.delete_expense_form)

        # Central widget setup
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def show_add_expense_form(self):
        """ Show the Add Expense form and hide the Delete Expense form """
        self.add_expense_form.setVisible(True)
        self.delete_expense_form.setVisible(False)

    def show_delete_expense_form(self):
        """ Show the Delete Expense form and hide the Add Expense form """
        self.add_expense_form.setVisible(False)
        self.delete_expense_form.setVisible(True)

    def add_expense_to_db(self):
        """ Logic to add an expense to the database """
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
            self.amount_input.clear()
            self.description_input.clear()
            self.category_dropdown.setCurrentIndex(0)
            self.date_input.setDate(QDate.currentDate())
        except Exception as e:
            QMessageBox.critical(self, "Database Error", str(e))

    def load_expenses(self):
        """ Load expenses based on the selected date """
        date = self.date_input_delete.date().toString('yyyy-MM-dd')
        expenses = self.addexpense.fetch_by_date(self.user_id, date)

        if not expenses:
            QMessageBox.information(self, "No Data", "No expenses found for the selected date.")
            self.expense_display.clear()
            return

        # Display expenses in the text area
        self.expense_display.clear()
        self.expense_display.append(f"{'ID':<10}{'Amount':<15}{'Description':<20}{'Date':<15}{'Category'}")
        self.expense_display.append("=" * 65)
        for expense in expenses:
            self.expense_display.append(f"{expense[0]:<10}{expense[1]:<15}{expense[2]:<20}{expense[3]:<15}{expense[4]}")

    def delete_expense(self):
        """ Delete selected expense based on the ID """
        expense_id = self.id_input.text()

        if not expense_id:
            QMessageBox.warning(self, "Input Error", "Please enter the ID of the expense to delete.")
            return

        confirmation = QMessageBox.question(
            self, "Confirm Delete", f"Are you sure you want to delete expense ID {expense_id}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if confirmation == QMessageBox.StandardButton.Yes:
            try:
                self.addexpense.delete(expense_id)
                QMessageBox.information(self, "Success", f"Expense ID {expense_id} deleted successfully.")
                self.load_expenses()  # Refresh the displayed expenses after deletion
            except Exception as e:
                QMessageBox.critical(self, "Database Error", str(e))
        
class WelcomeWindow(QMainWindow):
    def __init__(self, username):
        super().__init__()

        self.db = User()
        self.user_id = self.db.get_user_id(username)
        self.username = username
        self.setWindowTitle("Welcome")
        self.setGeometry(100, 100, 800, 400)

        # Main layout with QSplitter
        self.splitter = QSplitter(Qt.Orientation.Horizontal)

        # Left side layout (sidebar)
        self.sidebar_layout = QVBoxLayout()
        self.sidebar_widget = QWidget()

        welcome_label = QLabel(f"Welcome Back, {username}!")
        welcome_label.setFont(QFont('Arial', 18))
        welcome_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.sidebar_layout.addWidget(welcome_label)

        self.sidebar_layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        # Add buttons for sidebar
        add_expense_button = QPushButton("Add Expense")
        add_expense_button.clicked.connect(self.display_add_expense)
        self.sidebar_layout.addWidget(add_expense_button)

        analyze_button = QPushButton("Analyze")
        analyze_button.clicked.connect(self.display_analyze)
        self.sidebar_layout.addWidget(analyze_button)

        add_income_button = QPushButton("Add Income")
        add_income_button.clicked.connect(self.display_add_income)
        self.sidebar_layout.addWidget(add_income_button)

        see_history_button = QPushButton("See History")
        see_history_button.clicked.connect(self.display_history)
        self.sidebar_layout.addWidget(see_history_button)

        self.sidebar_layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        self.sidebar_widget.setLayout(self.sidebar_layout)
        self.splitter.addWidget(self.sidebar_widget)

        # Right side layout with QStackedWidget for content
        self.stacked_widget = QStackedWidget()
        self.splitter.addWidget(self.stacked_widget)

        # Set the sidebar width to take less space
        self.splitter.setSizes([150, 650])

        # Toggle button to show/hide the sidebar
        self.toggle_button = QPushButton("≡")  # Menu icon (you can use another symbol)
        self.toggle_button.setFixedWidth(30)
        self.toggle_button.clicked.connect(self.toggle_sidebar)

        # Create a layout for toggle button and splitter
        top_layout = QHBoxLayout()
        top_layout.addWidget(self.toggle_button)
        top_layout.addWidget(self.splitter)

        # Central widget for main window
        central_widget = QWidget()
        central_layout = QVBoxLayout()
        central_layout.addLayout(top_layout)
        central_widget.setLayout(central_layout)
        self.setCentralWidget(central_widget)

        # Display the first page (default content on load)
        self.display_add_expense()

        # Keep track of whether the sidebar is visible
        self.sidebar_visible = True

    # Methods to show different content in the right side of the window
    def display_add_expense(self):
        self.expense_window = AddExpenseWindow(self.user_id, self.username)
        self.stacked_widget.addWidget(self.expense_window)
        self.stacked_widget.setCurrentWidget(self.expense_window)

    def display_analyze(self):
        analyze_widget = QLabel("Analyze Data (To be implemented)")
        analyze_widget.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.stacked_widget.addWidget(analyze_widget)
        self.stacked_widget.setCurrentWidget(analyze_widget)

    def display_add_income(self):
        self.income_window = AddIncomeWindow(self.user_id, self.username)
        self.stacked_widget.addWidget(self.income_window)
        self.stacked_widget.setCurrentWidget(self.income_window)

    def display_history(self):
        self.history_window = History(self.user_id, self.username)
        self.stacked_widget.addWidget(self.history_window)
        self.stacked_widget.setCurrentWidget(self.history_window)

    # Method to toggle the sidebar
    def toggle_sidebar(self):
        if self.sidebar_visible:
            # Hide the sidebar by setting its width to 0
            self.splitter.setSizes([0, 800])
        else:
            # Show the sidebar by restoring its original size
            self.splitter.setSizes([150, 650])

        self.sidebar_visible = not self.sidebar_visible

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

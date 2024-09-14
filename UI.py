import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow,QStackedWidget,QSplitter,QTextEdit, QTableWidgetItem,QTableWidget,QDialog, QPushButton, QMessageBox, QLabel, QLineEdit, QVBoxLayout, QHBoxLayout, QSpacerItem, QSizePolicy, QWidget, QComboBox, QDateEdit
)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt, QDate
from database import User, AddExpense, DatabaseConnection , AddIncome
import matplotlib.pyplot as plt

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
        self.add_income_button.setFont(QFont("Verdana", 12))
        self.add_income_button.setStyleSheet("background-color: #4CAF50; color: white; padding: 10px;")  # Green
        button_layout.addWidget(self.add_income_button)

        # Update Income button
        self.update_income_button = QPushButton("Update Income")
        self.update_income_button.clicked.connect(self.show_update_income_form)
        self.update_income_button.setFont(QFont("Verdana", 12))
        self.update_income_button.setStyleSheet("background-color: #2196F3; color: white; padding: 10px;")  # Blue
        button_layout.addWidget(self.update_income_button)

        layout.addLayout(button_layout)

        # Add Income Form (Initially hidden)
        self.add_income_form = QWidget()
        add_income_layout = QVBoxLayout()

        amount_label = QLabel("Amount:")
        amount_label.setFont(QFont("Open Sans", 14, QFont.Weight.Bold))
        amount_label.setStyleSheet("color: #333333;")  # Dark Gray
        add_income_layout.addWidget(amount_label)
        self.amount_input = QLineEdit()
        self.amount_input.setPlaceholderText("Enter amount")
        self.amount_input.setStyleSheet("border: 1px solid #4CAF50; padding: 5px;")  # Green border
        add_income_layout.addWidget(self.amount_input)

        source_label = QLabel("Source of Income:")
        source_label.setFont(QFont("Open Sans", 14, QFont.Weight.Bold))
        source_label.setStyleSheet("color: #333333;")  # Dark Gray
        add_income_layout.addWidget(source_label)
        self.source_input = QComboBox()
        self.source_input.addItems(["Salary", "Business", "Investments", "Other"])
        self.source_input.setStyleSheet("border: 1px solid #4CAF50; padding: 5px;")  # Green border
        add_income_layout.addWidget(self.source_input)

        date_label = QLabel("Date:")
        date_label.setFont(QFont("Open Sans", 14, QFont.Weight.Bold))
        date_label.setStyleSheet("color: #333333;")  # Dark Gray
        add_income_layout.addWidget(date_label)
        self.date_input = QDateEdit()
        self.date_input.setDate(QDate.currentDate())
        add_income_layout.addWidget(self.date_input)

        submit_button = QPushButton("Submit Income")
        submit_button.clicked.connect(self.add_income)
        submit_button.setFont(QFont("Verdana", 12))
        submit_button.setStyleSheet("background-color: #4CAF50; color: white; padding: 10px;") # Green
        add_income_layout.addWidget(submit_button)

        self.add_income_form.setLayout(add_income_layout)
        self.add_income_form.setVisible(True)  # Initially visible
        layout.addWidget(self.add_income_form)

        # Update Income Form (Initially hidden)
        self.update_income_form = QWidget()
        update_income_layout = QVBoxLayout()

        update_amount_label = QLabel("New Amount:")
        update_amount_label.setFont(QFont("Open Sans", 14, QFont.Weight.Bold))
        update_amount_label.setStyleSheet("color: #333333;")  # Dark Gray
        update_income_layout.addWidget(update_amount_label)
        self.update_amount_input = QLineEdit()
        self.update_amount_input.setPlaceholderText("Enter new amount")
        self.update_amount_input.setStyleSheet("border: 1px solid #2196F3; padding: 5px;")  # Blue border
        update_income_layout.addWidget(self.update_amount_input)

        update_source_label = QLabel("New Source of Income:")
        update_source_label.setFont(QFont("Open Sans", 14, QFont.Weight.Bold))
        update_source_label.setStyleSheet("color: #333333;")  # Dark Gray
        update_income_layout.addWidget(update_source_label)
        self.update_source_input = QComboBox()
        self.update_source_input.addItems(["Salary", "Business", "Investments", "Other"])
        self.update_source_input.setStyleSheet("border: 1px solid #2196F3; padding: 5px;")  # Blue border
        update_income_layout.addWidget(self.update_source_input)

        update_button = QPushButton("Update Income")
        update_button.clicked.connect(self.update_income)
        update_button.setFont(QFont("Verdana", 12))
        update_button.setStyleSheet("background-color: #2196F3; color: white; padding: 10px;") #blue
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

        # Start Date label
        start_date_label = QLabel("Start Date:")
        start_date_label.setFont(QFont('Open Sans', 14, QFont.Weight.Bold))
        start_date_label.setStyleSheet("color: #2C3E50;")
        layout.addWidget(start_date_label)

        # Start Date input
        self.start_date_input = QDateEdit()
        self.start_date_input.setDate(QDate.currentDate())
        self.start_date_input.setStyleSheet("""
            QDateEdit {
                padding: 10px;
                border: 1px solid #BDC3C7;
                border-radius: 5px;
                font-size: 14px;
                background-color: #FFFFFF;
                color: #2C3E50;
            }
        """)
        layout.addWidget(self.start_date_input)

        # End Date label
        end_date_label = QLabel("End Date:")
        end_date_label.setFont(QFont('Open Sans', 14, QFont.Weight.Bold))
        end_date_label.setStyleSheet("color: #2C3E50;")
        layout.addWidget(end_date_label)

        # End Date input
        self.end_date_input = QDateEdit()
        self.end_date_input.setDate(QDate.currentDate())
        self.end_date_input.setStyleSheet("""
            QDateEdit {
                padding: 10px;
                border: 1px solid #BDC3C7;
                border-radius: 5px;
                font-size: 14px;
                background-color: #FFFFFF;
                color: #2C3E50;
            }
        """)
        layout.addWidget(self.end_date_input)

        # Show Transactions button
        show_button = QPushButton("Show Transactions")
        show_button.setFont(QFont('Montserrat', 14, QFont.Weight.Medium))
        show_button.setCursor(Qt.CursorShape.PointingHandCursor)
        show_button.setStyleSheet("""
            QPushButton {
                padding: 10px;
                background-color: #1ABC9C;
                color: white;
                border-radius: 8px;
                font-weight: bold;
                transition: background-color 0.3s ease;
            }
            QPushButton:hover {
                background-color: #16A085;
            }
        """)
        show_button.clicked.connect(self.load_expenses)
        layout.addWidget(show_button)
        
        # Display area for expenses
        self.expense_display = QTextEdit()
        self.expense_display.setReadOnly(True)
        layout.addWidget(self.expense_display)

         # Table for displaying expenses
        self.expense_table = QTableWidget()
        self.expense_table.setColumnCount(5)  # Number of columns
        self.expense_table.setHorizontalHeaderLabels(['ID', 'Amount', 'Description', 'Date', 'Category'])
        self.expense_table.horizontalHeader().setStretchLastSection(True)
        self.expense_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.expense_table.setStyleSheet("""
            QTableWidget {
                border: 1px solid #BDC3C7;
                border-radius: 5px;
                font-size: 14px;
                background-color: #FFFFFF;
                color: #2C3E50;
            }
            QHeaderView::section {
                background-color: #ECF0F1;
                color: #2C3E50;
                border: 1px solid #BDC3C7;
            }
        """)
        layout.addWidget(self.expense_table)

        # Central widget setup
        central_widget = QWidget()
        central_widget.setLayout(layout)
        central_widget.setStyleSheet("""
            QWidget {
                background-color: #ECF0F1;
            }
        """)
        self.setCentralWidget(central_widget)

    def load_expenses(self):
        start_date = self.start_date_input.date().toString('yyyy-MM-dd')
        end_date = self.end_date_input.date().toString('yyyy-MM-dd')

        # Fetch expenses from backend
        try:
            expenses = self.addexpense.fetch_between_date(self.user_id, start_date, end_date)

            if not expenses:
                QMessageBox.information(self, "No Data", "No expenses found for the selected date range.")
                self.expense_table.setRowCount(0)  # Clear the table
                return

            # Set the number of rows in the table
            self.expense_table.setRowCount(len(expenses))

            # Populate the table with data
            for row, expense in enumerate(expenses):
                if len(expense) == 5:
                    for col, data in enumerate(expense):
                        item = QTableWidgetItem(str(data))
                        self.expense_table.setItem(row, col, item)
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

        # Font settings for labels and buttons
        title_font = QFont("Open Sans", 14, QFont.Weight.Bold)  # QFont.Bold is the correct constant for bold text
        button_font = QFont("Verdana", 12)

        # Horizontal layout for Add and Delete buttons
        button_layout = QHBoxLayout()

        # Add Expense button
        self.add_expense_button = QPushButton("Add Expense")
        self.add_expense_button.setFont(button_font)
        self.add_expense_button.setStyleSheet("background-color: #4CAF50; color: white; padding: 10px;")
        self.add_expense_button.clicked.connect(self.show_add_expense_form)
        button_layout.addWidget(self.add_expense_button)

        # Delete Expense button
        self.delete_expense_button = QPushButton("Delete Expense")
        self.delete_expense_button.setFont(button_font)
        self.delete_expense_button.setStyleSheet("background-color: #F44336; color: white; padding: 10px;")
        self.delete_expense_button.clicked.connect(self.show_delete_expense_form)
        button_layout.addWidget(self.delete_expense_button)

        layout.addLayout(button_layout)

        # Add Expense Form (Initially hidden)
        self.add_expense_form = QWidget()
        add_expense_layout = QVBoxLayout()

        amount_label = QLabel("Amount:")
        amount_label.setFont(title_font)
        add_expense_layout.addWidget(amount_label)
        self.amount_input = QLineEdit()
        self.amount_input.setStyleSheet("border: 1px solid #2196F3; padding: 5px;")
        add_expense_layout.addWidget(self.amount_input)

        description_label = QLabel("Description:")
        description_label.setFont(title_font)
        add_expense_layout.addWidget(description_label)
        self.description_input = QLineEdit()
        self.description_input.setStyleSheet("border: 1px solid #2196F3; padding: 5px;")
        add_expense_layout.addWidget(self.description_input)

        category_label = QLabel("Category:")
        category_label.setFont(title_font)
        self.category_dropdown = QComboBox()
        self.category_dropdown.addItems(["Food", "Transport", "Entertainment", "Utilities", "Others"])
        self.category_dropdown.setStyleSheet("border: 1px solid #2196F3; padding: 5px;")
        add_expense_layout.addWidget(category_label)
        add_expense_layout.addWidget(self.category_dropdown)

        date_label = QLabel("Date:")
        date_label.setFont(title_font)
        self.date_input = QDateEdit()
        self.date_input.setDate(QDate.currentDate())
        self.date_input.setStyleSheet("border: 1px solid #2196F3; padding: 5px;")
        add_expense_layout.addWidget(date_label)
        add_expense_layout.addWidget(self.date_input)

        submit_button = QPushButton("Submit Expense")
        submit_button.setFont(button_font)
        submit_button.setStyleSheet("background-color: #2196F3; color: white; padding: 10px;")
        submit_button.clicked.connect(self.add_expense_to_db)
        add_expense_layout.addWidget(submit_button)

        self.add_expense_form.setLayout(add_expense_layout)
        self.add_expense_form.setVisible(True)  # Initially visible
        layout.addWidget(self.add_expense_form)

        # Delete Expense Form (Initially hidden)
        self.delete_expense_form = QWidget()
        delete_expense_layout = QVBoxLayout()

        date_label = QLabel("Select Date:")
        date_label.setFont(title_font)
        delete_expense_layout.addWidget(date_label)
        self.date_input_delete = QDateEdit()
        self.date_input_delete.setDate(QDate.currentDate())
        self.date_input_delete.setStyleSheet("border: 1px solid #F44336; padding: 5px;")
        delete_expense_layout.addWidget(self.date_input_delete)

        load_button = QPushButton("Load Expenses")
        load_button.setFont(button_font)
        load_button.setStyleSheet("background-color: #FF9800; color: white; padding: 10px;")
        load_button.clicked.connect(self.load_expenses)
        delete_expense_layout.addWidget(load_button)

        self.expense_display = QTextEdit()
        self.expense_display.setStyleSheet("border: 1px solid #F44336; padding: 5px;")
        self.expense_display.setReadOnly(True)
        delete_expense_layout.addWidget(self.expense_display)

        id_label = QLabel("Enter ID of the expense to delete:")
        id_label.setFont(title_font)
        delete_expense_layout.addWidget(id_label)
        self.id_input = QLineEdit()
        self.id_input.setStyleSheet("border: 1px solid #F44336; padding: 5px;")
        delete_expense_layout.addWidget(self.id_input)

        delete_button = QPushButton("Delete Selected Expense")
        delete_button.setFont(button_font)
        delete_button.setStyleSheet("background-color: #F44336; color: white; padding: 10px;")
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
        self.analyze_window = ExpensePlotWindow(self.user_id)
        self.stacked_widget.addWidget(self.analyze_window)
        self.stacked_widget.setCurrentWidget(self.analyze_window)

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

class ExpensePlotWindow(QWidget):
    def __init__(self, user_id):
        super().__init__()
        self.user_id = user_id
        self.setWindowTitle("Expense Plot")
        self.setGeometry(100, 100, 800, 600)
        self.addexpense = AddExpense()

        # Layout setup
        layout = QVBoxLayout()

        # Start Date input
        self.start_date_label = QLabel("Start Date:")
        self.start_date_input = QDateEdit()
        self.start_date_input.setDate(QDate.currentDate().addMonths(-1))  # Default to 1 month ago
        layout.addWidget(self.start_date_label)
        layout.addWidget(self.start_date_input)

        # End Date input
        self.end_date_label = QLabel("End Date:")
        self.end_date_input = QDateEdit()
        self.end_date_input.setDate(QDate.currentDate())  # Default to today
        layout.addWidget(self.end_date_label)
        layout.addWidget(self.end_date_input)

        # Button to fetch and plot the data
        self.plot_button = QPushButton("Plot Expenses")
        self.plot_button.clicked.connect(self.plot_expenses)
        layout.addWidget(self.plot_button)

        # Matplotlib canvas for displaying plots
        self.canvas = FigureCanvas(Figure(figsize=(5, 4)))
        layout.addWidget(self.canvas)
        self.ax = self.canvas.figure.add_subplot(111)

        # Set the layout for the window
        self.setLayout(layout)

    def plot_expenses(self):
        """Fetch data and generate plots."""
        # Get the date range from the user
        start_date = self.start_date_input.date().toString('yyyy-MM-dd')
        end_date = self.end_date_input.date().toString('yyyy-MM-dd')

        try:
            # Fetch data from the database
            data = self.addexpense.fetch_between_date(self.user_id, start_date, end_date)

            if not data:
                QMessageBox.warning(self, "No Data", "No expenses found in the given date range.")
                return

            # Prepare the data for plotting
            categories = {}
            for row in data:
                category = row[4]  # Assuming the 4th column is category
                amount = float(row[1])  # Assuming the 1st column is amount
                if category in categories:
                    categories[category] += amount
                else:
                    categories[category] = amount

            # If no expenses found, show a message
            if not categories:
                QMessageBox.information(self, "No Data", "No expenses to display.")
                return

            # Generate plots
            self.generate_plots(categories)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred while fetching the data: {str(e)}")

    def generate_plots(self, categories):
        """Generate and display the pie plot and bar plot inside the window."""
        labels = list(categories.keys())
        sizes = list(categories.values())

        # Clear any previous plots
        self.ax.clear()

        # Create pie plot
        # self.ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140, colors=plt.cm.Paired.colors)
        # self.ax.set_title('Expenses by Category (Pie Chart)')
        # self.canvas.draw()  # Update the canvas to reflect the new plot

        # You can toggle between pie plot and bar plot, or create separate tabs if needed
        # Uncomment below if you want to display a bar chart
        self.ax.bar(labels, sizes, color=plt.cm.Paired.colors)
        self.ax.set_title('Expenses by Category (Bar Chart)')
        self.ax.set_xlabel('Category')
        self.ax.set_ylabel('Amount Spent')
        self.canvas.draw()  # Update the canvas to reflect the new plot

        
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login & Registration")
        self.setGeometry(100, 100, 400, 300)
        self.setStyleSheet("""
            QMainWindow {
                background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 #89CFF0, stop:1 #006994);
            }
            QLabel {
                color: white;
                font-family: 'Roboto', sans-serif;
                font-size: 16px;
            }
            QLineEdit {
                padding: 10px;
                border: 2px solid #ccc;
                border-radius: 10px;
                background-color: rgba(255, 255, 255, 0.8);
                color: #333;
            }
            QPushButton {
                padding: 10px;
                background-color: #007BFF;
                color: white;
                border-radius: 10px;
                font-family: 'Roboto', sans-serif;
                font-size: 14px;
                box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.2);
                transition: background-color 0.3s ease, transform 0.3s ease;
            }
            QPushButton:hover {
                background-color: #0056b3;
                transform: scale(1.05);
            }
            QPushButton:pressed {
                background-color: #003d7a;
                transform: scale(1.0);
            }
            QPushButton#linkButton {
                color: #F0E68C;
                background: transparent;
                border: none;
                font-size: 12px;
                text-decoration: underline;
            }
            QPushButton#linkButton:hover {
                color: #FFD700;
            }
        """)
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
        title_label.setFont(QFont('Roboto', 18))
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)

        layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

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

        layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        login_button = QPushButton("Login")
        login_button.clicked.connect(self.login)
        layout.addWidget(login_button)

        register_link = QPushButton("No account? Register here.")
        register_link.setObjectName("linkButton")
        register_link.clicked.connect(self.show_register_page)
        layout.addWidget(register_link)

        widget = QWidget()
        widget.setLayout(layout)

        return widget

    def create_register_widget(self):
        layout = QVBoxLayout()

        title_label = QLabel("Register")
        title_label.setFont(QFont('Roboto', 18))
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)

        layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

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

        layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        register_button = QPushButton("Register")
        register_button.clicked.connect(self.register)
        layout.addWidget(register_button)

        login_link = QPushButton("Already have an account? Login here.")
        login_link.setObjectName("linkButton")
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

class HomePageWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Personal Income & Spending Analyzer")
        self.setGeometry(100, 100, 600, 400)
        self.init_ui()

    def init_ui(self):
        # Set up layout
        self.layout = QVBoxLayout()
        
        # Project title
        title_label = QLabel("Welcome to Your Financial Planner")
        title_label.setFont(QFont('Montserrat', 26, QFont.Weight.Bold))
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("color: #2C3E50; padding: 10px;")
        self.layout.addWidget(title_label)

        # About the project
        description_label = QLabel("Manage your income, track expenses, and unlock smart financial insights with our cutting-edge machine learning algorithms. "
                                   "Take the first step towards smarter financial decisions and a brighter financial future.")
        description_label.setWordWrap(True)
        description_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        description_label.setFont(QFont('Open Sans', 14))
        description_label.setStyleSheet("color: #34495E; padding: 20px;")
        self.layout.addWidget(description_label)

        # Spacer to center content
        self.layout.addSpacerItem(QSpacerItem(20, 60, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        # Button to navigate to login
        login_button = QPushButton("Start Managing Your Finances")
        login_button.setFont(QFont('Montserrat', 16, QFont.Weight.Medium))
        login_button.setCursor(Qt.CursorShape.PointingHandCursor)
        login_button.setStyleSheet("""
            QPushButton {
                padding: 15px 30px;
                background-color: #1ABC9C;
                color: white;
                border-radius: 10px;
                font-size: 16px;
                font-weight: bold;
                transition: background-color 0.3s ease;
            }
            QPushButton:hover {
                background-color: #16A085;
            }
        """)
        login_button.clicked.connect(self.go_to_login)
        self.layout.addWidget(login_button, alignment=Qt.AlignmentFlag.AlignCenter)

        # Set layout and background
        central_widget = QWidget()
        central_widget.setLayout(self.layout)
        central_widget.setStyleSheet("""
            QWidget {
                background-color: #ECF0F1;
            }
        """)
        self.setCentralWidget(central_widget)

    def go_to_login(self):
        self.login_window = MainWindow()
        self.login_window.show()
        self.close()
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    home_page = HomePageWindow()
    home_page.show()
    sys.exit(app.exec())

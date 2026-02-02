import requests
from dashboard import Dashboard

from PyQt5.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QMessageBox
)
from PyQt5.QtCore import Qt


class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login")
        self.setFixedSize(360, 300)

        self.access_token = None
        self.refresh_token = None

        # navigation hook (set from main.py)
        self.show_signup = None

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(12)

        # -------- TITLE --------
        title = QLabel("Welcome Back")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("""
            QLabel {
                font-size: 20px;
                font-weight: bold;
            }
        """)
        main_layout.addWidget(title)

        subtitle = QLabel("Login to continue")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet("color: gray;")
        main_layout.addWidget(subtitle)

        # -------- INPUTS --------
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")
        self.username_input.setStyleSheet("padding: 6px;")
        main_layout.addWidget(self.username_input)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setStyleSheet("padding: 6px;")
        main_layout.addWidget(self.password_input)

        # -------- LOGIN BUTTON --------
        self.login_btn = QPushButton("Login")
        self.login_btn.setCursor(Qt.PointingHandCursor)
        self.login_btn.setStyleSheet("""
            QPushButton {
                padding: 8px;
                font-size: 13px;
                font-weight: bold;
            }
        """)
        self.login_btn.clicked.connect(self.login)
        main_layout.addWidget(self.login_btn)

        # -------- SIGNUP LINK --------
        signup_btn = QPushButton("Create a new account")
        signup_btn.setCursor(Qt.PointingHandCursor)
        signup_btn.setFlat(True)
        signup_btn.setStyleSheet("""
            QPushButton {
                color: #1a73e8;
                text-decoration: underline;
            }
            QPushButton:hover {
                color: #0c59cf;
            }
        """)
        signup_btn.clicked.connect(self.open_signup)
        main_layout.addWidget(signup_btn)

        main_layout.addStretch()
        self.setLayout(main_layout)

    # -------- NAVIGATION --------
    def open_signup(self):
        if self.show_signup:
            self.show_signup()
            self.close()

    # -------- LOGIN LOGIC --------
    def login(self):
        username = self.username_input.text()
        password = self.password_input.text()

        if not username or not password:
            QMessageBox.warning(self, "Error", "All fields required")
            return

        url = "https://equipmentanalyzer.onrender.com/api/token/"

        try:
            response = requests.post(
                url,
                json={"username": username, "password": password}
            )

            if response.status_code == 200:
                data = response.json()
                self.access_token = data["access"]
                self.refresh_token = data["refresh"]

                self.dashboard = Dashboard(self.access_token, self.refresh_token)
                self.dashboard.show()
                self.close()

            else:
                QMessageBox.warning(self, "Login Failed", "Invalid credentials")

        except requests.exceptions.RequestException as e:
            QMessageBox.critical(self, "Error", str(e))

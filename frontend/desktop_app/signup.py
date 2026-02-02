import requests
from PyQt5.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QMessageBox
)
from PyQt5.QtCore import Qt


class SignupWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Signup")
        self.setFixedSize(360, 300)

        # navigation hook (set from main.py)
        self.show_login = None

        layout = QVBoxLayout()
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(12)

        # -------- TITLE --------
        title = QLabel("Create Account")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("""
            QLabel {
                font-size: 20px;
                font-weight: bold;
            }
        """)
        layout.addWidget(title)

        subtitle = QLabel("Sign up to get started")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet("color: gray;")
        layout.addWidget(subtitle)

        # -------- INPUTS --------
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")
        self.username_input.setStyleSheet("padding: 6px;")
        layout.addWidget(self.username_input)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setStyleSheet("padding: 6px;")
        layout.addWidget(self.password_input)

        # -------- SIGNUP BUTTON --------
        self.signup_btn = QPushButton("Sign Up")
        self.signup_btn.setCursor(Qt.PointingHandCursor)
        self.signup_btn.setStyleSheet("""
            QPushButton {
                padding: 8px;
                font-size: 13px;
                font-weight: bold;
            }
        """)
        self.signup_btn.clicked.connect(self.signup)
        layout.addWidget(self.signup_btn)

        # -------- BACK TO LOGIN --------
        back_btn = QPushButton("Back to Login")
        back_btn.setCursor(Qt.PointingHandCursor)
        back_btn.setFlat(True)
        back_btn.setStyleSheet("""
            QPushButton {
                color: #1a73e8;
                text-decoration: underline;
            }
            QPushButton:hover {
                color: #0c59cf;
            }
        """)
        back_btn.clicked.connect(self.go_to_login)
        layout.addWidget(back_btn)

        layout.addStretch()
        self.setLayout(layout)

    # -------- NAVIGATION --------
    def go_to_login(self):
        if self.show_login:
            self.show_login()
        self.close()

    # -------- SIGNUP LOGIC --------
    def signup(self):
        username = self.username_input.text()
        password = self.password_input.text()

        if not username or not password:
            QMessageBox.warning(self, "Error", "All fields required")
            return

        url = "https://equipmentanalyzer.onrender.com/api/signup/"

        try:
            response = requests.post(
                url,
                json={"username": username, "password": password}
            )

            if response.status_code == 201:
                QMessageBox.information(
                    self, "Success", "Account created successfully!"
                )
                # go back to login after signup
                self.go_to_login()
            else:
                QMessageBox.warning(
                    self, "Error",
                    response.json().get("error", "Signup failed")
                )

        except requests.exceptions.RequestException as e:
            QMessageBox.critical(self, "Error", str(e))

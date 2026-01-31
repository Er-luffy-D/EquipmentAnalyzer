import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from signup import SignupWindow
from login import LoginWindow


def main():
    # Enable High DPI scaling (IMPORTANT for Windows)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

    app = QApplication(sys.argv)

    # Application metadata
    app.setApplicationName("Chemical Equipment Visualizer")
    app.setOrganizationName("Simplifai")  # optional
    app.setOrganizationDomain("simplifai.local")  # optional

    # Optional: global light stylesheet (safe & clean)
    app.setStyleSheet("""
        QWidget {
            font-family: Segoe UI;
            font-size: 12px;
        }
        QPushButton {
            padding: 6px 12px;
        }
        QLineEdit {
            padding: 6px;
        }
    """)

    signup_window = SignupWindow()
    login_window = LoginWindow()

    login_window.show_signup = signup_window.show
    signup_window.show_login = login_window.show
    login_window.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()

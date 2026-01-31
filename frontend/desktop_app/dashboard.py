import requests
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import os, webbrowser

from PyQt5.QtWidgets import (
    QWidget, QPushButton, QVBoxLayout, QHBoxLayout,
    QFileDialog, QMessageBox, QTableWidget,
    QTableWidgetItem, QLabel, QSplitter
)
from PyQt5.QtCore import Qt


class ChartCanvas(FigureCanvas):
    def __init__(self, parent=None):
        self.fig = Figure(figsize=(5, 4))
        self.ax = self.fig.add_subplot(111)
        super().__init__(self.fig)
        self.setParent(parent)

    def plot_distribution(self, distribution):
        self.ax.clear()

        labels = list(distribution.keys())
        values = list(distribution.values())

        self.ax.bar(labels, values, color="#4C72B0")
        self.ax.set_title("Equipment Type Distribution", fontsize=12)
        self.ax.set_ylabel("Count")
        self.ax.grid(axis="y", linestyle="--", alpha=0.6)

        self.fig.tight_layout()
        self.draw()


class Dashboard(QWidget):
    def __init__(self, access_token, refresh_token):
        super().__init__()
        self.access_token = access_token
        self.refresh_token = refresh_token

        self.setWindowTitle("Chemical Equipment Dashboard")
        self.resize(1600, 500)

        main_layout = QVBoxLayout()
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(12, 12, 12, 12)

        # ---------- HEADER ----------
        header = QLabel("Chemical Equipment Parameter Visualizer")
        header.setAlignment(Qt.AlignLeft)
        header.setStyleSheet("""
            QLabel {
                font-size: 20px;
                font-weight: bold;
                padding: 6px 0;
            }
        """)
        main_layout.addWidget(header)

        # ---------- TOOLBAR ----------
        toolbar = QHBoxLayout()
        toolbar.setSpacing(10)

        self.upload_btn = QPushButton("Upload CSV")
        self.summary_btn = QPushButton("Fetch Summary")
        self.pdf_btn = QPushButton("Download PDF")

        for btn in (self.upload_btn, self.summary_btn, self.pdf_btn):
            btn.setCursor(Qt.PointingHandCursor)
            btn.setStyleSheet("""
                QPushButton {
                    padding: 6px 14px;
                    font-size: 13px;
                }
            """)

        self.upload_btn.clicked.connect(self.upload_csv)
        self.summary_btn.clicked.connect(self.fetch_summary)
        self.pdf_btn.clicked.connect(self.download_pdf)

        toolbar.addWidget(self.upload_btn)
        toolbar.addWidget(self.summary_btn)
        toolbar.addWidget(self.pdf_btn)
        toolbar.addStretch()

        main_layout.addLayout(toolbar)

        # ---------- SPLITTER (TABLE | CHART) ----------
        splitter = QSplitter(Qt.Horizontal)

        # Table
        self.table = QTableWidget()
        self.table.setStyleSheet("""
            QTableWidget {
                gridline-color: #ddd;
                font-size: 12px;
            }
            QHeaderView::section {
                background-color: #f2f2f2;
                font-weight: bold;
                padding: 4px;
            }
        """)
        self.table.cellClicked.connect(self.update_chart_from_table)
        splitter.addWidget(self.table)

        # Chart
        self.chart = ChartCanvas(self)
        splitter.addWidget(self.chart)

        splitter.setStretchFactor(0, 3)
        splitter.setStretchFactor(1, 2)

        main_layout.addWidget(splitter)

        self.setLayout(main_layout)

    # ---------- AUTH ----------
    def refresh_access_token(self):
        url = "http://127.0.0.1:8000/api/token/refresh/"
        response = requests.post(url, json={"refresh": self.refresh_token})
        if response.status_code == 200:
            self.access_token = response.json()["access"]
            return True
        return False

    # ---------- DATA ----------
    def fetch_summary(self):
        url = "http://127.0.0.1:8000/api/summary/"
        headers = {"Authorization": f"Bearer {self.access_token}"}

        response = requests.get(url, headers=headers)
        if response.status_code == 401 and self.refresh_access_token():
            return self.fetch_summary()

        if response.status_code == 200:
            data = response.json()
            self.populate_table(data)
            if data:
                self.chart.plot_distribution(data[-1]["type_distribution"])
        else:
            QMessageBox.warning(self, "Error", response.text)

    def populate_table(self, data):
        headers = [
            "ID", "File", "Total",
            "Avg Flowrate", "Avg Pressure", "Avg Temp"
        ]

        self.table.setColumnCount(len(headers))
        self.table.setHorizontalHeaderLabels(headers)
        self.table.setRowCount(len(data))

        for row, item in enumerate(data):
            self.table.setItem(row, 0, QTableWidgetItem(str(item["id"])))
            self.table.setItem(row, 1, QTableWidgetItem(item["file"]))
            self.table.setItem(row, 2, QTableWidgetItem(str(item["total_count"])))
            self.table.setItem(row, 3, QTableWidgetItem(f'{item["avg_flowrate"]:.2f}'))
            self.table.setItem(row, 4, QTableWidgetItem(f'{item["avg_pressure"]:.2f}'))
            self.table.setItem(row, 5, QTableWidgetItem(f'{item["avg_temperature"]:.2f}'))

        self.table.resizeColumnsToContents()

    def update_chart_from_table(self, row, column):
        url = "http://127.0.0.1:8000/api/summary/"
        headers = {"Authorization": f"Bearer {self.access_token}"}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            self.chart.plot_distribution(response.json()[row]["type_distribution"])

    # ---------- ACTIONS ----------
    def upload_csv(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select CSV", "", "CSV Files (*.csv)")
        if not file_path:
            return

        url = "http://127.0.0.1:8000/api/upload/"
        headers = {"Authorization": f"Bearer {self.access_token}"}
        with open(file_path, "rb") as f:
            response = requests.post(url, headers=headers, files={"file": f})

        QMessageBox.information(self, "Upload", "CSV uploaded" if response.ok else response.text)

    def download_pdf(self):
        row = self.table.currentRow()
        if row == -1:
            QMessageBox.warning(self, "Error", "Select a dataset first")
            return

        dataset_id = self.table.item(row, 0).text()
        url = f"http://127.0.0.1:8000/api/report/{dataset_id}/"
        headers = {"Authorization": f"Bearer {self.access_token}"}

        response = requests.get(url, headers=headers)
        if response.ok:
            path = f"report_{dataset_id}.pdf"
            with open(path, "wb") as f:
                f.write(response.content)
            webbrowser.open(os.path.abspath(path))

import sys
import requests
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget, QLineEdit, QHBoxLayout, QListWidget
)
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import QTimer, Qt
import webbrowser

class SpotMeWorkerApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("python spotme.py")
        self.setGeometry(100, 100, 800, 600)

        # Styling for the application
        self.setStyleSheet("""
            QWidget {
                background-color: #2E2E2E;
                color: #E0E0E0;
            }
            QLabel {
                color: #E0E0E0;
            }
            QPushButton {
                background-color: #444;
                border: 1px solid #555;
                color: #E0E0E0;
                padding: 10px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #555;
            }
            QPushButton#refresh_button {
                background-color: #FFA500;
                border: 1px solid #FF8C00;
                color: #fff;
            }
            QPushButton#refresh_button:hover {
                background-color: #FF8C00;
            }
            QLineEdit {
                background-color: #333;
                color: #E0E0E0;
                border: 1px solid #555;
                padding: 5px;
                border-radius: 5px;
            }
            QListWidget {
                background-color: #333;
                color: #E0E0E0;
                border: 1px solid #555;
            }
            QLabel.link {
                color: #FFA500;
                text-decoration: none;
            }
            QLabel.link:hover {
                color: #FF8C00;
            }
        """)

        # Main container setup
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        # Date and Time Display
        self.date_time_label = QLabel(self)
        self.layout.addWidget(self.date_time_label)
        self.update_date_time()

        # Title
        self.title_label = QLabel("<h1>python spotme.py</h1>", self)
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.title_label)

        # Worker Image
        self.worker_image = QLabel(self)
        self.worker_image.setPixmap(QPixmap("worker.svg").scaled(100, 100, Qt.AspectRatioMode.KeepAspectRatio))
        self.worker_image.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.worker_image)

        # Show IP Button
        self.toggle_ip_button = QPushButton("show my ip", self)
        self.toggle_ip_button.clicked.connect(self.fetch_user_ip)
        self.layout.addWidget(self.toggle_ip_button)

        # User IP Label
        self.user_ip_label = QLabel("(-(-_(-_-)_-)-)", self)
        self.user_ip_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.user_ip_label)

        # IP Input and Convert Button
        self.ip_input = QLineEdit(self)
        self.ip_input.setPlaceholderText("Enter an ipv4 or ipv6 to geo locate")
        self.convert_button = QPushButton("convert ip address", self)
        self.convert_button.clicked.connect(self.convert_ip_to_lat_long)
        self.layout.addWidget(self.ip_input)
        self.layout.addWidget(self.convert_button)

        # Lat/Long Label
        self.lat_long_label = QLabel("", self)
        self.layout.addWidget(self.lat_long_label)

        # Additional Info Label
        self.additional_info_label = QLabel(
            'The&nbsp;<a href="https://spotme.jessejesse.workers.dev">SpotmeWorker</a>&nbsp;captures the ip, device info, and timestamp from every visitor. A status 200 /ok is operational',
            self
        )
        self.additional_info_label.setOpenExternalLinks(True)
        self.layout.addWidget(self.additional_info_label)

        # IP List
        self.ip_list = QListWidget(self)
        self.layout.addWidget(self.ip_list)

        # Placeholder Label
        self.placeholder_label = QLabel("additional worker URLs", self)
        self.placeholder_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.placeholder_label.setStyleSheet("color: #888;")  # Light gray color for placeholder text
        self.layout.addWidget(self.placeholder_label)

        # Refresh and Share Buttons
        self.button_layout = QHBoxLayout()
        self.refresh_button = QPushButton("call worker", self)
        self.refresh_button.setObjectName("refresh_button")
        self.refresh_button.clicked.connect(self.fetch_ips)
        self.button_layout.addWidget(self.refresh_button)
        self.share_button_one = QPushButton("bit.ly", self)
        self.share_button_one.clicked.connect(self.open_link_one)
        self.button_layout.addWidget(self.share_button_one)
        self.share_button_two = QPushButton("tinyURL", self)
        self.share_button_two.clicked.connect(self.open_link_two)
        self.button_layout.addWidget(self.share_button_two)
        self.layout.addLayout(self.button_layout)

        # Link to SpotMe Website
        self.link_label = QLabel('<a href="https://spotme.jessejesse.com" style="color: #FFA500; text-decoration: none;">spotme website</a>', self)
        self.link_label.setOpenExternalLinks(True)
        self.layout.addWidget(self.link_label)
        self.link_label.setAlignment(Qt.AlignmentFlag.AlignRight)

        # Timer for Date/Time
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_date_time)
        self.timer.start(1000)

    def update_date_time(self):
        from datetime import datetime
        now = datetime.now()
        self.date_time_label.setText(now.strftime("%Y-%m-%d %H:%M:%S"))

    def fetch_user_ip(self):
        try:
            response = requests.get("https://api.ipify.org?format=json")
            response.raise_for_status()
            ip_data = response.json()
            self.user_ip_label.setText(f"IP: {ip_data['ip']}")
        except requests.RequestException as e:
            self.user_ip_label.setText("Error fetching IP")

    def convert_ip_to_lat_long(self):
        ip = self.ip_input.text()
        if not ip:
            self.lat_long_label.setText("did you try calling the worker?")
            return

        try:
            response = requests.get(f"https://ipinfo.io/{ip}/json?token=aa9635b0522f54")
            response.raise_for_status()
            data = response.json()
            loc = data.get("loc", "")
            if loc:
                latitude, longitude = loc.split(",")
                self.lat_long_label.setText(f"Latitude: {latitude}, Longitude: {longitude}")
                additional_info = (
                    f"City: {data.get('city', '')}<br>"
                    f"Region: {data.get('region', '')}<br>"
                    f"Country: {data.get('country', '')}<br>"
                    f"Timezone: {data.get('timezone', '')}"
                )
                self.additional_info_label.setText(additional_info)
            else:
                self.lat_long_label.setText("Location not found.")
                self.additional_info_label.clear()
        except requests.RequestException as e:
            self.lat_long_label.setText("Failed to fetch data.")
            self.additional_info_label.clear()

    def fetch_ips(self):
        try:
            response = requests.get(
                "https://definite-shrimp-39601.upstash.io/scan/0?match=ip:*",
                headers={
                    "Authorization": "Bearer AZqxAAIjcDExYTk3YTM0MTE2MWY0ODhjODhhNWIyNTVkNGE2MTU4OXAxMA"
                },
            )
            response.raise_for_status()
            data = response.json()
            keys = data.get("result", [])[1]
            self.ip_list.clear()
            if not keys:
                self.placeholder_label.setVisible(True)
            else:
                self.placeholder_label.setVisible(False)
                for key in keys:
                    ip_response = requests.get(
                        f"https://definite-shrimp-39601.upstash.io/get/{key}",
                        headers={
                            "Authorization": "Bearer AZqxAAIjcDExYTk3YTM0MTE2MWY0ODhjODhhNWIyNTVkNGE2MTU4OXAxMA"
                        },
                    )
                    ip_response.raise_for_status()
                    ip_data = ip_response.json()
                    self.ip_list.addItem(str(ip_data.get("result", "")))
        except requests.RequestException as e:
            self.ip_list.clear()
            self.ip_list.addItem("Failed to fetch IP addresses")
            self.placeholder_label.setVisible(True)

    def open_link_one(self):
        webbrowser.open("https://bit.ly/cfworker")

    def open_link_two(self):
        webbrowser.open("https://tinyurl.com/spotmewrkr")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_win = SpotMeWorkerApp()
    main_win.show()
    sys.exit(app.exec())



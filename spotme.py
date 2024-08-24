import sys
import requests
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget, QHBoxLayout, QLineEdit, QListWidget
)
from PyQt6.QtGui import QPixmap, QImage, QPainter
from PyQt6.QtSvg import QSvgRenderer
from PyQt6.QtCore import QTimer, Qt, QByteArray
import webbrowser
from datetime import datetime

class SpotMeWorkerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("python spotme.py")
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet(self.style_sheet())
        self.init_ui()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_date_time)
        self.timer.start(1000)
        self.update_date_time()

    def style_sheet(self):
        return """
            QWidget { background-color: #2E2E2E; color: #E0E0E0; }
            QLabel { color: #E0E0E0; }
            QPushButton { background-color: #444; border: 1px solid #555; color: #E0E0E0; padding: 10px; border-radius: 5px; }
            QPushButton:hover { background-color: #555; }
            QPushButton#refresh_button { background-color: #FFA500; border: 1px solid #FF8C00; color: #fff; }
            QPushButton#refresh_button:hover { background-color: #FF8C00; }
            QLineEdit { background-color: #333; color: #E0E0E0; border: 1px solid #555; padding: 5px; border-radius: 5px; }
            QListWidget { background-color: #333; color: #E0E0E0; border: 1px solid #555; }
            QLabel.link { color: #FFA500; text-decoration: none; }
            QLabel.link:hover { color: #FF8C00; }
        """

    def init_ui(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        layout = QVBoxLayout(self.central_widget)
        
        self.date_time_label = QLabel(self)
        layout.addWidget(self.date_time_label)
        title_label = QLabel("<h1>spotme.py</h1>", self)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)

        self.icons_layout = QHBoxLayout()
        icon_urls = [
            "https://api.iconify.design/logos:python.svg?color=%23ff2600",
            "https://api.iconify.design/devicon:redis-wordmark.svg?color=%23ff2600",
            "https://api.iconify.design/logos:upstash-icon.svg?color=%23ff2600",
            "https://api.iconify.design/logos:cloudflare-workers-icon.svg?color=%23ff2600",
            "https://api.iconify.design/logos:google-cloud.svg?color=%23ff2600",
            "https://api.iconify.design/arcticons:openai-chatgpt.svg?color=%23ff2600"
        ]
        for url in icon_urls:
            self.add_icon(self.icons_layout, url)

        icons_container = QWidget(self)
        icons_container.setLayout(self.icons_layout)
        layout.addWidget(icons_container)

        self.toggle_ip_button = QPushButton("show my ip", self)
        self.toggle_ip_button.clicked.connect(self.fetch_user_ip)
        layout.addWidget(self.toggle_ip_button)

        self.user_ip_label = QLabel("(-(-_(-_-)_-)-)", self)
        self.user_ip_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.user_ip_label)

        self.ip_input = QLineEdit(self)
        self.ip_input.setPlaceholderText("Enter an ipv4 or ipv6 to geo locate")
        self.convert_button = QPushButton("convert ip address", self)
        self.convert_button.clicked.connect(self.convert_ip_to_lat_long)
        layout.addWidget(self.ip_input)
        layout.addWidget(self.convert_button)

        self.lat_long_label = QLabel("", self)
        layout.addWidget(self.lat_long_label)

        self.additional_info_label = QLabel(
            'The&nbsp;<a href="https://spotme.jessejesse.workers.dev">SpotmeWorker</a>&nbsp;captures the ip, device info, and timestamp from every visitor.',
            self
        )
        self.additional_info_label.setOpenExternalLinks(True)
        layout.addWidget(self.additional_info_label)

        self.ip_list = QListWidget(self)
        layout.addWidget(self.ip_list)

        self.placeholder_label = QLabel("additional worker URLs", self)
        self.placeholder_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.placeholder_label.setStyleSheet("color: #888;")
        layout.addWidget(self.placeholder_label)

        button_layout = QHBoxLayout()
        self.refresh_button = QPushButton("call worker", self)
        self.refresh_button.setObjectName("refresh_button")
        self.refresh_button.clicked.connect(self.fetch_ips)
        button_layout.addWidget(self.refresh_button)
        share_button_one = QPushButton("bit.ly", self)
        share_button_one.clicked.connect(self.open_link_one)
        button_layout.addWidget(share_button_one)
        share_button_two = QPushButton("tinyURL", self)
        share_button_two.clicked.connect(self.open_link_two)
        button_layout.addWidget(share_button_two)
        layout.addLayout(button_layout)

        link_label = QLabel('<a href="https://spotme.jessejesse.com" style="color: #FFA500; text-decoration: none;">spotme website</a>', self)
        link_label.setOpenExternalLinks(True)
        layout.addWidget(link_label)
        link_label.setAlignment(Qt.AlignmentFlag.AlignRight)

    def update_date_time(self):
        now = datetime.now()
        self.date_time_label.setText(now.strftime("%Y-%m-%d %H:%M:%S"))

    def fetch_user_ip(self):
        try:
            response = requests.get("https://api.ipify.org?format=json")
            response.raise_for_status()
            ip_data = response.json()
            self.user_ip_label.setText(f"IP: {ip_data['ip']}")
        except requests.RequestException:
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
        except requests.RequestException:
            self.lat_long_label.setText("Failed to fetch data.")
            self.additional_info_label.clear()

    def fetch_ips(self):
        try:
            response = requests.get(
                "https://definite-shrimp-39601.upstash.io/scan/0?match=ip:*",
                headers={"Authorization": "Bearer AZqxAAIjcDExYTk3YTM0MTE2MWY0ODhjODhhNWIyNTVkNGE2MTU4OXAxMA"}
            )
            response.raise_for_status()
            data = response.json()
            keys = data.get("result", [])[1]
            self.ip_list.clear()
            self.placeholder_label.setVisible(not keys)
            if keys:
                for key in keys:
                    ip_response = requests.get(
                        f"https://definite-shrimp-39601.upstash.io/get/{key}",
                        headers={"Authorization": "Bearer AZqxAAIjcDExYTk3YTM0MTE2MWY0ODhjODhhNWIyNTVkNGE2MTU4OXAxMA"}
                    )
                    ip_response.raise_for_status()
                    ip_data = ip_response.json()
                    self.ip_list.addItem(str(ip_data.get("result", "")))
        except requests.RequestException as e:
            self.ip_list.clear()
            self.ip_list.addItem(f"Failed to fetch IPs: {e}")

    def open_link_one(self):
        webbrowser.open("https://bit.ly/3pZlJxJ")

    def open_link_two(self):
        webbrowser.open("https://tinyurl.com/4a69abm6")

    def add_icon(self, layout, url):
        try:
            response = requests.get(url)
            response.raise_for_status()
            svg_data = response.content
            renderer = QSvgRenderer(QByteArray(svg_data))
            pixmap = QPixmap(64, 64)
            pixmap.fill(Qt.GlobalColor.transparent)
            painter = QPainter(pixmap)
            renderer.render(painter)
            painter.end()
            label = QLabel()
            label.setPixmap(pixmap)
            layout.addWidget(label)
        except requests.RequestException:
            print(f"Failed to fetch or render icon from {url}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SpotMeWorkerApp()
    window.show()
    sys.exit(app.exec())



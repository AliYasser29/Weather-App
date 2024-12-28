import sys
import requests
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Weather App")
        self.setGeometry(100, 100, 600, 400)  # Enlarged window size

        # Create UI elements
        self.layout = QVBoxLayout()
        self.city_input = QLineEdit(self)
        self.city_input.setPlaceholderText("Enter city name")
        self.city_input.setFont(QFont("Arial", 16))
        self.city_input.setStyleSheet("padding: 10px; border: 2px solid #333; border-radius: 8px;")
        
        self.search_button = QPushButton("Get Weather", self)
        self.search_button.setFont(QFont("Arial", 16))
        self.search_button.setStyleSheet("""
            QPushButton {
                background-color: #007BFF;
                color: white;
                border-radius: 8px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
        """)
        
        self.result_label = QLabel("", self)
        self.result_label.setFont(QFont("Arial", 18))
        self.result_label.setWordWrap(True)
        self.result_label.setAlignment(Qt.AlignCenter)
        self.result_label.setStyleSheet("padding: 20px; color: #333;")

        # Add elements to the layout
        self.layout.addWidget(self.city_input)
        self.layout.addWidget(self.search_button)
        self.layout.addWidget(self.result_label)
        self.setLayout(self.layout)

        # Connect button to the function
        self.search_button.clicked.connect(self.get_weather)

        # Add window style
        self.setStyleSheet("""
            QWidget {
                background-color: #f4f4f9;
            }
        """)

    def get_weather(self):
        city = self.city_input.text().strip()
        if not city:
            self.result_label.setText("Please enter a city name!")
            return

        api_key = "a5cbbe7078d6aae3ac08c6c5837f483f"  # Your API key
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

        try:
            response = requests.get(url)
            data = response.json()

            if response.status_code == 200:
                temp = data["main"]["temp"]
                description = data["weather"][0]["description"]
                emoji = self.get_weather_emoji(description)
                self.result_label.setText(f"Weather in {city}:\n\n{temp}°C - {description} {emoji}")
            else:
                error_message = data.get("message", "Unknown error occurred")
                self.result_label.setText(f"Error: {error_message}")

        except Exception as e:
            self.result_label.setText("An error occurred!")
            print(f"Error: {e}")

    def get_weather_emoji(self, description):
        description = description.lower()
        if "clear" in description:
            return "☀️"
        elif "cloud" in description:
            return "☁️"
        elif "rain" in description or "drizzle" in description:
            return "🌧️"
        elif "thunderstorm" in description:
            return "⛈️"
        elif "snow" in description:
            return "❄️"
        elif "mist" in description or "fog" in description:
            return "🌫️"
        else:
            return "🌈"

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = WeatherApp()
    window.show()
    sys.exit(app.exec_())

from PyQt6.QtWidgets import QMainWindow, QLabel
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
import requests
import os


class MapApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Яндекс.Карты')
        self.setGeometry(100, 100, 650, 450)

        # Центр Москвы (точные координаты)
        self.ll = "37.617635,55.755814"  # Координаты Красной площади
        self.spn = "0.05,0.05"  # Оптимальный масштаб для центра города
        self.size = '650,450'

        # Создаем центральный виджет для точного позиционирования
        self.central_widget = QLabel()
        self.central_widget.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setCentralWidget(self.central_widget)

        self.load_map()

    def load_map(self):
        static_server_address = 'https://static-maps.yandex.ru/1.x/?'
        try:
            url = f'{static_server_address}ll={self.ll}&spn={self.spn}&size={self.size}&l=map'
            response = requests.get(url)
            response.raise_for_status()

            map_file = 'temp_map.png'
            with open(map_file, 'wb') as f:
                f.write(response.content)

            pixmap = QPixmap(map_file)
            self.central_widget.setPixmap(pixmap)
            self.resize(pixmap.width(), pixmap.height())

        except Exception as e:
            print(f'Ошибка при загрузке карты: {e}')

    def closeEvent(self, event):
        if os.path.exists('temp_map.png'):
            os.remove('temp_map.png')
        event.accept()

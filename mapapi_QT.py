from PyQt6.QtWidgets import QMainWindow, QLabel
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
import requests
import os


class MapApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Яндекс.Карты с масштабированием')
        self.setGeometry(100, 100, 650, 450)

        # Параметры карты
        self.ll = "37.617635,55.755814"  # Координаты Красной площади
        self.spn = 0.05  # Начальный масштаб
        self.min_spn = 0.001  # Минимальный масштаб
        self.max_spn = 90.0   # Максимальный масштаб (весь мир)
        self.size = '650,450'

        # Создаем центральный виджет
        self.central_widget = QLabel()
        self.central_widget.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setCentralWidget(self.central_widget)

        self.load_map()

    def load_map(self):
        try:
            url = f'https://static-maps.yandex.ru/1.x/?ll={self.ll}&spn={self.spn},{self.spn}&size={self.size}&l=map'
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

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_PageUp:
            # Увеличение масштаба (приближение)
            self.spn = max(self.spn / 1.5, self.min_spn)
            self.load_map()
        elif event.key() == Qt.Key.Key_PageDown:
            # Уменьшение масштаба (отдаление)
            self.spn = min(self.spn * 1.5, self.max_spn)
            self.load_map()
        else:
            super().keyPressEvent(event)

    def closeEvent(self, event):
        if os.path.exists('temp_map.png'):
            os.remove('temp_map.png')
        event.accept()

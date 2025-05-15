from PyQt6.QtWidgets import QMainWindow, QLabel
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
import requests
import os


class MapApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Яндекс.Карты с масштабированием и перемещением')
        self.setGeometry(100, 100, 650, 450)

        # Параметры карты
        self.lon, self.lat = 37.617635, 55.755814  # Координаты Красной площади
        self.spn = 0.05  # Начальный масштаб
        self.min_spn = 0.001  # Минимальный масштаб
        self.max_spn = 90.0  # Максимальный масштаб
        self.size = '650,450'
        self.move_step = 0.2  # Шаг перемещения (доля от текущего масштаба)

        # Границы допустимых координат
        self.min_lon, self.max_lon = -180, 180
        self.min_lat, self.max_lat = -85, 85

        # Центральный виджет
        self.central_widget = QLabel()
        self.central_widget.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setCentralWidget(self.central_widget)

        self.load_map()

    def update_map_url(self):
        """Обновление URL карты с текущими параметрами"""
        return f'https://static-maps.yandex.ru/1.x/?ll={self.lon},{self.lat}&spn={self.spn},{self.spn}&size={self.size}&l=map'

    def load_map(self):
        """Загрузка и отображение карты"""
        try:
            url = self.update_map_url()
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

    def move_map(self, dx, dy):
        """Перемещение карты с проверкой границ"""
        # Рассчитываем шаг перемещения в градусах
        step_lon = dx * self.spn * self.move_step
        step_lat = dy * self.spn * self.move_step

        # Обновляем координаты с проверкой границ
        self.lon = max(self.min_lon, min(self.lon + step_lon, self.max_lon))
        self.lat = max(self.min_lat, min(self.lat + step_lat, self.max_lat))

        self.load_map()

    def keyPressEvent(self, event):
        """Обработка нажатий клавиш"""
        if event.key() == Qt.Key.Key_PageUp:
            # Увеличение масштаба (приближение)
            self.spn = max(self.spn / 1.5, self.min_spn)
            self.load_map()
        elif event.key() == Qt.Key.Key_PageDown:
            # Уменьшение масштаба (отдаление)
            self.spn = min(self.spn * 1.5, self.max_spn)
            self.load_map()
        elif event.key() == Qt.Key.Key_Up:
            # Перемещение вверх
            self.move_map(0, 1)
        elif event.key() == Qt.Key.Key_Down:
            # Перемещение вниз
            self.move_map(0, -1)
        elif event.key() == Qt.Key.Key_Left:
            # Перемещение влево
            self.move_map(-1, 0)
        elif event.key() == Qt.Key.Key_Right:
            # Перемещение вправо
            self.move_map(1, 0)
        else:
            super().keyPressEvent(event)

    def closeEvent(self, event):
        """Очистка при закрытии"""
        if os.path.exists('temp_map.png'):
            os.remove('temp_map.png')
        event.accept()

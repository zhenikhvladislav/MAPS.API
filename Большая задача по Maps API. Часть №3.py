from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
import requests
import os


class MapApp(QMainWindow):
    def __init__(self):
        super().__init__()

        # Настройка окна
        self.setWindowTitle('Яндекс.Карты с перемещением')
        self.setGeometry(100, 100, 600, 400)

        # Параметры карты (Москва)
        self.lat = 55.751244  # Широта (-90 до 90)
        self.lon = 37.618423  # Долгота (-180 до 180)
        self.size = '600,400'
        self.zoom = 10
        self.min_zoom = 1
        self.max_zoom = 17
        self.step = 0.003  # Шаг перемещения

        # Предельные значения координат
        self.min_lat = -85  # Практические пределы для карт
        self.max_lat = 85
        self.min_lon = -180
        self.max_lon = 180

        # Создаем метку для карты
        self.map_label = QLabel(self)
        self.map_label.resize(600, 400)

        # Загружаем карту
        self.load_map()

    def load_map(self):
        try:
            # Проверяем предельные значения координат
            self.lat = max(self.min_lat, min(self.max_lat, self.lat))
            self.lon = max(self.min_lon, min(self.max_lon, self.lon))

            # Формируем запрос
            url = f'https://static-maps.yandex.ru/1.x/?ll={self.lon},{self.lat}&z={self.zoom}&size={self.size}&l=map'

            # Загружаем картинку
            response = requests.get(url)
            response.raise_for_status()

            # Сохраняем во временный файл
            with open('temp_map.png', 'wb') as f:
                f.write(response.content)

            # Показываем карту
            self.map_label.setPixmap(QPixmap('temp_map.png'))
            title = f'Карта: {self.lon:.3f}, {self.lat:.3f} (масштаб: {self.zoom})'
            self.setWindowTitle(title)

        except Exception as e:
            print(f'Ошибка при загрузке карты: {e}')

    def keyPressEvent(self, event):
        # Вычисляем динамический шаг в зависимости от масштаба
        dynamic_step = self.step * (18 - self.zoom)

        # Обработка клавиш перемещения с проверкой границ
        if event.key() == Qt.Key.Key_Up:
            self.lat = min(self.lat + dynamic_step, self.max_lat)
            self.load_map()
        elif event.key() == Qt.Key.Key_Down:
            self.lat = max(self.lat - dynamic_step, self.min_lat)
            self.load_map()
        elif event.key() == Qt.Key.Key_Left:
            self.lon = max(self.lon - dynamic_step, self.min_lon)
            self.load_map()
        elif event.key() == Qt.Key.Key_Right:
            self.lon = min(self.lon + dynamic_step, self.max_lon)
            self.load_map()

        # Обработка клавиш масштабирования
        elif event.key() == Qt.Key.Key_PageUp:
            self.zoom = min(self.zoom + 1, self.max_zoom)
            self.load_map()
        elif event.key() == Qt.Key.Key_PageDown:
            self.zoom = max(self.zoom - 1, self.min_zoom)
            self.load_map()
        else:
            super().keyPressEvent(event)

    def closeEvent(self, event):
        if os.path.exists('temp_map.png'):
            os.remove('temp_map.png')
        event.accept()


if __name__ == '__main__':
    app = QApplication([])
    window = MapApp()
    window.show()
    app.exec()

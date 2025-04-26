from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt6.QtGui import QPixmap
import requests
import os


class MapApp(QMainWindow):
    def __init__(self):
        super().__init__()

        # Настройка окна
        self.setWindowTitle('Яндекс.Карты')
        self.setGeometry(100, 100, 600, 400)

        # Параметры карты (Москва)
        self.lat = '55.751244'
        self.lon = '37.618423'
        self.size = '600,400'
        self.zoom = '10'  # Масштаб от 1 (весь мир) до 17 (максимальный)

        # Создаем метку для карты
        self.map_label = QLabel(self)
        self.map_label.resize(600, 400)

        # Загружаем карту
        self.load_map()

    def load_map(self):
        try:
            # Формируем запрос
            url = f'https://static-maps.yandex.ru/1.x/?ll={self.lon},{self.lat}&z={self.zoom}&size={self.size}&l=map'

            # Загружаем картинку
            response = requests.get(url)
            response.raise_for_status()  # Проверяем ошибки

            # Сохраняем во временный файл
            with open('temp_map.png', 'wb') as f:
                f.write(response.content)

            # Показываем карту
            self.map_label.setPixmap(QPixmap('temp_map.png'))

        except Exception as e:
            print(f'Ошибка при загрузке карты: {e}')

    def closeEvent(self, event):
        # Удаляем временный файл при закрытии
        if os.path.exists('temp_map.png'):
            os.remove('temp_map.png')
        event.accept()


if __name__ == '__main__':
    app = QApplication([])
    window = MapApp()
    window.show()
    app.exec()

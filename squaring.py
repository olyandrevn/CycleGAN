from PIL import Image
import os


def make_images_square(directory):
    # Получаем список всех файлов в указанной директории
    for filename in os.listdir(directory):
        if filename.endswith(".jpg"):
            filepath = os.path.join(directory, filename)
            image = Image.open(filepath)
            width, height = image.size

            # Вычисляем размер стороны квадрата
            new_size = max(width, height)

            # Создаем новый квадратный белый фон
            new_image = Image.new("RGB", (new_size, new_size), (255, 255, 255))

            # Вставляем исходное изображение на новый фон
            new_image.paste(image, ((new_size - width) // 2, (new_size - height) // 2))

            # Сохраняем новое изображение в ту же директорию
            new_image.save(filepath)


# Пример использования
make_images_square("khokhloma")
make_images_square("gzhel")

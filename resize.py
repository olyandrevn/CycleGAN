from PIL import Image
import os


def resize_images(directory, target_size=128):
    # Получаем список всех файлов в указанной директории
    for filename in os.listdir(directory):
        if filename.endswith(".jpg"):
            filepath = os.path.join(directory, filename)
            image = Image.open(filepath)

            # Изменяем размер изображения до целевого размера
            resized_image = image.resize((target_size, target_size), Image.Resampling.LANCZOS)

            # Сохраняем новое изображение в ту же директорию, заменяя оригинальное
            resized_image.save(filepath)


# Пример использования
resize_images("khokhloma")
resize_images("gzhel")


from PIL import Image
import os


def resize_images(directory, target_size=128):
    for filename in os.listdir(directory):
        if filename.endswith(".jpg"):
            filepath = os.path.join(directory, filename)
            image = Image.open(filepath)

            resized_image = image.resize((target_size, target_size), Image.Resampling.LANCZOS)

            resized_image.save(filepath)


resize_images("khokhloma")
resize_images("gzhel")


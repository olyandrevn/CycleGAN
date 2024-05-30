from PIL import Image
import os


def make_images_square(directory):
    for filename in os.listdir(directory):
        if filename.endswith(".jpg"):
            filepath = os.path.join(directory, filename)
            image = Image.open(filepath)
            width, height = image.size

            new_size = max(width, height)

            new_image = Image.new("RGB", (new_size, new_size), (255, 255, 255))

            new_image.paste(image, ((new_size - width) // 2, (new_size - height) // 2))

            new_image.save(filepath)


make_images_square("khokhloma")
make_images_square("gzhel")

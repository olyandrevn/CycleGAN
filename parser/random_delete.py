import os
import random


def delete_random_files(directory, number_of_files_to_delete=0):
    all_files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]

    if len(all_files) < number_of_files_to_delete:
        print(f"Недостаточно файлов для удаления. Всего файлов: {len(all_files)}")
        return

    files_to_delete = random.sample(all_files, number_of_files_to_delete)

    for file in files_to_delete:
        os.remove(os.path.join(directory, file))
        print(f"Удалён файл: {file}")


delete_random_files("gzhel", 659)

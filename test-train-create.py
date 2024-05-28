import os
import random
import shutil


def create_result_directory_structure(source_dir1, source_dir2):
    current_dir = os.path.dirname(os.path.abspath(__file__))

    result_dir = os.path.join(current_dir, "result")
    if not os.path.exists(result_dir):
        os.makedirs(result_dir)

    subdirs = ["testA", "trainA", "testB", "trainB"]
    for subdir in subdirs:
        os.makedirs(os.path.join(result_dir, subdir), exist_ok=True)

    def distribute_files(source_dir, target_dir_20, target_dir_80):
        all_files = [f for f in os.listdir(source_dir) if os.path.isfile(os.path.join(source_dir, f))]
        random.shuffle(all_files)

        num_files_20 = int(len(all_files) * 0.20)
        files_20_percent = all_files[:num_files_20]
        files_80_percent = all_files[num_files_20:]

        for file in files_20_percent:
            shutil.copy(os.path.join(source_dir, file), os.path.join(target_dir_20, file))

        for file in files_80_percent:
            shutil.copy(os.path.join(source_dir, file), os.path.join(target_dir_80, file))

    distribute_files(
        source_dir1,
        os.path.join(result_dir, "testA"),
        os.path.join(result_dir, "trainA")
    )

    distribute_files(
        source_dir2,
        os.path.join(result_dir, "testB"),
        os.path.join(result_dir, "trainB")
    )


create_result_directory_structure("gzhel", "khokhloma")

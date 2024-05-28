import os


def delete_last_n_images(folder_path, n):
    files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if
             os.path.isfile(os.path.join(folder_path, f))]

    image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp'}
    image_files = [f for f in files if os.path.splitext(f)[1].lower() in image_extensions]

    sorted_files = sorted(image_files, key=os.path.getmtime)

    files_to_delete = sorted_files[-n:]

    for file in files_to_delete:
        try:
            os.remove(file)
            print(f"Deleted: {file}")
        except Exception as e:
            print(f"Error deleting {file}: {e}")

from download_images import *

url = "https://farfor-gzhel.ru/internetmagazin/922/filter/color_list-is-cobalt/apply/"
folder_path = "gzhel_only"
download_images_from_site(url, folder_path, 274)
print("Page processed")

for page in range(2, 62):
    url_page = f"https://farfor-gzhel.ru/internetmagazin/922/filter/color_list-is-cobalt/apply/?PAGEN_1={page}"
    download_images_from_site(url_page, folder_path, 274)
    print(f"Page {page} processed")

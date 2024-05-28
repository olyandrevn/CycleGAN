from download_images import *
from delete_images import *

folder_path = "khokhloma"

# The first site
url = "https://xoxloma-magazin.ru/products/category/wooden-utensil-for-the-kitchen"
download_images_from_site(url, folder_path, 0)
delete_last_n_images(folder_path, 4)
print("Page processed")

for page in range(2, 4):
    url_page = f"https://xoxloma-magazin.ru/products/category/wooden-utensil-for-the-kitchen?page={page}"
    download_images_from_site(url_page, folder_path, 0)
    delete_last_n_images(folder_path, 3)
    print(f"Page {page} processed")

# The second site
url = "https://hohloms.ru/vse-tovary/posuda"
download_images_from_site(url, folder_path, 0)
print("Page processed")

# The third site
url = "https://goldenhohloma.com/catalog/posuda/?element_count=351"
download_images_from_site(url, folder_path, 0)
print("Page processed")

# The fourth site
url = "https://www.artshop-rus.com/suveniry/russkie-suveniry/khokhloma/posuda-khokhloma"
download_images_from_site(url, folder_path, 0)
print("Page processed")

for page in range(2, 4):
     url_page = f"https://www.artshop-rus.com/suveniry/russkie-suveniry/khokhloma/posuda-khokhloma?PAGEN_1={page}"
     download_images_from_site(url_page, folder_path, 0)
     print(f"Page {page} processed")

# The fifth site
url = "https://luxpodarki.ru/catalog/po-tehnike/hohloma/posuda.html"
download_images_from_site(url, folder_path, 0)
print("Page processed")

url = "https://luxpodarki.ru/catalog/po-tehnike/hohloma/posuda.html?page=2"
download_images_from_site(url, folder_path, 0)
print("Page processed")


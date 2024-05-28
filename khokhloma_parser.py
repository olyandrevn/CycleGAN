from download_images import *
from delete_images import *


def process_site(url, folder, delete_last_n=None, page_range=None, page_param="page"):
    """ Helper function to process downloading and deleting images from a site """
    download_images_from_site(url, folder, 0)
    if delete_last_n:
        delete_last_n_images(folder, delete_last_n)
    print("Page processed")

    if page_range:
        for page in page_range:
            url_page = f"{url}?{page_param}={page}"
            download_images_from_site(url_page, folder, 0)
            if delete_last_n:
                delete_last_n_images(folder, delete_last_n)
            print(f"Page {page} processed")


# Directory to save images
folder_path = "khokhloma1"

# Process the first site
first_site_url = "https://xoxloma-magazin.ru/products/category/wooden-utensil-for-the-kitchen"
process_site(first_site_url, folder_path, delete_last_n=4)

process_site(first_site_url, folder_path, delete_last_n=3, page_range=range(2, 4))

# Process the second site
second_site_url = "https://hohloms.ru/vse-tovary/posuda"
process_site(second_site_url, folder_path)

# Process the third site
third_site_url = "https://goldenhohloma.com/catalog/posuda/?element_count=351"
process_site(third_site_url, folder_path)

# Process the fourth site
fourth_site_url = "https://www.artshop-rus.com/suveniry/russkie-suveniry/khokhloma/posuda-khokhloma"
process_site(fourth_site_url, folder_path)

process_site(fourth_site_url, folder_path, page_range=range(2, 4), page_param="PAGEN_1")

# Process the fifth site
fifth_site_url = "https://luxpodarki.ru/catalog/po-tehnike/hohloma/posuda.html"
process_site(fifth_site_url, folder_path)

process_site(fifth_site_url, folder_path, page_range=[2])

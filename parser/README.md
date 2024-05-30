# Dataset Collection

## 1. Functions for Downloading and Parsing Images

### [download_images.py](https://github.com/olyandrevn/CycleGAN/blob/parser/parser/download_images.py)
- Searches for _img_ tags and downloads images from _src_.
- Starts downloading pictures from a specified number \(n\) if the images before this number are not Gzhel or Khokhloma products.
- Implemented in parallel across 10 streams for fast downloading.

### [delete_images.py](https://github.com/olyandrevn/CycleGAN/blob/parser/parser/delete_images.py)
- Removes unsuitable images from the end of the collection by deleting the last \(n\) pictures.

### [gzhel_parser.py](https://github.com/olyandrevn/CycleGAN/blob/parser/parser/gzhel_parser.py)
- Parses websites for Gzhel images.

### [khokhloma_parser.py](https://github.com/olyandrevn/CycleGAN/blob/parser/parser/khokhloma_parser.py)
- Parses websites for Khokhloma images.

## 2. Manual Deletion of Unsuitable Images
- Some unsuitable images still ended up in the folder and were deleted manually.

## 3. Balancing the Dataset

### [random_delete.py](https://github.com/olyandrevn/CycleGAN/blob/parser/parser/random_delete.py)
- After downloading, there were 800 Khokhloma images and over 1500 Gzhel images.
- Random images from the Gzhel collection were deleted until 800 remained.

## 4. Making Images Square and Resizing

### [squaring.py](https://github.com/olyandrevn/CycleGAN/blob/parser/parser/squaring.py)
- Adds white pixels to make images square.

### [resize.py](https://github.com/olyandrevn/CycleGAN/blob/parser/parser/resize.py)
- Resizes images to 128x128 pixels.

## 5. Splitting the Dataset for Training

### [test-train-create.py](https://github.com/olyandrevn/CycleGAN/blob/parser/parser/test-train-create.py)
- Splits images into 80% for training and 20% for validation.

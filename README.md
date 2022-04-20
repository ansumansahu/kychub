## kycHub

### Track for extraction tasks
----------------------------------------------------------------------------
#### Scroll To Bottom of the Page :
```python
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
driver.execute_script("window.scrollTo(0, 1000);")
```
----------------------------------------------------------------------------

#### Translation Options:
```python
options = webdriver.ChromeOptions()
prefs = {
    "translate_whitelists": {"ar": "en"},
    "translate": {"enabled": "true"}
}
options.add_experimental_option("prefs", prefs)

PATH = "C:\\Users\\Ansh\\Downloads\\Compressed\\chromedriver\\chromedriver.exe"
driver = webdriver.Chrome(options=options, executable_path=PATH)
driver.maximize_window()
```
-----------------------------------------------------------------------------

### Reference code for image extraction from pdfs :

#### STEP 1 - import libraries
```python
import fitz #(pip install PyMUPDF)
import io
from PIL import Image
```

#### STEP 2 - file path you want to extract images from and open the file
```python
file = "/content/pdf_file.pdf"
pdf_file = fitz.open(file)
```

#### STEP 3 - iterate over PDF pages
```python
for page_index in range(len(pdf_file)):    
    #get the page itself
    page = pdf_file[page_index]
    image_list = page.getImageList()
    
    # printing number of images found in this page
    if image_list:
        print(f"[+] Found a total of {len(image_list)} images in page {page_index}")
    else:
        print("[!] No images found on page", page_index)
    
    for image_index, img in enumerate(page.getImageList(), start=1):
        # get the XREF of the image
        xref = img[0]
        
        # extract the image bytes
        base_image = pdf_file.extractImage(xref)
        image_bytes = base_image["image"]
        
        # get the image extension and also display the image
        image_ext = base_image["ext"]
        image_data = image_bytes
        image = Image.open(io.BytesIO(image_data))
        image.show()
```

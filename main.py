from PIL import Image
import pytesseract
import numpy as np
from pytesseract import Output
import cv2

pytesseract.pytesseract.tesseract_cmd = r'C:\Users\kayaa\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'

filename = '1.png'
img = np.array(Image.open(filename))
text = pytesseract.image_to_string(img)
print(text)

results = pytesseract.image_to_data(img, output_type=Output.DICT)
for i in range(0, len(results['text'])):
    x = results['left'][i]
    y = results['top'][i]
    
    w = results['width'][i]
    h = results['height'][i]    
    text = results['text'][i]
    conf = float(results['conf'][i])  # Convert confidence to float
    print(conf)
    if conf > 5:
        text = "".join([c if ord(c) < 128 else "" for c in text]).strip() + " " + str(int(conf))
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(img, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 200), 2)

cv2.imshow(" ", img)
cv2.waitKey(0) 
  
# Closing all open windows 
cv2.destroyAllWindows()

from flask import Flask, render_template, request, jsonify
from PIL import Image
import pytesseract
import numpy as np
from pytesseract import Output
import cv2
import base64
import io

app = Flask(__name__)

pytesseract.pytesseract.tesseract_cmd = r'C:\Users\kayaa\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files or request.files['file'].filename == '':
        return jsonify({'error': 'No file part'})

    try:
        file = request.files['file']
        image_data = file.read()
        img = np.array(Image.open(io.BytesIO(image_data)))

        text = pytesseract.image_to_string(img)

        print("Extracted Text:", text)

        results = pytesseract.image_to_data(img, output_type=Output.DICT)
        for i in range(0, len(results['text'])):
            x = results['left'][i]
            y = results['top'][i]
            w = results['width'][i]
            h = results['height'][i]
            text_i = results['text'][i]
            conf = float(results['conf'][i])

            if conf > 5:
                text_i = "".join([c if ord(c) < 128 else "" for c in text_i]).strip() + " " + str(int(conf))
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.putText(img, text_i, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 200), 2)

        retval, buffer = cv2.imencode('.jpg', img)
        img_base64 = base64.b64encode(buffer).decode('utf-8')

        # Send both text and image_base64 in the response
        return jsonify({'text': text, 'img_base64': img_base64})
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)

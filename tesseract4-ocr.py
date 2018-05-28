import os
from datetime import datetime
from subprocess import Popen, PIPE
from urllib.parse import urlsplit
from urllib.request import urlretrieve

from flask import Flask, request, jsonify

app = Flask(__name__, static_url_path='/static')

BASE_DIR = os.path.dirname(os.path.realpath(__file__))


@app.route('/')
def ocr():
    startTime = datetime.now()

    # IMAGE
    img = request.args.get("img", False)
    if not img:
        dosya = os.path.join(BASE_DIR, 'static/test.jpg')
    else:
        dosya = os.path.join(BASE_DIR, 'static/') + urlsplit(img).path.split("/")[-1]
        indir = urlretrieve(img, dosya)

    # LANGUAGE
    lang = request.args.get("lang", False)
    if not lang:
        lang = "eng"
    else:
        lang = lang

    # OCR CONTENT
    pipe = Popen(["tesseract", dosya, "stdout", "-l", lang, "quiet"], stdout=PIPE)
    ocr_content = pipe.communicate()[0]
    ocr_content = ocr_content.decode("utf-8").replace('\n\n', '\n')

    # JSON Response
    json_response = {
        "status": True,
        "content": ocr_content,
        "length": len(ocr_content),
        "runtime": str(datetime.now() - startTime),
        "lines_count": str(len(ocr_content.split('\n'))),
        "words_count": str(len(ocr_content.split(' '))),
    }

    # result = json.dumps(json_response)
    # return render_template('result.html', result=result)
    return jsonify(json_response)


if __name__ == '__main__':
    app.run(debug=True)

import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.responses import PlainTextResponse, JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.staticfiles import StaticFiles
from starlette.exceptions import HTTPException as StarletteHTTPException
from typing import Optional
from steganogan import SteganoGAN
from datetime import datetime
from pyngrok import ngrok

import base64
import os
import nest_asyncio

#steganogan = SteganoGAN.load(architecture='dense', cuda=False, verbose=True)
steganogan = SteganoGAN.load(architecture='dense', verbose=True)

# Debug
# hiddenMsg = steganogan.decode('output.png')
# print(hiddenMsg)

app = FastAPI(debug=True)
app.mount("/static", StaticFiles(directory="static"), name="static")

class encodedImage(BaseModel):
    img: str
    data: str


class decodedImage(BaseModel):
    img: str

def decode_image(image_string):
    content = image_string.split(';')[1]
    image_encoded = content.split(',')[1]
    imgdata = base64.decodebytes(image_encoded.encode('utf-8'))

    # current date and time
    now = datetime.now()
    # date and time format: dd/mm/YYYY H:M:S
    format = "%d-%m-%Y_%H-%M-%S"
    # format datetime using strftime()
    time1 = now.strftime(format)

    filename = time1 + '.png'
    # filename = str(datetime.now().date()) + '.jpg'
    with open(os.path.join('static/original', filename), 'wb') as f:
        f.write(imgdata)

        return filename

@app.post("/encode/image")
def encodeImage(qImage: encodedImage):
    exampleHash = qImage.data  # "00966efaba812660d426a0f10542dadac919f6465dc0a87eac413f934bc0526a"
    q = qImage.img
    original_img_path = decode_image(q)
    input_image = 'static/original/' + original_img_path
    output_image = 'static/output/' + original_img_path
    steganogan.encode(input_image, output_image, exampleHash)
    return output_image


@app.post("/decode/image")
def decodeImage(qImage: decodedImage):
    q = qImage.img
    original_img_path = decode_image(q)
    input_image = 'static/original/' + original_img_path
    print("Path:", input_image)
    try:
        hiddenMsg = steganogan.decode(input_image)
    except ValueError as err:
        return {"error": "No message detected!"}
    return hiddenMsg

ngrok_tunnel = ngrok.connect(8000)
print('Public URL:', ngrok_tunnel.public_url)
nest_asyncio.apply()
uvicorn.run(app, host="0.0.0.0", port=8000)
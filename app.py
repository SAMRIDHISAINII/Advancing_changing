import cv2
from PIL.Image import Image
from flask import Flask, jsonify, request
from flask_cors import CORS
import base64
import io
import logging

import imageio
import torch

# configuration
from werkzeug.debug import console

from app.unet.Models.lightUnetPlusPlus import lightUnetPlusPlus
from app.unet.flask_main import predict
from app.unet.image import load_images_predict, draw_mask

DEBUG = True

# instantiate the app
app = Flask(__name__)

# enable CORS
cors = CORS(app, resources={r'/*': {'origins': '*'}})


@app.route('/predict', methods=['GET', 'POST'])
def all_predict():
    if request.method == 'POST':
            logging.info('getting images')
            content = request.get_json()
            #print(content)
            before_img = content['before'].split(',')[1]
            bi = base64.b64decode(str(before_img))
            print('before')
            print(before_img)
            print('\n\nafter')
            after_img = content['after'].split(',')[1]
            print(after_img)
            si = base64.b64decode(str(after_img))
            a = use_predict(bi, si)
            return a


def use_predict(before_img, after_img):
    resized_a = imageio.imread(io.BytesIO(before_img))
    resized_b = imageio.imread(io.BytesIO(after_img))

    logging.info('loading images')

    dataset, output_path = load_images_predict(resized_a, resized_b, 1)
    model = lightUnetPlusPlus(n_channels=6, n_classes=2)
    logging.info('starting cpu/cuda')
    device = torch.device('cpu' if not torch.cuda.is_available() else 'cuda')
    model.to(device)
    model.load_state_dict(torch.load('app/unet/Weights/last.pth', map_location=torch.device(device)))
    model.eval()
    logging.info('making prediction')
    res = predict(model=model, threshold=0.09, device=device, dataset=dataset, output_paths=output_path, color="red")
    visualized_res = draw_mask(resized_b, res)
    raw_bytes = io.BytesIO()
    visualized_res.save(raw_bytes, "png")
    raw_bytes.seek(0)
    img_base64 = base64.b64encode(raw_bytes.read())
    js = jsonify(image=str(img_base64))
    return js


if __name__ == '__main__':
    app.run()

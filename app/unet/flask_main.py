import sys
import os
import argparse
import torch
import logging
import time
from tqdm import tqdm
from app.unet.image import *
from app.unet.Models.lightUnetPlusPlus import lightUnetPlusPlus
from flask import Flask, request, jsonify
import io
import numpy as np
from PIL import Image
import cv2
import base64

app = Flask(__name__)


def predict(model,
            threshold,
            device,
            dataset,
            output_paths,
            color):
    with tqdm(desc=f'Prediction', unit=' img') as progress_bar:
        for i, (image, _) in enumerate(dataset):
            image = image[0, ...]

            image = image.to(device)

            with torch.no_grad():
                mask_predicted = model(image)

            placeholder_path(output_paths[i])
            img = save_predicted_mask(mask_predicted, device, color=color,
                                      filename=(output_paths[i] + "/predicted.png"),
                                      threshold=threshold)
            progress_bar.update()
            return img


@app.route('/predict', methods=['POST'])
def work():
    if request.method == 'POST':
        file1 = request.files['before']
        file2 = request.files["after"]
        img_bytes1 = file1.read()
        img_bytes2 = file2.read()
        resized_a = imageio.imread(io.BytesIO(img_bytes1))
        resized_b = imageio.imread(io.BytesIO(img_bytes2))
        dataset, output_path = load_images_predict(resized_a, resized_b, 1)
        model = lightUnetPlusPlus(n_channels=6, n_classes=2)
        device = torch.device('cpu' if not torch.cuda.is_available() else 'cuda')
        model.to(device)
        model.load_state_dict(torch.load('Weights/last.pth', map_location=torch.device(device)))
        model.eval()

        res = predict(model=model,
                      threshold=0.09,
                      device=device,
                      dataset=dataset,
                      output_paths=output_path,
                      color="red")
        # make_mask(resized_a, res)
        raw_bytes = io.BytesIO()
        res.save(raw_bytes, "JPEG")
        raw_bytes.seek(0)
        img_base64 = base64.b64encode(raw_bytes.read())

        return jsonify({"status": str(img_base64)})


if __name__ == '__main__':
    app.run(host="127.0.0.1")

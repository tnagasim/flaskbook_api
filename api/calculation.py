from pathlib import Path

import cv2
import numpy as np
import torch
from flask import current_app, jsonify


from api.postprocess import draw_lines, draw_texts, make_color, make_line
from api.preparation import load_image
from api.preprocess import image_to_tensor


baseedir = Path(__file__).parent.parent


def detection(request):
    dict_results = {}
    labels = current_app.config["LABELS"]
    image, filename = load_image(request)
    image_tensor = image_to_tensor(image)
    try:
        model = torch.load("model.pt", weights_only=False)
    except FileNotFoundError:
        return jsonify("The model is not found"), 404
    model = model.eval()
    output = model([image_tensor])[0]
    result_image = np.array(image.copy())
    for box, label, score in zip(
            output["boxes"], output["labels"], output["scores"]):
        if score > 0.6 and labels[label] not in dict_results:
            color = make_color(labels)
            line = make_line(result_image)
            c1 = int(box[0]), int(box[1])
            c2 = int(box[2]), int(box[3])
            draw_lines(c1, c2, result_image, line, color)
            draw_texts(result_image, line, c1, color, labels[label])
            dict_results[labels[label]] = round(100 * score.item())
    dir_image = str(baseedir / "data" / "output" / filename)
    cv2.imwrite(dir_image, cv2.cvtColor(result_image, cv2.COLOR_RGB2BGR))
    return jsonify(dict_results), 201

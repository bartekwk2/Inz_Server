from keras import models
import numpy as np
from PIL import Image
import io
import json


def gesture_from_image(image:Image,model,labels):
    image1 = np.array(image).astype('float32')
    image2 = np.expand_dims(image1, axis=0)
    probabilities = model.predict_proba(image2)
    pred_indexes = np.argsort(probabilities, axis=1)[:,-3:][0][::-1]

    json_data = []

    for index in pred_indexes:
        json_entry = {}
        json_entry["label"] = labels[index]
        json_entry['confidence'] = float(probabilities[0][index])
        json_entry["index"] = int(index)
        json_data.append(json_entry)

    return json.dumps(json_data)


def prepare_image(bytesImg):
    image = Image.open(bytesImg)
    image = image.resize(((64,64)))
    return image


def prepare_classifier():
    model = models.load_model('gestureClassifier.h5')
    labels = []
    with open('labels.txt') as f:
        labels = f.read().splitlines()
    return model,labels


    
def stuff():
    im = Image.open('W1.jpg')
    buf = io.BytesIO()
    im.save(buf, format='JPEG')
    imageConv = Image.open(buf)


    newImg = Image.open(buf)
    newImg = newImg.resize((64,64))


    gesture_from_image(newImg)
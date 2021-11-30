from keras import models
import numpy as np
from PIL import Image
import io
import json
import cv2


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
    img = cv2.imdecode(np.frombuffer(bytesImg.read(), np.uint8), 1)
    img = cv2.flip(img,1)
    image = cv2.resize(img,(64,64))
    #cv2.imshow("a",image)
    #cv2.waitKey(0)
    return image


def prepare_classifier():
    model = models.load_model('gestureClassifier.h5')
    labels = []
    with open('labels.txt') as f:
        labels = f.read().splitlines()
    return model,labels


def test_stuff():
    imagesDirectoryPath = "C:/Programowanie/Python/Inz/inzynierka/data/zdjecia_proba/"
    imagePath = "L/L1603"
    im = Image.open(imagesDirectoryPath + imagePath + ".jpg")
    buf = io.BytesIO()
    im.save(buf, format='JPEG')

    with open(imagesDirectoryPath + imagePath + ".jpg", "rb") as image:
        f = image.read()
        b = io.BytesIO(bytearray(f))
        img = cv2.imdecode(np.frombuffer(b.read(), np.uint8), 1)
        image = cv2.resize(img,(64,64))
        model,labels = prepare_classifier()
        classified = gesture_from_image(image, model,labels)
        print(classified)

    '''
    newImg = Image.open(buf)
    im.show()
    newImg = newImg.resize((64,64))
    model,labels = prepare_classifier()
    classified = gesture_from_image(im, model,labels)
    print(classified)

def prepare_image2(bytesImg):
    image = Image.open(bytesImg)
    image.show()
    image = image.resize(((64,64)))
    return image

    '''


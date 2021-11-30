from flask import Flask, jsonify, request
import io
from gesture_classification import gesture_from_image,prepare_classifier,prepare_image

application = Flask(__name__)
model,labels = prepare_classifier()


@application.route("/classifyImage",methods=['POST'])
def classify_image():
    try:
        imageBytes = io.BytesIO(request.get_data())
        image = prepare_image(imageBytes)
        jsonData = gesture_from_image(image,model,labels)
        print(jsonify(result = jsonData,statusCode = 200))
        return jsonify(result = jsonData,statusCode = 200), 200
    except Exception as e:
        print(e)
        return jsonify(errorMsg = "Server error",statusCode = 500), 500


if __name__ == "__main__":
    application.run(host='0.0.0.0', port='3000',)

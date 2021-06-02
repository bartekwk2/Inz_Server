from my_keys import MY_AWS_ACCESS_KEY_ID,MY_AWS_SECRET_ACCESS_KEY_ID,MY_REGION_NAME
from flask import Flask, jsonify, request
import boto3
import base64
import six
import imghdr
import io
from gesture_classification import gesture_from_image,prepare_classifier,prepare_image


application = Flask(__name__)

dynamodb = boto3.client('dynamodb',aws_access_key_id = MY_AWS_ACCESS_KEY_ID,region_name=MY_REGION_NAME,
                    aws_secret_access_key = MY_AWS_SECRET_ACCESS_KEY_ID,)

s3 =  boto3.client('s3',aws_access_key_id = MY_AWS_ACCESS_KEY_ID,region_name=MY_REGION_NAME,
                    aws_secret_access_key = MY_AWS_SECRET_ACCESS_KEY_ID,)

cognito = boto3.client('cognito-idp',aws_access_key_id = MY_AWS_ACCESS_KEY_ID,region_name=MY_REGION_NAME,
                    aws_secret_access_key = MY_AWS_SECRET_ACCESS_KEY_ID,)

#proba 


model,labels = prepare_classifier()



@application.route("/classifyImage",methods=['POST'])
def classify_image():
    try:
        imageBytes = io.BytesIO(request.get_data())
        image = prepare_image(imageBytes)
        jsonData = gesture_from_image(image,model,labels)
        return jsonify(result = jsonData,statusCode = 200), 200
    except Exception as e:
        print(e)
        return jsonify(errorMsg = "Server error",statusCode = 500), 500

@application.route('/')
def get_hello():
    return "Helloł World!"
    

@application.route("/uploadRawImage",methods=['POST'])
def upload_raw_image():
    try:
        image = io.BytesIO(request.get_data())
        imageName = request.headers.get("Name")
        imageExtension = request.headers.get("Content-Type").split('/')[1]
        imageUrl = upload_to_storage(image,imageName,imageExtension)
        return jsonify(data = imageUrl), 200
    except Exception :
        return jsonify(errorMsg = "Server error"), 500


@application.route("/uploadEncodedImage",methods=['POST'])
def upload_encoded_image():
    try:
        image = request.form.get('image')
        imageName = request.form.get('name')
        file, file_name, file_extenstion = decode_base64_file(image,imageName)
        imageUrl = upload_to_storage(file,file_name,file_extenstion)
        return jsonify(data = imageUrl), 200
    except Exception :
        return jsonify(errorMsg = "Server error"), 500


def upload_to_storage(file,name,extension):
    bucket_name = 'bartekwk'
    file_name = f"{name}.{extension}"

    s3.upload_fileobj(
        file,
        bucket_name,
        file_name,
        ExtraArgs={'ACL': 'public-read'}
    )
    return f"https://{bucket_name}.s3.amazonaws.com/{file_name}"


def decode_base64_file(data,file_name):

    if isinstance(data, six.string_types):
        if 'data:' in data and ';base64,' in data:
            header, data = data.split(';base64,')
        try:
            decoded_file = base64.b64decode(data)
        except TypeError:
            TypeError('invalid_image')
        file_extension = get_file_extension(file_name, decoded_file)

        return io.BytesIO(decoded_file), file_name,file_extension


def get_file_extension(file_name, decoded_file):
    extension = imghdr.what(file_name, decoded_file)
    extension = "jpg" if extension == "jpeg" else extension
    return extension


@application.route("/add_book",methods=["POST"])
def add_books():
    print(request)
    author = request.form.get("author")
    title = request.form.get("title")
    category = request.form.get("category")
    table = dynamodb.Table("Books") 

    table.put_item(Item={
        "Author": author,
        "Title": title,
        "Category": category
    })
    return "Item is already in!" 

'''

@application.route("/books")
def get_books():
    author = request.args.get("author")
    title = request.args.get("title")

    try:
        table = dynamodb.Table("Books")
        response = table.query(KeyConditionExpression=Key("Author").eq(author))
        results = []
        for item in response["Items"]:
            results.append(item)
            return item

    except Exception as ex:
        print("Error when getting an item")
        print(ex)


@application.route("/add_book")
def add_books():
    author = request.args.get("author")
    title = request.args.get("title")
    category = request.args.get("category")

    table = dynamodb.Table("Books")

    table.put_item(Item={
        "Author": author,
        "Title": title,
        "Category": category
    })
    return "Item is already in!"


@application.route("/v1/bestmusic/90s/<string:artist>")
def get_artist(artist):
    resp = client.get_item(
        TableName=dynamoTableName,
        Key={
            'artist': { 'S': artist }
        }
    )
    item = resp.get('Item')
    if not item:
        return jsonify({'error': 'Artist does not exist'}), 404

    return jsonify({
        'artist': item.get('artist').get('S'),
        'song': item.get('song').get('S')
    })


@application.route("/v1/bestmusic/90s", methods=["POST"])
def create_artist():
    artist = request.json.get('artist')
    song = request.json.get('song')
    if not artist or not song:
        return jsonify({'error': 'Please provide Artist and Song'}), 400

    resp = client.put_item(
        TableName=dynamoTableName,
        Item={
            'artist': {'S': artist },
            'song': {'S': song }
        }
    )

    return jsonify({
        'artist': artist,
        'song': song
    })
'''

if __name__ == "__main__":
    #application.run(host='192.168.0.106', port='3000', debug=True)
    application.run(host="0.0.0.0", port='3000', debug=True)

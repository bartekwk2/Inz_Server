import boto3

dynamodb = boto3.client('dynamodb',aws_access_key_id = "AKIAQNIIDHABNWXF5OIY", region_name="us-east-2",
                    aws_secret_access_key = "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",)

s3 = boto3.client('s3',aws_access_key_id = "AKIAQNIIDHABNWXF5OIY", region_name="us-east-2",
                    aws_secret_access_key = "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",)


def create_table():
    try:
        table = dynamodb.create_table(
            TableName = "Books",
            KeySchema = [{
                "AttributeName": "Author",
                "KeyType": "HASH"
                },
                {
                "AttributeName": "Title",
                "KeyType": "RANGE"
                }],
            AttributeDefinitions = [{
                "AttributeName": "Author",
                "AttributeType": "S"
            },{
                "AttributeName": "Title",
                "AttributeType": "S"
            }],
            ProvisionedThroughput={
            "ReadCapacityUnits": 1,
            "WriteCapacityUnits": 1
        })
        print(f"Stworzono pomyślnie {table}")
    
    except Exception as e:
        print("Wystąpił błąd")
        print(e)


with open("requirements.txt") as f: 
    for line in f: 
        line = line.replace("\n","").split('=')
        lineOut = line[0]+"==" + line[1]
        print(lineOut)

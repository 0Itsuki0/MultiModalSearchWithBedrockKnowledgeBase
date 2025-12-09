import boto3
import requests

BUCKET_NAME = "multimodal-image-db"
BUCKET_REGION = "us-east-1"

def upload_file(file_name: str, data_bytes: bytes):
    s3_client = boto3.client('s3', region_name=BUCKET_REGION)
    try:
        s3_client.put_object(Bucket=BUCKET_NAME, Key=file_name, Body=data_bytes)
    except Exception as e:
        print(e)


def get_image_bytes(url) -> bytes:
    response = requests.get(url, verify=False)
    return response.content


def main():
    url = "https://api.pokemontcg.io/v2/cards?page=2&pageSize=1"
    response = requests.get(url, verify=False)

    if response.status_code == 200:
        json_body = response.json()
        data_list: list[dict] = json_body["data"]

        for data in data_list:
            image_url = data["images"]["small"]
            name = data["name"]

            print(f"getting image for {name}")
            image_bytes = get_image_bytes(image_url)

            print(f"Uploading file for {name}")
            upload_file(f"source/{name}.png", image_bytes)

    else:
        print(f"Error: {response.status_code}")


if __name__ == "__main__":
    main()

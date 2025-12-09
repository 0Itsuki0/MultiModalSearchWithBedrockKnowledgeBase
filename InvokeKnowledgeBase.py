import boto3
import base64

KNOWLEDGE_BASE_ID = "..."
BUCKET_REGION = "us-east-1"

def save_image_from_response(response: dict, image_path: str):
    retrieval_results: list[dict] = response["retrievalResults"]
    if len(retrieval_results) == 0:
        return
    first = retrieval_results[0]
    content = first["content"]
    if content["type"].lower() != "image":
        return
    # data:image/jpeg;base64,${base64-encoded string}
    base64_string = content["byteContent"]
    keyword = "base64,"
    index = base64_string.find(keyword)
    if index != -1:
        base64_string = base64_string[index:].removeprefix(keyword)
    print(base64_string[:20])
    image_data = base64.b64decode(base64_string)
    with open(image_path, "wb") as image_file:
        image_file.write(image_data)

    print(f"image saved to {image_path}")

def main():
    client = boto3.client('bedrock-agent-runtime', region_name=BUCKET_REGION)

    # text
    response = client.retrieve(
        knowledgeBaseId=KNOWLEDGE_BASE_ID,
        retrievalConfiguration={
            'vectorSearchConfiguration': {
                'numberOfResults': 1
            }
        },
        retrievalQuery={
            'text': 'tell me about Raikou',
            'type': 'TEXT'
        }
    )
    print(f"received {len(response["retrievalResults"])} results.")
    save_image_from_response(response=response, image_path="text_output.png")

    # image
    query_image_path = "/Users/itsuki/Desktop/test_raikou.png"
    query_image_bytes = open(query_image_path, "rb").read()
    response = client.retrieve(
        knowledgeBaseId=KNOWLEDGE_BASE_ID,
        retrievalQuery={
            'image': {
                'format': 'png',
                'inlineContent': query_image_bytes
            },
            'type': 'IMAGE'
        }
    )
    print(f"received {len(response["retrievalResults"])} results.")
    save_image_from_response(response=response, image_path="image_output.png")


if __name__ == "__main__":
    main()

import base64
from openai import OpenAI

# Initialize client
#client = OpenAI()
client = OpenAI(api_key="")

# Encode image to base64
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

# Prepare payload
image_path = "./images/image_7_xref38.jpeg"
base64_image = encode_image(image_path)

# API call
response = client.chat.completions.create(
    model="gpt-4o", # Use a vision-capable model
    messages=[
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "Extract the product, brand and price from this image:"},
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}} #
            ],
        }
    ],
    max_tokens=500,
)

print(type(response.choices[0].message.content))
print(response.choices[0].message.content)

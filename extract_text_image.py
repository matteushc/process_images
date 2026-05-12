import ollama
from pydantic import BaseModel
from deep_translator import GoogleTranslator


class ObjectDetection(BaseModel):
    product_name: str
    product_type: str
    prices: list[float]
    brand: str
    description: str
    
    
models_types = ['llama3.2-vision', 'qwen2.5vl:7b']


with open('./image_1_xref20_hsv_removed_extracted_746.png', 'rb') as f:
  response = ollama.chat(
    model=models_types[1],
    format=ObjectDetection.model_json_schema(), # Pass JSON schema
    messages=[{
      'role': 'system',
      'content': "Return the product name, product type, brand, prices and description of the product in the image. Return the response in JSON format according to the provided schema."
      }, 
      {
      'role': 'user',
      'content': """
        Extract the product name, product type, prices, brand and description from this image.
        If you cannot find the prices, return 0. 
        If you cannot find the brand, return "Unknown".""",
      'images': [f.read()]
    }]
  )

analysis = ObjectDetection.model_validate_json(response.message.content)
print(analysis.product_name)
print(analysis.prices)
print(analysis.brand)

product_type = GoogleTranslator(source='en', target='pt').translate(analysis.product_type)
description = GoogleTranslator(source='en', target='pt').translate(analysis.description)
print(product_type)
print(description)

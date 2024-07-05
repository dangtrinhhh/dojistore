from dotenv import load_dotenv
import os
import time
from PIL import Image, ImageDraw
from matplotlib import pyplot as plt

# Import namespaces
from azure.core.credentials import AzureKeyCredential
#  Import Text Anaysis
from azure.ai.textanalytics import TextAnalyticsClient

import base64
from PIL import Image
from io import BytesIO
import re
import requests, uuid, json

def getKeyPhrase(text):
    try:   
        result = []
        load_dotenv()
        
        # Azure Text Analysis (Language Services)
        ai_endpoint_text_analysis = os.getenv('AI_SERVICE_ENDPOINT_TEXT_ANALYSIS')
        ai_key_text_analysis = os.getenv('AI_SERVICE_KEY_TEXT_ANALYSIS')

        # Create client using endpoint and key
        credential_text = AzureKeyCredential(ai_key_text_analysis)
        ai_client = TextAnalyticsClient(endpoint=ai_endpoint_text_analysis, credential=credential_text)

        # text = 'Tôi muốn mua vợt cầu lông rẻ, dành cho người mới.'

        # Add your key and endpoint
        key = "07b2db767e9948c3885f87f0dcaaa6e3"
        endpoint = "https://api.cognitive.microsofttranslator.com"

        # location, also known as region.
        # required if you're using a multi-service or regional (not global) resource. It can be found in the Azure portal on the Keys and Endpoint page.
        location = "eastus"

        path = '/translate'
        constructed_url = endpoint + path

        params = {
            'api-version': '3.0',
            'from': 'vi',
            'to': ['en']
        }

        paramsRevert = {
            'api-version': '3.0',
            'from': 'en',
            'to': ['vi']
        }

        headers = {
            'Ocp-Apim-Subscription-Key': key,
            # location required if you're using a multi-service or regional (not global) resource.
            'Ocp-Apim-Subscription-Region': location,
            'Content-type': 'application/json',
            'X-ClientTraceId': str(uuid.uuid4())
        }

        # You can pass more than one object in body.
        body = [{
            'text': text
        }]

        request = requests.post(constructed_url, params=params, headers=headers, json=body)
        response = request.json()
        textEn = response[0]['translations'][0]['text']

        print(json.dumps(response, sort_keys=True, ensure_ascii=False, indent=4, separators=(',', ': ')))

        phrases = ai_client.extract_key_phrases(documents=[textEn])[0].key_phrases
        if len(phrases) > 0:
            print("\nKey Phrases:")
            for phrase in phrases:
                request = requests.post(constructed_url, params=paramsRevert, headers=headers, json=[{'text': phrase}])
                response = request.json()
                textVi = response[0]['translations'][0]['text']
                result.append(textVi)
                print('\t{}'.format(textVi))
        return result
    
    except Exception as ex:
        print(ex)

if __name__ == "__main__":
    getKeyPhrase('Tôi muốn mua vợt cầu lông rẻ, dành cho người mới.')

from dotenv import load_dotenv
import os
import time
from PIL import Image, ImageDraw
from matplotlib import pyplot as plt

# Import namespaces
from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.ai.vision.imageanalysis.models import VisualFeatures
from azure.core.credentials import AzureKeyCredential
#  Import Text Anaysis
from azure.ai.textanalytics import TextAnalyticsClient

import base64
from PIL import Image
from io import BytesIO
import re


def main(file):
    
    personal_information = {
        'identity_card_no': '',
        'full_name': '',
        'date_of_birth': '',
        'sex': '',
        'nationality': '',
        'place_of_origin': '',
        'place_of_resident': '',
        'date_expiry': ''
    }

    global cv_client

    try:   
        # Azure AI Vision
        load_dotenv()
        endpoint = os.environ["VISION_ENDPOINT"]
        key = os.environ["VISION_KEY"]
        
        cv_client = ImageAnalysisClient(
            endpoint=endpoint,
            credential=AzureKeyCredential(key)
        )
        
        # Azure Text Analysis (Language Services)
        ai_endpoint_text_analysis = os.getenv('AI_SERVICE_ENDPOINT_TEXT_ANALYSIS')
        ai_key_text_analysis = os.getenv('AI_SERVICE_KEY_TEXT_ANALYSIS')

        # Create client using endpoint and key
        credential_text = AzureKeyCredential(ai_key_text_analysis)
        ai_client = TextAnalyticsClient(endpoint=ai_endpoint_text_analysis, credential=credential_text)

        # image_file = os.path.join('images','cccd_clear.jpg')
        # image_file = os.path.join('images','cccd_notclear.jpg')
        
        image_data = base64.b64decode(file)
        filename = 'D:\Github\dojistore\order\some_image.jpg'
        with open(filename, 'wb') as f:
            f.write(image_data)
        
        text = GetTextRead(filename, personal_information)
        print(text)
        getEntities(text, ai_client, personal_information)    
        
        is_empty = False
        #  Check if there are any empty values
        for key, value in personal_information.items():
            if value == '':
                is_empty = True
                break
        
        print(f'\nFinal result\n')
        if is_empty:
            return('The photo is blurry, please try again')
            
        else:
            return personal_information
                

    except Exception as ex:
        print(ex)


def GetTextRead(image_file, personal_information):
    try:
        # Open image file
        with open(image_file, "rb") as f:
                image_data = f.read()

        # Use Analyze image function to read text in image
        result = cv_client.analyze(
            image_data=image_data,
            visual_features=[VisualFeatures.READ]
        )
        # image_data = base64.b64decode(image_file.split(",")[1])
        
        # result = cv_client.analyze(
        #     image_data=image_data,
        #     visual_features=[VisualFeatures.READ]
        # )

        if result.read is not None:
            texts = [obj["text"] for obj in result.read.blocks[0].lines]
            print(texts)
            for i in range(len(texts)):
                if 'Nationality' in texts[i] or 'Sex' in texts[i]:
                    sex_nationality = texts[i].split(": ")
                    if len(sex_nationality) == 2:
                        personal_information['nationality'] = texts[i + 1] if i + 1 < len(texts) else ""
                    elif len(sex_nationality) == 3:
                        personal_information['nationality'] = texts[i].split(": ")[2].strip() if len(texts[i].split(": ")) >= 3 else ""
                    
                    if 'Nữ' in texts[i]:
                        personal_information['sex'] = 'Nữ'
                    else:
                        personal_information['sex'] = 'Nam'
                
                if 'Place of origin' in texts[i]:
                    personal_information['place_of_origin'] = texts[i+1] if i + 1 < len(texts) else ""
                
                if 'Place of residence' in texts[i]:
                    personal_information['place_of_resident'] = texts[i].split(": ")[1].strip() if len(texts[i].split(": ")) >= 2 else ""
                
                if 'Date of expiry' in texts[i]:
                    personal_information['place_of_resident'] += ' '
                    for j in range(i + 1, len(texts)):
                        personal_information['place_of_resident'] += texts[j] if j < len(texts) else ""
                             
            final_text = " ".join(texts)
            return final_text
        else:
            return "No text detected in the image"
    except Exception as e:
        return f"Error processing image: {str(e)}"

def extract_date(text):
    pattern = r'\b\d{2}/\d{2}/\d{4}\b'
    
    match = re.search(pattern, text)
    
    if match:
        return match.group()
    else:
        return None


def getEntities(text, ai_client, personal_information):
    entities = ai_client.recognize_entities(documents=[text])[0].entities
    if len(entities) > 0:
        print("\nEntities")
        for entity in entities:
            print('\t{} ({})'.format(entity.text, entity.category))
            
        # Get Person
        persons = [obj for obj in entities if obj.get("category") == "Person"]
        cccd = [obj for obj in entities if obj.get("category") == "PhoneNumber"]
        datetimes = [obj for obj in entities if obj.get("category") == "DateTime"]
        
        if len(datetimes) == 1:
            dob = datetimes[0].text
        elif len(datetimes) == 2:
            dob = min(datetimes[0].text, datetimes[1].text)
            # date_expiry = max(datetimes[0].text, datetimes[1].text)
            date_expiry = extract_date(max(datetimes[0].text, datetimes[1].text))
        else:
            dob = None

        if persons:
            personal_information['full_name'] = persons[0].text
        if cccd:
            personal_information['identity_card_no'] = cccd[0].text
        if dob:
            personal_information['date_of_birth'] = dob
            personal_information['date_expiry'] = date_expiry
                
        is_empty = False
        #  Check if there are any empty values
        for key, value in personal_information.items():
            if value == '':
                is_empty = True
                break
        
        print(f'\nFinal result\n')
        if is_empty:
            print('The photo is blurry, please try again\n')
            
        else:
            for key, value in personal_information.items():
                print(f"\t{key}: {value}")
        
        print('-------------------------------------------------------------------\n')


if __name__ == "__main__":
    main()

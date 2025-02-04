from django.shortcuts import render, HttpResponse, redirect
from predictions.utils.model import ResNet9
import torch
import torchvision.transforms as transforms
from django.utils.safestring import mark_safe
from PIL import Image
import numpy as np
import pandas as pd
from predictions.utils.disease import disease_dic
from predictions.utils.fertilizer import fertilizer_dic
import requests
import config
import pickle
import io






disease_classes = ['Apple___Apple_scab', 'Apple___Black_rot', 'Apple___Cedar_apple_rust',
                   'Apple___healthy', 'Blueberry___healthy', 'Cherry_(including_sour)___Powdery_mildew',
                   'Cherry_(including_sour)___healthy', 'Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot',
                   'Corn_(maize)___Common_rust_', 'Corn_(maize)___Northern_Leaf_Blight',
                   'Corn_(maize)___healthy', 'Grape___Black_rot', 'Grape___Esca_(Black_Measles)',
                   'Grape___Leaf_blight_(Isariopsis_Leaf_Spot)', 'Grape___healthy',
                   'Orange___Haunglongbing_(Citrus_greening)', 'Peach___Bacterial_spot', 'Peach___healthy',
                   'Pepper,_bell___Bacterial_spot', 'Pepper,_bell___healthy', 'Potato___Early_blight',
                   'Potato___Late_blight', 'Potato___healthy', 'Raspberry___healthy', 'Soybean___healthy',
                   'Squash___Powdery_mildew', 'Strawberry___Leaf_scorch', 'Strawberry___healthy',
                   'Tomato___Bacterial_spot', 'Tomato___Early_blight', 'Tomato___Late_blight',
                   'Tomato___Leaf_Mold', 'Tomato___Septoria_leaf_spot', 'Tomato___Spider_mites Two-spotted_spider_mite',
                   'Tomato___Target_Spot', 'Tomato___Tomato_Yellow_Leaf_Curl_Virus',
                   'Tomato___Tomato_mosaic_virus', 'Tomato___healthy']



disease_model_path = 'D:\\Django Major project\\django_major_project\\predictions\\models\\plant_disease_model.pth'
disease_model = ResNet9(3, len(disease_classes))
disease_model.load_state_dict(torch.load(
    disease_model_path, map_location=torch.device('cpu')))
disease_model.eval()

# Loading crop recommendation model

crop_recommendation_model_path = 'D:\\Django Major project\\django_major_project\\predictions\\models\\DecisionTree.pkl'
crop_recommendation_model = pickle.load(
    open(crop_recommendation_model_path, 'rb'))


#home page
def home(request):
    return render(request, "predictions/index.html")


#Crop prediction
def weather_fetch(city_name):
    api_key = "44a7f00aee44beb46c48424125e55157"
    base_url = "https://api.openweathermap.org/data/2.5/weather?"
    complete_url = f"{base_url}appid={api_key}&q={city_name}"

    response = requests.get(complete_url)
    x = response.json()

    if x["cod"] != "404":
        y = x["main"]
        temperature = round((y["temp"] - 273.15), 2)
        humidity = y["humidity"]
        return temperature, humidity
    return None

def crop_prediction(request):
    if request.method == 'POST':
        N = int(request.POST['nitrogen'])
        P = int(request.POST['phosphorous'])
        K = int(request.POST['pottasium'])
        ph = float(request.POST['ph'])
        rainfall = float(request.POST['rainfall'])
        city = request.POST.get("city")

        weather_data = weather_fetch(city)
        if weather_data:
            temperature, humidity = weather_data
            data = np.array([[N, P, K, temperature, humidity, ph, rainfall]])
            my_prediction = crop_recommendation_model.predict(data)
            final_prediction = my_prediction[0]

            return render(request, 'predictions/crop-result.html', {'prediction': final_prediction})
        else:
            return render(request, 'predictions/try_again.html')

    return render(request, "predictions/crop.html")



def fert_recommend(request):
    if request.method == "POST":
        crop_name = request.POST.get('cropname', '').strip()
        N = int(request.POST.get('nitrogen', 0))
        P = int(request.POST.get('phosphorous', 0))
        K = int(request.POST.get('pottasium', 0))

        # Load the fertilizer data
        df = pd.read_csv('D:\\Django Major project\\django_major_project\\predictions\\Data\\fertilizer.csv')

        # Get recommended values
        try:
            nr = df.loc[df['Crop'] == crop_name, 'N'].values[0]
            pr = df.loc[df['Crop'] == crop_name, 'P'].values[0]
            kr = df.loc[df['Crop'] == crop_name, 'K'].values[0]
        except IndexError:
            return render(request, 'fertilizer.html', {"error": "Crop not found in database."})

        # Calculate the deficiencies/excesses
        n, p, k = nr - N, pr - P, kr - K
        temp = {abs(n): "N", abs(p): "P", abs(k): "K"}
        max_value = temp[max(temp.keys())]

        key = f"{max_value}High" if eval(max_value.lower()) < 0 else f"{max_value}low"
        response = mark_safe(fertilizer_dic.get(key, "No recommendation available."))

        return render(request, 'predictions/fertilizer-result.html', {"recommendation": response})

    return render(request, 'predictions/fertilizer.html')


#Disease prediction view

def predict_image(img, model=disease_model):
    """
    Transforms image to tensor and predicts disease label
    :params: image
    :return: prediction (string)
    """
    transform = transforms.Compose([
        transforms.Resize(256),
        transforms.ToTensor(),
    ])
    image = Image.open(io.BytesIO(img))
    img_t = transform(image)
    img_u = torch.unsqueeze(img_t, 0)

    # Get predictions from model
    yb = model(img_u)
    # Pick index with highest probability
    _, preds = torch.max(yb, dim=1)
    prediction = disease_classes[preds[0].item()]
    # Retrieve the class label
    return prediction

def disease_prediction(request):
    title = 'Harvestify - Disease Detection'

    if request.method == 'POST':
        if 'file' not in request.FILES:
            return redirect(request.path)
        
        file = request.FILES.get('file')
        if not file:
            return render(request, 'predictions/disease.html', {'title': title})

        try:
            img = file.read()  # Read the image file

            prediction = predict_image(img)  # Call the prediction function

            prediction = disease_dic.get(prediction, "Unknown Disease")  # Get the result
            return render(request, 'predictions/disease-result.html', {'prediction': prediction, 'title': title})
        except:
            pass

    return render(request, 'predictions/disease.html', {'title': title})


# Create your views here.
def first(request):
    return render(request, "predictions/hello.html")
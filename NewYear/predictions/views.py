from django.shortcuts import render
from predictions.models import Prediction
import random

def Main_page(request):
    return render(request, 'main_page.html')
def Predictions(request):
    return render(request, 'predictions.html')
def Viewing(request):
    return render(request, 'viewing.html', {'Predictions':Prediction.objects.all()})
def Prediction_random(request):
    predictions = Prediction.objects.all()
    return render(request, 'prediction.html',{'Prediction':predictions[random.randint(0,len(predictions)-1)]})
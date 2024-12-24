from django.shortcuts import render
from django.core.paginator import Paginator
from predictions.models import Prediction
import random

def Main_page(request):
    return render(request, 'main_page.html')
def Predictions(request):
    return render(request, 'predictions.html')
def Viewing(request):
    predictions = Prediction.objects.all()
    paginator = Paginator(predictions, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page((page_number))
    return render(request, 'viewing.html', {'page_obj':page_obj})
def Prediction_random(request):
    predictions = Prediction.objects.all()
    return render(request, 'prediction.html',{'Prediction':predictions[random.randint(0,len(predictions)-1)]})
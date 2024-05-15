from django.shortcuts import render
from .models import LecturaTemperatura
from django.http import JsonResponse

def recibir_temperatura(request):
    if request.method == 'POST':
        temperatura = request.POST.get('temperatura')
        LecturaTemperatura.objects.create(temperatura=temperatura)
        return JsonResponse({'mensaje':'Lectura de temperatura guardada correctamente'})
    else:
        return JsonResponse({'error':'Solicitud no válida. Se esperaba un POST'})

        
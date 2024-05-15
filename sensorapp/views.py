from django.shortcuts import render
from .models import LecturaTemperatura
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

def recibir_temperatura(request):
    if request.method == 'POST':
        temperatura = request.POST.get('temperatura')
        LecturaTemperatura.objects.create(temperatura=temperatura)
        return JsonResponse({'mensaje':'Lectura de temperatura guardada correctamente'})
    else:
        return JsonResponse({'error':'Solicitud no válida. Se esperaba un POST'})


def panel_control(request):
    lecturas = LecturaTemperatura.objects.all()
    return render(request, 'sensorapp/panel_control.html', {'lecturas': lecturas})

@csrf_exempt
def recibir_temperatura(request):
    if request.method == 'POST':
        temperatura = request.POST.get('temperatura')
        LecturaTemperatura.objects.create(temperatura=temperatura)
        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'bad request'}, status=400)


def ultima_temperatura(request):
    # Obtener la última lectura de temperatura
    ultima_lectura = LecturaTemperatura.objects.order_by('-fecha').first()
    if ultima_lectura:
        data = {
            'temperatura': ultima_lectura.temperatura,
            'fecha': ultima_lectura.fecha.strftime('%Y-%m-%d %H:%M:%S')  # Formateando la fecha y hora
        }
    else:
        data = {
            'temperatura': 'No disponible',
            'fecha': 'Sin datos'
        }

    return JsonResponse(data)

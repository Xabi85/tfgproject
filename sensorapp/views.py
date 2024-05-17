from django.shortcuts import render
from .models import LecturaTemperatura
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone




def panel_control(request):
    lecturas = LecturaTemperatura.objects.all()
    return render(request, 'sensorapp/panel_control.html', {'lecturas': lecturas})

@csrf_exempt
def recibir_temperatura(request):
    if request.method == 'POST':
        temperatura = request.POST.get('temperatura')
        print("POST data:", request.POST)  # Esto imprimirá los datos recibidos en la consola
        print("Temperatura recibida:", temperatura)  # Verifica qué recibes exactamente aquí
        if temperatura is not None:
            try:
                temperatura_float = float(temperatura)  # Intenta convertir a float
                LecturaTemperatura.objects.create(temperatura=temperatura_float)
                return JsonResponse({'status': 'success'})
            except ValueError:
                return JsonResponse({'status': 'bad request', 'error': 'Temperatura inválida'}, status=400)
        else:
            return JsonResponse({'status': 'bad request', 'error': 'Temperatura no proporcionada'}, status=400)
    else:
        return JsonResponse({'status': 'bad request'}, status=400)

def ultima_temperatura(request):
    # Obtener la última lectura de temperatura
    ultima_lectura = LecturaTemperatura.objects.order_by('-fecha').first()
    if ultima_lectura:
        fecha_local = timezone.localtime(ultima_lectura.fecha)
        data = {
            'temperatura': ultima_lectura.temperatura,
            'fecha': fecha_local.strftime('%Y-%m-%d %H:%M:%S')  # Formateando la fecha y hora
        }
    else:
        data = {
            'temperatura': 'No disponible',
            'fecha': 'Sin datos'
        }

    return JsonResponse(data)

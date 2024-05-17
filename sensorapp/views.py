from django.shortcuts import render
from .models import LecturaTemperatura
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone

API_KEY = 'abcd'




def panel_control(request):
    lecturas = LecturaTemperatura.objects.all()
    return render(request, 'sensorapp/panel_control.html', {'lecturas': lecturas})

@csrf_exempt
def recibir_temperatura(request):
    # Verificar la clave de API en el encabezado
    api_key = request.headers.get('Authorization')
    if api_key != API_KEY:
        return JsonResponse({'status': 'unauthorized', 'error': 'Clave de API incorrecta'}, status=401)

    if request.method == 'POST':
        temperatura = request.POST.get('temperatura')
        if temperatura is not None:
            try:
                temperatura_float = float(temperatura)
                LecturaTemperatura.objects.create(temperatura=temperatura_float)
                return JsonResponse({'status': 'success'})
            except ValueError:
                return JsonResponse({'status': 'bad request', 'error': 'Temperatura inválida'}, status=400)
        else:
            return JsonResponse({'status': 'bad request', 'error': 'Temperatura no proporcionada'}, status=400)
    else:
        return JsonResponse({'status': 'bad request', 'error': 'Método no permitido'}, status=405)

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

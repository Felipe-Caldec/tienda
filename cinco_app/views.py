from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.templatetags.static import static
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.humanize.templatetags.humanize import intcomma

def portada(request):
    cards = [
        {"titulo": "Corazon de yeso", 'descripcion': ' Lindo corazon para regalo', "Precio": "2.000", 'imagen': static('img1.jpg'), 'categoria':'Hogar', 'adicional':' Corazon hecho de yeso sin pintar'},
        {"titulo": "Card 2", 'descripcion': 'Texto 2', "Precio": "2.000", 'imagen': 'ruta2.jpg', 'categoria':'Hogar'},
        {"titulo": "Card 3", 'descripcion': 'Texto 3', "Precio": "2.000", 'imagen': 'ruta3.jpg', 'categoria':'Hogar'},
        {"titulo": "Card 4", 'descripcion': 'Texto 4', "Precio": "2.000", 'imagen': 'ruta4.jpg', 'categoria':'Limpieza'},
        {"titulo": "Card 5", 'descripcion': 'Texto 5', "Precio": "2.000", 'imagen': 'ruta5.jpg', 'categoria':'Infantil'},
        {"titulo": "Card 6", 'descripcion': 'Texto 6', "Precio": "2.000", 'imagen': 'ruta6.jpg', 'categoria':'Jardín'},
        {"titulo": "Card 7", 'descripcion': 'Texto 7', "Precio": "2.000", 'imagen': 'ruta7.jpg', 'categoria':'Infantil'},
        {"titulo": "Card 8", 'descripcion': 'Texto 8', "Precio": "2.000", 'imagen': static('img2.png'), 'categoria':'Jardín'},
        {"titulo": "Card 9", 'descripcion': 'Texto 9', "Precio": "2.000", 'imagen': static('img3.png'), 'categoria':'Jardín'},
        {"titulo": "Card 10", 'descripcion': 'Texto 10', "Precio": "2.000", 'imagen': static('img4.jpg'), 'categoria':'Jardín'},
        {"titulo": "Card 11", 'descripcion': 'Texto 11', "Precio": "2.000", 'imagen': static('img5.jpg'), 'categoria':'Infantil'},
        {"titulo": "Card 12", 'descripcion': 'Texto 12', "Precio": "2.000", 'imagen': static('img6.png'), 'categoria':'Infantil'},
        {"titulo": "Card 13", 'descripcion': 'Texto 13', "Precio": "2.000",'imagen': static('images.jpg'), 'categoria':'Infantil'},
        {"titulo": "Card 14", 'descripcion': 'Texto 14', "Precio": "2.000",'imagen': static('images.jpg'), 'categoria':'Limpieza'},
        {"titulo": "Card 15", 'descripcion': 'Texto 15', "Precio": "2.000",'imagen': static('images.jpg'), 'categoria':'Limpieza'},
        {"titulo": "Card 16", 'descripcion': 'Texto 16', "Precio": "2.000",'imagen': static('images.jpg'), 'categoria':'Limpieza'},
        {"titulo": "Card 17", 'descripcion': 'Texto 17', "Precio": "2.000",'imagen': static('images.jpg'), 'categoria':'Limpieza'},
        {"titulo": "Card 18", 'descripcion': 'Texto 18', "Precio": "2.000",'imagen': static('images.jpg'), 'categoria':'Hogar'},
        {"titulo": "Card 19", 'descripcion': 'Texto 19', "Precio": "2.000",'imagen': static('images.jpg'), 'categoria':'Hogar'},
        {"titulo": "Card 20", 'descripcion': 'Texto 20', "Precio": "2.000",'imagen': static('images.jpg'), 'categoria':'Hogar'}
      
    ]

    categoria = request.GET.get('categoria')
    if categoria:
        cards = [card for card in cards if card['categoria'] == categoria]
    
    paginator = Paginator(cards, 16)  
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'portada.html', {'page_obj': page_obj, 'categoria': categoria})

@csrf_exempt
def procesar_carrito(request):
    if request.method == 'POST':
        items_json = request.POST.get('items')
        items = json.loads(items_json)

        # Aquí puedes guardar en base de datos, enviar por correo, etc.
        for item in items:
            print(f"Producto: {item['titulo']} - Precio: {item['precio']}")

        return render(request, 'pedido_exitoso.html', {'items': items})
    return JsonResponse({'error': 'Método no permitido'}, status=405)

def checkout(request):
    if request.method == 'POST':
        items_json = request.POST.get('items')
        items = json.loads(items_json)
        total = sum(
            int(item['precio'].replace('.', '')) for item in items
            )
        return render(request, 'checkout.html', {'items': items, 'items_json': items_json, 'total': total})
    return redirect('portada')

def procesar_pedido(request):
    if request.method == 'POST':
        items = json.loads(request.POST.get('items'))
        nombre = request.POST.get('nombre')
        direccion = request.POST.get('direccion')
        correo = request.POST.get('correo')
        telefono = request.POST.get('telefono')

        mensaje = f"Nuevo pedido de: {nombre}\n\n"
        mensaje += f"Dirección: {direccion}\nCorreo: {correo}\nTeléfono: {telefono}\n\n"
        mensaje += "Productos solicitados:\n"

        for item in items:
            mensaje += f"- {item['titulo']} (${item['precio']})\n"

        send_mail(
            subject="Nuevo Pedido",
            message=mensaje,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.DEFAULT_FROM_EMAIL],  # o tu correo
            fail_silently=False,
        )

        return render(request, 'pedido_exitoso.html', {'nombre': nombre})
    return redirect('portada')

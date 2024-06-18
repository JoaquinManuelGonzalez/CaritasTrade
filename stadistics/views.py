from django.http import HttpResponse
import matplotlib.pyplot as plt
import pandas as pd
from django.shortcuts import render
from django.utils.timezone import now
from datetime import datetime, timedelta
from io import BytesIO
import base64
from data_base.models import Affiliate, ExchangeSolicitude, Products, ExchangePost, Exchange
from adjustText import adjust_text


def main_view(request):
    return render(request, "main_view.html")


# Función auxiliar para crear gráficos y convertirlos a base64
def create_base64_image(fig):
    buf = BytesIO()
    fig.savefig(buf, format="png")
    buf.seek(0)
    image_base64 = base64.b64encode(buf.read()).decode("utf-8")
    buf.close()
    return image_base64


def transactions_pie_chart(request):
    # Obtén los datos de las publicaciones de intercambio y sus estados
    exchange_posts = ExchangePost.objects.all()
    states = ['is_paused', 'is_rejected', 'is_active', 'is_finished']
    state_counts = {state: exchange_posts.filter(**{state: True}).count() for state in states}

    # Datos y etiquetas para el gráfico
    data = list(state_counts.values())
    labels = list(state_counts.keys())

    # Crear el gráfico
    fig, ax = plt.subplots(figsize=(8, 8))
    wedges, texts, autotexts = ax.pie(data, labels=labels, autopct='%1.1f%%', startangle=140)

    # Ajustar las etiquetas
    adjust_text(texts + autotexts, arrowprops=dict(arrowstyle="->", color='r', lw=1))

    ax.axis('equal')  # Asegura que el gráfico es circular
    plt.tight_layout()

    # Guardar la gráfica en un buffer
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)

    return HttpResponse(buffer, content_type='image/png')


def transactions_by_age(request, age_range=None):
    # Obtener todas las transacciones
    exchange_solicitudes = ExchangeSolicitude.objects.all().select_related('affiliate_id')

    # Crear una lista con los datos de las transacciones
    data = []
    for sol in exchange_solicitudes:
        affiliate = sol.affiliate_id
        age = datetime.now().year - affiliate.birth_day.year
        data.append({
            'timestamp': sol.timestamp,
            'age': age
        })

    # Convertir a DataFrame
    df = pd.DataFrame(data)

    # Verificar si 'timestamp' está en el DataFrame
    if 'timestamp' not in df.columns:
        return HttpResponse("La columna 'timestamp' no se encuentra en los datos.")

    # Filtros de rango etario
    if age_range:
        age_min, age_max = map(int, age_range.split('-'))
        df = df[(df['age'] >= age_min) & (df['age'] <= age_max)]

    # Crear el histograma
    plt.hist(df['age'], bins=10, edgecolor='black')
    plt.title('Transacciones por edades')
    plt.xlabel('Edad')
    plt.ylabel('Número de transacciones')
    plt.grid(True)

    # Guardar la gráfica en un buffer
    import io
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)

    # Devolver la gráfica como respuesta HTTP
    return HttpResponse(buffer, content_type='image/png')


def category_histogram(request):
    try:
        # Obtener todas las publicaciones de intercambio finalizadas
        exchange_posts = ExchangePost.objects.filter(is_finished=True)

        # Crear una lista con los datos de las publicaciones
        data = []
        for post in exchange_posts:
            data.append({
                'category': post.product_category.name if post.product_category else 'No Category'
            })

        # Convertir a DataFrame
        df = pd.DataFrame(data)

        # Crear el histograma
        category_counts = df['category'].value_counts()
        plt.figure(figsize=(10, 6))
        plt.bar(category_counts.index, category_counts.values, color='skyblue')
        plt.title('Frecuencia de trueques finalizados por categoría')
        plt.xlabel('Categoría de producto')
        plt.ylabel('Número de trueques finalizados')
        plt.xticks(rotation=45)
        plt.tight_layout()

        # Guardar la gráfica en un buffer
        import io
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)

        # Devolver la gráfica como respuesta HTTP
        return HttpResponse(buffer, content_type='image/png')

    except Exception as e:
        return HttpResponse(f"Error al generar el histograma: {str(e)}", content_type='text/plain')
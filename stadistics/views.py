import io
import base64
from datetime import datetime
from django.http import HttpResponse
from django.shortcuts import render
import matplotlib.pyplot as plt
import pandas as pd
from data_base.models import ExchangeSolicitude, ExchangePost
from adjustText import adjust_text

def stadistics_menu(request):
    return render(
        request,
        "stadistics_menu.html",
        {
            "session_id": request.session.get("id"),
            "user_session": False,
        },
    )

def create_base64_image(fig):
    buf = io.BytesIO()
    fig.savefig(buf, format="png")
    buf.seek(0)
    image_base64 = base64.b64encode(buf.read()).decode("utf-8")
    buf.close()
    return image_base64

def render_chart(request, template_name, fig):
    image_base64 = create_base64_image(fig)
    return render(
        request,
        template_name,
        {
            "image": image_base64,
            "session_id": request.session.get("id"),
            "user_session": False,
        },
    )

def transactions_pie_chart(request):
    exchange_posts = ExchangePost.objects.all()
    states = ["is_paused", "is_rejected", "is_active", "is_finished"]
    state_counts = {state: exchange_posts.filter(**{state: True}).count() for state in states}
    data = list(state_counts.values())
    labels = list(state_counts.keys())

    fig, ax = plt.subplots(figsize=(6, 6))
    wedges, texts, autotexts = ax.pie(data, labels=labels, autopct="%1.1f%%", startangle=140)
    adjust_text(texts + autotexts, arrowprops=dict(arrowstyle="->", color="r", lw=1))
    ax.axis("equal")
    plt.tight_layout()

    return render_chart(request, "transactions_pie_chart.html", fig)

def transactions_by_age(request, age_range=None):
    exchange_solicitudes = ExchangeSolicitude.objects.all().select_related("affiliate_id")
    data = [{"timestamp": sol.timestamp, "age": datetime.now().year - sol.affiliate_id.birth_day.year} for sol in exchange_solicitudes]

    df = pd.DataFrame(data)
    if "timestamp" not in df.columns:
        return HttpResponse("La columna 'timestamp' no se encuentra en los datos.")

    if age_range:
        age_min, age_max = map(int, age_range.split("-"))
        df = df[(df["age"] >= age_min) & (df["age"] <= age_max)]

    plt.hist(df["age"], bins=10, edgecolor="black")
    plt.title("Transacciones por edades")
    plt.xlabel("Edad")
    plt.ylabel("Número de transacciones")
    plt.grid(True)

    return render_chart(request, "transactions_by_age.html", plt)

def category_histogram(request):
    try:
        exchange_posts = ExchangePost.objects.filter(is_finished=True)
        data = [{"category": post.product_category.name if post.product_category else "No Category"} for post in exchange_posts]
        df = pd.DataFrame(data)

        category_counts = df["category"].value_counts()
        plt.figure(figsize=(10, 6))
        plt.bar(category_counts.index, category_counts.values, color="skyblue")
        plt.title("Frecuencia de trueques finalizados por categoría")
        plt.xlabel("Categoría de producto")
        plt.ylabel("Número de trueques finalizados")
        plt.xticks(rotation=45)
        plt.tight_layout()

        return render_chart(request, "category_histogram.html", plt)

    except Exception as e:
        return HttpResponse(f"Error al generar el histograma: {str(e)}", content_type="text/plain")

import io
import base64
from datetime import datetime
from django.http import HttpResponse
from django.shortcuts import render
import matplotlib.pyplot as plt
import pandas as pd
from data_base.models import ExchangePost
from adjustText import adjust_text
from matplotlib import colors as mcolors


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

def no_data():
    # Si no hay datos, mostrar un gráfico con una leyenda específica
    fig, ax = plt.subplots()
    ax.text(
        0.5,
        0.5,
        "Aún no se registran datos",
        horizontalalignment="center",
        verticalalignment="center",
        transform=ax.transAxes,
        fontsize=12,
    )
    plt.axis("off")
    return fig

def transactions_pie_chart(request):
    try:
        exchange_posts = ExchangePost.objects.all()
        state_counts = {
            "Activas": exchange_posts.filter(
                is_active=True,
                is_paused=False,
                is_rejected=False,
                is_finished=False,
                has_failed=False,
            ).count(),
            "Rechazadas": exchange_posts.filter(
                is_rejected=True,
                is_active=False,
                is_paused=False,
                is_finished=False,
                has_failed=False,
            ).count(),
            "Pausadas": exchange_posts.filter(
                is_paused=True,
                is_active=True,
                is_finished=False,
                is_rejected=False,
                has_failed=False,
            ).count(),
            "Finalizadas": exchange_posts.filter(
                is_finished=True,
                is_active=True,
                is_paused=False,
                is_rejected=False,
                has_failed=False,
            ).count(),
            "Fallidas": exchange_posts.filter(
                is_finished=False,
                is_active=True,
                is_paused=False,
                is_rejected=False,
                has_failed=True,
            ).count(),
        }
        data = list(state_counts.values())
        labels = list(state_counts.keys())

        fig, ax = plt.subplots(figsize=(6, 6))
        wedges, texts, autotexts = ax.pie(
            data, labels=labels, autopct="%1.1f%%", startangle=140
        )
        adjust_text(texts + autotexts, arrowprops=dict(arrowstyle="->", color="r", lw=1))
        ax.axis("equal")
        plt.tight_layout()

        return render_chart(request, "transactions_pie_chart.html", fig)
    except Exception:
        return render_chart(request, "transactions_pie_chart.html",no_data())


def transactions_by_age(request):
    try:
        exchange_posts = ExchangePost.objects.filter(has_failed=True).select_related(
            "affiliate"
        )

        # Obtener los datos y calcular la edad
        data = [
            {
                "age": datetime.now().year - post.affiliate.birth_day.year,
            }
            for post in exchange_posts
        ]

        # Crear un DataFrame a partir de los datos
        df = pd.DataFrame(data)

        # Definir los rangos etarios
        age_bins = [18, 30, 45, 60, 100]
        age_labels = ["18-29", "30-44", "45-59", "60+"]

        # Categorizar las edades en los rangos definidos
        df["age_range"] = pd.cut(df["age"], bins=age_bins, labels=age_labels, right=False)

        # Contar las publicaciones fallidas por rango etario
        failed_counts = df["age_range"].value_counts().reindex(age_labels, fill_value=0)

        # Crear el gráfico
        fig, ax = plt.subplots(figsize=(10, 6))
        failed_counts.plot(kind="bar", color="skyblue", ax=ax)
        ax.set_title("Publicaciones Fallidas por Rango Etario")
        ax.set_xlabel("Rango Etario")
        ax.set_ylabel("Número de Publicaciones Fallidas")
        plt.xticks(rotation=45)
        plt.tight_layout()

        return render_chart(request, "transactions_by_age.html", fig)
    except Exception:
        return render_chart(request, "transactions_by_age.html",no_data())

def category_histogram(request):
    try:
        exchange_posts = ExchangePost.objects.filter(
            is_finished=True, is_active=True, is_paused=False, is_rejected=False
        )
        data = [
            {
                "category": (
                    post.product_category.name if post.product_category else "No Category"
                )
            }
            for post in exchange_posts
        ]
        df = pd.DataFrame(data)

        category_counts = df["category"].value_counts()

        # Crear una lista de colores
        colors = list(mcolors.TABLEAU_COLORS.values())

        # Asegurarse de que haya suficientes colores para todas las categorías
        if len(category_counts) > len(colors):
            colors = colors * (len(category_counts) // len(colors) + 1)

        plt.figure(figsize=(10, 6))
        plt.bar(
            category_counts.index,
            category_counts.values,
            color=colors[: len(category_counts)],
        )
        plt.title("Frecuencia de trueques finalizados por categoría")
        plt.xlabel("Categoría de producto")
        plt.ylabel("Número de trueques finalizados")
        plt.xticks(rotation=45)
        plt.tight_layout()

        return render_chart(request, "category_histogram.html", plt)

    except Exception:
        return render_chart(request, "category_histogram.html",no_data())
        

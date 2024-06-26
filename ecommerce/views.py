from datetime import datetime
import uuid
from django.http import HttpResponse
from django.shortcuts import redirect, render
from requests import session
from list_exchange_products.views import session_name
from data_base.models import (
    Branches,
    EcommercePost,
    ProductCategory,
    Affiliate,
    Cupon,
    Workers,
)
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import qrcode
from django.core.files.base import ContentFile
from reportlab.lib.utils import ImageReader


def decode_images(post):
    decoded_images = []
    for p in post:
        if p.image:
            image_data = p.image.decode("utf-8")
            decoded_images.append(image_data)
        else:
            decoded_images.append(None)
    combined_data = list(zip(decoded_images, post))
    return combined_data


# Create your views here.
def list_ecommerce(request):
    posts = EcommercePost.objects.filter(stock__gt=0)

    query = request.GET.get("q")
    category = request.GET.get("category")

    if query:
        posts = posts.filter(title__icontains=query)
    if category:
        posts = posts.filter(product_category_id=category)
    if not request.session.get("id"):
        return redirect("landing_page")
    print(decode_images(posts))
    return render(
        request,
        "ecommerce.html",
        {
            "posts": decode_images(posts),
            "session_id": request.session.get("id"),
            "role": request.session.get("role"),
            "user_session": False,
            "session_name": session_name(request),
            "categories": ProductCategory.objects.all(),
        },
    )


def see_ecommerce_post(request, id):
    post = EcommercePost.objects.get(id=id)
    post_image = None
    if bool(post.image):
        post_image = post.image.decode("utf-8")
    own_post = False
    if (
        request.session.get("role") == "worker"
        and Branches.objects.filter(worker=request.session.get("id")).exists()
    ):
        if (
            bool(post.branch)
            and post.branch.id
            == Branches.objects.get(worker=request.session.get("id")).id
        ):
            own_post = True
    print(own_post)
    return render(
        request,
        "see_ecommerce_post.html",
        {
            "post": post,
            "post_image": post_image,
            "user_session": False,
            "session_name": session_name(request),
            "session_id": request.session.get("id"),
            "own_post": own_post,
            "category": ProductCategory.objects.filter(
                id=post.product_category_id
            ).first(),
            "role": request.session.get("role"),
        },
    )


def delete_post(request, id):
    if EcommercePost.objects.filter(id=id).exists():
        EcommercePost.objects.filter(id=id).first().delete()
    return redirect("list_ecommerce")


def exchange_points(request, id):
    if not request.session.get("id"):
        return redirect("list_ecommerce")
    post = EcommercePost.objects.get(id=id)
    message = "Los puntos han sido canjeados por el producto."
    type_of_alert = "success"
    user = Affiliate.objects.get(id=request.session.get("id"))
    if post.stock > 0 and user.points >= post.point_cost:
        post.stock -= 1
        user.points -= post.point_cost
        post.save()
        user.save()
        code = str(uuid.uuid4())[:5]
        timestamp = datetime.now()
        descriptions = [
            "Producto: " + post.title,
            "Descripcción: " + post.description,
            "Afiliado: " + user.name + " " + user.surname + " (" + user.dni + ")",
            f"Fecha: {timestamp.strftime('%Y-%m-%d %H:%M:%S')}",
            "Costo: " + str(post.point_cost),
            "Filial: " + post.branch.name if post.branch else None,
        ]
        pdf = generate_pdf_with_qr(code, descriptions)
        cupon = Cupon(
            code=code,
            pdf=pdf,
            timestamp=timestamp,
            affiliate=user,
            exchange_post=post,
            branch=post.branch if post.branch else None,
        )
        cupon.save()
    elif post.stock <= 0:
        message = "No hay suficiente stock disponible de este producto."
        type_of_alert = "danger"
    elif user.points < post.point_cost:
        message = "Su cuenta no tiene suficientes puntos para adquirir este producto."
        type_of_alert = "danger"
    post_image = None
    if bool(post.image):
        post_image = post.image.decode("utf-8")
    own_post = False
    if (
        request.session.get("role") == "worker"
        and Branches.objects.filter(worker=request.session.get("id")).exists()
    ):
        if (
            bool(post.branch)
            and post.branch.id
            == Branches.objects.get(worker=request.session.get("id")).id
        ):
            own_post = True
    return render(
        request,
        "see_ecommerce_post.html",
        {
            "post": post,
            "post_image": post_image,
            "user_session": False,
            "session_name": session_name(request),
            "session_id": request.session.get("id"),
            "own_post": own_post,
            "category": ProductCategory.objects.filter(
                id=post.product_category_id
            ).first(),
            "role": request.session.get("role"),
            "message": message,
            "type_of_alert": type_of_alert,
        },
    )


def see_cupons(request):
    cupons = Cupon.objects.filter(
        affiliate=Affiliate.objects.get(id=request.session.get("id"))
    )
    context = {
        "cupons": cupons,
        "user_session": False,
        "session_name": session_name(request),
        "session_id": request.session.get("id"),
    }
    return render(request, "see_cupons.html", context)


def download_cupon(request, cupon_id):
    cupon = Cupon.objects.get(id=cupon_id)
    response = HttpResponse(cupon.pdf, content_type="application/pdf")
    response["Content-Disposition"] = f'attachment; filename="{cupon.code}.pdf"'
    return response


def generate_pdf_with_qr(code, descriptions=None):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    # Preparar el contenido del QR
    qr_content = str(code)

    # Generar el código QR
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(qr_content)
    qr.make(fit=True)
    qr_img = qr.make_image(fill="black", back_color="white")

    # Convertir el código QR en un objeto ImageReader
    qr_buffer = BytesIO()
    qr_img.save(qr_buffer, format="PNG")
    qr_buffer.seek(0)
    qr_image = ImageReader(qr_buffer)

    # Calcular la posición para centrar horizontalmente el QR
    qr_width, qr_height = 200, 200  # Tamaño del QR
    qr_x = (width - qr_width) / 2  # Centrar horizontalmente

    # Dibujar el código QR centrado horizontalmente en el PDF
    c.drawImage(qr_image, qr_x, height - 200, width=qr_width, height=qr_height)

    # Agregar descripciones adicionales al PDF si existen
    if descriptions:
        text_y = height - 200
        for description in descriptions:
            c.drawString(20, text_y, description)
            text_y -= 20  # Espacio entre descripciones

    c.showPage()
    c.save()

    buffer.seek(0)
    pdf_file = buffer.getvalue()

    return pdf_file


def register_cupons(request):
    if not request.session.get("role") == "worker":
        return redirect("landing_page")
    if request.method == "POST":
        code = request.POST.get("code")
        if not code:
            return render(
                request,
                "message.html",
                {
                    "message": "Debe ingresar un código",
                    "type_of_alert": "danger",
                },
            )
        if not Cupon.objects.filter(code=code).exists():
            return render(
                request,
                "message.html",
                {
                    "message": "No existe un cupón con ese código",
                    "type_of_alert": "danger",
                },
            )
        if Cupon.objects.filter(code=code).first().used == True:
            return render(
                request,
                "message.html",
                {
                    "message": "Este código ya fue usado",
                    "type_of_alert": "danger",
                },
            )
        if (
            not Cupon.objects.filter(code=code).first().branch
            == Branches.objects.get(worker=request.session.get("id"))
        ):
            return render(
                request,
                "message.html",
                {
                    "message": "Este código no corresponde a esta sucursal",	
                    "type_of_alert": "danger",
                },
            )
        c = Cupon.objects.get(code=code)
        c.used = True
        c.save()
        return render(
            request,
            "message.html",
            {
                "message": "Cupón registrado exitosamente",
                "type_of_alert": "success",
            },
        )
    elif request.method == "GET":
        return render(
            request,
            "register_cupons.html",
            {
                "user_session": False,
                "session_name": session_name(request),
                "session_id": request.session.get("id"),
            },
        )

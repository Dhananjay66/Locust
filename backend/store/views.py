from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Product
from django.shortcuts import get_object_or_404, render


import json
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

def home(request):
    return JsonResponse({"message": "Welcome to the shop"})

def product_list(request):
    products = list(Product.objects.values("id", "name", "price"))
    return JsonResponse({"products": products})

def product_detail(request, pk):
    p = get_object_or_404(Product, pk=pk)
    return JsonResponse({"id": p.id, "name": p.name, "price": str(p.price)})



@csrf_exempt
@require_POST
def login_view(request):
    data = json.loads(request.body)
    user = authenticate(
        request,
        username=data.get("username"),
        password=data.get("password"),
    )
    if user is None:
        return JsonResponse({"error": "invalid credentials"}, status=401)
    login(request, user)
    return JsonResponse({"message": "logged in"})


def profile(request):
    if not request.user.is_authenticated:
        return JsonResponse({"error": "unauthorized"}, status=401)
    return JsonResponse({"username": request.user.username})

def login_page(request):
    return render(request, "store/login_page.html")
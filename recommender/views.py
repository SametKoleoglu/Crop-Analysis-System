from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from .models import UserProfile, Prediction
from .ml.loader import predict_one, load_bundle as load_model

def home(request):
    return render(request, "home.html")


def profile(request):
    return render(request, "profile.html")



def signup(request):
    try:
        if request.method == "POST":
            fullname = request.POST["fullname"]
            email = request.POST["email"]
            phone = request.POST["phone_number"]
            password = request.POST["password"]
            if not fullname or not email or not phone or not password:
                messages.error(request, "All fields are required.")
                return redirect("signup")
            if len(password) < 6:
                messages.error(request, "Password must be at least 6 characters long.")
                return redirect("signup")
            if User.objects.filter(username=email).exists():
                messages.error(request, "Account already exists with this email.")
                return redirect("signup")
            user = User.objects.create_user(username=email, password=password)
            if " " in fullname:
                first, last = fullname.split(" ", 1)
            else:
                first, last = fullname, ""
            user.first_name, user.last_name = first, last
            user.save()
            UserProfile.objects.create(user=user, phone=phone)
            login(request, user)
            messages.success(request, "Account created successfully.")
            return redirect("prediction")
        return render(request, "signup.html")
    except Exception as e:
        print("Error during signup:", e)
        return render(
            request,
            "signup.html",
            {"error": "An error occurred during signup. Please try again."},
        )


def signin(request):
    try:
        if request.method == "POST":
            username = request.POST["email_username"]
            password = request.POST["password"]
            user = authenticate(request, username=username, password=password)
            if not user:
                messages.error(request, "Invalid email or password.")
                return redirect("signin")
            if user and user.check_password(password):
                login(request, user)
                messages.success(request, "Signed in successfully.")
                return redirect("prediction")
        return render(request, "signin.html")
    except Exception as e:
        messages.error(request, "An error occurred during sign in. Please try again.")
        return redirect("signin")



def signout(request):
    try:
        if not request.user.is_authenticated:
            return redirect("signin")
        logout(request)
        messages.success(request, "You have been signed out successfully.")
        return redirect("signin")
    except Exception as e:
        messages.error(request, "An error occurred during sign out. Please try again.")
        return redirect("signin")


def prediction(request):
    if not request.user.is_authenticated:
        return redirect("signin")
    
    feature_order = load_model()["feature_cols"]
    result = None
    last_data = None
    
    if request.method == "POST":
        try:
            
            data= {}
            for c in feature_order:
                data[c] = float(request.POST.get(c))

            
        except ValueError as e:
            messages.error(request, "Lütfen geçerli bir sayı girin!")
            return redirect("prediction")
        
        label = predict_one(data)
        
        Prediction.objects.create(user=request.user, predicted_crop=label, **data)
        
        result = label
        last_data = data
        
        messages.success(request, f"Önerilen Ürün: {label.title()}")
   
    return render(request, "prediction.html", locals())




def history(request):
    return render(request, "history.html")

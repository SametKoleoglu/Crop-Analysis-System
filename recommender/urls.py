from django.urls import path
from recommender import views

urlpatterns = [
    path("", views.home, name="home"),
    path("prediction/", views.prediction, name="prediction"),
    path("predictions-history/", views.history, name="history"),
    path("signup/", views.signup, name="signup"),
    path("signin/", views.signin, name="signin"),
    path("signout/", views.signout, name="signout"),
    path("profile/", views.profile, name="profile"),
]
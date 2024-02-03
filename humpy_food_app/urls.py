from django.contrib import admin
from django.urls import path, include
from humpy_food_app import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", views.index, name="index"),
    path("register", views.register, name="register"),
    path("login", views.loginuser, name="login"),
    path("logout", views.logoutuser, name="logout"),
    path("setprofile", views.setprofile, name="setprofile"),
    path("profile", views.profile, name="profile"),
    path("addmenu", views.addmenu, name="addmenu"),
    path("editmenu", views.editmenu, name="editmenu"),
    path("deletemenu", views.deletemenu, name="deletemenu"),
    path("contact", views.contact, name="contact"),
    path("about", views.about, name="about"),
    path("faq", views.faq, name="faq"),
    path("tc", views.tc, name="tc"),
    path("menu", views.menu, name="menu"),
    path("cart", views.cart, name="cart"),
    path("editcart/<int:id>", views.editcart, name="editcart"),
    path("deletecart", views.deletecart, name="deletecart"),
    path("payment", views.payment, name="payment"),
    path('paypal/', include('paypal.standard.ipn.urls')),
    path("payment_done", views.payment_done, name="payment_done"),
    path("payment_cancelled", views.payment_cancelled, name="payment_cancelled"),
    path("tracking", views.tracking, name="tracking"),
    path("edittrack", views.edittrack, name="edittrack"),
    path("thank", views.thank, name="thank"),
    path("feedback", views.feedback, name="feedback"),
]

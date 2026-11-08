from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("shop/", views.catalog, name="catalog"),
    path("search/", views.search, name="search"),
    path("collections/<slug:slug>/", views.collection, name="collection"),
    path("products/<slug:slug>/", views.product_detail, name="product_detail"),
    path("pages/<slug:slug>/", views.page, name="page"),
    path("basket/", views.cart_detail, name="cart_detail"),
    path("basket/add/<slug:slug>/", views.cart_add, name="cart_add"),
    path("basket/update/<int:pk>/", views.cart_update, name="cart_update"),
    path("basket/remove/<int:pk>/", views.cart_remove, name="cart_remove"),
    path("checkout/", views.checkout, name="checkout"),
    path("checkout/success/<int:pk>/", views.order_success, name="order_success"),
    path("contact/", views.contact, name="contact"),
    path("newsletter/", views.newsletter, name="newsletter"),
    path("robots.txt", views.robots, name="robots"),
    path("sitemap.xml", views.sitemap, name="sitemap"),
]
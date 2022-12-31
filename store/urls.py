from django.urls import path

from . import views

app_name = 'store'

urlpatterns = [
    path('', views.store, name='storehome'),
    path('category/<slug:category_slug>/',
         views.store, name='products_by_category'),
    path('color/<slug:color_slug>/', views.store, name='products_by_color'),
    path('size/<slug:size_slug>/', views.store, name='products_by_size'),
    path('<slug:category_slug>/<slug:product_slug>/',
         views.product_detail, name='product_detail'),
    

    path('suggestionapi/', views.suggestionApi, name="suggestionApi"),
    path('search/', views.search, name="search"),
]

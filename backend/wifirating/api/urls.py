from django.urls import path
from . import views

urlpatterns = [
    path('wifi-models/', views.get_wifi_models, name='get_wifi_models'),
    path('wifi-models/<int:model_id>/', views.get_wifi_model_detail, name='get_wifi_model_detail'),
    path('favorites/', views.toggle_favorite, name='toggle_favorite'),
    path('favorites/<int:user_id>/', views.get_user_favorites, name='get_user_favorites'),
    path('reviews/', views.add_review, name='add_review'),
    path('reviews/<int:model_id>/', views.get_model_reviews, name='get_model_reviews'),
    path('user-reviews/<int:user_id>/', views.get_user_reviews, name='get_user_reviews'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
]
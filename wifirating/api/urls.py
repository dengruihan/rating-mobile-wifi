from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import WifiModelViewSet, ReviewViewSet, FavoriteViewSet, register, login, get_wifi_model_reviews, get_user_favorites, get_user_reviews, add_favorite, remove_favorite

router = DefaultRouter()
router.register(r'wifi-models', WifiModelViewSet)
router.register(r'reviews', ReviewViewSet)
router.register(r'favorites', FavoriteViewSet)

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('reviews/<int:wifi_model_id>/', get_wifi_model_reviews, name='get_wifi_model_reviews'),
    path('favorites/<int:user_id>/', get_user_favorites, name='get_user_favorites'),
    path('user-reviews/<int:user_id>/', get_user_reviews, name='get_user_reviews'),
    path('favorites/', add_favorite, name='add_favorite'),
    path('favorites/delete/', remove_favorite, name='remove_favorite'),
    path('', include(router.urls)),
]

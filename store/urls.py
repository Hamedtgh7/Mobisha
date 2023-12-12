from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import LoginView, ProductViewSet, PriceChangeViewSet

router = DefaultRouter()
router.register('product', ProductViewSet, basename='product')

urlpatterns = [
    path('login/', LoginView.as_view()),
    path('', include(router.urls)),
    path('changes/', PriceChangeViewSet.as_view({'get': 'list'}))
]

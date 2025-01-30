from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AccountViewSet, DestinationViewSet, get_destinations, incoming_data

router = DefaultRouter()
router.register(r'accounts', AccountViewSet)
router.register(r'accounts/(?P<account_id>[^/.]+)/destinations', DestinationViewSet)

urlpatterns = [
    path('', include(router.urls)),  
    path('server/incoming_data/', incoming_data),  
    path('accounts/<uuid:account_id>/destinations/', get_destinations),  
]

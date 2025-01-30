from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Account, Destination
from .serializers import AccountSerializer, DestinationSerializer
import requests



class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer



class DestinationViewSet(viewsets.ModelViewSet):
    queryset = Destination.objects.all()
    serializer_class = DestinationSerializer

    def get_queryset(self):
        return self.queryset.filter(account_id=self.kwargs['account_id'])



@api_view(['GET'])
def get_destinations(request, account_id):
    account = get_object_or_404(Account, account_id=account_id)
    destinations = Destination.objects.filter(account=account)
    serializer = DestinationSerializer(destinations, many=True)
    return Response(serializer.data)

from .models import Account, Destination, IncomingDataLog
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
import requests
from django.shortcuts import get_object_or_404

@api_view(['POST'])
def incoming_data(request):
    secret_token = request.headers.get('CL-X-TOKEN')
    if not secret_token:
        return Response({"error": "Un Authenticate"}, status=status.HTTP_401_UNAUTHORIZED)

    account = get_object_or_404(Account, app_secret_token=secret_token)
    data = request.data  

    
    log = IncomingDataLog(
        account=account,
        user_id=data.get('user_id', ''),
        action=data.get('action', ''),
        data=data,
        response_status=200  
    )
    log.save()  

    
    for destination in account.destinations.all():
        try:
            headers = destination.headers
            if destination.http_method == "GET":
                response = requests.get(destination.url, params=data, headers=headers)
            else:
                response = requests.request(destination.http_method, destination.url, json=data, headers=headers)

            if response.status_code >= 400:
                print(f"Failed to send data to {destination.url}")
        except Exception as e:
            print(f"Error sending data: {e}")

    return Response({"message": "Data processed successfully"})

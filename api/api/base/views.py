from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import UserSerializers 

@api_view(['GET', 'POST'])  # Allow both GET and POST requests
def getData(request):
    if request.method == 'GET':
        # Retrieve and return existing data
        data = User.objects.all()
        serializers = UserSerializers(data, many=True)
        return Response(serializers.data)

    elif request.method == 'POST':
        # Create a new data entry
        serializers = UserSerializers(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
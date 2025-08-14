from rest_framework.generics import ListAPIView
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import AllowAny
from .models import IPO
from .serializers import IPOSerializer

class IPOListAPIView(ListAPIView):
    queryset = IPO.objects.all().order_by('-listing_date')
    serializer_class = IPOSerializer
    authentication_classes = [SessionAuthentication]
    permission_classes = [AllowAny]  # Allow public API access

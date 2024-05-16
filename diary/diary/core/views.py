from django.utils import timezone
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from diary.core.models import Entry
from diary.core.serializers import (
    EntryListSerializer,
    EntryDetailSerializer,
)

class EntryViewSet (ModelViewSet):
    
    """CRUD for a diary entry"""
    
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == "list":
            return EntryListSerializer
        return EntryDetailSerializer

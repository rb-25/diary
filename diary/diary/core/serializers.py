from rest_framework import serializers
from diary.core.models import Entry

class EntryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Entry
        fields = ['id','title','created_at','user']

class EntryDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Entry
        fields = "__all__"
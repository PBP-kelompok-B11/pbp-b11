# vidia_event/serializers.py
from rest_framework import serializers
from .models import Event

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = [
            'id',
            'nama_event',
            'lokasi',
            'tanggal',
            'tim_home',
            'tim_away',
            'logo_home',
            'logo_away',
        ]

from rest_framework import serializers
from .models import Team, Board, List, Card


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ("id", "name", "members")

class BoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = ("id", "name", "priority", "team", "is_active")

class ListSerializer(serializers.ModelSerializer):
    class Meta:
        model = List
        fields = ("id", "name", "board", "is_active")

class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = ("id", "title", "due_date", "created_by", "list", "is_active")

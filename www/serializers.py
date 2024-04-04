from django.shortcuts import get_object_or_404
from rest_framework import serializers
from django.utils import timezone
from better_profanity import profanity
from . import models


class StatusSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField(max_length=50)


class TaskRequestSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField(max_length=50)
    description = serializers.CharField(max_length=255)
    status = StatusSerializer(required=False)
    creation_data = serializers.DateTimeField()
    completion_data = serializers.DateTimeField()


class TaskResponseSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=50)
    description = serializers.CharField(max_length=255)
    status = serializers.IntegerField(write_only=True)

    def create(self, validated_data):
        status_id = validated_data.pop('status')
        status = models.Status.objects.get(id=status_id)
        return models.Task.objects.create(status=status, **validated_data)

    def update(self, instance, validated_data):
        status_id = validated_data.pop('status')
        status = get_object_or_404(models.Status, pk=status_id)
        instance.title = validated_data['title']
        instance.description = validated_data['description']
        instance.status = status
        if status_id == 2:
            instance.completion_data = timezone.now()
        instance.save()
        return instance

    @staticmethod
    def validate_title(value):
        if profanity.contains_profanity(value):
            raise serializers.ValidationError('The value must not contain inappropriate words')
        return value

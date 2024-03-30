from rest_framework import serializers
from django.utils import timezone
from better_profanity import profanity
from . import models


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Task
        fields = '__all__'
        read_only_field = ['id']

    def update(self, instance, validated_data):
        new_status = validated_data['status']
        if new_status == 2:
            instance.completion_data = timezone.now()
        instance.save()
        return instance

    @staticmethod
    def validate_title(value):
        if profanity.contains_profanity(value):
            raise serializers.ValidationError('The value must not contain inappropriate words')
        return value


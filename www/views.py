from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.shortcuts import get_object_or_404
from . import models, serializers


class TaskAPIView(APIView):
    pagination_class = PageNumberPagination
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):
        if pk is not None:
            task = get_object_or_404(models.Task, pk=pk)
            serializer = serializers.TaskSerializer(task)
            return Response(serializer.data)

        paginator = self.pagination_class()
        tasks = models.Task.objects.all()
        result_page = paginator.paginate_queryset(tasks, request)
        serializer = serializers.TaskSerializer(tasks, many=True)
        if tasks.exists():
            return paginator.get_paginated_response(serializer.data)
        return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)

    @staticmethod
    def post(request):
        serializer = serializers.TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def put(request, pk):
        task = get_object_or_404(models.Task, pk=pk)
        serializer = serializers.TaskSerializer(task, request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def delete(request, pk):
        task = get_object_or_404(models.Task, pk=pk)
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

from django.db import models


class Status(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Task(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    status = models.ForeignKey(Status, on_delete=models.DO_NOTHING)
    creation_data = models.DateTimeField(auto_now=True)
    completion_data = models.DateTimeField(null=True)

    def __str__(self):
        return self.title

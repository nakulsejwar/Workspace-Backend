from django.conf import settings
from django.db import models

User = settings.AUTH_USER_MODEL

class Project(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    owner = models.ForeignKey(
        User, related_name="owned_projects", on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Workspace(models.Model):
    project = models.ForeignKey(
        Project, related_name="workspaces", on_delete=models.CASCADE
    )
    name = models.CharField(max_length=255)

    owners = models.ManyToManyField(
        User, related_name="owned_workspaces", blank=True
    )
    collaborators = models.ManyToManyField(
        User, related_name="collaborated_workspaces", blank=True
    )
    viewers = models.ManyToManyField(
        User, related_name="viewed_workspaces", blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.project.name} - {self.name}"

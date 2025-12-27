from rest_framework import viewsets, permissions
from .models import Project, Workspace
from .serializers import ProjectSerializer, WorkspaceSerializer


class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # ✅ Fix for Swagger / drf-yasg schema generation
        if getattr(self, "swagger_fake_view", False):
            return Project.objects.none()

        return Project.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class WorkspaceViewSet(viewsets.ModelViewSet):
    serializer_class = WorkspaceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # ✅ Fix for Swagger / drf-yasg schema generation
        if getattr(self, "swagger_fake_view", False):
            return Workspace.objects.none()

        return Workspace.objects.filter(
            project__owner=self.request.user
        )

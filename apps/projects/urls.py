from rest_framework.routers import DefaultRouter
from .views import ProjectViewSet, WorkspaceViewSet

router = DefaultRouter()
router.register("projects", ProjectViewSet, basename="projects")
router.register("workspaces", WorkspaceViewSet, basename="workspaces")

urlpatterns = router.urls

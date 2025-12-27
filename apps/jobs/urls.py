from django.urls import path
from .views import JobSubmitView, test_celery

urlpatterns = [
    path("submit/", JobSubmitView.as_view(), name="job_submit"),
    path("test-celery/", test_celery),
]
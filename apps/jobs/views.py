from rest_framework.views import APIView
from rest_framework.response import Response
from .tasks import process_code_execution

class JobSubmitView(APIView):
    def post(self, request):
        code = request.data.get("code")
        # In a real app, you'd save a 'Job' model instance here first
        job_id = "job_123" 
        
        # Push to Celery
        process_code_execution.delay(job_id, code)
        
        return Response({"message": "Job queued", "job_id": job_id}, status=202)
    

from rest_framework.decorators import api_view
from rest_framework.response import Response
import uuid

from apps.jobs.tasks import process_code_execution


@api_view(["POST"])
def test_celery(request):
    # Generate a job ID
    job_id = str(uuid.uuid4())

    code_payload = {
        "language": "js",
        "code": "console.log('hello from api')"
    }

    # ✅ PASS BOTH REQUIRED ARGUMENTS
    process_code_execution.delay(job_id, code_payload)

    return Response({
        "status": "task queued",
        "job_id": job_id
    })

from datetime import datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny


class StatusView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        now = datetime.now()
        return Response({
            "status": "success",
            "data": now.isoformat()
        })

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import requests

# Create your views here.
class AdminSignupView(APIView):
    def post(self, request):
        backend_url = "https://toepwar.onrender.com/admin/signup"  # Backend signup endpoint
        response = requests.post(backend_url, json=request.data)
        if response.status_code == 200:
            return Response(response.json(), status=status.HTTP_200_OK)
        return Response(response.json(), status=response.status_code)
    
class LoginView(APIView):
    def post(self, request):
        backend_url = "https://toepwar.onrender.com/admin/login"  # Update with your backend login endpoint
        response = requests.post(backend_url, data=request.data)
        if response.status_code == 200:
            return Response(response.json(), status=status.HTTP_200_OK)
        return Response(response.json(), status=response.status_code)
    
class UserListView(APIView):
    def get(self, request):
        backend_url = "https://toepwar.onrender.com/admin/users"  # Update with your backend endpoint
        token = request.headers.get('Authorization')
        headers = {"Authorization": token}
        response = requests.get(backend_url, headers=headers)
        if response.status_code == 200:
            return Response(response.json(), status=status.HTTP_200_OK)
        return Response(response.json(), status=response.status_code)
    
class UserDetailView(APIView):
    def get(self, request, user_id):
        backend_url = f"https://toepwar.onrender.com/admin/users/{user_id}"
        token = request.headers.get('Authorization')
        headers = {"Authorization": token}
        response = requests.get(backend_url, headers=headers)
        if response.status_code == 200:
            return Response(response.json(), status=status.HTTP_200_OK)
        return Response(response.json(), status=response.status_code)

class UpdateUserStatusView(APIView):
    def put(self, request, user_id):
        backend_url = f"https://toepwar.onrender.com/admin/users/{user_id}/status"
        token = request.headers.get('Authorization')
        headers = {"Authorization": token}
        response = requests.put(backend_url, json=request.data, headers=headers)
        if response.status_code == 200:
            return Response(response.json(), status=status.HTTP_200_OK)
        return Response(response.json(), status=response.status_code)

class DeleteUserView(APIView):
    def delete(self, request, user_id):
        backend_url = f"https://toepwar.onrender.com/admin/users/{user_id}"
        token = request.headers.get('Authorization')
        headers = {"Authorization": token}
        response = requests.delete(backend_url, headers=headers)
        if response.status_code == 200:
            return Response(response.json(), status=status.HTTP_200_OK)
        return Response(response.json(), status=response.status_code)


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth.decorators import login_required
import requests

# Base URL for the backend API
BACKEND_URL = "https://toepwar.onrender.com/admin"


# Helper function to handle token retrieval
def get_auth_headers(request):
    token = request.headers.get("Authorization")
    if not token:
        raise ValueError("Authorization token is missing.")
    return {"Authorization": token}


# Admin Signup View
class AdminSignupView(APIView):
    def post(self, request):
        backend_url = f"{BACKEND_URL}/signup"
        response = requests.post(backend_url, json=request.data)
        if response.status_code == 200:
            return Response(response.json(), status=status.HTTP_200_OK)
        return Response(response.json(), status=response.status_code)


# Admin Login View
class LoginView(APIView):
    def post(self, request):
        backend_url = f"{BACKEND_URL}/login"
        response = requests.post(backend_url, json=request.data)
        if response.status_code == 200:
            return Response(response.json(), status=status.HTTP_200_OK)
        return Response(response.json(), status=response.status_code)


# User List View
class UserListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            headers = get_auth_headers(request)
            backend_url = f"{BACKEND_URL}/users"
            response = requests.get(backend_url, headers=headers)
            if response.status_code == 200:
                return Response(response.json(), status=status.HTTP_200_OK)
            return Response(response.json(), status=response.status_code)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


# User Detail View
class UserDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        try:
            headers = get_auth_headers(request)
            backend_url = f"{BACKEND_URL}/users/{user_id}"
            response = requests.get(backend_url, headers=headers)
            if response.status_code == 200:
                return Response(response.json(), status=status.HTTP_200_OK)
            return Response(response.json(), status=response.status_code)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


# Update User Status View
class UpdateUserStatusView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, user_id):
        try:
            headers = get_auth_headers(request)
            backend_url = f"{BACKEND_URL}/users/{user_id}/status"
            response = requests.put(backend_url, json=request.data, headers=headers)
            if response.status_code == 200:
                return Response(response.json(), status=status.HTTP_200_OK)
            return Response(response.json(), status=response.status_code)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


# Delete User View
class DeleteUserView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, user_id):
        try:
            headers = get_auth_headers(request)
            backend_url = f"{BACKEND_URL}/users/{user_id}"
            response = requests.delete(backend_url, headers=headers)
            if response.status_code == 200:
                return Response({"message": "User deleted successfully."}, status=status.HTTP_200_OK)
            return Response(response.json(), status=response.status_code)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


# Ban User View
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def ban_user(request, user_id):
    try:
        if request.user.role != "super_admin":
            return Response({"error": "Permission denied."}, status=status.HTTP_403_FORBIDDEN)

        headers = get_auth_headers(request)
        backend_url = f"{BACKEND_URL}/users/{user_id}/status"
        response = requests.put(backend_url, json={"status": "banned"}, headers=headers)
        if response.status_code == 200:
            return Response({"message": "User banned successfully."}, status=status.HTTP_200_OK)
        return Response(response.json(), status=response.status_code)
    except ValueError as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

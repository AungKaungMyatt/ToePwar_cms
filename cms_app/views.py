from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q
from .models import CustomUser

# Base backend API URL
BACKEND_URL = "https://toepwar.onrender.com/admin"

# Pagination Class
class UserPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 50


# User List View with Pagination, Search, and Filter
class UserListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        search = request.query_params.get("search", "").strip()
        status_filter = request.query_params.get("status", "").strip()
        page = request.query_params.get("page", 1)

        users = CustomUser.objects.all()
        if search:
            users = users.filter(Q(email__icontains=search) | Q(username__icontains=search))
        if status_filter:
            if status_filter == "active":
                users = users.filter(is_active=True)
            elif status_filter == "banned":
                users = users.filter(is_active=False)

        paginator = UserPagination()
        result_page = paginator.paginate_queryset(users, request)
        return paginator.get_paginated_response([
            {
                "id": user.id,
                "email": user.email,
                "username": user.username,
                "status": "active" if user.is_active else "banned",
                "created_at": user.date_joined,
            }
            for user in result_page
        ])

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


# User List View with Pagination, Search, and Filter
class UserListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        token = request.headers.get("Authorization")
        if not token:
            return Response({"error": "Authorization token missing."}, status=status.HTTP_401_UNAUTHORIZED)

        headers = {"Authorization": token}

        # Extract search, filter, and pagination parameters from the request
        search = request.query_params.get("search", "")
        status_filter = request.query_params.get("status", "")
        page = request.query_params.get("page", 1)

        backend_url = f"{BACKEND_URL}/users"
        params = {
            "search": search,
            "status": status_filter,
            "page": page,
        }

        try:
            # Send GET request to the backend
            response = requests.get(backend_url, headers=headers, params=params)
            if response.status_code == 200:
                return Response(response.json(), status=status.HTTP_200_OK)
            return Response(response.json(), status=response.status_code)
        except Exception as e:
            print("Error:", str(e))
            return Response({"error": "Failed to fetch users."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# User Detail View
class UserDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        token = request.headers.get("Authorization")
        if not token:
            return Response({"error": "Authorization token missing."}, status=status.HTTP_401_UNAUTHORIZED)

        headers = {"Authorization": token}
        backend_url = f"{BACKEND_URL}/users/{user_id}"

        try:
            response = requests.get(backend_url, headers=headers)
            if response.status_code == 200:
                return Response(response.json(), status=status.HTTP_200_OK)
            return Response(response.json(), status=response.status_code)
        except Exception as e:
            print("Error:", str(e))
            return Response({"error": "Failed to fetch user details."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Update User Status View
class UpdateUserStatusView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, user_id):
        token = request.headers.get("Authorization")
        if not token:
            return Response({"error": "Authorization token missing."}, status=status.HTTP_401_UNAUTHORIZED)

        headers = {"Authorization": token}
        backend_url = f"{BACKEND_URL}/users/{user_id}/status"

        try:
            response = requests.put(backend_url, json=request.data, headers=headers)
            if response.status_code == 200:
                return Response({"message": "User status updated successfully."}, status=status.HTTP_200_OK)
            return Response(response.json(), status=response.status_code)
        except Exception as e:
            print("Error:", str(e))
            return Response({"error": "Failed to update user status."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Delete User View
class DeleteUserView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, user_id):
        token = request.headers.get("Authorization")
        if not token:
            return Response({"error": "Authorization token missing."}, status=status.HTTP_401_UNAUTHORIZED)

        headers = {"Authorization": token}
        backend_url = f"{BACKEND_URL}/users/{user_id}"

        try:
            response = requests.delete(backend_url, headers=headers)
            if response.status_code == 200:
                return Response({"message": "User deleted successfully."}, status=status.HTTP_200_OK)
            return Response(response.json(), status=response.status_code)
        except Exception as e:
            print("Error:", str(e))
            return Response({"error": "Failed to delete user."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

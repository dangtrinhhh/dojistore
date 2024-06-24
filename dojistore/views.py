# views.py
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import redirect
from django.contrib import messages

class CustomTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        try:
            response = super().post(request, *args, **kwargs)
            return response
        except TokenError as e:
            if str(e) == 'Token is invalid or expired':
                messages.error(request, "Phiên đã hết hạn, vui lòng đăng nhập lại.")
                return redirect('/logout')
            return Response({'detail': str(e)}, status=status.HTTP_401_UNAUTHORIZED)

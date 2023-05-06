import os

from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.views import APIView, Response
from rest_framework_simplejwt.tokens import RefreshToken

from apps.Auth.jwttoken import get_tokens_for_user
from apps.Auth.messages import *
from apps.Auth.models import User
from apps.Auth.serializers import (ChangePasswordSerializer,
                                   UpdateUserSerializer, UserSerializer)
from utils.email import send_email, send_verification_email
from utils.generatetoken import ActivationTokenGenerator

FRONTEND_URL = os.getenv("FRONT_URL")


# Create your views here.
class Login(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email", None)
        password = request.data.get("password", None)
        if email is None or password is None:
            return Response(
                {"msg": EMAIL_PASSWORD_REQUIRED},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            user = User.objects.get(email=email)
        except:
            return Response(
                {"msg": USER_NOT_VALID},
                status=status.HTTP_400_BAD_REQUEST,
            )
        else:
            if not user.is_verified:
                return Response(
                    {"msg": USER_NOT_VERIFIED},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            if user.check_password(password):
                token = get_tokens_for_user(user)
                return Response(
                    {
                        "msg": SUCCESS_LOGIN,
                        "refresh": token["refresh"],
                        "access": token["access"],
                    },
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {"msg": USER_NOT_VALID},
                    status=status.HTTP_400_BAD_REQUEST,
                )


class Register(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email", None)
        password = request.data.get("password", None)
        if email is None or password is None:
            return Response(
                {"msg": EMAIL_PASSWORD_REQUIRED},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            user = User.objects.get(email=email)
        except:
            user = User.objects.create(email=email)
            user.set_password(password)
            user.save()
            id = urlsafe_base64_encode(force_bytes(user.pk))
            send_verification_email(user.email, id)
            return Response(
                {"msg": SUCCESS_REGISTER},
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(
                {"msg": USER_ALREADY_EXISTS},
                status=status.HTTP_400_BAD_REQUEST,
            )


class VerifyUser(APIView):
    permission_classes = [AllowAny]
    renderer_classes = [TemplateHTMLRenderer]

    def get(self, request):
        is_verified = False
        message = "User not valid"
        user_id = request.query_params.get("id", None)
        if user_id is None:
            return Response(
                {
                    "message": message,
                    "verified": is_verified,
                },
                template_name="auth/verify_user.html",
            )

        # get the user and verify
        try:
            id = force_str(urlsafe_base64_decode(user_id))
            user = User.objects.get(id=id)
        except:
            return Response(
                {
                    "message": message,
                    "verified": is_verified,
                },
                template_name="auth/verify_user.html",
            )
        message = "User Verified"
        is_verified = True
        user.is_verified = is_verified
        user.save()
        return Response(
            {
                "message": message,
                "verified": is_verified,
                "url": f"{FRONTEND_URL}/sign-in",
                "button_txt": "Back to Sign In",
            },
            template_name="auth/verify_user.html",
        )


class ViewAll(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        data = serializer.data
        return Response(data, status=status.HTTP_200_OK)


class Logout(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(
                {"msg": LOGGED_OUT},
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class ViewUser(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        current_user = request.user
        if current_user.id != user_id:
            return Response(
                {"msg": "User not Verified"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        serializer = UserSerializer(current_user)
        data = serializer.data
        return Response(data, status=status.HTTP_200_OK)


class ResetPassword(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email", None)
        new_password = request.data.get("new_password", None)
        if email is None or new_password is None:
            return Response(
                {
                    "msg": EMAIL_PASSWORD_REQUIRED,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        users = list(User.objects.filter(email=email))
        if users:
            user = users[0]
            token = ActivationTokenGenerator()
            token_key = token.make_token(user)
            id = urlsafe_base64_encode(force_bytes(user.pk))
            encoded_password = urlsafe_base64_encode(force_bytes(new_password))
            send_email(token_key, user.email, id, encoded_password)
            return Response(
                {
                    "msg": "Email Send Successfully",
                },
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {
                    "msg": USER_NOT_EXIST,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )


class ResetPasswordHandler(APIView):
    permission_classes = [AllowAny]
    renderer_classes = [TemplateHTMLRenderer]

    def get(self, request):
        reset_code = request.query_params.get("code", None)
        user_id = request.query_params.get("id", None)
        encoded_password = request.query_params.get("pass", None)
        message = "Code Not Valid"
        is_verified = False
        if reset_code is None or user_id is None or encoded_password is None:
            return Response(
                {
                    "message": message,
                    "verified": is_verified,
                },
                template_name="auth/verify_user.html",
            )

        # get the password and reset it
        try:
            id = force_str(urlsafe_base64_decode(user_id))
            new_password = force_str(urlsafe_base64_decode(encoded_password))
            user = User.objects.get(id=id)
        except:
            return Response(
                {
                    "message": message,
                    "verified": is_verified,
                },
                template_name="auth/verify_user.html",
            )
        token = ActivationTokenGenerator()
        if token.check_token(user, reset_code):
            user.set_password(new_password)
            user.save()
            message = "Password Changed Successfully"
            is_verified = True
            return Response(
                {
                    "message": message,
                    "verified": is_verified,
                    "url": f"{FRONTEND_URL}/sign-in",
                    "button_txt": "Back to Sign In",
                },
                template_name="auth/verify_user.html",
            )
        return Response(
            {
                "message": message,
                "verified": is_verified,
            },
            template_name="auth/verify_user.html",
        )


class ChangePassword(generics.UpdateAPIView):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = ChangePasswordSerializer

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(
            {
                "msg": "Password Updated Successfully",
            },
            status=status.HTTP_200_OK,
        )


class UpdateUser(generics.UpdateAPIView):
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = UpdateUserSerializer

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(
            {
                "msg": "An email sent for verification of this email",
            },
            status=status.HTTP_200_OK,
        )

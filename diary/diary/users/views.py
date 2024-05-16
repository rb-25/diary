from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView
from django.views.generic import RedirectView
from django.views.generic import UpdateView

from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken

from diary.users.models import User
from diary.users.api.serializers import UserSerializer

class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    slug_field = "id"
    slug_url_kwarg = "id"


user_detail_view = UserDetailView.as_view()


class UserUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = User
    fields = ["name"]
    success_message = _("Information successfully updated")

    def get_success_url(self):
        # for mypy to know that the user is authenticated
        assert self.request.user.is_authenticated
        return self.request.user.get_absolute_url()

    def get_object(self):
        return self.request.user


user_update_view = UserUpdateView.as_view()


class UserRedirectView(LoginRequiredMixin, RedirectView):
    permanent = False

    def get_redirect_url(self):
        return reverse("users:detail", kwargs={"pk": self.request.user.pk})


user_redirect_view = UserRedirectView.as_view()

class RegisterView(APIView):
    
    """ View to register users """
    
    permission_classes = [AllowAny]
    def post(self, request):
        serializer=UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    def get(self,request):
        serializer = UserSerializer(User.objects.all(), many=True)
        return Response(serializer.data)

class LoginView(APIView):
    
    """View for users to login"""
    
    permission_classes = []
    authentication_classes = []

    @staticmethod
    def post(request):
        email = request.data.get("email")
        password = request.data.get("password")
        username= request.data.get("username")
        
        if not username:
            if not email or not password:
                return Response(
                    {"detail": "Email and password are required."},
                    status=HTTPStatus.BAD_REQUEST,
                )

            user = get_object_or_404(User, email=email)
        elif not email:
            if not username or not password:
                return Response(
                    {"detail": "Username and password are required."},
                    status=HTTPStatus.BAD_REQUEST,
                )

            user = get_object_or_404(User, username=username)
        else:
            user=get_object_or_404(User,email=email)

        if not user.check_password(password):
            return Response(
                {"detail": "Incorrect password."}, status=HTTPStatus.BAD_REQUEST
            )


        # Generate JWT refresh token for the user
        refresh_token = RefreshToken.for_user(user)

        serializer = UserSerializer(user)
        print("Serializer Data:", serializer.data)
        serializer.access_token = refresh_token.access_token
        serializer.refresh_token = str(refresh_token)
        
        response={}
        for key in serializer.data:
            response[key]=serializer.data[key]
        response["access_token"]=str(refresh_token.access_token)
        response["refresh_token"]=str(refresh_token)
        return Response(
            {
                "data":response
                
            },
            status=HTTPStatus.OK,
        )
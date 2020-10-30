
from rest_framework import status
from rest_framework import permissions
from rest_framework.generics import CreateAPIView, GenericAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework_simplejwt.views import TokenObtainPairView

from .renderers import UserJSONRenderer
from .serializers import UserRegistrationSerializer, UserLoginSerializer#, ObtainTokenSerializer
from users.models import CustomUser


class UserRegistrationAPIView(CreateAPIView):
	authentication_classes = ()
	permission_classes = ()
	# renderer_classes = (UserJSONRenderer, )
	serializer_class = UserRegistrationSerializer
	
	def create(self, request, *args, **kwargs):
		serializer = self.get_serializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		self.perform_create(serializer)

		user = serializer.instance
		data = serializer.data

		headers = self.get_success_headers(serializer.data)

		return Response(data, status=status.HTTP_201_CREATED, headers=headers)

# class UserRegistrationAPIView(CreateAPIView):
#     permission_classes = (permissions.AllowAny,)
#     authentication_classes = ()
#     serializer_class = UserRegistrationSerializer


user_create = UserRegistrationAPIView.as_view()


from rest_framework_simplejwt.tokens import RefreshToken
class UserLoginAPIView(GenericAPIView):
    authentication_classes = ()
    permission_classes = (permissions.AllowAny,)
    # renderer_classes = (UserJSONRenderer, )
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
        	# token = RefreshToken.for_user(serializer.data.email)
        	print(serializer.data)
        	return Response(
                data=serializer.data,
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                data=serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )

user_login = UserLoginAPIView.as_view()


# class TokenObtainView(TokenObtainPairView):
#     serializer_class = ObtainTokenSerializer


class ProtectedView(APIView):
    def get(self, request):
        return Response(data={'type':'protected'})

protected = ProtectedView.as_view()
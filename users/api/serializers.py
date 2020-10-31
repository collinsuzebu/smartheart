from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers


from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


User = get_user_model()

class UserRegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    first_name = serializers.CharField(min_length=2, required=True)
    last_name = serializers.CharField(min_length=2, required=True)
    password = serializers.CharField(min_length=8, write_only=True)
    confirm_password = serializers.CharField(min_length=8, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)


    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'password', 'confirm_password', 'token')

    def validate(self, attrs):

        user = User.objects.filter(email=attrs.get("email"))

        if user:
            raise serializers.ValidationError("email address has already been taken")

        if attrs.get('password') != attrs.get('confirm_password'):
            raise serializers.ValidationError("password does not match")
        del attrs['confirm_password']

        return attrs
    
    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)

        if password is not None:
            instance.set_password(password)
        
        instance.save()

        return instance



class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    default_error_messages = {
        'inactive_account': _('User account is disabled.'),
        'invalid_credentials': _('Incorrect email or password.')
    }

    class Meta:
        model = User
        fields = ['email', 'password', 'token']

    def __init__(self, *args, **kwargs):
        super(UserLoginSerializer, self).__init__(*args, **kwargs)
        self.user = None

    def validate(self, attrs):
        self.user = authenticate(username=attrs.get("email"), password=attrs.get('password'))

        if self.user:
            if not self.user.is_active:
                raise serializers.ValidationError(self.error_messages['inactive_account'])
            

            return {
            
                "email": self.user.email,
                "password": self.user.password,
                "token": self.user.token,
            }

        else:
            raise serializers.ValidationError(self.error_messages['invalid_credentials'])





# class ObtainTokenSerializer(TokenObtainPairSerializer):
#     def validate(self, attrs):
#         data = super().validate(attrs)
#         refresh = self.get_token(self.user)
#         data['refresh'] = str(refresh)
#         data['access'] = str(refresh.access_token)

#         data['email'] = self.user.email
#         return data
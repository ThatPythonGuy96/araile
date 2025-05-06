from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from . import models

class LoginTokenSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, account):
        token = super().get_token(account)
        token['email'] = account.email
        return token
        
    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        try:
            account = models.Account.objects.get(email=email)
            if not account.check_password(password):
                raise serializers.ValidationError({"error": "Incorrect Password."})
        except models.Account.DoesNotExist:
            raise serializers.ValidationError({"error": "No Account Found with given credentials"})
        data = super().validate(attrs)
        data['email'] = account.email
        return data
    
class SignupSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True, validators=[UniqueValidator(queryset=models.Account.objects.all())])
    password1 = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = models.Account
        fields = ('email', 'password1', 'password2')

    def validate(self, attrs):
        if attrs['password1'] != attrs['password2']:
            raise serializers.ValidationError({"error": "Password fields don't match."})
        return attrs
    
    def create(self, validated_data):
        account = models.Account.objects.create(
            email=validated_data['email'],
        )
        account.set_password(validated_data['password1'])
        account.save()
        return account
    
class UpdateAccountSerializer(serializers.ModelSerializer):
    profile_picture = serializers.ImageField(required=False)
    email = serializers.EmailField(required=False)
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)

    class Meta:
        model = models.Account
        fields = ('email', 'profile_picture', 'first_name', 'last_name')

    def validate(self, data):
        request = self.context.get('request')
        data["email_sent"] = "email" in request.data
        data["profile_picture_sent"] = "profile_picture" in request.data
        data["first_name_sent"] = "first_name" in request.data
        data["last_name_sent"] = "last_name" in request.data
        return data

    def update(self, instance, validated_data):
        email_sent = validated_data.pop("email_sent", False)
        profile_picture_sent = validated_data.pop("profile_picture_sent", False)
        first_name_sent = validated_data.pop("first_name_sent", False)
        last_name_sent = validated_data.pop("last_name_sent", False)

        if email_sent:
            new_email = validated_data.get('email')
            if new_email and new_email != instance.email:
                instance.email = new_email

        if first_name_sent:
            new_first_name = validated_data.get('first_name')
            if new_first_name and new_first_name != instance.first_name:
                instance.first_name = new_first_name

        if last_name_sent:
            new_last_name = validated_data.get('last_name')
            if new_last_name and new_last_name != instance.last_name:
                instance.last_name = new_last_name

        if profile_picture_sent:
            new_profile_picture = validated_data.get('profile_picture')
            instance.profile_picture = new_profile_picture

        instance.save()
        return instance
    
class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True, required=True)
    new_password1 = serializers.CharField(write_only=True, required=True)
    new_password2 = serializers.CharField(write_only=True, required=True)

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError({"error": "Old Password is Incorrect."})
        return value
    
    def validate_new_password(self, value):
        if self.new_password1 != self.new_password2:
            raise serializers.ValidationError({"error": "Password fields don't match."})
        if self.old_password == self.new_password1:
            raise serializers.ValidationError({"error": "New Password can not be the same as old Password."})
        return value

class PasswordResetSerializers(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        if not models.Account.objects.filter(email=value).exists():
            raise serializers.ValidationError({"error": "Account with this email does not exist."})
        return value
    
class PasswordResetConfirmSerializers(serializers.Serializer):
    token = serializers.CharField()
    email = serializers.EmailField()
    new_password = serializers.CharField(write_only=True)

    def validate(self, data):
        try:
            account = models.Account.objects.get(email=data['email'])
        except models.Account.DoesNotExist:
            raise serializers.ValidationError("Account does not exist.")
        
        if not PasswordResetTokenGenerator().check_token(account, data['token']):
            raise serializers.ValidationError("Invalid or Expired Token")
        
        return data
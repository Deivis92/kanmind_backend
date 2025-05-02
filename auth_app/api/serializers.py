from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


class RegisterSerializer(serializers.ModelSerializer):
    repeated_password = serializers.CharField(write_only=True)
    fullname = serializers.CharField(write_only=True) 


    class Meta:

        model = User
        fields = ['fullname', 'email', 'password', 'repeated_password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, data):
        if data['password'] != data['repeated_password']:
            raise serializers.ValidationError({'password': 'Passwords do not match'}) 
        return data   
    
    def create(self, validated_data):
        fullname = validated_data.pop('fullname', '')
        validated_data.pop('repeated_password')

        if 'username' not in validated_data:
            validated_data['username'] = self.generate_username_from_fullname(fullname)

        user = User.objects.create_user(**validated_data)
        Token.objects.create(user=user)
        return user
    
    def generate_username_from_fullname(self, fullname):
        username = fullname.split()[0].lower()  
        return username
    
    
    
class UserListSerializer(serializers.ModelSerializer):
        class Meta:
            model = User
            fields = ['id', 'username', 'email', 'password']
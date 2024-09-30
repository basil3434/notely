from rest_framework import serializers
from notes.models import User,Task

class UserSerializer(serializers.ModelSerializer):

    password1=serializers.CharField(write_only=True)
    password2=serializers.CharField(write_only=True)
    password=serializers.CharField(read_only=True)

    class Meta:
        model=User
        fields=["id", "username", "email", "password1", "phone","password2","password"]

    def create(self, validate_data):                        # method overriding so that the password is encrypted
        password1=validate_data.pop("password1")
        password2=validate_data.pop("password2")

        return User.objects.create_user(**validate_data,password=password1)
    
    def validate(self, data):
        if data["password1"] != data["password2"]:
            raise serializers.ValidationError({"password mismatch"})
        return data
        
class TaskSerializer(serializers.ModelSerializer):
    

    class Meta:
        model=Task
        fields="__all__"
        read_only_fields=["id","created_data","owner","is_active"]
from rest_framework.serializers import ModelSerializer


from .models import User

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = (
            'email', 'full_name', 'gaards_number', 'bruks_number', 'municipality'
        )
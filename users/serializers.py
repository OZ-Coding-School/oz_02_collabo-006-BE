from rest_framework.serializers import ModelSerializer
from users.models import User
from rest_framework import serializers
from django.contrib.auth import authenticate

# (1) 전체 데이터를 다 보여주는 Serialize
class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
        # 현재의 모델과 연결된 모델들까지 serialize 시키겠다는 뜻        
        # Feed - User 모델 => 현재 코드는 Feed 모델 객체를 직렬화 하고 있지만,
        # depth = 1 이라는 코드를 통해 User 객체도 직렬화하겠다는 뜻.
        depth = 1 # objects도 serialize화 시킴

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("이메일이 이미 사용 중입니다.")
        return value

    def validate_phone(self, value):
        if User.objects.filter(phone=value).exists():
            raise serializers.ValidationError("휴대폰 번호가 이미 사용 중입니다.")
        return value

    def validate_referrer(self, value):
        if value and not User.objects.filter(username=value).exists():
            raise serializers.ValidationError("유효하지 않은 추천인입니다.")
        return value




class UserDetailSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["id","username","phone","referrer","email","profile_image","subscription","status","created_at","updated_at"]
        # If you need to make email and profile_image optional:
        extra_kwargs = {
            'email': {'required': False, 'allow_blank': True},
            'profile_image': {'required': False, 'allow_null': True}
        }

    def to_representation(self, instance):
        """ Modify the output format, if necessary, to display specific formats of fields """
        ret = super().to_representation(instance)
        # Here you can further customize the output if needed, such as formatting dates
        return ret


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id","username","phone","referrer","email","profile_image","subscription","status","created_at","updated_at"]
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def update(self, instance, validated_data):
        print(instance)
        instance.username = validated_data.get('username', instance.username)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.email = validated_data.get('email', instance.email)
        instance.subscription = validated_data.get('subscription', instance.subscription)
        instance.status = validated_data.get('status', instance.status)
        instance.profile_image = validated_data.get('profile_image', instance.profile_image)
        
        if 'password' in validated_data:
            password = validated_data.get('password', instance.password)
            instance.set_password(password)

        instance.save()
        return instance




# class UserUpdateSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ['username', 'phone', 'email', 'subscription', 'status', 'profile_image']

#     def update(self, instance, validated_data):
#         instance.username = validated_data.get('username', instance.username)
#         instance.phone = validated_data.get('phone', instance.phone)
#         instance.email = validated_data.get('email', instance.email)
#         instance.subscription = validated_data.get('subscription', instance.subscription)
#         instance.status = validated_data.get('status', instance.status)
#         instance.profile_image = validated_data.get('profile_image', instance.profile_image)
#         if 'password' in validated_data:
#             instance.set_password(validated_data['password'])
#         instance.save()
#         return instance


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')
        user = authenticate(username=username, password=password)

        if user is None:
            raise serializers.ValidationError("잘못된 사용자명 또는 비밀번호.")

        if not user.is_active:
            raise serializers.ValidationError("계정 비활성화.")

        data['user'] = user
        return data




# serializers.py

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        # Add custom claims
        data['username'] = self.user.username
        data['is_staff'] = self.user.is_staff
        return data

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

from rest_framework import serializers
from .models import UsuarioPersonalizado
from .validators import CustomUserdValidator

class UsuarioPersonalizadoSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = UsuarioPersonalizado
        fields = ['id', 'first_name', 'last_name', 'email', 'password', 'tipo_usuario']
        extra_kwargs = {
            'tipo_usuario': {'read_only': True}
        }

    def validate(self, data):
        # Validaciones personalizadas
        nombre = data.get('first_name')
        apellido = data.get('last_name')
        email = data.get('email')
        password = data.get('password')

        error = CustomUserdValidator.validar_email_campos_llenos(nombre, apellido, email, password) 
        if error:
            raise serializers.ValidationError(error)

        error = CustomUserdValidator.validar_nombre_apellido(nombre, apellido)
        if error:
            raise serializers.ValidationError(error)

        error = CustomUserdValidator.validar_email(email)
        if error:
            raise serializers.ValidationError(error)

        error = CustomUserdValidator.validar_contrasena(password)
        if error:
            raise serializers.ValidationError(error)

        error = CustomUserdValidator.validar_email_existente(email)
        if error:
            raise serializers.ValidationError(error)
        
        return data

    def create(self, validated_data):
        password = validated_data.pop('password')

        user = UsuarioPersonalizado.objects.create(
            username=validated_data['email'].split('@')[0],
            tipo_usuario='residente',
            **validated_data
        )
        user.set_password(password)
        user.save()
        return user

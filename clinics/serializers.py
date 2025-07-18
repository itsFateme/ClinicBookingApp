# clinics/serializers.py
from rest_framework import serializers
from .models import Clinic
from users.serializers import UserSerializer
from users.models import User

class ClinicSerializer(serializers.ModelSerializer):
    clinic_admin = UserSerializer(read_only=True)
    clinic_admin_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(role='clinic_admin'),
        source='clinic_admin',
        write_only=True,
        required=False,
        allow_null=True
    )

    class Meta:
        model = Clinic
        fields = ['id', 'name', 'address', 'phone_number', 'description', 'clinic_admin', 'clinic_admin_id']

    def create(self, validated_data):
        clinic_admin_id = validated_data.pop('clinic_admin_id', None)
        clinic = Clinic.objects.create(**validated_data)
        if clinic_admin_id:
            clinic.clinic_admin = clinic_admin_id
            clinic.save()
        return clinic

    def update(self, instance, validated_data):
        clinic_admin_id = validated_data.pop('clinic_admin_id', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if clinic_admin_id:
            instance.clinic_admin = clinic_admin_id
        instance.save()
        return instance
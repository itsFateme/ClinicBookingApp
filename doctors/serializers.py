from rest_framework import serializers
from .models import Doctor, DoctorAvailability
from users.models import User
from users.serializers import UserSerializer
from clinics.models import Clinic
from clinics.serializers import ClinicSerializer

class DoctorSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True) 
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(role='doctor'),
        source='user',
        write_only=True
    )
    clinic = ClinicSerializer(read_only=True)
    clinic_id = serializers.PrimaryKeyRelatedField(
        queryset=Clinic.objects.all(),
        source='clinic',
        write_only=True
    )

    class Meta:
        model = Doctor
        fields = ['user', 'user_id', 'clinic', 'clinic_id', 'specialty', 'bio', 'experience_years']

    def create(self, validated_data):
        user_id_data = validated_data.pop('user', None) 
        clinic_id_data = validated_data.pop('clinic', None) 

        if user_id_data:
            user_instance = user_id_data
            user_instance.is_staff = True
            user_instance.is_active = True
            user_instance.save(update_fields=['is_staff', 'is_active'])

        doctor = Doctor.objects.create(user=user_id_data, clinic=clinic_id_data, **validated_data)
        return doctor

    def update(self, instance, validated_data):
        user_id_data = validated_data.pop('user', None)
        clinic_id_data = validated_data.pop('clinic', None)

        if user_id_data:
            instance.user = user_id_data
        if clinic_id_data:
            instance.clinic = clinic_id_data

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class DoctorAvailabilitySerializer(serializers.ModelSerializer):
    doctor = DoctorSerializer(read_only=True)
    doctor_id = serializers.PrimaryKeyRelatedField(
        queryset=Doctor.objects.all(),
        source='doctor',
        write_only=True
    )

    class Meta:
        model = DoctorAvailability
        fields = ['id', 'doctor', 'doctor_id', 'date', 'start_time', 'end_time', 'slot_duration']
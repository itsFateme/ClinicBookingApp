from rest_framework import serializers
from .models import Service
from clinics.serializers import ClinicSerializer 
from doctors.serializers import DoctorSerializer  
from clinics.models import Clinic 
from doctors.models import Doctor

class ServiceSerializer(serializers.ModelSerializer):
    clinic = ClinicSerializer(read_only=True)
    clinic_id = serializers.PrimaryKeyRelatedField(
        queryset=Clinic.objects.all(),
        source='clinic',
        write_only=True
    )
    doctors = DoctorSerializer(many=True, read_only=True) 
    doctor_ids = serializers.PrimaryKeyRelatedField(
        queryset=Doctor.objects.all(),
        many=True, 
        source='doctors',
        write_only=True
    )

    class Meta:
        model = Service
        fields = ['id', 'name', 'description', 'price', 'clinic', 'clinic_id', 'doctors', 'doctor_ids']

    def create(self, validated_data):
        doctor_ids = validated_data.pop('doctors', []) 
        service = Service.objects.create(**validated_data)
        service.doctors.set(doctor_ids) 
        return service

    def update(self, instance, validated_data):
        doctor_ids = validated_data.pop('doctors', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if doctor_ids is not None:
            instance.doctors.set(doctor_ids)

        instance.save()
        return instance
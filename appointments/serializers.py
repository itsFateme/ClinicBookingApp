# appointments/serializers.py
from rest_framework import serializers
from .models import Appointment
from users.models import User
from doctors.models import Doctor, Clinic 


from users.serializers import UserSerializer
from doctors.serializers import DoctorSerializer
from clinics.serializers import ClinicSerializer


class AppointmentSerializer(serializers.ModelSerializer):

    patient = UserSerializer(read_only=True)
    doctor = DoctorSerializer(read_only=True)
    clinic = ClinicSerializer(read_only=True) 


    patient_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(role='patient'), 
        source='patient',
        write_only=True
    )
    doctor_id = serializers.PrimaryKeyRelatedField(
        queryset=Doctor.objects.all(),
        source='doctor',
        write_only=True
    )


    class Meta:
        model = Appointment
        fields = [
            'id', 'patient', 'patient_id', 'doctor', 'doctor_id', 'clinic',
            'date', 'start_time', 'end_time', 'status', 'notes', 'booking_timestamp'
        ]
        read_only_fields = ['status', 'booking_timestamp', 'clinic', 'end_time'] 
    def validate(self, data):

        doctor = data.get('doctor')
        date = data.get('date')
        start_time = data.get('start_time')


        if Appointment.objects.filter(doctor=doctor, date=date, start_time=start_time, status__in=['pending', 'confirmed']).exists():
            raise serializers.ValidationError("This doctor already has an appointment at this time.")


        from doctors.models import DoctorAvailability
        availability = DoctorAvailability.objects.filter(
            doctor=doctor,
            date=date,
            start_time__lte=start_time, 
            end_time__gte=start_time 
        ).first()

        if not availability:
            raise serializers.ValidationError("The doctor is not available at this exact time.")

 
        import datetime
        slot_duration_minutes = availability.slot_duration
        end_time = (datetime.datetime.combine(date, start_time) + datetime.timedelta(minutes=slot_duration_minutes)).time()
        data['end_time'] = end_time

        data['clinic'] = doctor.clinic

        return data

    def create(self, validated_data):
        
        return super().create(validated_data)
from rest_framework import serializers
from django.utils import timezone
from apps.meeting.models import Meeting
from apps.users.models import User, Patients, StaffSchedule, uzbek_phone_validator


class MeetingCreateSerializer(serializers.ModelSerializer):
    doctor = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(is_active=True, role='doctor')
    )
    date_time = serializers.DateTimeField()

    patient_phone = serializers.CharField(
        max_length=15,
        validators=[uzbek_phone_validator],
        write_only=True
    )

    patient_full_name = serializers.CharField(
        max_length=150,
        write_only=True
    )

    patient_birth_date = serializers.DateField(
        required=False,
        allow_null=True,
        write_only=True
    )

    patient_gender = serializers.ChoiceField(
        choices=[('male', 'Male'), ('female', 'Female')],
        default='male',
        write_only=True
    )

    patient_address = serializers.CharField(
        max_length=255,
        required=False,
        allow_blank=True,
        write_only=True
    )

    patient_notes = serializers.CharField(
        required=False,
        allow_blank=True,
        write_only=True
    )

    id = serializers.IntegerField(read_only=True)
    status = serializers.CharField(read_only=True)

    class Meta:
        model = Meeting
        fields = (
            'id', 'doctor', 'date_time', 'patient_phone', 'patient_full_name', 'patient_birth_date',
            'patient_gender', 'patient_address', 'patient_notes', 'status',
        )

    def validate_date_time(self, value):
        if value <= timezone.now():
            raise serializers.ValidationError(
                "Meeting time cannot be in the past"
            )
        return value

    def validate(self, data):
        doctor = data['doctor']
        date_time = data['date_time']

        day_code = date_time.strftime('%a')
        meeting_time = date_time.time()

        schedules = StaffSchedule.objects.filter(
            staff=doctor,
            day=day_code
        )

        if not schedules.exists():
            raise serializers.ValidationError(
                f"{doctor.full_name} does not work on this day"
            )

        is_in_working_time = schedules.filter(
            start_time__lte=meeting_time,
            end_time__gt=meeting_time
        ).exists()

        if not is_in_working_time:
            raise serializers.ValidationError(
                f"{doctor.full_name} is not in working time"
            )

        if Meeting.objects.filter(
            doctor=doctor,
            date_time=date_time,
            status__in=['pending', 'approved']
        ).exists():
            raise serializers.ValidationError(
                f"{doctor.full_name} is already busy at this time"
            )

        return data

    def create(self, validated_data):
        user = self.context['request'].user

        phone = validated_data.pop('patient_phone')
        full_name = validated_data.pop('patient_full_name')

        patient, created = Patients.objects.get_or_create(
            phone_number=phone,
            defaults={
                'full_name': full_name,
                'birth_date': validated_data.pop('patient_birth_date', None),
                'gender': validated_data.pop('patient_gender', 'male'),
                'address': validated_data.pop('patient_address', ''),
                'notes': validated_data.pop('patient_notes', ''),
            }
        )

        meeting = Meeting.objects.create(
            patient=patient,
            doctor=validated_data['doctor'],
            date_time=validated_data['date_time'],
            created_by=user,
            status='pending'
        )
        return meeting


class DoctorShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'full_name', 'email', 'phone_number')


class PatientShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patients
        fields = ('id', 'full_name', 'phone_number')


class MeetingListSerializer(serializers.ModelSerializer):
    doctor = DoctorShortSerializer(read_only=True)
    patient = PatientShortSerializer(read_only=True)

    class Meta:
        model = Meeting
        fields = ('id', 'patient', 'doctor', 'date_time', 'status')


class MeetingDoctorListSerializer(serializers.ModelSerializer):
    patient = PatientShortSerializer(read_only=True)

    class Meta:
        model = Meeting
        fields = ('id', 'patient', 'date_time', 'status')


class PatientDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patients
        fields = (
            'id', 'full_name', 'phone_number', 'image_patient',
            'birth_date', 'gender', 'address', 'notes'
        )


class DoctorDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id', 'email', 'full_name', 'phone_number', 'descriptor', 'image_user'
        )


class MeetingRetrieveSerializer(serializers.ModelSerializer):
    patient = PatientDetailSerializer(read_only=True)
    doctor = DoctorDetailSerializer(read_only=True)

    class Meta:
        model = Meeting
        fields = (
            'id', 'patient', 'doctor', 'date_time', 'status', 'created_by', 'created_at'
        )


class MeetingDoctorRetrieveSerializer(serializers.ModelSerializer):
    patient = PatientDetailSerializer(read_only=True)

    class Meta:
        model = Meeting
        fields = (
            'id', 'patient', 'date_time', 'status', 'created_by', 'created_at'
        )


class MeetingUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meeting
        fields = ('doctor', 'patient', 'date_time', 'status')
        extra_kwargs = {
            'doctor': {'required': False},
            'patient': {'required': False},
            'date_time': {'required': False},
            'status': {'required': False},
        }

    def validate(self, attrs):
        meeting = self.instance

        new_doctor = attrs.get('doctor', meeting.doctor)
        new_patient = attrs.get('patient', meeting.patient)
        new_date_time = attrs.get('date_time', meeting.date_time)
        new_status = attrs.get('status', meeting.status)

        if meeting.status in ['cancelled', 'completed']:
            raise serializers.ValidationError(
                "Cannot update a cancelled or completed meeting."
            )

        status_transitions = {
            'pending': ['approved', 'cancelled'],
            'approved': ['completed', 'cancelled'],
        }

        if meeting.status != new_status:
            allowed = status_transitions.get(meeting.status, [])
            if new_status not in allowed:
                raise serializers.ValidationError(
                    f"Invalid status transition from {meeting.status} to {new_status}."
                )

        if new_date_time < timezone.now():
            raise serializers.ValidationError(
                "Meeting time cannot be in the past."
            )

        if meeting.status == 'approved':
            if new_doctor != meeting.doctor or new_patient != meeting.patient:
                raise serializers.ValidationError(
                    "Cannot change doctor or patient for an approved meeting."
                )

        conflict = Meeting.objects.filter(
            doctor=new_doctor,
            date_time=new_date_time
        ).exclude(id=meeting.id).exists()

        if conflict:
            raise serializers.ValidationError(
                f"{new_doctor.full_name} is already busy at this time."
            )

        return attrs
    

class MeetingStatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meeting
        fields = ('status',)

    def validate(self, attrs):
        meeting = self.instance
        user = self.context['request'].user
        new_status = attrs.get('status')

        if meeting.status in ['cancelled', 'completed']:
            raise serializers.ValidationError(
                'Cannot update a cancelled or completed meeting.'
            )   

        status_transitions = {
            'pending': ['approved', 'cancelled'],
            'approved': ['completed', 'cancelled'],
        }

        allowed = status_transitions.get(meeting.status, [])
        if new_status not in allowed:
            raise serializers.ValidationError(
                f'Invalid status transition from {meeting.status} to {new_status}.'
            )

        if user.role == 'doctor':
            if meeting.doctor != user:
                raise serializers.ValidationError(
                    'Doctors can only update their own meetings.'
                )     
            
            if new_status != 'completed':
                raise serializers.ValidationError(
                    'Doctors can only mark meetings as completed.'
                )
            
        if new_status == 'approved' and meeting.date_time < timezone.now():
            raise serializers.ValidationError(
                'Cannot approve a meeting scheduled in the past.'
            )

        return attrs    
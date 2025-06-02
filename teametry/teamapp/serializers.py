# teamapp/serializers.py – API 요청/응답 포맷 정의
from rest_framework import serializers
from .models import Team, Participant, SurveyResponse

# 방 생성 요청용 Serializer
class TeamCreateSerializer(serializers.Serializer):
    team_type = serializers.ChoiceField(choices=["development", "general"])
    division_type = serializers.ChoiceField(choices=["BY_MEMBER_COUNT", "BY_TEAM_COUNT"])
    total_members = serializers.IntegerField(min_value=1)
    max_members = serializers.IntegerField(min_value=1, required=False)
    total_teams = serializers.IntegerField(min_value=1, required=False)

    def validate(self, data):
        division_type = data.get("division_type")

        if division_type == "BY_MEMBER_COUNT":
            if not data.get("max_members"):
                raise serializers.ValidationError("division_type이 'BY_MEMBER_COUNT'인 경우 max_members는 필수입니다.")
        elif division_type == "BY_TEAM_COUNT":
            if not data.get("total_teams"):
                raise serializers.ValidationError("division_type이 'BY_TEAM_COUNT'인 경우 total_teams는 필수입니다.")
        else:
            raise serializers.ValidationError("division_type 값이 유효하지 않습니다.")
        return data

# 방 생성 완료 시 관리자에게 반환할 응답 Serializer
class TeamResponseSerializer(serializers.ModelSerializer):
    link = serializers.SerializerMethodField()

    class Meta:
        model = Team
        fields = ["room_code", "password", "link"]

    def get_link(self, obj):
        return f"https://teametry.kr/team/{obj.room_code}"

# 참가자가 방에 입장할 때 방 코드 유효성 확인
class RoomJoinSerializer(serializers.Serializer):
    room_code = serializers.CharField(max_length=10)

    def validate_room_code(self, value):
        if not Team.objects.filter(room_code=value).exists():
            raise serializers.ValidationError("존재하지 않는 방 코드입니다.")
        return value

# 참가자 정보 입력용 Serializer
class ParticipantCreateSerializer(serializers.ModelSerializer):
    room_code = serializers.CharField(write_only=True)

    class Meta:
        model = Participant
        fields = [
            "room_code",
            "name",
            "student_id",
            "email",
            "phone_number",
            "position",
            "leader_preference"
        ]

    def validate_room_code(self, value):
        """
        입력받은 room_code로 Team(방)을 찾고, self.team에 저장.
        존재하지 않으면 validation error 반환.
        """
        team_qs = Team.objects.filter(room_code=value)
        if not team_qs.exists():
            raise serializers.ValidationError("유효하지 않은 방 코드입니다.")
        self.team = team_qs.first()  # ✅ get → filter().first()로 수정
        return value

    def validate(self, data):
        team_type = self.team.team_type
        if team_type != "development":
            data["position"] = "none"
        return data

    def create(self, validated_data):
        validated_data["team"] = self.team
        validated_data.pop("room_code")
        return Participant.objects.create(**validated_data)

# 성격 검사 결과 저장용 Serializer
class SurveyResponseSerializer(serializers.ModelSerializer):
    participant_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = SurveyResponse
        fields = [
            "participant_id", "openness", "conscientiousness",
            "mbti_ie_score", "mbti_sn_score",
            "mbti_tf_score", "mbti_jp_score",
            "inferred_mbti"
        ]

    def validate_participant_id(self, value):
        if not Participant.objects.filter(id=value).exists():
            raise serializers.ValidationError("존재하지 않는 참가자입니다.")
        return value

    def create(self, validated_data):
        participant_id = validated_data.pop("participant_id")
        participant = Participant.objects.get(id=participant_id)
        return SurveyResponse.objects.create(participant=participant, **validated_data)

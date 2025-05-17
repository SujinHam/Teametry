# ✅ teamapp/serializers.py – API 요청/응답 포맷 정의
from rest_framework import serializers
from .models import Team, Participant, SurveyResponse

# ✅ 조 생성 요청용 Serializer
class TeamCreateSerializer(serializers.Serializer):
    team_type = serializers.ChoiceField(choices=["development", "general"])  # 개발/일반 선택
    total_members = serializers.IntegerField(min_value=1)                       # 전체 인원 수 (필수)
    max_members = serializers.IntegerField(min_value=1, required=False)        # 한 조당 인원 수 (선택)
    total_teams = serializers.IntegerField(min_value=1, required=False)        # 조 개수 (선택)

    # max_members 또는 total_teams 둘 중 하나는 반드시 있어야 함
    def validate(self, data):
        if not data.get("max_members") and not data.get("total_teams"):
            raise serializers.ValidationError("max_members 또는 total_teams 중 하나는 필수입니다.")
        return data

# ✅ 조 생성 완료 시 관리자에게 반환할 응답 Serializer
class TeamResponseSerializer(serializers.ModelSerializer):
    link = serializers.SerializerMethodField()  # 링크는 room_code로 동적 생성

    class Meta:
        model = Team
        fields = ["room_code", "password", "link"]

    def get_link(self, obj):
        return f"https://teametry.kr/team/{obj.room_code}"  # 링크 규칙

# ✅ 참가자 정보 입력용 Serializer
class ParticipantCreateSerializer(serializers.ModelSerializer):
    room_code = serializers.CharField(write_only=True)  # 사용자가 입력한 방 코드

    class Meta:
        model = Participant
        fields = [
            "room_code", "name", "student_id",
            "email", "phone_number", "position",
            "leader_preference"
        ]

    # 입력된 방 코드가 실제 존재하는지 확인하고, team 필드로 연결
    def validate_room_code(self, value):
        try:
            self.team = Team.objects.get(room_code=value)
        except Team.DoesNotExist:
            raise serializers.ValidationError("유효하지 않은 방 코드입니다.")
        return value

    def create(self, validated_data):
        validated_data["team"] = self.team
        validated_data.pop("room_code")
        return Participant.objects.create(**validated_data)

# ✅ 참가자가 방에 입장할 때 방 코드 유효성 확인
class RoomJoinSerializer(serializers.Serializer):
    room_code = serializers.CharField(max_length=10)

    def validate_room_code(self, value):
        if not Team.objects.filter(room_code=value).exists():
            raise serializers.ValidationError("존재하지 않는 방 코드입니다.")
        return value

# ✅ 성격 검사 결과 저장용 Serializer
class SurveyResponseSerializer(serializers.ModelSerializer):
    participant_id = serializers.IntegerField(write_only=True)  # 참가자 ID만 받아서 내부 연결

    class Meta:
        model = SurveyResponse
        fields = [
            "participant_id", "openness", "conscientiousness",
            "mbti_ie_score", "mbti_sn_score",
            "mbti_tf_score", "mbti_jp_score",
            "inferred_mbti"
        ]

    # 참가자 ID 유효성 확인
    def validate_participant_id(self, value):
        if not Participant.objects.filter(id=value).exists():
            raise serializers.ValidationError("존재하지 않는 참가자입니다.")
        return value

    # participant를 직접 연결하여 생성
    def create(self, validated_data):
        participant_id = validated_data.pop("participant_id")
        participant = Participant.objects.get(id=participant_id)
        return SurveyResponse.objects.create(participant=participant, **validated_data)

# ✅ 팀 결과 페이지(result2.html)에서 팀원 리스트 반환용
class ParticipantSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Participant
        fields = ["id", "name", "student_id", "email", "phone_number"]

# ✅ 자연어 요약 응답용
class ParticipantSummaryResponseSerializer(serializers.Serializer):
    participant_id = serializers.IntegerField()
    summary = serializers.CharField()

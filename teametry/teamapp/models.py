# ✅ teamapp/models.py – 데이터베이스 모델 정의
from django.db import models

# 팀(방) 정보 저장
class Team(models.Model):
    TEAM_TYPES = [
        ('development', '개발'),  # 개발 팀
        ('general', '일반'),      # 일반 팀
    ]

    team_type = models.CharField(max_length=20, choices=TEAM_TYPES)  # 조 유형 선택 (개발/일반)
    room_code = models.CharField(max_length=10, unique=True)         # 참가자 입장용 고유 방 코드
    password = models.CharField(max_length=100)                      # 관리자용 비밀번호
    max_members = models.PositiveIntegerField()                      # 한 조당 최대 인원 수
    total_members = models.PositiveIntegerField()                    # 총 참가자 수
    created_at = models.DateTimeField(auto_now_add=True)             # 조 생성 요청 시각 자동 기록

# 참가자 정보 저장
class Participant(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)         # 어떤 방(Team)에 참가했는지
    name = models.CharField(max_length=30)                           # 이름
    student_id = models.CharField(max_length=20)                     # 학번
    email = models.EmailField()                                      # 이메일
    phone_number = models.CharField(max_length=20)                   # 전화번호

    POSITION_CHOICES = [
        ('frontend', '프론트엔드'),
        ('backend', '백엔드'),
        ('none', '선택 안 함'),
    ]
    position = models.CharField(
        max_length=20,
        choices=POSITION_CHOICES,
        default='none'  # 일반 팀이거나 선택 안 한 경우
    )  # 역할 선택

    assigned_position = models.CharField(
        max_length=20,
        choices=POSITION_CHOICES,
        default='none'  # 조 편성 시 자동 분류된 역할
    )  # 실제 조 편성에 반영되는 역할

    leader_preference = models.BooleanField(default=False)           # 리더 희망 여부
    created_at = models.DateTimeField(auto_now_add=True)             # 제출 시각 자동 기록

# 성격 검사 결과 요약 저장
class SurveyResponse(models.Model):
    participant = models.OneToOneField(Participant, on_delete=models.CASCADE)  # 1:1로 참가자와 연결

    # Big Five 요약 점수 (100점 만점 기준)
    openness = models.IntegerField()
    conscientiousness = models.IntegerField()

    # MBTI 차원별 점수 (기준점: 0, +면 앞쪽 유형, -면 반대)
    mbti_ie_score = models.FloatField()
    mbti_sn_score = models.FloatField()
    mbti_tf_score = models.FloatField()
    mbti_jp_score = models.FloatField()

    inferred_mbti = models.CharField(max_length=4, null=True, blank=True)  # 계산된 최종 MBTI (ex: INTP)
    submitted_at = models.DateTimeField(auto_now_add=True)  # 제출 시간 자동 저장

    def __str__(self):
        return f"{self.participant.name} ({self.inferred_mbti})"


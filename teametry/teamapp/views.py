from django.shortcuts import render

# Create your views here.
# ✅ views.py – 조 생성 요청 처리 (주석 포함)
import math, random, string
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Team, Participant, SurveyResponse
from .serializers import TeamCreateSerializer, TeamResponseSerializer, RoomJoinSerializer, ParticipantCreateSerializer, SurveyResponseSerializer
from .major import assign_developer_teams_final_logic
from .import_random import assign_non_developer_teams_rule_based

# 전역 조 편성 결과 매핑 (임시, 메모리 기반)
PARTICIPANT_TEAM_MAP = {}

# 방 코드 및 비밀번호 생성을 위한 랜덤 문자열 생성 함수
def generate_code(length=8):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

# 조 생성 API View
class TeamCreateView(APIView):
    def post(self, request):
        # 요청 데이터 유효성 검사
        serializer = TeamCreateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data
        total_members = data['total_members']

        # 입력에 따라 조 개수 또는 조당 인원 계산
        if 'max_members' in data:
            max_members = data['max_members']
            total_teams = math.ceil(total_members / max_members)
        else:
            total_teams = data['total_teams']
            max_members = math.ceil(total_members / total_teams)

        created_teams = []

        # 조 개수만큼 Team 객체 생성
        for _ in range(total_teams):
            room_code = generate_code()
            while Team.objects.filter(room_code=room_code).exists():  # 중복 방지
                room_code = generate_code()

            password = generate_code(8)  # 관리자용 비밀번호

            team = Team.objects.create(
                team_type=data['team_type'],
                room_code=room_code,
                password=password,
                max_members=max_members,
                total_members=total_members,
            )
            created_teams.append(team)

        # 첫 번째 조의 정보를 응답 (관리자에게만 보여줄 정보)
        response_data = TeamResponseSerializer(created_teams[0]).data
        return Response({"message": "Team created successfully", **response_data}, status=201)

# ✅ 방 입장 API View – 참가자가 room_code 입력 시 유효성 확인 및 방 정보 제공
class RoomJoinView(APIView):
    def post(self, request):
        serializer = RoomJoinSerializer(data=request.data)  # room_code만 받아서 검증
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        room_code = serializer.validated_data['room_code']
        team = Team.objects.get(room_code=room_code)  # 검증된 코드로 Team 인스턴스 가져옴

        return Response({
            "message": "방 입장에 성공했습니다.",
            "room_code": team.room_code,
            "team_type": team.team_type,
            "max_members": team.max_members,
            "total_members": team.total_members
        }, status=200)

# ✅ 참가자 정보 등록 처리 API
class ParticipantJoinView(APIView):
    def post(self, request):
        serializer = ParticipantCreateSerializer(data=request.data)  # 입력값 검증
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        participant = serializer.save()  # 유효한 경우 DB에 저장

        return Response({
            "message": "참가자 정보가 성공적으로 등록되었습니다.",
            "user_id": participant.id
        }, status=201)

# ✅ 참가자가 성격 검사 결과를 제출하는 API
class SurveySubmitView(APIView):
    def post(self, request):
        serializer = SurveyResponseSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        survey = serializer.save()  # 결과 저장

        return Response({
            "message": "성격 검사 결과가 성공적으로 저장되었습니다.",
            "survey_id": survey.id
        }, status=201)

# ✅ 관리자 요청으로 참가자들을 성격 및 역할 기반으로 조 편성하는 API
class TeamAssignView(APIView):
    def post(self, request):
        room_code = request.data.get("room_code")  # 요청에서 방 코드 받기
        password = request.data.get("password")    # 요청에서 비밀번호 받기

        # 해당 방 존재 여부 확인
        try:
            team = Team.objects.get(room_code=room_code)
        except Team.DoesNotExist:
            return Response({"error": "존재하지 않는 방 코드입니다."}, status=400)

        # 비밀번호 검증
        if team.password != password:
            return Response({"error": "비밀번호가 올바르지 않습니다."}, status=403)

        # 해당 방 참가자와 설문 응답 불러오기
        participants = Participant.objects.filter(team=team)
        responses = SurveyResponse.objects.filter(participant__team=team)
        response_map = {res.participant_id: res for res in responses}  # 빠른 조회용 매핑

        students = []
        for p in participants:
            res = response_map.get(p.id)
            if not res:
                continue  # 설문 미제출자는 조 편성에서 제외

            # 참가자 + 성격 검사 결과를 통합한 구조로 변환
            student = {
                "id": p.id,
                "name": p.name,
                "student_id": p.student_id,
                "email": p.email,
                "phone_number": p.phone_number,
                "position": p.position,
                "leader": p.leader_preference,
                "openness": res.openness,
                "conscientiousness": res.conscientiousness,
                "leader_score": res.openness + res.conscientiousness,  # 사용자 정의 기준
                "mbti_ie_score": res.mbti_ie_score,
                "mbti_sn_score": res.mbti_sn_score,
                "mbti_tf_score": res.mbti_tf_score,
                "mbti_jp_score": res.mbti_jp_score,
                "mbti": res.inferred_mbti,
            }
            students.append(student)

        if not students:
            return Response({"error": "설문을 완료한 참가자가 없습니다."}, status=400)

        # ✅ team_type 에 따라 알고리즘 분기
        if team.team_type == "development":
            teams, team_leaders_info = assign_developer_teams_final_logic(students)
        else:
            teams, team_leaders_info = assign_non_developer_teams_rule_based(students)

        # 결과 반환
        return Response({
            "message": "조 편성이 완료되었습니다.",
            "teams": teams,
            "leaders": team_leaders_info
        }, status=200)

# ✅ 설문 응답 현황 확인 (관리자용)
class SurveyStatusView(APIView):
    def post(self, request):
        room_code = request.data.get("room_code")
        password = request.data.get("password")

        # 팀 존재 확인
        try:
            team = Team.objects.get(room_code=room_code)
        except Team.DoesNotExist:
            return Response({"error": "존재하지 않는 방 코드입니다."}, status=400)

        # 비밀번호 확인
        if team.password != password:
            return Response({"error": "비밀번호가 올바르지 않습니다."}, status=403)

        # 전체 참가자 수 및 설문 완료 수 계산
        total = Participant.objects.filter(team=team).count()
        responded = SurveyResponse.objects.filter(participant__team=team).count()

        return Response({
            "room_code": room_code,
            "total": total,
            "responded": responded,
            "progress": f"{responded} / {total}"
        }, status=200)

class TeamResultView(APIView):
    def post(self, request):
        room_code = request.data.get("room_code")
        password = request.data.get("password")

        try:
            team = Team.objects.get(room_code=room_code)
        except Team.DoesNotExist:
            return Response({"error": "존재하지 않는 방 코드입니다."}, status=400)

        if team.password != password:
            return Response({"error": "비밀번호가 올바르지 않습니다."}, status=403)

        participants = Participant.objects.filter(team=team)

        result = {}
        for p in participants:
            team_num = PARTICIPANT_TEAM_MAP.get(p.id)
            if team_num is None:
                continue
            if team_num not in result:
                result[team_num] = []
            result[team_num].append({
                "id": p.id,
                "name": p.name
            })

        return Response({
            "message": "조 편성 결과 조회 성공",
            "teams": result
        }, status=200)

# ✅ 특정 팀 상세 정보 조회 (result2.html 용)
class TeamDetailView(APIView):
    def get(self, request, room_code: str, team_number: int):
        # 해당 방에서 조 편성된 참가자들 중 팀 번호가 일치하는 사람들만 필터링
        team_members = []
        for p in Participant.objects.filter(team__room_code=room_code):
            if PARTICIPANT_TEAM_MAP.get(p.id) == team_number:
                team_members.append({
                    "id": p.id,
                    "name": p.name,
                    "student_id": p.student_id,
                    "email": p.email,
                    "phone_number": p.phone_number
                })

        if not team_members:
            return Response({"error": "해당 팀에 속한 참가자가 없습니다."}, status=404)

        return Response({
            "team_number": team_number,
            "members": team_members
        }, status=200)

# ✅ 참가자 성격/역할 요약 설명 API (자연어 요약)
class ParticipantSummaryView(APIView):
    def get(self, request, participant_id: int):
        try:
            p = Participant.objects.get(id=participant_id)
            s = SurveyResponse.objects.get(participant=p)
        except (Participant.DoesNotExist, SurveyResponse.DoesNotExist):
            return Response({"error": "해당 참가자 또는 설문 결과가 없습니다."}, status=404)

        # 자연어 요약 생성
        lines = [
            f"{p.name}님은 {p.position} 역할을 희망하며,",
            f"조장 역할 {'선호합니다' if p.leader_preference else '선호하지 않습니다'}."
        ]

        if s.openness >= 70:
            lines.append("새로운 아이디어와 다양한 경험을 즐기는 개방성이 높은 성격입니다.")
        elif s.openness <= 30:
            lines.append("익숙하고 안정적인 방식을 선호하는 성향입니다.")

        if s.conscientiousness >= 70:
            lines.append("매우 책임감 있고 계획적인 태도를 갖고 있습니다.")
        elif s.conscientiousness <= 30:
            lines.append("즉흥적이고 융통성 있는 성격입니다.")

        lines.append(f"MBTI 유형은 {s.inferred_mbti}입니다.")

        return Response({
            "participant_id": p.id,
            "summary": " ".join(lines)
        }, status=200)
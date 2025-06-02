from django.shortcuts import render

# Create your views here.
# views.py – 조 생성 요청 처리 (주석 포함)
import math, random, string
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Team, Participant, SurveyResponse
from .serializers import TeamCreateSerializer, TeamResponseSerializer, RoomJoinSerializer, ParticipantCreateSerializer, SurveyResponseSerializer
from .major import assign_developer_teams_final_logic
from .import_random import assign_non_developer_teams_rule_based
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator



# 방 코드 및 비밀번호 생성을 위한 랜덤 문자열 생성 함수
def generate_code(length=8):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

@method_decorator(csrf_exempt, name='dispatch')
class TeamCreateView(APIView):
    def post(self, request):
        # 1. 요청 데이터 유효성 검사
        serializer = TeamCreateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data
        total_members = data['total_members']
        division_type = data['division_type']

        # 2. 나누는 방식에 따라 조 개수와 조당 인원 계산
        if division_type == "BY_MEMBER_COUNT":
            max_members = data['max_members']
            total_teams = math.ceil(total_members / max_members)
        else:  # "BY_TEAM_COUNT"
            total_teams = data['total_teams']
            max_members = math.ceil(total_members / total_teams)

        # 3. 방 단위로 room_code 및 비밀번호 1회 생성
        room_code = generate_code()
        while Team.objects.filter(room_code=room_code).exists():
            room_code = generate_code()

        password = generate_code(8)  # 관리자용 비밀번호

        created_teams = []

        # 4. 조 개수만큼 Team(조) 생성 (room_code는 공통)
        for _ in range(total_teams):
            team = Team.objects.create(
                team_type=data['team_type'],
                division_type=division_type,
                room_code=room_code,  # ✅ 방 단위로 공통 room_code
                password=password,    # ✅ 방 단위로 공통 비밀번호
                max_members=max_members,
                total_members=total_members,
                total_teams=data.get('total_teams') if division_type == "BY_TEAM_COUNT" else None,
            )
            created_teams.append(team)

        # 5. 첫 번째 조의 정보를 응답
        response_data = TeamResponseSerializer(created_teams[0]).data
        return Response({"message": "Team created successfully", **response_data}, status=201)


class RoomJoinView(APIView):
    def post(self, request):
        serializer = RoomJoinSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        room_code = serializer.validated_data['room_code']

        # ✅ get() → filter().first()로 변경
        team = Team.objects.filter(room_code=room_code).first()
        if not team:
            return Response({"error": "존재하지 않는 방 코드입니다."}, status=400)

        return Response({
            "message": "방 입장에 성공했습니다.",
            "room_code": team.room_code,
            "team_type": team.team_type,
            "division_type": team.division_type,
            "max_members": team.max_members if team.division_type == "BY_MEMBER_COUNT" else None,
            "total_teams": team.total_teams if team.division_type == "BY_TEAM_COUNT" else None,
            "total_members": team.total_members
        }, status=200)



@method_decorator(csrf_exempt, name='dispatch')
class ParticipantJoinView(APIView):
    def post(self, request):
        room_code = request.data.get("room_code")
        
        # ❗ 이 부분이 핵심입니다
        team = Team.objects.filter(room_code=room_code).first()
        if not team:
            return Response({"error": "유효하지 않은 방 코드입니다."}, status=400)

        data = request.data.copy()
        data["team"] = team.id  # ✅ team id를 명시적으로 전달

        serializer = ParticipantCreateSerializer(data=data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        participant = serializer.save()

        return Response({
            "message": "참가자 정보가 성공적으로 등록되었습니다.",
            "user_id": participant.id
        }, status=201)
 



# 참가자가 성격 검사 결과를 제출하는 API
@method_decorator(csrf_exempt, name="dispatch")
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
    
# 설문 응답 현황 확인 (관리자용)
class SurveyStatusView(APIView):
    def post(self, request):
        room_code = request.data.get("room_code")
        password = request.data.get("password")

        # 방 존재 확인
        try:
            team = Team.objects.get(room_code=room_code)
        except Team.DoesNotExist:
            return Response({"error": "존재하지 않는 방 코드입니다."}, status=400)

        # 비밀번호 확인
        if team.password != password:
            return Response({"error": "비밀번호가 올바르지 않습니다."}, status=403)

        # 전체 참가자 및 설문 응답자 수 계산
        total = Participant.objects.filter(team=team).count()
        responded = SurveyResponse.objects.filter(participant__team=team).count()

        # 설문 미제출자 명단 추출
        submitted_ids = SurveyResponse.objects.filter(participant__team=team).values_list("participant_id", flat=True)
        unsubmitted_participants = Participant.objects.filter(team=team).exclude(id__in=submitted_ids)
        unsubmitted_names = [p.name for p in unsubmitted_participants]

        return Response({
            "room_code": room_code,
            "total": total,
            "responded": responded,
            "progress": f"{responded} / {total}",
            "unsubmitted": unsubmitted_names  # 미제출자 이름 목록
        }, status=200)

# 관리자 요청으로 참가자들을 성격 및 역할 기반으로 조 편성하는 API
class TeamAssignView(APIView):
    def post(self, request):
        room_code = request.data.get("room_code")  # 요청에서 방 코드 받기
        password = request.data.get("password")    # 요청에서 비밀번호 받기

        # 방 코드로 팀 찾기
        try:
            team = Team.objects.get(room_code=room_code)
        except Team.DoesNotExist:
            return Response({"error": "존재하지 않는 방 코드입니다."}, status=400)

        #  비밀번호 검증
        if team.password != password:
            return Response({"error": "비밀번호가 올바르지 않습니다."}, status=403)

        # 해당 방의 참가자와 설문 응답 불러오기
        participants = Participant.objects.filter(team=team)
        responses = SurveyResponse.objects.filter(participant__team=team)

        # 설문 미제출자 존재 여부 확인
        if len(participants) != len(responses):
            return Response({"error": "아직 설문을 완료하지 않은 참가자가 있습니다."}, status=400)

        # 응답을 participant_id 기준으로 빠르게 찾기 위한 dict
        response_map = {res.participant_id: res for res in responses}

        students = []
        for p in participants:
            res = response_map.get(p.id)
            if not res:
                continue  # (이론상 없음) 방어용

            # 포지션이 'none'인 경우 MBTI 기반으로 자동 지정
            position = p.position
            if position == "none" and res.inferred_mbti:
                mbti = res.inferred_mbti.upper()
                if mbti[0:2] == "IF":
                    position = "frontend"
                elif mbti[0:2] in ("IT", "ET"):
                    position = "backend"

            # 참가자 + 성격 검사 결과를 통합한 구조로 변환
            student = {
                "id": p.id,
                "name": p.name,
                "student_id": p.student_id,
                "email": p.email,
                "phone_number": p.phone_number,
                "position": position,
                "leader": p.leader_preference,
                "openness": res.openness,
                "conscientiousness": res.conscientiousness,
                "leader_score": res.openness + res.conscientiousness,
                "mbti_ie_score": res.mbti_ie_score,
                "mbti_sn_score": res.mbti_sn_score,
                "mbti_tf_score": res.mbti_tf_score,
                "mbti_jp_score": res.mbti_jp_score,
                "mbti": res.inferred_mbti,
            }
            students.append(student)

        # 알고리즘 분기: 개발팀 vs 일반팀
        if team.team_type == "development":
            teams, team_leaders_info = assign_developer_teams_final_logic(students)
        else:
            teams, team_leaders_info = assign_non_developer_teams_rule_based(students)
        # 모든 참가자의 is_leader 초기화
        Participant.objects.filter(team=team).update(is_leader=False)


        # 조 번호와 역할 모두 저장
        for team_index, team_group in enumerate(teams, start=1):
            for member in team_group:
                Participant.objects.filter(id=member["id"]).update(
                    assigned_position=member["position"],
                    assigned_team_number=team_index  # ✅ 조 번호 저장
                )
        # 리더 정보 저장 (is_leader=True)
        for leader in team_leaders_info:
            Participant.objects.filter(id=leader["id"]).update(is_leader=True)

        #  조편성 결과 반환
        return Response({
            "message": "조 편성이 완료되었습니다.",
            "teams": teams,
            "leaders": team_leaders_info
        }, status=200)



class TeamResultView(APIView):
    def post(self, request):
        room_code = request.data.get("room_code")
        password = request.data.get("password")

        # ✅ 동일한 room_code로 여러 팀이 있을 수 있으므로 filter 사용
        teams = Team.objects.filter(room_code=room_code)

        if not teams.exists():
            return Response({"error": "존재하지 않는 방 코드입니다."}, status=400)

        # ✅ 첫 번째 팀 객체에서 비밀번호 검증
        team = teams.first()
        if team.password != password:
            return Response({"error": "비밀번호가 올바르지 않습니다."}, status=403)

        # ✅ 동일 room_code를 가진 모든 팀의 참가자 조회
        participants = Participant.objects.filter(team__room_code=room_code)

        result = {}

        for p in participants:
            team_num = p.assigned_team_number
            if team_num is None:
                continue

            if team_num not in result:
                result[team_num] = []

            result[team_num].append({
                "id": p.id,
                "name": p.name,
                "student_id": p.student_id,
                "email": p.email,
                "phone_number": p.phone_number,
                "position": p.assigned_position,
                "is_leader": p.is_leader  # ✅ 실제 리더 여부 반영
            })

        sorted_result = dict(sorted(result.items()))

        return Response({
            "message": "조 편성 결과 조회 성공",
            "teams": sorted_result
        }, status=200)


class TeamChangeView(APIView):
    def post(self, request):
        room_code = request.data.get("room_code")
        password = request.data.get("password")
        teams = request.data.get("teams", {})
        finalize = request.data.get("finalize", False)  # ✅ 최종 확정 버튼 눌렀는지 여부(프론트에서 전달)

        #  방 찾기
        try:
            team = Team.objects.get(room_code=room_code)
        except Team.DoesNotExist:
            return Response({"error": "존재하지 않는 방입니다."}, status=400)

        if team.password != password:
            return Response({"error": "비밀번호가 올바르지 않습니다."}, status=403)

        # 이미 최종 확정된 경우 수정 불가
        if team.is_assign_finalized:
            return Response({"error": "조 편성이 최종 확정되어 더이상 변경할 수 없습니다."}, status=403)

        # 참가자 리더 상태 초기화
        Participant.objects.filter(team=team).update(is_leader=False)

        # 전달받은 teams 구조로 참가자 정보 일괄 업데이트
        for team_number, members in teams.items():
            for member in members:
                participant_id = member.get("participant_id")
                position = member.get("position")
                is_leader = member.get("is_leader", False)

                try:
                    p = Participant.objects.get(id=participant_id, team=team)
                    p.assigned_team_number = int(team_number)
                    p.assigned_position = position
                    p.is_leader = is_leader
                    p.save()
                except Participant.DoesNotExist:
                    continue  # 잘못된 참가자 ID는 무시

        # 완료 버튼이 눌린 경우, 조 편성 확정
        if finalize:
            team.is_assign_finalized = True
            team.save()

        return Response({"message": "조 편성 결과가 성공적으로 반영되었습니다."}, status=200)

# 특정 팀 상세 정보 조회 (result2.html 용)
class TeamDetailView(APIView):
    def get(self, request, room_code: str, team_number: int):
        #  DB에서 직접 필터링: 해당 방 + 해당 조 번호
        team_members = Participant.objects.filter(
            team__room_code=room_code,
            assigned_team_number=team_number
        )

        if not team_members.exists():
            return Response({"error": "해당 팀에 속한 참가자가 없습니다."}, status=404)

        member_list = []
        for p in team_members:
            member_list.append({
                "id": p.id,
                "name": p.name,
                "student_id": p.student_id,
                "email": p.email,
                "phone_number": p.phone_number,
                "position": p.assigned_position,
                "is_leader": p.is_leader  
            })

        return Response({
            "team_number": team_number,
            "members": member_list
        }, status=200)



#  참가자 성격/역할 요약 설명 API (자연어 요약)
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

# teamapp/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Team

class RoomVerifyView(APIView):
    def post(self, request, room_code):
        password = request.data.get("password")
        try:
            team = Team.objects.filter(room_code=room_code).first()
            if not team:
                return Response({"error": "존재하지 않는 방 코드입니다."}, status=404)
            if team.password != password:
                return Response({"error": "비밀번호가 일치하지 않습니다."}, status=403)
            return Response({"message": "검증 성공"}, status=200)
        except Exception as e:
            return Response({"error": str(e)}, status=500)

import random
import pandas as pd
from collections import Counter
import math

# --- 데이터 정의 (개발자용 - 역할 포함) ---
students_data_dev = [
    {"name": "김서연", "mbti": "ISFJ", "ei": "I", "temperament": "SJ", "role": "프론트엔드", "leader_score": 103, "wants_leader": True},
    {"name": "박지후", "mbti": "ISFJ", "ei": "I", "temperament": "SJ", "role": "프론트엔드", "leader_score": 69, "wants_leader": False},
    {"name": "이민재", "mbti": "ENFJ", "ei": "E", "temperament": "NF", "role": "백엔드", "leader_score": 73, "wants_leader": True},
    {"name": "정하윤", "mbti": "ESTP", "ei": "E", "temperament": "SP", "role": "프론트엔드", "leader_score": 56, "wants_leader": False},
    {"name": "최예진", "mbti": "INTJ", "ei": "I", "temperament": "NT", "role": "백엔드", "leader_score": 85, "wants_leader": False},
    {"name": "윤지호", "mbti": "ISFP", "ei": "I", "temperament": "SP", "role": "프론트엔드", "leader_score": 77, "wants_leader": True},
    {"name": "조하은", "mbti": "ESFP", "ei": "E", "temperament": "SP", "role": "프론트엔드", "leader_score": 68, "wants_leader": False},
    {"name": "한도윤", "mbti": "INTP", "ei": "I", "temperament": "NT", "role": "프론트엔드", "leader_score": 92, "wants_leader": True},
    {"name": "장수아", "mbti": "INFP", "ei": "I", "temperament": "NF", "role": "백엔드", "leader_score": 80, "wants_leader": False},
    {"name": "오지민", "mbti": "ENFP", "ei": "E", "temperament": "NF", "role": "프론트엔드", "leader_score": 63, "wants_leader": True},
    {"name": "서우진", "mbti": "INTP", "ei": "I", "temperament": "NT", "role": "백엔드", "leader_score": 99, "wants_leader": False},
    {"name": "홍다연", "mbti": "ESTJ", "ei": "E", "temperament": "SJ", "role": "프론트엔드", "leader_score": 75, "wants_leader": True},
    {"name": "임현우", "mbti": "ISFJ", "ei": "I", "temperament": "SJ", "role": "프론트엔드", "leader_score": 82, "wants_leader": False},
    {"name": "강세은", "mbti": "ENFP", "ei": "E", "temperament": "NF", "role": "프론트엔드", "leader_score": 91, "wants_leader": True},
    {"name": "배시우", "mbti": "ISFP", "ei": "I", "temperament": "SP", "role": "백엔드", "leader_score": 66, "wants_leader": False},
    {"name": "유예린", "mbti": "INFP", "ei": "I", "temperament": "NF", "role": "프론트엔드", "leader_score": 88, "wants_leader": True},
    {"name": "신지안", "mbti": "INTJ", "ei": "I", "temperament": "NT", "role": "백엔드", "leader_score": 80, "wants_leader": False},
    {"name": "문서준", "mbti": "ISTJ", "ei": "I", "temperament": "SJ", "role": "프론트엔드", "leader_score": 70, "wants_leader": True},
    {"name": "노예은", "mbti": "ISTP", "ei": "I", "temperament": "SP", "role": "프론트엔드", "leader_score": 66, "wants_leader": False},
    {"name": "백하린", "mbti": "ENTJ", "ei": "E", "temperament": "NT", "role": "프론트엔드", "leader_score": 100, "wants_leader": True},
    {"name": "김상우", "mbti": "INFJ", "ei": "I", "temperament": "NF", "role": "백엔드", "leader_score": 67, "wants_leader": False},
]

# --- 공통 함수: 팀 크기 계산 ---
def calculate_team_sizes_45_priority(total_students):
    if total_students <= 0: return [], 0
    for num_teams5 in range(total_students // 5 + 1):
        remaining_students = total_students - 5 * num_teams5
        if remaining_students >= 0 and remaining_students % 4 == 0:
            num_teams4 = remaining_students // 4; sizes = [5] * num_teams5 + [4] * num_teams4
            random.shuffle(sizes); return sizes, num_teams4 + num_teams5
    raise ValueError(f"총 {total_students}명의 학생을 4명 또는 5명 팀으로 정확히 나눌 수 없습니다.")

def calculate_team_sizes_fallback(total_students):
    if total_students <= 0: return [], 0
    if total_students <= 3: return [total_students], 1
    ideal_team_size = 4.0; num_teams = round(total_students / ideal_team_size)
    if num_teams == 0: num_teams = 1
    base_size = total_students // num_teams; remainder = total_students % num_teams
    sizes = [base_size + 1] * remainder + [base_size] * (num_teams - remainder)
    final_sizes = [max(3, min(5, s)) for s in sizes]
    current_sum = sum(final_sizes); diff = total_students - current_sum
    idx = 0
    while diff > 0 and idx < len(final_sizes):
        if final_sizes[idx] < 5: final_sizes[idx] += 1; diff -= 1
        idx = (idx + 1) % len(final_sizes)
    idx = 0
    while diff < 0 and idx < len(final_sizes):
        if final_sizes[idx] > 3: final_sizes[idx] -= 1; diff += 1
        idx = (idx + 1) % len(final_sizes)
    sizes = final_sizes; num_teams = len(sizes)
    if sum(sizes) != total_students: print(f"경고: Fallback 크기 조정 후 합계 불일치! ({sum(sizes)} vs {total_students})")
    print(f"Fallback 팀 크기 계산: {total_students}명 -> {sizes}")
    return sizes, num_teams


# --- 개발자 팀 구성 함수 (조장 우선 선정, 나머지 학생 규칙 기반 배정) ---
def assign_developer_teams_final_logic(students):
    """개발자 팀 구성: (전체 학생 대상)조장 우선 선정 -> 나머지 학생 역할 우선 배정 (후순위 E/I, 기질)"""
    n_students = len(students)
    if n_students == 0: return [], []

    # --- 초기 설정 및 팀 구조 결정 ---
    try:
        target_sizes, num_final_teams = calculate_team_sizes_45_priority(n_students)
        print(f"\n개발자 팀 구성 목표 (4/5명 우선): {n_students}명 -> {num_final_teams}개 팀 {dict(Counter(target_sizes))}")
    except ValueError as e:
        print(f"\n알림: {e} -> 3명을 포함한 Fallback 팀 크기 계산 시도.")
        target_sizes, num_final_teams = calculate_team_sizes_fallback(n_students)
        if num_final_teams == 0: print("오류: Fallback 팀 크기 계산 실패."); return [], []

    teams = [[] for _ in range(num_final_teams)]
    team_leaders_info = [None] * num_final_teams # 최종 리더 정보 문자열 저장
    assigned_students_names = set()
    students_list_original = list(students)

    # --- 1단계: 조장 배정 (전체 학생 대상) ---
    print("\n--- 1단계: 조장 배정 시작 (전체 학생 대상) ---")
    willing_leaders = sorted([s for s in students_list_original if s["wants_leader"]], key=lambda x: x["leader_score"], reverse=True)
    non_willing_sorted = sorted([s for s in students_list_original if not s["wants_leader"]], key=lambda x: x["leader_score"], reverse=True)
    designated_leaders = []
    leader_names_temp = set()

    for leader in willing_leaders:
        if len(designated_leaders) < num_final_teams:
            designated_leaders.append(leader); leader_names_temp.add(leader["name"])
        else: break
    
    num_needed = num_final_teams - len(designated_leaders)
    if num_needed > 0:
        for student in non_willing_sorted:
            if student["name"] not in leader_names_temp:
                designated_leaders.append(student); leader_names_temp.add(student["name"])
                if len(designated_leaders) == num_final_teams: break
    
    for i in range(num_final_teams):
        if i < len(designated_leaders):
            leader = designated_leaders[i]
            teams[i].append(leader)
            assigned_students_names.add(leader["name"])
            status = "희망" if leader["wants_leader"] else "비희망"
            team_leaders_info[i] = f"{leader['name']} ({status}, 점수: {leader['leader_score']}) [리더]"
            print(f"  Team {i+1}: 조장 {leader['name']} ({status}, 역할: {leader['role']}) 배정")
        else:
            team_leaders_info[i] = "N/A [조장 배정 오류]"
            print(f"  경고: Team {i+1}에 배정할 조장 후보 부족!")
    print(f"--- 1단계: 조장 {len(designated_leaders)}명 배정 완료 ---")


    # --- 2단계: 나머지 학생 배정 (역할 최우선, 그 후 E/I, 기질 순) ---
    print("\n--- 2단계: 나머지 학생 배정 시작 ---")
    remaining_students = [s for s in students_list_original if s["name"] not in assigned_students_names]
    random.shuffle(remaining_students)

    for student in remaining_students:
        possible_teams_indices = [i for i in range(num_final_teams) if len(teams[i]) < target_sizes[i]]
        if not possible_teams_indices: print(f"오류: {student['name']} 배정 팀 없음 (모든 팀 목표 인원 도달)!"); continue

        evaluated_teams = []
        for i in possible_teams_indices:
            team = teams[i]
            # 역할 관련
            be_count = sum(1 for m in team if m["role"] == "백엔드"); fe_count = sum(1 for m in team if m["role"] == "프론트엔드")
            new_be_count = be_count + (1 if student["role"] == "백엔드" else 0); new_fe_count = fe_count + (1 if student["role"] == "프론트엔드" else 0)
            fills_role_need = (student["role"] == "백엔드" and be_count == 0) or (student["role"] == "프론트엔드" and fe_count == 0)
            role_diff_after = abs(new_be_count - new_fe_count); current_role_diff = abs(be_count - fe_count)
            improves_role_balance = role_diff_after < current_role_diff
            # E/I 관련
            e_in_team = any(m['ei'] == 'E' for m in team); i_in_team = any(m['ei'] == 'I' for m in team)
            fills_ei_need = (not e_in_team and student['ei'] == 'E') or (not i_in_team and student['ei'] == 'I')
            e_count = sum(1 for m in team if m['ei'] == 'E'); i_count = sum(1 for m in team if m['ei'] == 'I')
            new_e_count = e_count + (1 if student['ei'] == 'E' else 0); new_i_count = i_count + (1 if student['ei'] == 'I' else 0)
            ei_diff_after = abs(new_e_count - new_i_count)
            # 기질 관련
            current_temperaments = {m['temperament'] for m in team}
            fills_temperament_need = student['temperament'] not in current_temperaments
            temperament_count_student = sum(1 for m in team if m['temperament'] == student['temperament'])

            evaluated_teams.append({
                'id': i, 'fills_role_need': fills_role_need, 'improves_role_balance': improves_role_balance,
                'role_diff_after': role_diff_after, 'fills_temperament_need': fills_temperament_need,
                'fills_ei_need': fills_ei_need, 'temperament_count_student': temperament_count_student,
                'ei_diff_after': ei_diff_after, 'current_size': len(team)
            })
        
        # 나머지 학생 배정 시 우선순위: 역할 그룹 -> E/I 그룹 -> 기질 그룹 -> 최소 인원
        evaluated_teams.sort(key=lambda x: (
            x['fills_role_need'],           # P1: 필수 역할 충족
            x['improves_role_balance'],     # P2a: 역할 비율 개선 여부
            -x['role_diff_after'],          # P2b: 역할 차이 최소화 (낮을수록 좋음 -> 음수)
            # --- 역할 관련 우선순위 그룹 종료 ---
            x['fills_ei_need'],             # P3: 필수 E/I 충족
            -x['ei_diff_after'],            # P4: E/I 차이 최소화
            # --- E/I 관련 우선순위 그룹 종료 ---
            x['fills_temperament_need'],    # P5: 필수 기질 충족
            -x['temperament_count_student'],# P6: 기질 집중 방지
            # --- 기질 관련 우선순위 그룹 종료 ---
            -x['current_size']              # P7: 최소 인원 팀
        ), reverse=True)

        if evaluated_teams:
            final_team_idx = evaluated_teams[0]['id']
            teams[final_team_idx].append(student)
            assigned_students_names.add(student["name"])
            # 로그 필요시 주석 해제
            # print(f"  2단계: {student['name']}({student['role']},{student['ei']},{student['temperament']}) -> Team {final_team_idx + 1} ({len(teams[final_team_idx])}/{target_sizes[final_team_idx]})")
        else: print(f"오류: {student['name']} 배정 규칙 적용 실패! (2단계)")
    print(f"--- 2단계: 나머지 {len(remaining_students)}명 학생 배정 완료 ---")

    # 조장 정보는 1단계에서 이미 team_leaders_info에 저장 및 확정됨
    return teams, team_leaders_info


# --- 실행 ---
print("="*50)
print(" 개발팀 팀 구성 ".center(50, "="))
print("="*50)
final_teams_dev_final, final_leaders_dev_final = assign_developer_teams_final_logic(students_data_dev)

# --- 결과 출력 ---
print("\n--- 개발자 최종 팀 배정 결과 ---")
total_assigned_count_df = 0
all_student_names_df = {s['name'] for s in students_data_dev}
assigned_in_output_df = set()

if not final_teams_dev_final:
    print("팀 배정에 실패했습니다.")
else:
    team_size_counts_df = Counter(len(team) for team in final_teams_dev_final)
    print(f"팀 크기 분포: {dict(team_size_counts_df)}")
    for i, team in enumerate(final_teams_dev_final):
        leader_info = final_leaders_dev_final[i] if i < len(final_leaders_dev_final) else "리더 정보 없음"
        print(f"\nTeam {i + 1} (인원: {len(team)}): {leader_info}")
        backend_count = sum(1 for m in team if m['role'] == '백엔드'); frontend_count = sum(1 for m in team if m['role'] == '프론트엔드')
        e_count = sum(1 for m in team if m['ei'] == 'E'); i_count = sum(1 for m in team if m['ei'] == 'I')
        temperaments = [m['temperament'] for m in team]; temperament_counts = Counter(temperaments)
        for member in team:
            print(f"  - {member['name']} / MBTI: {member['mbti']} / 기질: {member['temperament']} / E/I: {member['ei']} / 역할: {member['role']} / 리더점수: {member['leader_score']}")
            assigned_in_output_df.add(member['name']); total_assigned_count_df += 1
        print(f"  팀 통계: **백엔드={backend_count}, 프론트엔드={frontend_count}** | E={e_count}, I={i_count} | 기질={dict(temperament_counts)}")
    print(f"\n총 학생 수: {len(students_data_dev)}")
    print(f"배정된 학생 수: {total_assigned_count_df}")
    unassigned_df = all_student_names_df - assigned_in_output_df
    if unassigned_df: print(f"\n오류: 다음 학생 배정 안됨: {unassigned_df}")
    if total_assigned_count_df != len(students_data_dev): print(f"\n오류: 학생 수 불일치!")
import random
import pandas as pd
from collections import Counter
import math

students_data = [
    {"name": "Student1", "mbti": "ISFJ", "ei": "I", "temperament": "SJ", "leader_score": 103, "wants_leader": True},
    {"name": "Student2", "mbti": "ESFJ", "ei": "E", "temperament": "SJ", "leader_score": 69, "wants_leader": False},
    {"name": "Student3", "mbti": "INFJ", "ei": "I", "temperament": "NF", "leader_score": 73, "wants_leader": True},
    {"name": "Student4", "mbti": "ISTP", "ei": "I", "temperament": "SP", "leader_score": 56, "wants_leader": False},
    {"name": "Student5", "mbti": "INTJ", "ei": "I", "temperament": "NT", "leader_score": 85, "wants_leader": False},
    {"name": "Student6", "mbti": "ISFP", "ei": "I", "temperament": "SP", "leader_score": 77, "wants_leader": True},
    {"name": "Student7", "mbti": "ISFP", "ei": "I", "temperament": "SP", "leader_score": 68, "wants_leader": False},
    {"name": "Student8", "mbti": "ENTP", "ei": "E", "temperament": "NT", "leader_score": 92, "wants_leader": True},
    {"name": "Student9", "mbti": "INFP", "ei": "I", "temperament": "NF", "leader_score": 80, "wants_leader": False},
    {"name": "Student10", "mbti": "ENFP", "ei": "E", "temperament": "NF", "leader_score": 63, "wants_leader": True},
    {"name": "Student11", "mbti": "INTP", "ei": "I", "temperament": "NT", "leader_score": 99, "wants_leader": False},
    {"name": "Student12", "mbti": "ESTJ", "ei": "E", "temperament": "SJ", "leader_score": 75, "wants_leader": True},
    {"name": "Student13", "mbti": "ISFP", "ei": "I", "temperament": "SP", "leader_score": 82, "wants_leader": False},
    {"name": "Student14", "mbti": "ENFP", "ei": "E", "temperament": "NF", "leader_score": 91, "wants_leader": True},
    {"name": "Student15", "mbti": "ISFP", "ei": "I", "temperament": "SP", "leader_score": 66, "wants_leader": False},
    {"name": "Student16", "mbti": "INFP", "ei": "I", "temperament": "NF", "leader_score": 88, "wants_leader": True},
    {"name": "Student17", "mbti": "INTJ", "ei": "I", "temperament": "NT", "leader_score": 80, "wants_leader": False},
    {"name": "Student18", "mbti": "ENTJ", "ei": "E", "temperament": "NT", "leader_score": 70, "wants_leader": True},
    {"name": "Student19", "mbti": "ISTP", "ei": "I", "temperament": "SP", "leader_score": 66, "wants_leader": False},
    {"name": "Student20", "mbti": "INTJ", "ei": "I", "temperament": "NT", "leader_score": 100, "wants_leader": True},
    {"name": "Student21", "mbti": "ESFJ", "ei": "E", "temperament": "SJ", "leader_score": 67, "wants_leader": False},
]


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
    adjusted = False; final_sizes = []; extra_students = 0
    for s in sizes:
        if s <= 2 and total_students > 3: extra_students += s; adjusted = True
        elif s >= 6: extra_students += s - 5; final_sizes.append(5); adjusted = True
        else: final_sizes.append(s)
    if adjusted and extra_students > 0:
         final_sizes.sort(); idx = 0
         while extra_students > 0 and idx < len(final_sizes):
              if final_sizes[idx] < 5: final_sizes[idx] += 1; extra_students -= 1
              idx += 1
         sizes = final_sizes; num_teams = len(sizes)
    print(f"Fallback 팀 크기 계산: {total_students}명 -> {sizes}")
    return sizes, num_teams



def assign_non_developer_teams_rule_based(students):
    """
    비개발자 팀 구성: 조장 우선 배정 후, 규칙 기반으로 E/I 및 기질 균형 맞춰 배정.
    점수 계산 없음. 4/5명 우선, 불가피 시 3명 허용.
    """
    n_students = len(students)
    if n_students == 0: return [], []


    try:
        target_sizes, num_final_teams = calculate_team_sizes_45_priority(n_students)
        print(f"비개발자 팀 구성 목표 (4/5명 우선): {n_students}명 -> {num_final_teams}개 팀 {dict(Counter(target_sizes))}")
    except ValueError as e:
        print(f"알림: {e} -> 3명을 포함한 Fallback 팀 크기 계산 시도.")
        target_sizes, num_final_teams = calculate_team_sizes_fallback(n_students)
        if num_final_teams == 0: print("오류: Fallback 팀 크기 계산 실패."); return [], []

    teams = [[] for _ in range(num_final_teams)]
    team_leaders_info = [None] * num_final_teams
    assigned_students_names = set()
    students_list = list(students)


def assign_non_developer_teams_rule_based(students):
    n_students = len(students)
    if n_students == 0: return [], []

    try:
        target_sizes, num_final_teams = calculate_team_sizes_45_priority(n_students)
        print(f"비개발자 팀 구성 목표 (4/5명 우선): {n_students}명 -> {num_final_teams}개 팀 {dict(Counter(target_sizes))}")
    except ValueError as e:
        print(f"알림: {e} -> 3명을 포함한 Fallback 팀 크기 계산 시도.")
        target_sizes, num_final_teams = calculate_team_sizes_fallback(n_students)
        if num_final_teams == 0: print("오류: Fallback 팀 크기 계산 실패."); return [], []

    teams = [[] for _ in range(num_final_teams)]
    team_leaders_info = [None] * num_final_teams
    assigned_students_names = set()
    students_list = list(students)

    print("\n--- 단계 2: 조장 선정 및 우선 배정 ---")
    willing_leaders = sorted([s for s in students_list if s["wants_leader"]], key=lambda x: x["leader_score"], reverse=True)
    non_willing_sorted = sorted([s for s in students_list if not s["wants_leader"]], key=lambda x: x["leader_score"], reverse=True)
    designated_leaders = []; leader_names_temp = set()
    for leader in willing_leaders:
        if len(designated_leaders) < num_final_teams: designated_leaders.append(leader); leader_names_temp.add(leader["name"])
        else: break
    num_needed = num_final_teams - len(designated_leaders)
    if num_needed > 0:
        for student in non_willing_sorted:
            if student["name"] not in leader_names_temp:
                designated_leaders.append(student); leader_names_temp.add(student["name"])
                if len(designated_leaders) == num_final_teams: break
    for i in range(num_final_teams):
        if i < len(designated_leaders):
            leader = designated_leaders[i]; teams[i].append(leader); assigned_students_names.add(leader["name"])
            status = "희망" if leader["wants_leader"] else "비희망"
            team_leaders_info[i] = f"{leader['name']} ({status}, 점수: {leader['leader_score']}) [리더]"
        else: team_leaders_info[i] = "N/A [조장 배정 오류]"; print(f"  경고: Team {i+1} 조장 부족!")
    print("--- 조장 배정 완료 ---")


    print("\n--- 단계 3: 나머지 학생 배정 시작 (규칙 기반, 최종 우선순위) ---")
    remaining_students = [s for s in students_list if s["name"] not in assigned_students_names]
    random.shuffle(remaining_students)

    for student in remaining_students:
        possible_teams_indices = [i for i in range(num_final_teams) if len(teams[i]) < target_sizes[i]]
        if not possible_teams_indices: print(f"오류: {student['name']} 배정 팀 없음!"); continue

        evaluated_teams = []
        for i in possible_teams_indices:
            team = teams[i]
            e_in_team = any(m['ei'] == 'E' for m in team); i_in_team = any(m['ei'] == 'I' for m in team)
            fills_ei_need = (not e_in_team and student['ei'] == 'E') or (not i_in_team and student['ei'] == 'I')
            current_temperaments = {m['temperament'] for m in team}
            fills_temperament_need = student['temperament'] not in current_temperaments
            e_count = sum(1 for m in team if m['ei'] == 'E'); i_count = sum(1 for m in team if m['ei'] == 'I')
            new_e_count = e_count + (1 if student['ei'] == 'E' else 0); new_i_count = i_count + (1 if student['ei'] == 'I' else 0)
            ei_diff_after = abs(new_e_count - new_i_count)
            temperament_count_student = sum(1 for m in team if m['temperament'] == student['temperament'])
            evaluated_teams.append({
                'id': i, 'fills_ei_need': fills_ei_need, 'fills_temperament_need': fills_temperament_need,
                'ei_diff_after': ei_diff_after, 'temperament_count_student': temperament_count_student,
                'current_size': len(team)
            })

        # 우선순위: 필수 E/I > 필수 기질 > E/I 비율 > 기질 집중 방지 > 최소 인원
        evaluated_teams.sort(key=lambda x: (
            x['fills_ei_need'],             # 1. 필수 E/I 충족 
            x['fills_temperament_need'],    # 2. 필수 기질 충족 
            -x['ei_diff_after'],            # 3. E/I 차이 최소화 
            -x['temperament_count_student'],# 4. 기질 집중 방지 
            -x['current_size']              # 5. 최소 인원 팀 
        ), reverse=True)

        if evaluated_teams:
            final_team_idx = evaluated_teams[0]['id']
            teams[final_team_idx].append(student)
            assigned_students_names.add(student["name"])
        else: print(f"오류: {student['name']} 배정 규칙 적용 실패!")

    print("--- 나머지 학생 배정 완료 ---")
    return teams, team_leaders_info


final_teams_non_dev_rule, final_leaders_non_dev_rule = assign_non_developer_teams_rule_based(students_data)

print("\n--- 비개발자 최종 팀 배정 결과 ---")
total_assigned_count_ndr = 0
all_student_names_ndr = {s['name'] for s in students_data}
assigned_in_output_ndr = set()

if not final_teams_non_dev_rule:
    print("팀 배정에 실패했습니다.")
else:
    team_size_counts_ndr = Counter(len(team) for team in final_teams_non_dev_rule)
    print(f"팀 크기 분포: {dict(team_size_counts_ndr)}")

    for i, team in enumerate(final_teams_non_dev_rule):
        leader_info = final_leaders_non_dev_rule[i] if i < len(final_leaders_non_dev_rule) else "리더 정보 없음"
        print(f"\nTeam {i + 1} (인원: {len(team)}): {leader_info}") # 리더 정보에 [리더] 포함됨

        e_count = sum(1 for m in team if m['ei'] == 'E')
        i_count = sum(1 for m in team if m['ei'] == 'I')
        temperaments = [m['temperament'] for m in team]
        temperament_counts = Counter(temperaments)

        for member in team:
            print(f"  - {member['name']} / MBTI: {member['mbti']} / 기질: {member['temperament']} / E/I: {member['ei']} / 리더점수: {member['leader_score']}")
            assigned_in_output_ndr.add(member['name'])
            total_assigned_count_ndr += 1

        print(f"  팀 통계: E={e_count}, I={i_count} | 기질={dict(temperament_counts)}")

    print(f"\n총 학생 수: {len(students_data)}")
    print(f"배정된 학생 수: {total_assigned_count_ndr}")

    unassigned_ndr = all_student_names_ndr - assigned_in_output_ndr
    if unassigned_ndr: print(f"\n오류: 다음 학생이 배정되지 않았습니다: {unassigned_ndr}")
    if total_assigned_count_ndr != len(students_data): print(f"\n오류: 총 학생 수 불일치! 예상: {len(students_data)}, 실제 배정: {total_assigned_count_ndr}")
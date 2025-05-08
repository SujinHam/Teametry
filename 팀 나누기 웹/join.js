function goToSurvey(event) {
    event.preventDefault(); // 기본 제출 동작 막기

    // 입력값 수집 (필요할 경우 활용 가능)
    const name = document.querySelector('input[placeholder="이름을 입력하세요"]').value;
    const studentId = document.querySelector('input[placeholder="학번을 입력하세요"]').value;
    const phone = document.querySelector('input[placeholder="전화번호를 입력하세요"]').value;
    const email = document.querySelector('input[placeholder="이메일을 입력하세요"]').value;

    const leader = document.querySelector('input[name="leader"]:checked');
    const role = document.querySelector('input[name="role"]:checked');

    if (!leader || !role) {
        alert("조장 선호 여부와 역할을 선택해주세요.");
        return;
    }

    // 콘솔로 확인 (디버깅용)
    console.log("이름:", name);
    console.log("학번:", studentId);
    console.log("전화번호:", phone);
    console.log("이메일:", email);
    console.log("조장 선호:", leader.id);
    console.log("선호 역할:", role.id);

    // TODO: 나중에 서버 전송 또는 로컬 저장 추가 가능

    // 다음 페이지로 이동
    window.location.href = "survey.html";
}

console.log("✅ join.js 연결 성공");

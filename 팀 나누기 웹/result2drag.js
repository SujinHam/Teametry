document.addEventListener("DOMContentLoaded", () => {
    const modal = document.getElementById("modal");
    const closeBtn = document.getElementById("closeBtn");
    const personName = document.getElementById("person-name");
    const personInfo = document.getElementById("person-info");
    const memberButtons = document.querySelectorAll(".member");

    // 이름별 설명 예시 데이터. 하드코딩 해놨으니 나중에 서버에서 불러오기로 바꾸면 된다.
    const infoMap = {
        "홍길동": "모험심이 강하고 리더십 있는 사람입니다.",
        "신짱구": "유쾌하고 창의적인 분위기 메이커입니다.",
        "고길동": "신중하고 책임감이 강한 타입입니다.",
    };

    memberButtons.forEach((btn) => {
        btn.addEventListener("click", () => {
            const name = btn.dataset.name;
            personName.textContent = name;
            personInfo.textContent = infoMap[name] || "정보가 없습니다.";
            modal.style.display = "block";
        });
    });

    closeBtn.addEventListener("click", () => {
        modal.style.display = "none";
    });

    // 바깥 영역 클릭 시 모달 닫기
    window.addEventListener("click", (e) => {
        if (e.target === modal) {
            modal.style.display = "none";
        }
    });
});

console.log("✅ result2.js 연결 완료");

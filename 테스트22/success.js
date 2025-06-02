document.addEventListener("DOMContentLoaded", () => {
    const params = new URLSearchParams(window.location.search);
    const room = params.get("room");
    const pw = params.get("pw");

    if (!room || !pw) {
        alert("방 정보가 유효하지 않습니다.");
        return;
    }

    // 입력창에 링크, 코드, 비밀번호 표시
    const link = `https://teametry.ac.kr/team/${room}`;

    document.getElementById("team-link").value = link;
    document.getElementById("room-code").value = room;
    document.getElementById("room-password").value = pw;
});

function copyText(button) {
    const input = button.previousElementSibling;
    input.select();
    document.execCommand("copy");
    alert("복사되었습니다: " + input.value);
}

function goHome() {
    window.location.href = "home.html";
}

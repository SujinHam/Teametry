document.addEventListener("DOMContentLoaded", () => {
    const params = new URLSearchParams(window.location.search);
    const room = params.get("room");
    const pw = params.get("pw");

    if (!room || !pw) {
        alert("방 정보가 유효하지 않습니다.");
        return;
    }

    // 입력창에 코드와 비번 먼저 표시
    document.getElementById("room-code").value = room;
    document.getElementById("room-password").value = pw;

    // 서버에서 링크 등 정보 받아오기
    fetch(`/api/rooms/${room}/info?pw=${encodeURIComponent(pw)}`)
        .then((res) => {
            if (!res.ok) throw new Error("정보를 불러오지 못했습니다.");
            return res.json();
        })
        .then((data) => {
            // 예: { link: "https://teametry.ac.kr/team/123" }
            document.getElementById("team-link").value = data.link;
        })
        .catch((err) => {
            alert("팀 정보를 불러오는 데 실패했습니다.");
            console.error(err);
        });
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

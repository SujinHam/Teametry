function goHome() {
    window.location.href = "home.html";
}

function goSuccess(event) {
    event.preventDefault();

    const form = document.querySelector(".create-form");

    const type = form.type.value;
    const total = parseInt(form.total.value, 10);

    const mode = form.mode.value;
    const countValue = parseInt(form.count.value, 10);
    const peopleValue = parseInt(form.people.value, 10);

    if (isNaN(total) || total <= 0) {
        alert("인원 수를 올바르게 입력하세요.");
        return;
    }

    // ✅ 필드 이름을 백엔드 기준으로 수정
    let payload = {
        total_members: total,
        team_type: type === "dev" ? "development" : "non-development",
        division_type: mode === "count" ? "BY_TEAM_COUNT" : "BY_MEMBER_COUNT",
    };

    if (mode === "count") {
        if (isNaN(countValue) || countValue <= 0) {
            alert("조 갯수를 올바르게 입력하세요.");
            return;
        }
        payload.total_teams = countValue;
    } else if (mode === "people") {
        if (isNaN(peopleValue) || peopleValue <= 0) {
            alert("조 인원 수를 올바르게 입력하세요.");
            return;
        }
        payload.max_members = peopleValue;
    }

    fetch("http://127.0.0.1:8000/api/create_team/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
    })
        .then((res) => {
            if (!res.ok) throw new Error("조 생성 실패");
            return res.json();
        })
        .then((data) => {
            const roomCode = data.room_code;
            const password = data.password;

            localStorage.setItem("room_code", roomCode);
            localStorage.setItem("room_password", password); // 선택 사항

            window.location.href = `success.html?room=${encodeURIComponent(roomCode)}&pw=${encodeURIComponent(password)}`;
        })

        .catch((err) => {
            alert("조 생성에 실패했습니다.");
            console.error(err);
        });
}

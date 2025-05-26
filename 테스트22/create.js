function goHome() {
    window.location.href = "home.html";
}

function goSuccess(event) {
    event.preventDefault(); // 기본 제출 막기

    const form = document.querySelector(".create-form");

    const type = form.type.value; // 'dev' or 'general'
    const total = parseInt(form.total.value, 10);

    const mode = form.mode.value; // 'count' or 'people'
    const countValue = parseInt(form.count.value, 10);
    const peopleValue = parseInt(form.people.value, 10);

    // 유효성 검사
    if (isNaN(total) || total <= 0) {
        alert("인원 수를 올바르게 입력하세요.");
        return;
    }

    let payload = {
        type: type,
        total: total,
        mode: mode,
    };

    if (mode === "count") {
        if (isNaN(countValue) || countValue <= 0) {
            alert("조 갯수를 올바르게 입력하세요.");
            return;
        }
        payload.count = countValue;
    } else if (mode === "people") {
        if (isNaN(peopleValue) || peopleValue <= 0) {
            alert("조 인원 수를 올바르게 입력하세요.");
            return;
        }
        payload.people = peopleValue;
    }

    // ✅ Django 서버로 POST 요청
    fetch("http://127.0.0.1:8000/api/create_team/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload), // 여기서 'payload' 사용!
    })
        .then((res) => {
            if (!res.ok) throw new Error("조 생성 실패");
            return res.json();
        })
        .then((data) => {
            const roomCode = data.room_code;
            window.location.href = `success.html?room=${encodeURIComponent(roomCode)}`;
        })
        .catch((err) => {
            alert("조 생성에 실패했습니다.");
            console.error(err);
        });
}

// main.js

function goBack() {
    window.location.href = "index.html";
}

function handleSubmit(event) {
    event.preventDefault();

    const form = event.target;
    const type = form.type.value;
    const mode = form.mode.value;
    const count = form.count.value;
    const people = form.people.value;

    if (mode === "count" && !count) {
        alert("조 개수를 입력해주세요!");
        return;
    }

    if (mode === "people" && !people) {
        alert("조 인원 수를 입력해주세요!");
        return;
    }

    const payload = {
        type,
        mode,
        value: mode === "count" ? count : people,
    };

    // 서버에 데이터 전송. 실제 서버와 연결 시 이 URL 수정 예정!!!!
    fetch("https://example.com/api/create-team", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(payload),
    })
        .then((response) => {
            if (!response.ok) {
                throw new Error("서버 오류 발생");
            }
            return response.json();
        })
        .then((data) => {
            console.log("성공:", data);
            // 성공 후 이동
            window.location.href = "success.html";
        })
        .catch((error) => {
            console.error("에러:", error);
            alert("조 생성에 실패했습니다. 다시 시도해주세요.");
        });
}

console.log("✅ create.js 연결 성공!");

document.addEventListener("DOMContentLoaded", () => {
    const roomCode = new URLSearchParams(location.search).get("code");
    const password = new URLSearchParams(location.search).get("pw");

    if (!roomCode || !password) {
        alert("방 정보가 유효하지 않습니다.");
        return;
    }

    // ✅ API 연결: survey_status 엔드포인트 사용
    fetch(`/api/survey_status/?code=${encodeURIComponent(roomCode)}&pw=${encodeURIComponent(password)}`)
        .then((res) => {
            if (!res.ok) throw new Error("참여자 상태를 불러올 수 없습니다.");
            return res.json();
        })
        .then((data) => {
            updateProgress(data.total, data.submitted);
            renderMembers(data.members);
        })
        .catch((err) => {
            alert("상태를 불러오는 데 실패했습니다.");
            console.error(err);
        });

    document.getElementById("create-btn").addEventListener("click", () => {
        fetch("/api/team_assign/", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ room_code: roomCode, password: password }),
        })
            .then((res) => {
                if (!res.ok) throw new Error("조 생성 실패");
                return res.json();
            })
            .then(() => {
                // 조 생성 후 결과 페이지로 이동
                window.location.href = `result.html?code=${encodeURIComponent(roomCode)}&pw=${encodeURIComponent(password)}`;
            })
            .catch((err) => {
                alert("조 생성 중 오류가 발생했습니다.");
                console.error(err);
            });
    });


    function updateProgress(total, submitted) {
        const percent = Math.round((submitted / total) * 100);
        document.getElementById("progress-count").textContent = `${submitted}/${total}`;
        document.getElementById("progress-percent").textContent = `${percent}%`;
    }

    function renderMembers(members) {
        const list = document.getElementById("member-list");
        list.innerHTML = members
            .map((m) => `<p><strong>${m.name}</strong></p>`)
            .join("");
    }

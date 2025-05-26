document.addEventListener("DOMContentLoaded", () => {
    const form = document.querySelector(".form");

    form.addEventListener("submit", async (e) => {
        e.preventDefault();

        // 👉 입력값 수집
        const inputs = form.querySelectorAll("input");
        const name = inputs[0].value;
        const student_id = inputs[1].value;
        const phone = inputs[2].value;
        const email = inputs[3].value;

        const leaderInput = form.querySelector("input[name='leader']:checked");
        const roleInput = form.querySelector("input[name='role']:checked");

        if (!leaderInput || !roleInput) {
            alert("조장 선호와 역할을 선택해주세요.");
            return;
        }

        const isLeaderPreferred = leaderInput.id === "yes";
        const preferredRole = roleInput.id;

        // 👉 room_code는 localStorage에서 가져온다고 가정
        const room_code = localStorage.getItem("room_code");
        if (!room_code) {
            alert("방 코드가 없습니다. 방 생성 또는 초대 링크를 통해 입장해주세요.");
            return;
        }

        try {
            // ✅ 1단계: 방 코드 유효성 확인 (선택적 단계)
            const roomRes = await fetch("/api/join_room/", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ room_code }),
            });

            if (!roomRes.ok) throw new Error("방 코드 확인 실패");

            // ✅ 2단계: 참가자 정보 등록
            const participantPayload = {
                room_code,
                name,
                student_id,
                phone,
                email,
                is_leader_preferred: isLeaderPreferred,
                preferred_role: preferredRole,
            };

            const participantRes = await fetch("/api/join_participant/", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(participantPayload),
            });

            if (!participantRes.ok) throw new Error("참가자 등록 실패");

            const participantData = await participantRes.json();
            const userId = participantData.user_id;

            // ✅ 3단계: survey.html로 이동 (user_id 전달)
            window.location.href = `survey.html?user=${encodeURIComponent(userId)}`;
        } catch (err) {
            console.error(err);
            alert("참가 처리 중 오류가 발생했습니다.");
        }
    });
});

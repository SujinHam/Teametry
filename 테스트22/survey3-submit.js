document.addEventListener("DOMContentLoaded", () => {
    const form = document.querySelector(".survey-form");

    form.addEventListener("submit", async (e) => {
        e.preventDefault();

        // ✅ 현재 페이지 응답 수집 (Q1~Q25)
        const part3 = [];
        for (let i = 1; i <= 25; i++) {
            const selected = document.querySelector(`input[name="q${i}"]:checked`);
            if (!selected) {
                alert(`${i}번 문항에 응답해주세요.`);
                return;
            }
            const score = parseInt(selected.id.split("-")[1]);
            part3.push(score);
        }

        // ✅ 로컬스토리지에서 나머지 파트 불러오기
        const part1 = JSON.parse(localStorage.getItem("survey_part1") || "[]");
        const part2 = JSON.parse(localStorage.getItem("survey_part2") || "[]");

        const answers = [...part1, ...part2, ...part3];

        if (answers.length !== 70) {
            alert("모든 설문에 응답하지 않았습니다.");
            return;
        }

        const params = new URLSearchParams(window.location.search);
        const user_id = params.get("user");
        if (!user_id) {
            alert("사용자 정보가 없습니다.");
            return;
        }

        const payload = {
            user_id,
            answers,
        };

        try {
            const res = await fetch("/api/submit_survey/", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(payload),
            });

            if (!res.ok) throw new Error("제출 실패");

            alert("설문 제출이 완료되었습니다!");
            window.location.href = `result.html?room=${encodeURIComponent(localStorage.getItem("room_code"))}`;
        } catch (err) {
            console.error(err);
            alert("제출 중 오류가 발생했습니다.");
        }
    });
});

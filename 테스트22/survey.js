document.addEventListener("DOMContentLoaded", () => {
    const form = document.querySelector(".survey-form");

    form.addEventListener("submit", (e) => {
        e.preventDefault();

        const answers = [];

        for (let i = 1; i <= 20; i++) {
            const selected = document.querySelector(`input[name="q${i}"]:checked`);
            if (!selected) {
                alert(`${i}번 문항에 응답해주세요.`);
                return;
            }
            const score = parseInt(selected.id.split("-")[1]); // 예: "q5-3" → 3
            answers.push(score);
        }

        // 로컬에 저장
        localStorage.setItem("survey_part1", JSON.stringify(answers));

        // user_id를 다음 페이지로 넘김
        const params = new URLSearchParams(window.location.search);
        const user_id = params.get("user");

        // ✅ 디버깅용 로그 출력
        console.log("Submit fired!");
        console.log("user_id:", user_id);
        console.log("Redirecting to: survey2.html?user=" + user_id);

        window.location.href = `survey2.html?user=${encodeURIComponent(user_id)}`;
    });
});

document.addEventListener("DOMContentLoaded", () => {
    const form = document.querySelector(".survey-form");

    form.addEventListener("submit", (e) => {
        e.preventDefault();

        const answers = [];

        for (let i = 1; i <= 25; i++) {
            const selected = document.querySelector(`input[name="q${i}"]:checked`);
            if (!selected) {
                alert(`${i}번 문항에 응답해주세요.`);
                return;
            }
            const score = parseInt(selected.id.split("-")[1]); // 예: "q5-3" → 3
            answers.push(score);
        }

        // 저장
        localStorage.setItem("survey_part2", JSON.stringify(answers));

        // 다음 페이지로 이동 (user 유지)
        const params = new URLSearchParams(window.location.search);
        const user_id = params.get("user");
        window.location.href = `survey3.html?user=${encodeURIComponent(user_id)}`;
    });
});

document.addEventListener("DOMContentLoaded", () => {
    const form = document.querySelector(".survey-form");

    form.addEventListener("submit", async (e) => {
        e.preventDefault(); // 기본 제출 막기

        const totalQuestions = 5;
        let allAnswered = true;
        const answers = {};

        for (let i = 1; i <= totalQuestions; i++) {
            const checked = document.querySelector(`input[name="q${i}"]:checked`);
            if (!checked) {
                allAnswered = false;
                break;
            }
            answers[`q${i}`] = checked.id; // 또는 .value
        }

        if (!allAnswered) {
            alert("모든 질문에 응답해주세요.");
            return;
        }

        try {
            const response = await fetch("https://example.com/api/survey", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(answers),
            });

            if (!response.ok) {
                throw new Error("서버 전송 실패");
            }

            console.log("✅ 전송 성공:", answers);
            window.location.href = "success.html";
        } catch (error) {
            console.error("❌ 전송 오류:", error);
            alert("설문 결과 전송 중 오류가 발생했습니다. 다시 시도해주세요.");
        }
    });
});

console.log("✅ survey.js 연결 완료");

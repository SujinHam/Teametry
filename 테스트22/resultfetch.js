document.addEventListener("DOMContentLoaded", () => {
    const roomCode = new URLSearchParams(location.search).get("code");
    const password = new URLSearchParams(location.search).get("pw");

    if (!roomCode || !password) {
        alert("방 정보가 유효하지 않습니다.");
        return;
    }

    // 팀 결과 불러오기
    fetch("/api/team_result/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ room_code: roomCode, password }),
    })
        .then((res) => {
            if (!res.ok) throw new Error("팀 결과 불러오기 실패");
            return res.json();
        })
        .then((teams) => {
            const board = document.getElementById("team-board");
            board.innerHTML = "";

            teams.forEach((team, index) => {
                const teamDiv = document.createElement("div");
                teamDiv.className = "team-column";
                teamDiv.id = `team-${index + 1}`;

                const title = document.createElement("h3");
                title.innerText = `${team.teamName} (성향점수)`;
                teamDiv.appendChild(title);

                const leaderDiv = document.createElement("div");
                leaderDiv.className = "member";
                leaderDiv.draggable = true;
                leaderDiv.innerHTML = `<strong>조장</strong><br />
          이름: ${team.leader.name}<br />
          전화번호: ${team.leader.phone}<br />
          이메일: ${team.leader.email}<br />
          점수: ${team.leader.score}`;
                teamDiv.appendChild(leaderDiv);

                team.members.forEach((member) => {
                    const memberDiv = document.createElement("div");
                    memberDiv.className = "member";
                    memberDiv.draggable = true;
                    memberDiv.innerHTML = `이름: ${member.name}<br />
            전화번호: ${member.phone}<br />
            이메일: ${member.email}<br />
            점수: ${member.score}`;
                    teamDiv.appendChild(memberDiv);
                });

                const link = document.createElement("a");
                link.href = "result2.html";
                link.className = "team-link";
                link.innerText = "👉 result2.html로 이동";
                teamDiv.appendChild(link);

                board.appendChild(teamDiv);
            });
        })
        .catch((err) => {
            alert("팀 데이터를 불러오지 못했습니다.");
            console.error(err);
        });

    // 드래그 앤 드롭 기능
    document.addEventListener("dragstart", (e) => {
        if (e.target.classList.contains("member")) {
            e.dataTransfer.setData("text/plain", e.target.outerHTML);
            e.target.classList.add("dragging");
        }
    });

    document.addEventListener("dragover", (e) => {
        if (e.target.classList.contains("team-column")) {
            e.preventDefault();
        }
    });

    document.addEventListener("drop", (e) => {
        if (e.target.classList.contains("team-column")) {
            e.preventDefault();
            const draggedHTML = e.dataTransfer.getData("text/plain");
            const draggedElement = document.createElement("div");
            draggedElement.outerHTML = draggedHTML;

            e.target.insertAdjacentHTML("beforeend", draggedHTML);
            document.querySelector(".dragging")?.remove();
        }
    });

    document.addEventListener("dragend", (e) => {
        e.target.classList.remove("dragging");
    });

    // 저장 버튼 클릭 시 변경사항 저장
    document.getElementById("save-button")?.addEventListener("click", () => {
        const teams = Array.from(document.querySelectorAll(".team-column")).map((teamDiv) => {
            const members = Array.from(teamDiv.querySelectorAll(".member")).map((div) => {
                const lines = div.innerHTML.split("<br>");
                const getValue = (line) => line.split(":")[1]?.trim() ?? "";

                return {
                    name: getValue(lines.find((l) => l.includes("이름")) || ""),
                    phone: getValue(lines.find((l) => l.includes("전화번호")) || ""),
                    email: getValue(lines.find((l) => l.includes("이메일")) || ""),
                    score: Number(getValue(lines.find((l) => l.includes("점수")) || "0")),
                    is_leader: div.innerHTML.includes("조장"),
                };
            });

            return {
                team_name: teamDiv.querySelector("h3")?.innerText?.split(" ")[0] || "팀",
                members,
            };
        });

        const payload = {
            room_code: roomCode,
            password,
            teams,
            finalize: true,
        };

        fetch("/api/change_team_assignment/", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload),
        })
            .then((res) => {
                if (!res.ok) throw new Error("조 변경 실패");
                alert("변경사항이 저장되었습니다!");
            })
            .catch((err) => {
                alert("조 변경 중 오류 발생");
                console.error(err);
            });
    });
});

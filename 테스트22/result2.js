document.addEventListener("DOMContentLoaded", () => {
  const teamBox = document.getElementById("team-box");
  const urlParams = new URLSearchParams(window.location.search);
  const roomCode = urlParams.get("code");
  const teamId = urlParams.get("team");

  if (!roomCode || !teamId) {
    teamBox.innerHTML = "<p>팀 정보가 없습니다.</p>";
    return;
  }

  fetch(`/api/team_detail/${roomCode}/${teamId}`)
    .then((res) => {
      if (!res.ok) throw new Error("서버 응답 오류");
      return res.json();
    })
    .then((team) => {
      teamBox.innerHTML = `
        <h3>${team.teamName}</h3>
        <ul>
          <li>
            <span class="leader">👑</span>
            <button class="member" data-id="${team.leader.id}" data-name="${team.leader.name}">
              ${team.leader.name}
            </button>
          </li>
          ${team.members
          .map(
            (m) => `
            <li>
              <button class="member" data-id="${m.id}" data-name="${m.name}">
                ${m.name}
              </button>
            </li>
          `
          )
          .join("")}
        </ul>
      `;

      attachModalListeners(); // 모달 이벤트 바인딩
    })
    .catch((err) => {
      teamBox.innerHTML = "<p>팀 정보를 불러오는 데 실패했습니다.</p>";
      console.error(err);
    });
});

function attachModalListeners() {
  const modal = document.getElementById("modal");
  const personName = document.getElementById("person-name");
  const personInfo = document.getElementById("person-info");
  const closeBtn = document.getElementById("closeBtn");

  document.querySelectorAll(".member").forEach((btn) => {
    btn.addEventListener("click", () => {
      const name = btn.dataset.name;
      const id = btn.dataset.id;

      personName.textContent = name;
      personInfo.textContent = "요약 정보를 불러오는 중...";

      // ✅ 요약 API 호출
      fetch(`/api/participant_summary/${id}`)
        .then((res) => {
          if (!res.ok) throw new Error("요약 정보를 불러오지 못했습니다.");
          return res.text(); // 혹은 res.json() if server returns structured data
        })
        .then((summary) => {
          personInfo.textContent = summary;
        })
        .catch(() => {
          personInfo.textContent = "요약 정보를 불러오는 데 실패했습니다.";
        });

      modal.style.display = "block";
    });
  });

  closeBtn.addEventListener("click", () => {
    modal.style.display = "none";
  });

  window.addEventListener("click", (e) => {
    if (e.target === modal) {
      modal.style.display = "none";
    }
  });
}

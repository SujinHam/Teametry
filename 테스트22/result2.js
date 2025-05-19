document.addEventListener("DOMContentLoaded", () => {
  const teamBox = document.getElementById("team-box");
  const urlParams = new URLSearchParams(window.location.search);
  const teamId = urlParams.get("team");

  if (!teamId) {
    teamBox.innerHTML = "<p>팀 정보가 없습니다.</p>";
    return;
  }

  fetch(`/api/teams/${teamId}`)
    .then((res) => {
      if (!res.ok) throw new Error("서버 응답 오류");
      return res.json();
    })
    .then((team) => {
      // 1. 팀 UI 구성
      teamBox.innerHTML = `
        <h3>${team.teamName}</h3>
        <ul>
          <li>
            <span class="leader">👑</span>
            <button class="member" data-name="${team.leader.name}" data-description="${team.leader.description}">
              ${team.leader.name}
            </button>
          </li>
          ${team.members.map((m) => `
            <li>
              <button class="member" data-name="${m.name}" data-description="${m.description}">
                ${m.name}
              </button>
            </li>
          `).join("")}
        </ul>
      `;

      // 2. 모달 리스너 연결
      attachModalListeners();
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
      const description = btn.dataset.description || "아직 등록된 설명이 없습니다.";
      personName.textContent = name;
      personInfo.textContent = description;
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

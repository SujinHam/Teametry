let mode = "";

function goCreate() {
  window.location.href = "create.html";
}

function startListFlow() {
  mode = "list";
  openModal("room-code-box");
}

function startJoinFlow() {
  mode = "join";
  openModal("room-code-box");
}

// ✅ 공통 모달 열기
function openModal(id) {
  document.getElementById("modal-backdrop").classList.remove("hidden");
  document.getElementById(id).classList.remove("hidden");
}

// ✅ 공통 모달 닫기
function closeModal() {
  document.getElementById("modal-backdrop").classList.add("hidden");
  document.getElementById("room-code-box").classList.add("hidden");
  document.getElementById("password-box").classList.add("hidden");
}

// ✅ ESC 키로 모달 닫기
document.addEventListener("keydown", (e) => {
  if (e.key === "Escape") {
    closeModal();
  }
});

function submitRoomCode() {
  const code = document.getElementById("roomCodeInput").value.trim();
  if (!code) {
    alert("방 코드를 입력하세요.");
    return;
  }

  if (mode === "join") {
    window.location.href = "join.html?code=" + encodeURIComponent(code);
  } else if (mode === "list") {
    localStorage.setItem("roomCode", code);
    document.getElementById("room-code-box").classList.add("hidden");
    document.getElementById("password-box").classList.remove("hidden");
  }
}

function goToResult() {
  const code = localStorage.getItem("roomCode");
  const pw = document.getElementById("passwordInput").value.trim();

  fetch(`/api/rooms/${encodeURIComponent(code)}/verify`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ password: pw }),
  })
    .then((res) => {
      if (!res.ok) {
        throw new Error("비밀번호가 틀렸거나 방이 존재하지 않습니다.");
      }
      return res.json();
    })
    .then((data) => {
      window.location.href = `status.html?code=${encodeURIComponent(code)}&pw=${encodeURIComponent(pw)}`;
    })
    .catch((err) => {
      alert("비밀번호가 틀렸거나 유효하지 않은 방 코드입니다.");
      console.error(err);
    });
}

let mode = "";

function goCreate() {
  window.location.href = "create.html";
}

function startListFlow() {
  mode = "list";
  document.getElementById("room-code-box").classList.remove("hidden");
  document.getElementById("password-box").classList.add("hidden");
}

function startJoinFlow() {
  mode = "join";
  document.getElementById("room-code-box").classList.remove("hidden");
  document.getElementById("password-box").classList.add("hidden");
}

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

  // 🔽 서버에 방 코드 + 비밀번호 검증 요청
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
      // 성공 시 → 결과 페이지로 이동
      window.location.href = `status.html?code=${encodeURIComponent(code)}&pw=${encodeURIComponent(pw)}`;
    })
    .catch((err) => {
      alert("비밀번호가 틀렸거나 유효하지 않은 방 코드입니다.");
      console.error(err);
    });
}

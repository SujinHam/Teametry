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
  const pw = document.getElementById("passwordInput").value.trim();
  const code = localStorage.getItem("roomCode");
  if (!pw) {
    alert("비밀번호를 입력하세요.");
    return;
  }
  window.location.href = `result.html?code=${encodeURIComponent(code)}&pw=${encodeURIComponent(pw)}`;
}

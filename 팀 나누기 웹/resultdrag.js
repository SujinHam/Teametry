document.addEventListener("DOMContentLoaded", () => {
    const members = document.querySelectorAll(".member");
    const columns = document.querySelectorAll(".team-column");

    // 드래그 시작
    members.forEach((member) => {
        member.addEventListener("dragstart", (e) => {
            e.dataTransfer.setData("text/html", e.target.outerHTML);
            e.dataTransfer.effectAllowed = "move";
            e.target.classList.add("dragging");
        });

        member.addEventListener("dragend", () => {
            member.classList.remove("dragging");
        });
    });

    // 각 조 영역에 드롭 허용
    columns.forEach((column) => {
        column.addEventListener("dragover", (e) => {
            e.preventDefault(); // 기본 이벤트 막아야 drop 가능
            e.dataTransfer.dropEffect = "move";
        });

        column.addEventListener("drop", (e) => {
            e.preventDefault();

            const draggedHTML = e.dataTransfer.getData("text/html");

            // 현재 드래그된 요소 제거
            const dragging = document.querySelector(".dragging");
            if (dragging) {
                dragging.remove();
            }

            // 드롭 위치에 추가
            column.insertAdjacentHTML("beforeend", draggedHTML);

            // 새롭게 추가된 요소에도 이벤트 다시 연결
            const newMember = column.lastElementChild;
            addDragEventToMember(newMember);
        });
    });

    // 동적으로 추가된 member에도 이벤트 붙이기 위한 함수
    function addDragEventToMember(member) {
        member.addEventListener("dragstart", (e) => {
            e.dataTransfer.setData("text/html", e.target.outerHTML);
            e.dataTransfer.effectAllowed = "move";
            e.target.classList.add("dragging");
        });

        member.addEventListener("dragend", () => {
            member.classList.remove("dragging");
        });
    }
});

console.log("✅ resultdrag.js 연결 완료");


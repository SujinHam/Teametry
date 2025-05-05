const members = document.querySelectorAll('.member');
const modal = document.getElementById('modal');
const personName = document.getElementById('person-name');
const personInfo = document.getElementById('person-info');
const closeBtn = document.getElementById('closeBtn');

// 인물 설명 사전
const infoMap = {
  '홍길동': '리더십이 강한 조장입니다. 개발과 발표에 모두 능합니다.',
  '신짱구': '엉뚱하지만 창의적인 아이디어가 많은 친구입니다.',
  '고길동': '꼼꼼하게 정리를 잘하고 지원 역할에 뛰어납니다.'
};

members.forEach(member => {
  member.addEventListener('click', () => {
    const name = member.dataset.name;
    personName.textContent = name;
    personInfo.textContent = infoMap[name] || '설명이 없습니다.';
    modal.style.display = 'block';
  });
});

closeBtn.addEventListener('click', () => {
  modal.style.display = 'none';
});

window.addEventListener('click', e => {
  if (e.target === modal) {
    modal.style.display = 'none';
  }
});

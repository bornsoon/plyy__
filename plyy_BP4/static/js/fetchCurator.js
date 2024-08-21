// 큐레이터 카드
function fetchCurator(api_route) {
    const sessionId = document.getElementById('session-data').getAttribute('data-session-id');
    fetch(api_route)
    .then(response => response.json())
    .then(data => {
        data.forEach((c, index) => {
            let updateTagId = 'updateTag' + index;
            let curatorTagId1 = 'curatorTag1' + index;
            let curatorTagId2 = 'curatorTag2' + index;
            const curatorCard = document.createElement('li');
            curatorCard.innerHTML =
                `<a href="/curator/${c.id}">` +
                    '<div class="curator-card__top">' +
                        `<img src="/static/cardimage/${c.img}" alt="" class="curator-card__top__img">` +
                        `<div id="${updateTagId}" class="badge green"><span class="hide">UPDATE</span>UPDATE</div>` +
                        '<div class="curator-card__top__tag-list">' +
                            `<div id="${curatorTagId1}" class="badge tag"></div>` +
                            `<div id="${curatorTagId2}" class="badge tag"></div>` +
                        '</div>' +
                        `<button class="btn-clike--${c.cliked ? 'fill' : 'unfill'}" id="like-${c.id}" aria-label="큐레이터 좋아요 즐겨찾기"></button>` +
                    '</div>' +
                    '<div class="curator-card__bottom">' +
                        '<div>' +
                            `<div class="curator-card__bottom__title fs16"><span class="hide">${c.name}</span>${c.name}</div>` +
                            '<div class="align both">' +
                                `<div class="curator-card__bottom__intro fs12"><span class="hide">${c.intro}</span>${c.intro}</div>` +
                            '</div>' +
                        '</div>' +
                    '</div>' +
                '</a>';
            mainList.appendChild(curatorCard); 
            
            // UPDATE 태그
            let updateTag = document.getElementById(updateTagId);
            let isUpdate = isTag(c.generate, c.update);
            if (!(isUpdate)) {
                updateTag.style.visibility = "hidden";
            };
            
            // 큐레이터의 플리 태그 2개까지
            let curatorTag1 = document.getElementById(curatorTagId1);
            let curatorTag2 = document.getElementById(curatorTagId2);
            let tag = [curatorTag1, curatorTag2];
            if (c.tag == '') {
                tag[0].style.visibility = "hidden";
                tag[1].style.visibility = "hidden";
            }
            c.tag.forEach((element, index) => {
                if (element == '') {
                    tag[index].style.visibility = "hidden";
                } else {
                    tag[index].textContent = '#' + element;
                    tag[index].setAttribute('onclick' , `location.href="/search/curator?q=%23+${element}"`);
                };
                tag[index].addEventListener('click', function(event) {
                    event.preventDefault();
                })
            });


            // 큐레이터 좋아요 버튼 클릭 이벤트 처리
            const likeButton = document.getElementById(`like-${c.id}`);
            likeButton.addEventListener('click', function(event) {
                event.preventDefault();
                const cid = c.id;
                if (sessionId) {
                    CuratorToggleLike(sessionId, cid);
                } else {
                    const modal = document.getElementById('logineed')
                    modal.classList.remove('hide');
                    modal.style.display = 'flex'; // 모달을 화면에 표시
                    modal.style.position = 'fixed';
                    modal.style.top = '45%'; // 화면 중앙에 위치
                    modal.style.left = '50%'; // 화면 중앙에 위치
                    modal.style.transform = 'translate(-50%, -50%)'; // 중앙 정렬
                }
            });
        });
    })
    .catch(error => console.error('데이터를 처리하는 과정에서 오류가 발생하였습니다.', error))
};
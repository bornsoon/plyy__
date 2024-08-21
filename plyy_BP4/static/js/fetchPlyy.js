// 플리 카드
function fetchPlyy(api_route) {
    const sessionId = document.getElementById('session-data').getAttribute('data-session-id');
    fetch(api_route)
    .then(response => response.json())
    .then(data => {
        data.forEach((plyy, index) => {
            let dateTagId = 'dateTag' + index;
            let plyyTagId = 'plyyTag' + index;
            const plyyCard = document.createElement('li');
            plyyCard.innerHTML = 
                `<a href="/plyy/${plyy.id}">` +
                    '<div class="plyy-card__top">' +
                        `<img src="/static/cardimage/${plyy.img}" alt="" class="plyy-card__top__img">` +
                        `<div id="${dateTagId}" class="badge green"></div>` + 
                        '<div class="plyy-card__top__tag-list">' +
                            `<div id="genreTag" class="badge tag" onclick='location.href="/search/plyy?q=%23+${plyy.genre}"'># ${plyy.genre}</div>` +
                            `<div id="${plyyTagId}" class="badge tag"></div>` +
                        '</div>' +
                        `<button class="btn-plike--${plyy.pliked ? 'fill' : 'unfill'}" id="like-${plyy.id}" aria-label="플레이리스트 좋아요 즐겨찾기"></button>` +
                    '</div>' +
                    '<div class="plyy-card__bottom">' +
                        '<div>' +
                            `<div class="plyy-card__bottom__title fs16"><span class="hide">${plyy.title}</span>${plyy.title}</div>` +
                            '<div class="align both">' +
                                `<div class="plyy-card__bottom--cname fs12"><span class="hide">${plyy.curator}</span>${plyy.curator}</div>` +
                                `<div class="plyy-card__bottom--count fs12"><span class="hide">${plyy.tracks}곡 | ${plyy_time(plyy.times)}</span>${plyy.tracks}곡 | ${plyy_time(plyy.times)}</div>` +
                            '</div>' +
                        '</div>' +
                    '</div>' +
                '</a>';
            mainList.appendChild(plyyCard);

            // NEW | UPDATE 태그
            let dateTag = document.getElementById(dateTagId);
            isDate = isTag(plyy.generate, plyy.update);
            if (isDate) {
                dateTag.innerHTML = '<span class="hide">' + isDate + '</span>' + isDate;
            } else {
                dateTag.style.visibility = "hidden";
            };
            
            // 플리태그 2개까지
            let plyy_tag = document.getElementById(plyyTagId);
            let genre_tag = document.getElementById("genreTag");
            if (plyy.tag) {
                plyy_tag.textContent = '#' + plyy.tag;
                plyy_tag.setAttribute('onclick' , `location.href="/search/plyy?q=%23+${plyy.tag}"`);
            } else {
                plyy_tag.style.visibility = "hidden";
            };
            genre_tag.addEventListener('click', function(event) {
                event.preventDefault();
            })
            plyy_tag.addEventListener('click', function(event) {
                event.preventDefault();
            })

            // 플레이리스트 좋아요 버튼 클릭 이벤트 처리
            const likeButton = document.getElementById(`like-${plyy.id}`);
            likeButton.addEventListener('click', function(event) {
                event.preventDefault();
                const pid = plyy.id;
                if (sessionId) {
                    PlaylistToggleLike(sessionId, pid);
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
    .catch(error => console.error('데이터를 처리하는 과정에서 오류가 발생하였습니다.', error));
};

//플로팅 바 클릭처리
document.addEventListener('DOMContentLoaded', () => {
    const back = document.querySelector('.floating-song .btn__float__arrow__left')
    const share = document.querySelector('.floating-song .btn__float__share--black');
    let tostMessage = document.getElementById('tost_message');

    let url = window.location.href.split('/')
    let plyyId = url[url.length - 2]
    
    back.addEventListener('click',function() {
        window.location.href=`/plyy/${plyyId}`
    })

    //2. 토스트 메시지 노출-사라짐 함수 작성
    function tostOn(){
        navigator.clipboard.writeText(window.location.href)
        tostMessage.classList.add('active');
        setTimeout(function(){
            tostMessage.classList.remove('active');
        },1000);
    }

    //3. 토스트 버튼에 이벤트 연결
    share.addEventListener('click',function(){
        tostOn()
    });

});
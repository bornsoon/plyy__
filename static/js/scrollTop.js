document.addEventListener('DOMContentLoaded', () => {
    const scrollToTopButton = document.querySelector('.fixed-floating .btn__main__arrow');

    // Scroll to top on button click
    scrollToTopButton.addEventListener('click', () => {
        window.scrollTo({
            top: 0,
            behavior: 'smooth' // 부드럽게 스크롤
        });
    });
});
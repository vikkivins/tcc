
document.addEventListener('DOMContentLoaded', function() {
    const mainAddButton = document.getElementById('mainAddButton');
    const optionButtons = document.getElementById('optionButtons');

    mainAddButton.addEventListener('click', function() {
        this.classList.toggle('active');
        optionButtons.classList.toggle('active');
    });
    
    // Inicializar o Swiper para os livros
    var livrosSwiper = new Swiper(".livros-swiper", {
        effect: "coverflow",
        grabCursor: true,
        centeredSlides: true,
        slidesPerView: "auto",
        coverflowEffect: {
            rotate: 0,
            stretch: 0,
            depth: 100,
            modifier: 2,
            slideShadows: true
        },
        spaceBetween: 60,
        loop: true,
        pagination: {
            el: ".livros-swiper .swiper-pagination",
            clickable: true
        }
    });
    
    // Inicializar o Swiper para as ideias
    var ideiasSwiper = new Swiper(".ideias-swiper", {
        effect: "coverflow",
        grabCursor: true,
        centeredSlides: true,
        slidesPerView: "auto",
        coverflowEffect: {
            rotate: 0,
            stretch: 0,
            depth: 100,
            modifier: 2,
            slideShadows: true
        },
        spaceBetween: 60,
        loop: true,
        pagination: {
            el: ".ideias-swiper .swiper-pagination",
            clickable: true
        }
    });
    
    // Adicionar evento de clique para navegar para a página do livro/ideia
    const livroSlides = document.querySelectorAll('.livros-swiper .swiper-slide');
    livroSlides.forEach((slide) => {
        slide.addEventListener('click', function() {
            if (this.classList.contains('swiper-slide-active')) {
                const livroId = this.getAttribute('data-id');
                window.location.href = this.getAttribute('data-url');
            }
        });
    });

    const ideiaSlides = document.querySelectorAll('.ideias-swiper .swiper-slide');
    ideiaSlides.forEach((slide) => {
        slide.addEventListener('click', function() {
            if (this.classList.contains('swiper-slide-active')) {
                const ideiaId = this.getAttribute('data-id');
                window.location.href = this.getAttribute('data-url');
            }
        });
    });
});
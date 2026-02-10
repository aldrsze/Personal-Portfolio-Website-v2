// Mobile Menu
const mobileMenuBtn = document.querySelector('.mobile-menu-btn');
const navigation = document.querySelector('.navigation');
const menuOverlay = document.querySelector('.menu-overlay');
const navClose = document.querySelector('.nav-close');
const navLinks = document.querySelectorAll('.navigation a');
const mobileContactBtn = document.querySelector('.mobile-contact');

function openMenu() {
    navigation.classList.add('active');
    menuOverlay.classList.add('active');
    mobileMenuBtn.classList.add('active');
    document.body.style.overflow = 'hidden';
}

function closeMenu() {
    navigation.classList.remove('active');
    menuOverlay.classList.remove('active');
    mobileMenuBtn.classList.remove('active');
    document.body.style.overflow = '';
}

// Toggle menu
mobileMenuBtn.addEventListener('click', function() {
    if (navigation.classList.contains('active')) {
        closeMenu();
    } else {
        openMenu();
    }
});

// Close menu events
menuOverlay.addEventListener('click', closeMenu);
navClose.addEventListener('click', closeMenu);
mobileContactBtn.addEventListener('click', closeMenu);

navLinks.forEach(function(link) {
    link.addEventListener('click', closeMenu);
});

// Close menu on window resize
window.addEventListener('resize', function() {
    if (window.innerWidth > 768) {
        closeMenu();
    }
});

// Certificate Carousel
function scrollCert(direction) {
    const slider = document.getElementById('cert-slider');
    const cardWidth = slider.querySelector('.cert-card').offsetWidth;
    const gap = 30;
    const isMobile = window.innerWidth <= 768;
    const scrollAmount = isMobile ? (cardWidth + gap) : (cardWidth + gap) * 2; // 1 image on mobile, 2 on desktop
    
    if (direction === 1) {
        // Going right
        if (slider.scrollLeft + slider.offsetWidth >= slider.scrollWidth - 10) {
            slider.scrollTo({ left: 0, behavior: 'smooth' });
        } else {
            slider.scrollBy({ left: scrollAmount, behavior: 'smooth' });
        }
    } else {
        // Going left
        if (slider.scrollLeft <= 10) {
            slider.scrollTo({ left: slider.scrollWidth, behavior: 'smooth' });
        } else {
            slider.scrollBy({ left: -scrollAmount, behavior: 'smooth' });
        }
    }
}

const observerOptions = {
    root: null,
    rootMargin: '-20% 0px -70% 0px', 
    threshold: 0
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        const id = entry.target.getAttribute('id');
        const navLink = document.querySelector(`.navigation a[href="#${id}"]`);
        
        if (entry.isIntersecting) {
            // Remove active from all links first
            document.querySelectorAll('.navigation a').forEach(link => {
                link.classList.remove('active');
            });
            
            // Add active to the current link
            if (navLink) navLink.classList.add('active');
        }
    });
}, observerOptions);

// Track every section that has an ID
document.querySelectorAll('section[id]').forEach(section => {
    observer.observe(section);
});

// Extra check for the very top of the page
window.addEventListener('scroll', () => {
    if (window.scrollY < 50) {
        document.querySelectorAll('.navigation a').forEach(link => {
            link.classList.remove('active');
            if (link.getAttribute('href') === '#home') {
                link.classList.add('active');
            }
        });
    }
});
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
    link.addEventListener('click', function(e) {
        e.preventDefault();
        const targetId = this.getAttribute('href').substring(1);
        showSection(targetId);
        closeMenu();
    });
});

// Close menu on window resize
window.addEventListener('resize', function() {
    if (window.innerWidth > 768) {
        closeMenu();
    }
});

// Section Switching
function showSection(sectionId) {
    // Hide all sections
    document.querySelectorAll('section').forEach(section => {
        section.classList.remove('active-section');
    });
    
    // Show target section
    const targetSection = document.getElementById(sectionId);
    if (targetSection) {
        targetSection.classList.add('active-section');
    }
    
    // Update active navigation link
    document.querySelectorAll('.navigation a').forEach(link => {
        link.classList.remove('active');
        if (link.getAttribute('href') === '#' + sectionId) {
            link.classList.add('active');
        }
    });
}

// Initialize - show home section by default
document.addEventListener('DOMContentLoaded', function() {
    showSection('home');
    
    // Handle logo click
    const logo = document.querySelector('.logo a');
    if (logo) {
        logo.addEventListener('click', function(e) {
            e.preventDefault();
            showSection('home');
        });
    }
    
    // Handle "View Projects" button
    const viewProjectsBtn = document.querySelector('.view-projects-btn');
    if (viewProjectsBtn) {
        viewProjectsBtn.addEventListener('click', function() {
            // Navigate to projects if exists, otherwise go to skills
            const projectsSection = document.getElementById('projects');
            showSection(projectsSection ? 'projects' : 'skills');
        });
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
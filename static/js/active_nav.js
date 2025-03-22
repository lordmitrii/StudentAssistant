document.addEventListener("DOMContentLoaded", function() {
    const currentPath = window.location.pathname;
    
    const navLinks = document.querySelectorAll('.navbar-nav .nav-link');
    
    navLinks.forEach(link => {
        const linkHref = link.getAttribute('href');
        
        if ((linkHref === '/' || linkHref.includes('home')) && 
            (currentPath === '/' || currentPath === '/assistant_app/')) {
            link.classList.add('active');
        }
        else if (currentPath.includes('courses') && linkHref.includes('courses')) {
            link.classList.add('active');
        }
        else if (currentPath.includes('calculator') && linkHref.includes('calculator')) {
            link.classList.add('active');
        }
        else if (currentPath.includes('about') && linkHref.includes('about')) {
            link.classList.add('active');
        }
        else if (currentPath.includes('account') && linkHref.includes('account')) {
            link.classList.add('active');
        }
        else if (currentPath.includes('login') && linkHref.includes('login')) {
            link.classList.add('active');
        }
    });
});
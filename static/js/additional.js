const navLinks = document.querySelectorAll('.nav-link');

// Add click event listener to each link
navLinks.forEach(link => {
    link.addEventListener('click', function() {
        // Remove the 'active' class from all links
        navLinks.forEach(link => {
            link.parentElement.classList.remove('active');
        });

        // Add the 'active' class to the clicked link's parent element
        this.parentElement.classList.add('active');
    });
});
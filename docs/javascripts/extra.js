// Make site title clickable to go home
document.addEventListener('DOMContentLoaded', function() {
    // Get the site title element (first topic)
    const siteTitleElement = document.querySelector('.md-header__topic:first-child .md-ellipsis');
    
    if (siteTitleElement) {
        // Make it clickable
        siteTitleElement.style.cursor = 'pointer';
        siteTitleElement.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            // Navigate to home, adjusting for base URL
            const baseUrl = document.querySelector('base')?.getAttribute('href') || '/';
            window.location.href = baseUrl;
        });
    }
});
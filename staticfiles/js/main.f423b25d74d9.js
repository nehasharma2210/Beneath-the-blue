// Main JavaScript for Beneath the Blue

// Tab functionality for homepage forms
function setupTabs() {
    const tabButtons = document.querySelectorAll('.tab-button');
    
    tabButtons.forEach(button => {
        button.addEventListener('click', function() {
            console.log('Tab clicked:', this.dataset.tab); // Debug log
            
            // Remove active class from all buttons and content
            document.querySelectorAll('.tab-button').forEach(btn => {
                btn.classList.remove('active');
            });
            document.querySelectorAll('.tab-content').forEach(content => {
                content.classList.remove('active');
            });
            
            // Add active class to clicked button and corresponding content
            this.classList.add('active');
            const tabId = this.getAttribute('data-tab');
            const content = document.getElementById(tabId);
            if (content) {
                content.classList.add('active');
                console.log('Switched to tab:', tabId);
            } else {
                console.error('No content found for tab:', tabId);
            }
        });
    });
}

// Smooth scrolling
function setupSmoothScrolling() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            
            const targetId = this.getAttribute('href');
            if (targetId === '#') return;
            
            const targetElement = document.querySelector(targetId);
            if (targetElement) {
                window.scrollTo({
                    top: targetElement.offsetTop - 80,
                    behavior: 'smooth'
                });
            }
        });
    });
}

// Video autoplay
function setupVideoAutoplay() {
    const video = document.getElementById('fullpage-video-bg');
    if (video) {
        video.play().catch(error => {
            console.log('Video autoplay prevented:', error);
        });
    }
}

// Navbar hide/show on scroll
function setupNavbarScroll() {
    const header = document.querySelector('header');
    let lastScroll = 0;
    const scrollThreshold = 100; // How far to scroll before hiding
    
    window.addEventListener('scroll', function() {
        const currentScroll = window.pageYOffset;
        
        if (currentScroll <= 0) {
            // At top of page - always show header
            header.classList.remove('hide');
            return;
        }
        
        if (currentScroll > lastScroll && currentScroll > scrollThreshold) {
            // Scrolling down and past threshold - hide header
            header.classList.add('hide');
        } else if (currentScroll < lastScroll) {
            // Scrolling up - show header
            header.classList.remove('hide');
        }
        
        lastScroll = currentScroll;
    });
}

function setupFormHandlers() {
    document.querySelectorAll('.action-form').forEach(form => {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            const url = this.dataset.submitUrl;
            const formData = new FormData(this);
            
            // Show loading state
            const submitBtn = this.querySelector('button[type="submit"]');
            const originalText = submitBtn.innerHTML;
            submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Submitting...';
            submitBtn.disabled = true;
            
            fetch(url, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': getCookie('csrftoken')
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Show success message
                    this.innerHTML = `<div class="success-message"><i class="fas fa-check-circle"></i> ${data.message}</div>`;
                    // Reset form after 3 seconds
                    setTimeout(() => {
                        this.reset();
                        this.innerHTML = originalText;
                        submitBtn.disabled = false;
                    }, 3000);
                } else {
                    // Show error messages
                    let errorHtml = '<div class="error-messages">';
                    for (const [field, errors] of Object.entries(data.errors)) {
                        errorHtml += `<div class="error"><strong>${field}:</strong> ${errors.join(', ')}</div>`;
                    }
                    errorHtml += '</div>';
                    
                    // Insert errors at top of form
                    this.insertAdjacentHTML('afterbegin', errorHtml);
                    
                    // Remove error messages after 5 seconds
                    setTimeout(() => {
                        const errorDiv = this.querySelector('.error-messages');
                        if (errorDiv) errorDiv.remove();
                    }, 5000);
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('An error occurred. Please try again.');
            })
            .finally(() => {
                // Reset button state
                submitBtn.innerHTML = originalText;
                submitBtn.disabled = false;
            });
        });
    });
}

// Initialize all functionality
document.addEventListener('DOMContentLoaded', function() {
    setupTabs();
    setupSmoothScrolling();
    setupVideoAutoplay();
    setupNavbarScroll();
    setupFormHandlers();
    setupLikeButtons();
});

// Like button functionality - runs after DOM is loaded
function setupLikeButtons() {
    document.querySelectorAll('.like-btn').forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            const postId = this.dataset.postId;
            
            console.log('Like button clicked for post:', postId); // Debug log
            
            fetch(`/posts/${postId}/like/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'),
                    'Content-Type': 'application/x-www-form-urlencoded'
                },
                credentials: 'same-origin'
            })
            .then(response => {
                console.log('Response status:', response.status); // Debug log
                return response.json();
            })
            .then(data => {
                console.log('Response data:', data); // Debug log
                const icon = this.querySelector('i');
                const countSpan = this.querySelector('.like-count');
                
                if (data.liked) {
                    icon.className = 'fas fa-thumbs-up liked';
                    this.style.color = '#e74c3c';
                } else {
                    icon.className = 'far fa-thumbs-up';
                    this.style.color = '';
                }
                countSpan.textContent = data.total_likes;
            })
            .catch(error => {
                console.error('Like error:', error);
                alert('Error liking post. Please try again.');
            });
        });
    });
}

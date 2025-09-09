// Handle like button clicks
document.querySelectorAll('.like-btn').forEach(button => {
    button.addEventListener('click', function(e) {
        e.preventDefault();
        const postId = this.getAttribute('data-post-id');
        const icon = this.querySelector('i');
        const likeCount = this.querySelector('.like-count');

        fetch(`/posts/${postId}/like/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            credentials: 'same-origin',
        })
        .then(response => response.json())
        .then(data => {
            if (data.liked) {
                icon.className = 'fas fa-thumbs-up liked';
                this.style.color = '#e74c3c';
            } else {
                icon.className = 'far fa-thumbs-up';
                this.style.color = '';
            }
            likeCount.textContent = data.total_likes;
        })
        .catch(error => {
            console.error('Like error:', error);
            alert('Error liking post. Please try again.');
        });
    });
});

// Handle comment form submission
document.querySelectorAll('.comment-form').forEach(form => {
    form.addEventListener('submit', async function(e) {
        e.preventDefault();
        const formData = new FormData(this);
        const commentInput = this.querySelector('input[name="content"]');
        const commentsSection = this.closest('.comments-section');

        // Disable submit button and show feedback
        const submitBtn = this.querySelector('button[type="submit"]');
        const originalText = submitBtn.textContent;
        submitBtn.disabled = true;
        submitBtn.textContent = 'Posting...';

        try {
            const res = await fetch(this.action, {
                method: 'POST',
                body: formData,
                headers: { 'X-CSRFToken': getCookie('csrftoken') },
                credentials: 'same-origin'
            });
            const data = await res.json();
            if (!res.ok || !data.success) throw new Error(data.error || 'Failed to post');

            // Clear input
            commentInput.value = '';

            // Build new comment DOM
            const commentDiv = document.createElement('div');
            commentDiv.className = 'comment';
            commentDiv.innerHTML = `
                <div class="comment-author">${data.comment.author.charAt(0).toUpperCase()}</div>
                <div class="comment-content">
                    <strong>${data.comment.author}</strong>
                    <p>${data.comment.content}</p>
                    <small>just now</small>
                </div>
            `;

            // Insert new comment ABOVE the form (newest first)
            commentsSection.insertBefore(commentDiv, this);
        } catch (err) {
            console.error('Comment error:', err);
            alert('Error posting comment. Please try again.');
        } finally {
            submitBtn.disabled = false;
            submitBtn.textContent = originalText;
        }
    });
});

// Handle comment button toggle
document.querySelectorAll('.comment-btn').forEach(button => {
    button.addEventListener('click', function(e) {
        e.preventDefault();
        const postCard = this.closest('.post-card');
        const commentsSection = postCard.querySelector('.comments-section');

        // Toggle visibility
        if (commentsSection.style.display === 'none' || commentsSection.style.display === '') {
            commentsSection.style.display = 'block';
            this.style.color = '#3498db';
        } else {
            commentsSection.style.display = 'none';
            this.style.color = '';
        }
    });
});

// Initialize comment sections as hidden on page load
document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.comments-section').forEach(section => {
        section.style.display = 'none';
    });
});

// Helper function to get CSRF token
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

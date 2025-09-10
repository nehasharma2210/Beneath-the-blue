document.addEventListener('DOMContentLoaded', function() {
    // Media upload preview
    const mediaInput = document.getElementById('post-media');
    const mediaPreview = document.getElementById('media-preview');
    
    if (mediaInput && mediaPreview) {
        mediaInput.addEventListener('change', function(e) {
            mediaPreview.innerHTML = '';
            mediaPreview.style.display = 'none';
            
            const file = e.target.files[0];
            if (!file) return;
            
            const fileType = file.type.split('/')[0];
            const reader = new FileReader();
            
            reader.onload = function(e) {
                if (fileType === 'image') {
                    const img = document.createElement('img');
                    img.src = e.target.result;
                    mediaPreview.appendChild(img);
                } else if (fileType === 'video') {
                    const video = document.createElement('video');
                    video.src = e.target.result;
                    video.controls = true;
                    mediaPreview.appendChild(video);
                }
                mediaPreview.style.display = 'block';
            };
            
            reader.readAsDataURL(file);
        });
    }
    
    // Like functionality
    document.querySelectorAll('.like-btn').forEach(button => {
        button.addEventListener('click', function() {
            const postId = this.getAttribute('data-post-id');
            const likeCount = this.querySelector('.like-count');
            const isLiked = this.classList.contains('liked');
            
            fetch(/posts/${postId}/like/, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'),
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    action: isLiked ? 'unlike' : 'like'
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    likeCount.textContent = data.like_count;
                    this.classList.toggle('liked');
                }
            })
            .catch(error => console.error('Error:', error));
        });
    });
    
    // Comment functionality
    document.querySelectorAll('.comment-form').forEach(form => {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            const postId = this.getAttribute('data-post-id');
            const input = this.querySelector('input');
            const commentText = input.value.trim();
            
            if (!commentText) return;
            
            fetch(/posts/${postId}/comment/, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'),
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    text: commentText
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    input.value = '';
                    // In a real app, you would append the new comment to the DOM
                    location.reload(); // Simple refresh for demo
                }
            })
            .catch(error => console.error('Error:', error));
        });
    });
    
    // View all comments
    document.querySelectorAll('.view-all-comments').forEach(button => {
        button.addEventListener('click', function() {
            const postId = this.closest('.post').getAttribute('data-post-id');
            // In a real app, you would fetch all comments and display them
            window.location.href = /posts/${postId}/;
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
});
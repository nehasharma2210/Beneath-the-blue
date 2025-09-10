// Media upload preview
const mediaUpload = document.getElementById('mediaUpload');
const mediaInput = document.getElementById('postMedia');
const mediaPreview = document.getElementById('mediaPreview');

mediaUpload.addEventListener('click', function() {
    mediaInput.click();
});

mediaUpload.addEventListener('dragover', function(e) {
    e.preventDefault();
    this.style.borderColor = 'var(--secondary-color)';
});

mediaUpload.addEventListener('dragleave', function() {
    this.style.borderColor = '#ddd';
});

mediaUpload.addEventListener('drop', function(e) {
    e.preventDefault();
    this.style.borderColor = '#ddd';
    if (e.dataTransfer.files.length > 0) {
        mediaInput.files = e.dataTransfer.files;
        previewMedia();
    }
});

mediaInput.addEventListener('change', previewMedia);

function previewMedia() {
    mediaPreview.innerHTML = '';
    const files = mediaInput.files;
    
    for (let i = 0; i < files.length; i++) {
        const file = files[i];
        const reader = new FileReader();
        
        reader.onload = function(e) {
            const previewItem = document.createElement('div');
            previewItem.className = 'preview-item';
            
            if (file.type.startsWith('image/')) {
                previewItem.innerHTML = `
                    <img src="${e.target.result}" alt="Preview">
                    <div class="remove-btn" data-index="${i}">&times;</div>
                `;
            } else if (file.type.startsWith('video/')) {
                previewItem.innerHTML = `
                    <video controls>
                        <source src="${e.target.result}" type="${file.type}">
                    </video>
                    <div class="remove-btn" data-index="${i}">&times;</div>
                `;
            }
            
            mediaPreview.appendChild(previewItem);
            
            // Add remove functionality
            const removeBtn = previewItem.querySelector('.remove-btn');
            removeBtn.addEventListener('click', function(e) {
                e.stopPropagation();
                removeFile(parseInt(this.getAttribute('data-index')));
            });
        };
        
        reader.readAsDataURL(file);
    }
}

function removeFile(index) {
    const dt = new DataTransfer();
    const files = mediaInput.files;
    
    for (let i = 0; i < files.length; i++) {
        if (i !== index) {
            dt.items.add(files[i]);
        }
    }
    
    mediaInput.files = dt.files;
    previewMedia();
}
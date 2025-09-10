document.addEventListener('DOMContentLoaded', function() {
            const video = document.querySelector('.video-background');
            video.play().catch(e => {
                video.muted = true;
                video.play();
            });

            const quizForm = document.getElementById('quizForm');
            const summaryBtn = document.getElementById('summaryBtn');
            const summaryModal = document.getElementById('summaryModal');
            const closeSummary = document.getElementById('closeSummary');
            
            // Initially hide summary button
            summaryBtn.style.display = 'none';
            
            quizForm.addEventListener('submit', function(e) {
                e.preventDefault();
                
                // Show summary button
                summaryBtn.style.display = 'block';
                summaryBtn.scrollIntoView({ behavior: 'smooth' });
                
                // Calculate results (replace with your actual scoring logic)
                const totalQuestions = 10;
                let correctAnswers = 0;
                let attempted = 0;
                
                // Check each question (this is simplified - adapt to your needs)
                for (let i = 1; i <= totalQuestions; i++) {
                    const selectedOption = document.querySelector(`input[name="question_${i}"]:checked`);
                    if (selectedOption) {
                        attempted++;
                        // This assumes correct answers have value="2" - adjust based on your actual correct answers
                        if (selectedOption.value === "2") {
                            correctAnswers++;
                        }
                    }
                }
                
                // Update summary
                document.getElementById('totalQuestions').textContent = totalQuestions;
                document.getElementById('questionsAttempted').textContent = attempted;
                document.getElementById('correctAnswers').textContent = correctAnswers;
                document.getElementById('wrongAnswers').textContent = attempted - correctAnswers;
                document.getElementById('totalScore').textContent = correctAnswers;
            });
            
            summaryBtn.addEventListener('click', function() {
                summaryModal.style.display = 'flex';
            });
            
            closeSummary.addEventListener('click', function() {
                summaryModal.style.display = 'none';
            });
            
            window.addEventListener('click', function(e) {
                if (e.target === summaryModal) {
                    summaryModal.style.display = 'none';
                }
            });
        });
/* QuestMate - JavaScript Functions */

// Modal Functions
function openModal(modalId) {
    document.getElementById(modalId).style.display = "block";
}

function closeModal(modalId) {
    document.getElementById(modalId).style.display = "none";
}

// Close modal when clicking outside
window.onclick = function(event) {
    if (event.target.classList.contains('modal')) {
        event.target.style.display = "none";
    }
}

// Reset code textarea
function resetCode() {
    const textarea = document.querySelector('.submission-form textarea');
    if (textarea) {
        textarea.value = '';
        textarea.focus();
    }
}

// Form handling
document.addEventListener('DOMContentLoaded', function() {
    // Auto-hide alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.opacity = '0';
            alert.style.transition = 'opacity 0.3s ease';
            setTimeout(() => {
                alert.remove();
            }, 300);
        }, 5000);
    });

    // Smooth scroll for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth'
                });
            }
        });
    });
});

// API Helper Functions
async function apiCall(endpoint, method = 'GET', data = null) {
    const options = {
        method,
        headers: {
            'Content-Type': 'application/json',
        }
    };

    if (data) {
        options.body = JSON.stringify(data);
    }

    const token = localStorage.getItem('access_token');
    if (token) {
        options.headers['Authorization'] = `Bearer ${token}`;
    }

    try {
        const response = await fetch(`/api${endpoint}`, options);
        return await response.json();
    } catch (error) {
        console.error('API Error:', error);
        return { error: error.message };
    }
}

// Get user profile
async function getUserProfile() {
    const result = await apiCall('/user/profile');
    if (!result.error) {
        return result;
    }
    return null;
}

// Submit task code
async function submitCode(code) {
    const result = await apiCall('/task/submit', 'POST', { code });
    return result;
}

// Get available mentors
async function getMentors(skill) {
    const result = await apiCall(`/mentors/${skill}`);
    return result;
}

// Activate consistency shield
async function activateShield(reason, days) {
    const result = await apiCall('/shield/activate', 'POST', { reason, days });
    return result;
}

// Request mentorship
async function requestMentorship(mentorName, skill, topic) {
    const result = await apiCall(`/mentorship/request/${mentorName}`, 'POST', { skill, topic });
    return result;
}

// Get leaderboard
async function getLeaderboard(skill) {
    const result = await apiCall(`/leaderboard/${skill}`);
    return result;
}

// Keyboard shortcuts
document.addEventListener('keydown', function(event) {
    // Ctrl/Cmd + Enter to submit form
    if ((event.ctrlKey || event.metaKey) && event.key === 'Enter') {
        const form = document.querySelector('.submission-form');
        if (form) {
            form.submit();
        }
    }

    // Escape to close modals
    if (event.key === 'Escape') {
        document.querySelectorAll('.modal').forEach(modal => {
            modal.style.display = 'none';
        });
    }
});

// Logout
function logout() {
    localStorage.removeItem('access_token');
    window.location.href = '/logout';
}

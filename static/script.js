/**
 * HealthCare Symptom Checker - Frontend JavaScript
 * Handles form submission, API communication, and UI interactions
 */

// Global variables
let currentResults = null;
const API_BASE_URL = 'http://localhost:5000';

// DOM elements
const symptomForm = document.getElementById('symptomForm');
const resultsSection = document.getElementById('results');
const loadingOverlay = document.getElementById('loadingOverlay');
const summaryText = document.getElementById('summaryText');
const conditionsList = document.getElementById('conditionsList');
const actionsList = document.getElementById('actionsList');
const emergencyList = document.getElementById('emergencyList');

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

/**
 * Initialize the application
 */
function initializeApp() {
    // Set up form submission handler
    symptomForm.addEventListener('submit', handleFormSubmission);
    
    // Set up navigation
    setupNavigation();
    
    // Add smooth scrolling for navigation links
    setupSmoothScrolling();
    
    // Initialize form validation
    setupFormValidation();
    
    console.log('HealthCare Symptom Checker initialized successfully');
}

/**
 * Set up navigation functionality
 */
function setupNavigation() {
    const navLinks = document.querySelectorAll('.nav-link');
    const sections = document.querySelectorAll('section[id]');
    
    // Handle navigation link clicks
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href').substring(1);
            
            // Update active navigation link
            navLinks.forEach(l => l.classList.remove('active'));
            this.classList.add('active');
            
            // Scroll to target section
            const targetSection = document.getElementById(targetId);
            if (targetSection) {
                targetSection.scrollIntoView({ behavior: 'smooth' });
            }
        });
    });
    
    // Update active navigation based on scroll position
    window.addEventListener('scroll', function() {
        let current = '';
        sections.forEach(section => {
            const sectionTop = section.offsetTop;
            const sectionHeight = section.clientHeight;
            if (pageYOffset >= sectionTop - 200) {
                current = section.getAttribute('id');
            }
        });
        
        navLinks.forEach(link => {
            link.classList.remove('active');
            if (link.getAttribute('href') === `#${current}`) {
                link.classList.add('active');
            }
        });
    });
}

/**
 * Set up smooth scrolling for anchor links
 */
function setupSmoothScrolling() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

/**
 * Set up form validation
 */
function setupFormValidation() {
    const inputs = symptomForm.querySelectorAll('input, select, textarea');
    
    inputs.forEach(input => {
        input.addEventListener('blur', validateField);
        input.addEventListener('input', clearFieldError);
    });
}

/**
 * Validate individual form field
 */
function validateField(event) {
    const field = event.target;
    const value = field.value.trim();
    const fieldName = field.name;
    
    // Remove existing error styling
    clearFieldError(event);
    
    // Validate based on field type
    let isValid = true;
    let errorMessage = '';
    
    switch (fieldName) {
        case 'age':
            if (!value || value < 1 || value > 120) {
                isValid = false;
                errorMessage = 'Please enter a valid age between 1 and 120';
            }
            break;
            
        case 'gender':
            if (!value) {
                isValid = false;
                errorMessage = 'Please select your gender';
            }
            break;
            
        case 'symptoms':
            if (!value || value.length < 10) {
                isValid = false;
                errorMessage = 'Please describe your symptoms in detail (at least 10 characters)';
            }
            break;
            
        case 'duration':
            if (!value) {
                isValid = false;
                errorMessage = 'Please select the duration of your symptoms';
            }
            break;
            
        case 'severity':
            if (!document.querySelector('input[name="severity"]:checked')) {
                isValid = false;
                errorMessage = 'Please select the severity level';
            }
            break;
    }
    
    if (!isValid) {
        showFieldError(field, errorMessage);
    }
    
    return isValid;
}

/**
 * Show field error message
 */
function showFieldError(field, message) {
    // Remove existing error message
    const existingError = field.parentNode.querySelector('.error-message');
    if (existingError) {
        existingError.remove();
    }
    
    // Add error styling
    field.style.borderColor = '#e53e3e';
    
    // Create and add error message
    const errorDiv = document.createElement('div');
    errorDiv.className = 'error-message';
    errorDiv.style.color = '#e53e3e';
    errorDiv.style.fontSize = '0.875rem';
    errorDiv.style.marginTop = '0.25rem';
    errorDiv.textContent = message;
    
    field.parentNode.appendChild(errorDiv);
}

/**
 * Clear field error styling
 */
function clearFieldError(event) {
    const field = event.target;
    field.style.borderColor = '#e2e8f0';
    
    const errorMessage = field.parentNode.querySelector('.error-message');
    if (errorMessage) {
        errorMessage.remove();
    }
}

/**
 * Handle form submission
 */
async function handleFormSubmission(event) {
    event.preventDefault();
    
    // Validate all fields
    const inputs = symptomForm.querySelectorAll('input, select, textarea');
    let isValid = true;
    
    inputs.forEach(input => {
        if (!validateField({ target: input })) {
            isValid = false;
        }
    });
    
    if (!isValid) {
        showNotification('Please fill in all required fields correctly', 'error');
        return;
    }
    
    // Collect form data
    const formData = new FormData(symptomForm);
    const symptomData = {
        age: parseInt(formData.get('age')),
        gender: formData.get('gender'),
        symptoms: formData.get('symptoms'),
        duration: formData.get('duration'),
        severity: formData.get('severity')
    };
    
    try {
        // Show loading state
        showLoading(true);
        
        // Send data to backend
        const response = await analyzeSymptoms(symptomData);
        
        // Display results
        displayResults(response);
        
        // Hide loading state
        showLoading(false);
        
        // Scroll to results
        resultsSection.scrollIntoView({ behavior: 'smooth' });
        
        // Show success notification
        showNotification('Symptoms analyzed successfully!', 'success');
        
    } catch (error) {
        showLoading(false);
        console.error('Error analyzing symptoms:', error);
        showNotification('Error analyzing symptoms. Please try again.', 'error');
    }
}

/**
 * Send symptoms data to backend API
 */
async function analyzeSymptoms(symptomData) {
    try {
        const response = await fetch(`${API_BASE_URL}/api/analyze`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(symptomData)
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        return data;
        
    } catch (error) {
        console.error('API request failed:', error);
        throw new Error('Failed to connect to the symptom analyzer service');
    }
}

/**
 * Display analysis results
 */
function displayResults(results) {
    currentResults = results;
    
    // Update summary text
    summaryText.textContent = results.summary || 'Analysis complete';
    
    // Update possible conditions
    updateList(conditionsList, results.possible_conditions || []);
    
    // Update recommended actions
    updateList(actionsList, results.recommended_actions || []);
    
    // Update emergency warnings
    updateList(emergencyList, results.emergency_warnings || []);
    
    // Show results section with animation
    resultsSection.style.display = 'block';
    resultsSection.classList.add('fade-in');
    
    // Add slide-up animation to result details
    const resultDetails = resultsSection.querySelector('.result-details');
    resultDetails.classList.add('slide-up');
}

/**
 * Update list elements with new content
 */
function updateList(listElement, items) {
    listElement.innerHTML = '';
    
    if (items.length === 0) {
        const noItems = document.createElement('li');
        noItems.textContent = 'No specific information available';
        noItems.style.fontStyle = 'italic';
        noItems.style.color = '#718096';
        listElement.appendChild(noItems);
        return;
    }
    
    items.forEach(item => {
        const listItem = document.createElement('li');
        listItem.textContent = item;
        listElement.appendChild(listItem);
    });
}

/**
 * Show/hide loading overlay
 */
function showLoading(show) {
    if (show) {
        loadingOverlay.style.display = 'flex';
        document.body.style.overflow = 'hidden';
    } else {
        loadingOverlay.style.display = 'none';
        document.body.style.overflow = 'auto';
    }
}

/**
 * Save results to local storage
 */
function saveResults() {
    if (!currentResults) {
        showNotification('No results to save', 'warning');
        return;
    }
    
    try {
        const savedResults = JSON.parse(localStorage.getItem('savedResults') || '[]');
        const resultToSave = {
            ...currentResults,
            timestamp: new Date().toISOString(),
            id: Date.now()
        };
        
        savedResults.push(resultToSave);
        localStorage.setItem('savedResults', JSON.stringify(savedResults));
        
        showNotification('Results saved successfully!', 'success');
        
    } catch (error) {
        console.error('Error saving results:', error);
        showNotification('Failed to save results', 'error');
    }
}

/**
 * Reset form and hide results
 */
function resetForm() {
    // Reset form fields
    symptomForm.reset();
    
    // Clear any error styling
    const inputs = symptomForm.querySelectorAll('input, select, textarea');
    inputs.forEach(input => {
        input.style.borderColor = '#e2e8f0';
        const errorMessage = input.parentNode.querySelector('.error-message');
        if (errorMessage) {
            errorMessage.remove();
        }
    });
    
    // Hide results section
    resultsSection.style.display = 'none';
    resultsSection.classList.remove('fade-in');
    
    // Clear current results
    currentResults = null;
    
    // Scroll to form
    document.getElementById('checker').scrollIntoView({ behavior: 'smooth' });
    
    showNotification('Form reset successfully', 'info');
}

/**
 * Show notification message
 */
function showNotification(message, type = 'info') {
    // Remove existing notifications
    const existingNotifications = document.querySelectorAll('.notification');
    existingNotifications.forEach(notification => notification.remove());
    
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 1rem 1.5rem;
        border-radius: 10px;
        color: white;
        font-weight: 500;
        z-index: 10000;
        max-width: 400px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
        transform: translateX(100%);
        transition: transform 0.3s ease;
    `;
    
    // Set background color based on type
    const colors = {
        success: '#48bb78',
        error: '#f56565',
        warning: '#ed8936',
        info: '#4299e1'
    };
    
    notification.style.backgroundColor = colors[type] || colors.info;
    notification.textContent = message;
    
    // Add to page
    document.body.appendChild(notification);
    
    // Animate in
    setTimeout(() => {
        notification.style.transform = 'translateX(0)';
    }, 100);
    
    // Auto-remove after 5 seconds
    setTimeout(() => {
        notification.style.transform = 'translateX(100%)';
        setTimeout(() => {
            if (notification.parentNode) {
                notification.parentNode.removeChild(notification);
            }
        }, 300);
    }, 5000);
}

/**
 * Utility function to format date
 */
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
}

/**
 * Handle window resize for responsive design
 */
window.addEventListener('resize', function() {
    // Add any responsive behavior here if needed
    console.log('Window resized');
});

/**
 * Add keyboard shortcuts
 */
document.addEventListener('keydown', function(event) {
    // Ctrl/Cmd + Enter to submit form
    if ((event.ctrlKey || event.metaKey) && event.key === 'Enter') {
        if (symptomForm.contains(document.activeElement)) {
            handleFormSubmission(new Event('submit'));
        }
    }
    
    // Escape key to close loading overlay
    if (event.key === 'Escape') {
        if (loadingOverlay.style.display === 'flex') {
            showLoading(false);
        }
    }
});

// Export functions for potential external use
window.HealthCareChecker = {
    analyzeSymptoms,
    saveResults,
    resetForm,
    showNotification
};

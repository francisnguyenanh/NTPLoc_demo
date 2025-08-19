// JavaScript for Idle Management System

// Global functions
function showAlert(type, message, duration = 5000) {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    const main = document.querySelector('main');
    main.insertBefore(alertDiv, main.firstChild);
    
    // Auto dismiss after duration
    setTimeout(() => {
        if (alertDiv.parentNode) {
            alertDiv.remove();
        }
    }, duration);
}

// Loading spinner
function showLoading(element) {
    const originalContent = element.innerHTML;
    element.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Đang xử lý...';
    element.disabled = true;
    
    return () => {
        element.innerHTML = originalContent;
        element.disabled = false;
    };
}

// Form validation
function validateForm(formElement) {
    const requiredFields = formElement.querySelectorAll('[required]');
    let isValid = true;
    
    requiredFields.forEach(field => {
        if (!field.value.trim()) {
            field.classList.add('is-invalid');
            isValid = false;
        } else {
            field.classList.remove('is-invalid');
        }
    });
    
    return isValid;
}

// Auto-hide alerts
document.addEventListener('DOMContentLoaded', function() {
    // Auto-hide success alerts after 3 seconds
    const successAlerts = document.querySelectorAll('.alert-success');
    successAlerts.forEach(alert => {
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 3000);
    });
    
    // Initialize tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Initialize popovers
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });
});

// Search functionality
function initializeSearch() {
    const searchInput = document.getElementById('searchInput');
    if (searchInput) {
        searchInput.addEventListener('input', function(e) {
            const searchTerm = e.target.value.toLowerCase();
            const tableRows = document.querySelectorAll('tbody tr');
            
            tableRows.forEach(row => {
                const text = row.textContent.toLowerCase();
                if (text.includes(searchTerm)) {
                    row.style.display = '';
                } else {
                    row.style.display = 'none';
                }
            });
        });
    }
}

// Filter functionality
function initializeFilters() {
    const filterSelects = document.querySelectorAll('.filter-select');
    
    filterSelects.forEach(select => {
        select.addEventListener('change', function() {
            applyFilters();
        });
    });
}

function applyFilters() {
    const filters = {};
    document.querySelectorAll('.filter-select').forEach(select => {
        if (select.value) {
            filters[select.dataset.column] = select.value;
        }
    });
    
    const tableRows = document.querySelectorAll('tbody tr');
    tableRows.forEach(row => {
        let showRow = true;
        
        Object.keys(filters).forEach(column => {
            const cell = row.querySelector(`[data-column="${column}"]`);
            if (cell && !cell.textContent.includes(filters[column])) {
                showRow = false;
            }
        });
        
        row.style.display = showRow ? '' : 'none';
    });
}

// Export functionality
function exportToExcel() {
    showAlert('info', 'Chức năng xuất Excel đang được phát triển...');
}

function exportToPDF() {
    showAlert('info', 'Chức năng xuất PDF đang được phát triển...');
}

// Confirmation dialogs
function confirmDelete(message = 'Bạn có chắc chắn muốn xóa?') {
    return confirm(message);
}

// Date formatting
function formatDate(dateString) {
    if (!dateString) return '-';
    
    const date = new Date(dateString);
    return date.toLocaleDateString('vi-VN', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric'
    });
}

// Number formatting
function formatNumber(number) {
    if (number === null || number === undefined) return '-';
    return new Intl.NumberFormat('vi-VN').format(number);
}

// Status badge helper
function getStatusBadge(status) {
    const statusClasses = {
        'Being Idle': 'bg-warning',
        'To be Idle': 'bg-info',
        'Idle Short Term': 'bg-primary',
        'Yes': 'bg-danger',
        'No': 'bg-success'
    };
    
    const className = statusClasses[status] || 'bg-secondary';
    return `<span class="badge ${className}">${status}</span>`;
}

// Initialize page-specific functionality
function initializePage() {
    const currentPage = document.body.dataset.page;
    
    switch (currentPage) {
        case 'idle-management':
            initializeSearch();
            initializeFilters();
            break;
        case 'dashboard':
            // Dashboard specific initialization
            break;
        case 'settings':
            // Settings specific initialization
            break;
    }
}

// Call initialization when DOM is loaded
document.addEventListener('DOMContentLoaded', initializePage);

// Global error handler
window.addEventListener('error', function(e) {
    console.error('JavaScript error:', e.error);
    showAlert('danger', 'Đã xảy ra lỗi. Vui lòng thử lại sau.');
});

// AJAX helper function
function makeRequest(url, options = {}) {
    const defaultOptions = {
        headers: {
            'Content-Type': 'application/json',
        },
    };
    
    const mergedOptions = { ...defaultOptions, ...options };
    
    return fetch(url, mergedOptions)
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .catch(error => {
            console.error('Request failed:', error);
            showAlert('danger', 'Kết nối thất bại. Vui lòng kiểm tra mạng và thử lại.');
            throw error;
        });
}

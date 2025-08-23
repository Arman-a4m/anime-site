/**
 * Base JavaScript functionality for Anime Catalog
 * Основная JavaScript функциональность для каталога аниме
 */

// DOM Content Loaded
document.addEventListener('DOMContentLoaded', function() {
    // Initialize all components
    initLoadingScreen();
    initMobileMenu();
    initBackToTop();
    initHeaderScroll();
    initSmoothScrolling();
    initAccessibility();
    
    console.log('🎌 Anime Catalog loaded successfully!');
});

/**
 * Loading Screen Management
 * Управление экраном загрузки
 */
function initLoadingScreen() {
    const loadingOverlay = document.getElementById('loading');
    
    if (loadingOverlay) {
        // Hide loading screen after page load
        window.addEventListener('load', function() {
            setTimeout(() => {
                loadingOverlay.classList.add('hidden');
                // Remove from DOM after animation
                setTimeout(() => {
                    loadingOverlay.remove();
                }, 300);
            }, 500);
        });
        
        // Fallback: hide after 3 seconds
        setTimeout(() => {
            if (loadingOverlay && !loadingOverlay.classList.contains('hidden')) {
                loadingOverlay.classList.add('hidden');
                setTimeout(() => loadingOverlay.remove(), 300);
            }
        }, 3000);
    }
}

/**
 * Mobile Menu Toggle
 * Переключение мобильного меню
 */
function initMobileMenu() {
    const mobileMenuBtn = document.getElementById('mobileMenuBtn');
    const navList = document.querySelector('.nav-list');
    
    if (mobileMenuBtn && navList) {
        mobileMenuBtn.addEventListener('click', function() {
            const isActive = navList.classList.contains('active');
            
            // Toggle menu
            navList.classList.toggle('active');
            mobileMenuBtn.classList.toggle('active');
            
            // Update aria attributes
            mobileMenuBtn.setAttribute('aria-expanded', !isActive);
            mobileMenuBtn.setAttribute('aria-label', isActive ? 'Открыть меню' : 'Закрыть меню');
            
            // Prevent body scroll when menu is open
            document.body.style.overflow = isActive ? '' : 'hidden';
        });
        
        // Close menu when clicking outside
        document.addEventListener('click', function(event) {
            if (!mobileMenuBtn.contains(event.target) && !navList.contains(event.target)) {
                navList.classList.remove('active');
                mobileMenuBtn.classList.remove('active');
                mobileMenuBtn.setAttribute('aria-expanded', 'false');
                mobileMenuBtn.setAttribute('aria-label', 'Открыть меню');
                document.body.style.overflow = '';
            }
        });
        
        // Close menu on escape key
        document.addEventListener('keydown', function(event) {
            if (event.key === 'Escape' && navList.classList.contains('active')) {
                navList.classList.remove('active');
                mobileMenuBtn.classList.remove('active');
                mobileMenuBtn.setAttribute('aria-expanded', 'false');
                mobileMenuBtn.setAttribute('aria-label', 'Открыть меню');
                document.body.style.overflow = '';
            }
        });
    }
}

/**
 * Back to Top Button
 * Кнопка "Наверх"
 */
function initBackToTop() {
    const backToTopBtn = document.getElementById('backToTop');
    
    if (backToTopBtn) {
        // Show/hide button based on scroll position
        window.addEventListener('scroll', function() {
            if (window.pageYOffset > 300) {
                backToTopBtn.classList.add('visible');
            } else {
                backToTopBtn.classList.remove('visible');
            }
        });
        
        // Smooth scroll to top
        backToTopBtn.addEventListener('click', function() {
            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
        });
    }
}

/**
 * Header Scroll Effects
 * Эффекты при прокрутке заголовка
 */
function initHeaderScroll() {
    const header = document.getElementById('header');
    let lastScrollY = window.pageYOffset;
    
    if (header) {
        window.addEventListener('scroll', function() {
            const currentScrollY = window.pageYOffset;
            
            // Add shadow on scroll
            if (currentScrollY > 10) {
                header.classList.add('scrolled');
            } else {
                header.classList.remove('scrolled');
            }
            
            // Hide/show header on scroll (optional)
            if (currentScrollY > lastScrollY && currentScrollY > 100) {
                // Scrolling down
                header.style.transform = 'translateY(-100%)';
            } else {
                // Scrolling up
                header.style.transform = 'translateY(0)';
            }
            
            lastScrollY = currentScrollY;
        });
    }
}

/**
 * Smooth Scrolling for Anchor Links
 * Плавная прокрутка для якорных ссылок
 */
function initSmoothScrolling() {
    // Smooth scroll for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            
            if (target) {
                const headerHeight = document.querySelector('.site-header').offsetHeight;
                const targetPosition = target.offsetTop - headerHeight - 20;
                
                window.scrollTo({
                    top: targetPosition,
                    behavior: 'smooth'
                });
            }
        });
    });
}

/**
 * Accessibility Features
 * Функции доступности
 */
function initAccessibility() {
    // Skip to main content link
    const skipLink = document.createElement('a');
    skipLink.href = '#main-content';
    skipLink.textContent = 'Перейти к основному содержимому';
    skipLink.className = 'skip-link sr-only';
    skipLink.style.cssText = `
        position: absolute;
        top: -40px;
        left: 6px;
        background: var(--primary-color);
        color: white;
        padding: 8px;
        text-decoration: none;
        border-radius: 4px;
        z-index: 10000;
    `;
    
    skipLink.addEventListener('focus', function() {
        this.style.top = '6px';
    });
    
    skipLink.addEventListener('blur', function() {
        this.style.top = '-40px';
    });
    
    document.body.insertBefore(skipLink, document.body.firstChild);
    
    // Add main content id
    const mainContent = document.querySelector('.site-content');
    if (mainContent) {
        mainContent.id = 'main-content';
    }
    
    // Keyboard navigation for interactive elements
    document.addEventListener('keydown', function(event) {
        // Tab navigation
        if (event.key === 'Tab') {
            document.body.classList.add('keyboard-navigation');
        }
    });
    
    // Remove keyboard navigation class on mouse use
    document.addEventListener('mousedown', function() {
        document.body.classList.remove('keyboard-navigation');
    });
}

/**
 * Utility Functions
 * Утилитарные функции
 */

// Debounce function for performance
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Throttle function for scroll events
function throttle(func, limit) {
    let inThrottle;
    return function() {
        const args = arguments;
        const context = this;
        if (!inThrottle) {
            func.apply(context, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    };
}

// Show notification
function showNotification(message, type = 'info', duration = 3000) {
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.textContent = message;
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 12px 20px;
        border-radius: 8px;
        color: white;
        font-weight: 500;
        z-index: 10000;
        transform: translateX(100%);
        transition: transform 0.3s ease;
        max-width: 300px;
    `;
    
    // Set background color based on type
    const colors = {
        success: '#4ade80',
        error: '#f87171',
        warning: '#fbbf24',
        info: '#667eea'
    };
    notification.style.backgroundColor = colors[type] || colors.info;
    
    document.body.appendChild(notification);
    
    // Animate in
    setTimeout(() => {
        notification.style.transform = 'translateX(0)';
    }, 100);
    
    // Remove after duration
    setTimeout(() => {
        notification.style.transform = 'translateX(100%)';
        setTimeout(() => {
            if (notification.parentNode) {
                notification.parentNode.removeChild(notification);
            }
        }, 300);
    }, duration);
}

// Modal functions
function showModal(content, title = '') {
    const modal = document.createElement('div');
    modal.className = 'modal-overlay';
    modal.innerHTML = `
        <div class="modal">
            <div class="modal-header">
                <h3>${title}</h3>
                <button class="modal-close" aria-label="Закрыть">&times;</button>
            </div>
            <div class="modal-content">
                ${content}
            </div>
        </div>
    `;
    
    modal.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0, 0, 0, 0.5);
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 1000;
        opacity: 0;
        transition: opacity 0.3s ease;
    `;
    
    const modalContent = modal.querySelector('.modal');
    modalContent.style.cssText = `
        background: white;
        border-radius: 12px;
        max-width: 500px;
        width: 90%;
        max-height: 80vh;
        overflow-y: auto;
        transform: scale(0.9);
        transition: transform 0.3s ease;
    `;
    
    document.body.appendChild(modal);
    
    // Animate in
    setTimeout(() => {
        modal.style.opacity = '1';
        modalContent.style.transform = 'scale(1)';
    }, 10);
    
    // Close functionality
    const closeBtn = modal.querySelector('.modal-close');
    closeBtn.addEventListener('click', () => closeModal(modal));
    
    modal.addEventListener('click', (e) => {
        if (e.target === modal) {
            closeModal(modal);
        }
    });
    
    // Close on escape
    document.addEventListener('keydown', function closeOnEscape(e) {
        if (e.key === 'Escape') {
            closeModal(modal);
            document.removeEventListener('keydown', closeOnEscape);
        }
    });
    
    return modal;
}

function closeModal(modal) {
    const modalContent = modal.querySelector('.modal');
    modal.style.opacity = '0';
    modalContent.style.transform = 'scale(0.9)';
    
    setTimeout(() => {
        if (modal.parentNode) {
            modal.parentNode.removeChild(modal);
        }
    }, 300);
}

// Footer link functions
function showAbout() {
    const content = `
        <p>Anime Catalog - это современное веб-приложение для каталогизации и поиска аниме.</p>
        <p>Проект создан с использованием Flask, HTML5, CSS3 и JavaScript.</p>
        <p>Все данные взяты из официальных источников и не нарушают авторские права.</p>
    `;
    showModal(content, 'О проекте');
}

function showPrivacy() {
    const content = `
        <p>Мы уважаем вашу конфиденциальность и не собираем персональные данные.</p>
        <p>Сайт использует только необходимые cookies для улучшения пользовательского опыта.</p>
        <p>Все данные обрабатываются локально в вашем браузере.</p>
    `;
    showModal(content, 'Политика конфиденциальности');
}

function showTerms() {
    const content = `
        <p>Используя этот сайт, вы соглашаетесь с условиями использования.</p>
        <p>Сайт предназначен только для информационных целей.</p>
        <p>Мы не несем ответственности за любые внешние ссылки или контент.</p>
    `;
    showModal(content, 'Условия использования');
}

// Export functions for global use
window.AnimeCatalog = {
    showNotification,
    showModal,
    closeModal,
    showAbout,
    showPrivacy,
    showTerms
}; 
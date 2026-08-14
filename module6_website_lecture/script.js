/* ============================================================
   Module 5 Lecture — JavaScript
   Odoo 19 CE  |  Ntech Batch 2
   ============================================================ */

document.addEventListener('DOMContentLoaded', () => {

    // ---------- ELEMENTS ----------
    const sidebar     = document.getElementById('sidebar');
    const hamburger   = document.getElementById('hamburger');
    const navLinks    = document.querySelectorAll('.nav-link');
    const sections    = document.querySelectorAll('.section');
    const progressBar = document.getElementById('progressBar');

    // Create overlay for mobile
    const overlay = document.createElement('div');
    overlay.className = 'sidebar-overlay';
    document.body.appendChild(overlay);

    // ---------- MOBILE SIDEBAR TOGGLE ----------
    function toggleSidebar() {
        sidebar.classList.toggle('open');
        hamburger.classList.toggle('open');
        overlay.classList.toggle('active');
    }

    function closeSidebar() {
        sidebar.classList.remove('open');
        hamburger.classList.remove('open');
        overlay.classList.remove('active');
    }

    hamburger.addEventListener('click', toggleSidebar);
    overlay.addEventListener('click', closeSidebar);

    // Close sidebar on nav click (mobile)
    navLinks.forEach(link => {
        link.addEventListener('click', () => {
            if (window.innerWidth <= 900) {
                closeSidebar();
            }
        });
    });

    // ---------- SCROLL PROGRESS ----------
    function updateProgress() {
        const scrollTop    = window.scrollY;
        const docHeight    = document.documentElement.scrollHeight - window.innerHeight;
        const scrollPercent = docHeight > 0 ? (scrollTop / docHeight) * 100 : 0;
        progressBar.style.width = scrollPercent + '%';
    }

    // ---------- ACTIVE NAV TRACKING ----------
    function updateActiveNav() {
        let currentSection = '';
        const scrollPos = window.scrollY + 120;

        sections.forEach(section => {
            const top    = section.offsetTop;
            const height = section.offsetHeight;

            if (scrollPos >= top && scrollPos < top + height) {
                currentSection = section.id;
            }
        });

        if (!currentSection && window.scrollY < 200) {
            currentSection = 'intro';
        }

        navLinks.forEach(link => {
            link.classList.remove('active');
            if (link.getAttribute('data-section') === currentSection) {
                link.classList.add('active');
            }
        });
    }

    // Throttled scroll handler
    let ticking = false;
    window.addEventListener('scroll', () => {
        if (!ticking) {
            window.requestAnimationFrame(() => {
                updateProgress();
                updateActiveNav();
                ticking = false;
            });
            ticking = true;
        }
    });

    // Initial call
    updateProgress();
    updateActiveNav();

    // ---------- SECTION FADE-IN ON SCROLL ----------
    const observerOptions = {
        root: null,
        rootMargin: '0px 0px -60px 0px',
        threshold: 0.05,
    };

    const sectionObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.animationPlayState = 'running';
                sectionObserver.unobserve(entry.target);
            }
        });
    }, observerOptions);

    sections.forEach(section => {
        section.style.animationPlayState = 'paused';
        sectionObserver.observe(section);
    });

    // Make first section always visible
    const intro = document.getElementById('intro');
    if (intro) intro.style.animationPlayState = 'running';

    // ---------- CHECKLIST PERSISTENCE ----------
    const checkboxes = document.querySelectorAll('.lab-checklist input[type="checkbox"]');

    // Load saved state
    checkboxes.forEach(cb => {
        const saved = localStorage.getItem('m5_lab_' + cb.id);
        if (saved === 'true') cb.checked = true;
    });

    // Save on change
    checkboxes.forEach(cb => {
        cb.addEventListener('change', () => {
            localStorage.setItem('m5_lab_' + cb.id, cb.checked);
        });
    });

    // ---------- KEYBOARD SHORTCUTS ----------
    document.addEventListener('keydown', (e) => {
        // Escape closes sidebar
        if (e.key === 'Escape') closeSidebar();
    });
});

// ---------- COPY CODE FUNCTION ----------
function copyCode(button) {
    const codeBlock = button.closest('.code-block');
    const code = codeBlock.querySelector('code');
    const text = code.textContent;

    navigator.clipboard.writeText(text).then(() => {
        const original = button.textContent;
        button.textContent = 'Copied!';
        button.classList.add('copied');

        setTimeout(() => {
            button.textContent = original;
            button.classList.remove('copied');
        }, 2000);
    }).catch(() => {
        // Fallback for older browsers
        const textarea = document.createElement('textarea');
        textarea.value = text;
        textarea.style.position = 'fixed';
        textarea.style.opacity = '0';
        document.body.appendChild(textarea);
        textarea.select();
        document.execCommand('copy');
        document.body.removeChild(textarea);

        const original = button.textContent;
        button.textContent = 'Copied!';
        button.classList.add('copied');

        setTimeout(() => {
            button.textContent = original;
            button.classList.remove('copied');
        }, 2000);
    });
}

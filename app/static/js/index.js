// Main website JavaScript file
'use strict';

// Wait for DOM content to be fully loaded before initializing
document.addEventListener('DOMContentLoaded', () => {
  // Initialize all components
  initAnimations();
  initFormValidation();
  initCarousel();
  initNoticeBoard();
  initCaptions();
  initDateTime();
  initLeadershipSlideshow();
  
  // Only initialize parallax on larger screens
  if (window.innerWidth > 768) {
    initParallax();
  }

  // Testimonial Carousel
  const slides = document.querySelectorAll('.testimonial-slide');
  const dots = document.querySelectorAll('.testimonial-dot span');
  let currentSlide = 0;
  const slideInterval = 3000; // Change slide every 3 seconds

  function showSlide(n) {
    slides[currentSlide].classList.remove('active');
    dots[currentSlide].classList.remove('active');
    currentSlide = (n + slides.length) % slides.length;
    slides[currentSlide].classList.add('active');
    dots[currentSlide].classList.add('active');
  }

  function nextSlide() {
    showSlide(currentSlide + 1);
  }

  // Add click handlers to dots
  dots.forEach((dot, index) => {
    dot.addEventListener('click', () => {
      showSlide(index);
    });
  });

  // Start the slideshow
  setInterval(nextSlide, slideInterval);
});

// Global variables
let isScrollPaused = false;
let scrollInterval = null;

/**
 * Animation on scroll functionality
 */
function initAnimations() {
  const animateOnScroll = () => {
    const elements = document.querySelectorAll('.content, .feature-card, .achievement-card, .stat-card, .campus-card');
    
    if (elements.length === 0) {
      return;
    }
    
    elements.forEach(element => {
      const rect = element.getBoundingClientRect();
      const isVisible = rect.top < window.innerHeight && rect.bottom > 0;
      
      if (isVisible) {
        element.classList.add('in-view');
      } else {
        element.classList.remove('in-view');
      }
    });
  };
  
  // Add scroll event listener with throttling
  let scrollThrottleTimer;
  window.addEventListener('scroll', () => {
    if (!scrollThrottleTimer) {
      scrollThrottleTimer = setTimeout(() => {
        animateOnScroll();
        scrollThrottleTimer = null;
      }, 100);
    }
  });
  
  // Run once on initial load
  animateOnScroll();
}

/**
 * Form validation for input fields
 */
function initFormValidation() {
  const formInputs = document.querySelectorAll('.m3-text-field input');
  
  formInputs.forEach(input => {
    const validateInput = () => {
      const field = input.closest('.m3-text-field');
      if (input.validity.valid) {
        field.classList.remove('invalid');
        field.classList.add('valid');
      } else {
        field.classList.remove('valid');
        field.classList.add('invalid');
      }
    };
    
    input.addEventListener('blur', validateInput);
    input.addEventListener('input', validateInput);
  });
  
  const newsletterForm = document.querySelector('.m3-form');
  if (newsletterForm) {
    newsletterForm.addEventListener('submit', function(e) {
      e.preventDefault();
      const emailField = this.querySelector('input[type="email"]');
      
      if (emailField && emailField.validity.valid) {
        const successMsg = document.createElement('div');
        successMsg.textContent = 'Thank you for subscribing!';
        successMsg.classList.add('m3-success-message');
        
        this.appendChild(successMsg);
        emailField.value = '';
        
        setTimeout(() => {
          successMsg.remove();
        }, 3000);
      }
    });
  }
}

/**
 * Carousel/Slideshow functionality
 */
function initCarousel() {
  let currentSlide = 0;
  const slides = document.querySelectorAll('.carousel-item');
  const indicatorsContainer = document.querySelector('.carousel-indicators');
  let autoAdvanceTimer = null;
  
  if (slides.length === 0 || !indicatorsContainer) {
    console.warn("Carousel elements not found");
    return;
  }
  
  // Create indicators
  slides.forEach((_, index) => {
    const indicator = document.createElement('div');
    indicator.classList.add('indicator');
    indicator.onclick = () => goToSlide(index);
    indicatorsContainer.appendChild(indicator);
  });
  
  const indicators = document.querySelectorAll('.indicator');
  
  function updateSlides() {
    if (!slides[currentSlide] || !indicators[currentSlide]) {
      return;
    }
    
    // Stop any currently playing videos
    slides.forEach(slide => {
      const video = slide.querySelector('video');
      if (video) {
        video.pause();
        video.currentTime = 0;
      }
      slide.classList.remove('active');
    });
    
    indicators.forEach(indicator => indicator.classList.remove('active'));
    
    // Activate current slide and handle video if present
    slides[currentSlide].classList.add('active');
    indicators[currentSlide].classList.add('active');
    
    // If current slide has video, play it
    const currentVideo = slides[currentSlide].querySelector('video');
    if (currentVideo) {
      currentVideo.currentTime = 0; // Reset video to start
      const playPromise = currentVideo.play();
      if (playPromise !== undefined) {
        playPromise.catch(error => console.log("Auto-play prevented:", error));
      }
    }
    
    // Clear any existing auto-advance timer
    if (autoAdvanceTimer) {
      clearTimeout(autoAdvanceTimer);
    }
    
    // Set up the next slide transition
    scheduleNextSlide();
  }
  
  function moveSlide(direction) {
    currentSlide += direction;
    if (currentSlide >= slides.length) currentSlide = 0;
    if (currentSlide < 0) currentSlide = slides.length - 1;
    updateSlides();
  }
  
  function goToSlide(index) {
    if (index < 0 || index >= slides.length) {
      return;
    }
    currentSlide = index;
    updateSlides();
  }
  
  function scheduleNextSlide() {
    // If we're on a slide with video
    const currentVideoElement = slides[currentSlide].querySelector('video');
    
    if (currentVideoElement) {
      // Remove any existing event listeners first
      currentVideoElement.removeEventListener('ended', handleVideoEnd);
      
      // Add the event listener for when video ends
      currentVideoElement.addEventListener('ended', handleVideoEnd);
    } else {
      // No video in this slide, use standard delay
      autoAdvanceTimer = setTimeout(() => moveSlide(1), 2000);
    }
  }
  
  // Function to handle video end event
  function handleVideoEnd() {
    moveSlide(1);
  }
  
  // Initialize first slide
  updateSlides();
  
  // Make moveSlide available globally
  window.moveSlide = moveSlide;
}

/**
 * Notice board functionality including auto-scrolling and API-based notice fetching
 */
function initNoticeBoard() {
  // Notice fetch variables
  let currentGeneralPage = 1;
  let currentExamPage = 1;
  const perPage = 10;
  let loading = false;
  let scrollTimer = ;
  
  // Get notice content elements
  const generalNoticeContent = document.getElementById('generalNoticeContent');
  const examNoticeContent = document.getElementById('examNoticeContent');
  const generalNoticesContainer = document.getElementById('generalNoticesContainer');
  const examNoticesContainer = document.getElementById('examNoticesContainer');
  
  // Check if elements exist
  if (!generalNoticeContent || !examNoticeContent) return;
  // Format dates in IST timezone
  function formatDate(dateString) {
    const options = {
      day: '2-digit',
      month: 'short',
      year: 'numeric',
      timeZone: 'Asia/Kolkata' // IST timezone
    };
    
    try {
      const date = new Date(dateString);
      if (isNaN(date.getTime())) {
        return 'Invalid date';
      }
      return date.toLocaleDateString('en-IN', options);
    } catch (error) {
      console.error('Error formatting date:', error);
      return dateString || 'No date';
    }
  }

  // Fetch notices from the API
  async function fetchNotices(page, type = 'general') {
    try {
      loading = true;
      const loadingElement = document.getElementById('noticeLoading');
      if (loadingElement) loadingElement.style.display = 'block';

      const response = await fetch(`/api/notices?page=${page}&per_page=${perPage}&type=${type}`);
      const data = await response.json();
      
      // Select the appropriate container based on notice type
      const noticeContainer = type === 'general' 
        ? document.getElementById('generalNoticeContent') 
        : document.getElementById('examNoticeContent');
      
      if (!noticeContainer) return;
      
      // Show all notices without date filtering to maintain 10 notices scrolling
      data.notices.forEach(notice => {
        const noticeElement = document.createElement('div');
        noticeElement.className = 'notice';
        noticeElement.innerHTML = `
          <span class="notice-date">${formatDate(notice.date_uploaded)}</span>
          <a href="${notice.url}" target="_blank" class="notice-link">
            ${notice.title}
            <span class="material-icons notice-icon">arrow_forward</span>
          </a>
        `;
        
        // Add hover effect and animation
        noticeElement.style.animation = 'fadeIn 0.5s ease forwards';
        noticeElement.style.animationDelay = '0.1s';
        
        noticeContainer.appendChild(noticeElement);
      });      // Update load more button visibility if it exists
      const loadMoreButton = document.getElementById(`loadMore${type.charAt(0).toUpperCase() + type.slice(1)}Button`);
      if (loadMoreButton) {
        loadMoreButton.style.display = data.has_next ? 'block' : 'none';
      }
      
      // Check if auto-scrolling is needed after adding new notices
      setTimeout(() => {
        const contentContainer = type === 'general' 
          ? document.getElementById('generalNoticeContent') 
          : document.getElementById('examNoticeContent');
          
        const wrapperContainer = type === 'general' 
          ? document.getElementById('generalNoticesContainer') 
          : document.getElementById('examNoticesContainer');
          
        if (contentContainer && wrapperContainer) {
          // Check if content exceeds container height
          const contentHeight = contentContainer.scrollHeight;
          const containerHeight = wrapperContainer.clientHeight - 50; // Account for padding
            if (contentHeight > containerHeight) {
            // Enable animation if content exceeds container
            contentContainer.classList.remove('no-scroll');
            contentContainer.style.animationPlayState = 'running';
            // Adjust scroll speed based on content length
            adjustScrollSpeed(contentContainer, contentHeight, containerHeight);
          } else {
            // Disable animation if content fits within container
            contentContainer.classList.add('no-scroll');
          }
          
          // Adjust scroll speed based on content length
          adjustScrollSpeed(contentContainer, contentHeight, containerHeight);
        }
      }, 300); // Short delay to ensure DOM is updated
    } catch (error) {
      console.error(`Error fetching ${type} notices:`, error);
    } finally {
      loading = false;
      const loadingElement = document.getElementById('noticeLoading');
      if (loadingElement) loadingElement.style.display = 'none';
    }
  }  // Initial fetch of notices
  fetchNotices(currentGeneralPage, 'general');
  fetchNotices(currentExamPage, 'exam');

  // Set up load more button functionality
  const loadMoreGeneralBtn = document.getElementById('loadMoreGeneralButton');
  if (loadMoreGeneralBtn) {
    loadMoreGeneralBtn.addEventListener('click', () => {
      if (!loading) {
        currentGeneralPage++;
        fetchNotices(currentGeneralPage, 'general');
        setTimeout(checkScrollNeeded, 500); // Check after content is loaded and rendered
      }
    });
  }

  const loadMoreExamBtn = document.getElementById('loadMoreExamButton');
  if (loadMoreExamBtn) {
    loadMoreExamBtn.addEventListener('click', () => {
      if (!loading) {
        currentExamPage++;
        fetchNotices(currentExamPage, 'exam');
        setTimeout(checkScrollNeeded, 500); // Check after content is loaded and rendered
      }
    });
  }
    // Function to check if scrolling is needed
  function checkScrollNeeded() {
    // Check for general notices
    if (generalNoticeContent && generalNoticesContainer) {
      const contentHeight = generalNoticeContent.scrollHeight;
      const containerHeight = generalNoticesContainer.clientHeight - 50; // Account for padding
      
      if (contentHeight <= containerHeight) {
        generalNoticeContent.classList.add('no-scroll');
      } else {
        generalNoticeContent.classList.remove('no-scroll');
        adjustScrollSpeed(generalNoticeContent, contentHeight, containerHeight);
      }
    }
    
    // Check for exam notices
    if (examNoticeContent && examNoticesContainer) {
      const contentHeight = examNoticeContent.scrollHeight;
      const containerHeight = examNoticesContainer.clientHeight - 50; // Account for padding
      
      if (contentHeight <= containerHeight) {
        examNoticeContent.classList.add('no-scroll');
      } else {
        examNoticeContent.classList.remove('no-scroll');
        adjustScrollSpeed(examNoticeContent, contentHeight, containerHeight);
      }
    }
  }
  
  // Set a timeout to check if scrolling is needed after initial content load
  setTimeout(checkScrollNeeded, 1000);  // Set event listeners for pause/resume on hover
  if (generalNoticeContent) {
    generalNoticeContent.addEventListener('mouseenter', function() {
      this.style.animationPlayState = 'paused';
    });
    
    generalNoticeContent.addEventListener('mouseleave', function() {
      if (!this.classList.contains('no-scroll')) {
        this.style.animationPlayState = 'running';
      }
    });
  }
  
  if (examNoticeContent) {
    examNoticeContent.addEventListener('mouseenter', function() {
      this.style.animationPlayState = 'paused';
    });
    
    examNoticeContent.addEventListener('mouseleave', function() {
      if (!this.classList.contains('no-scroll')) {
        this.style.animationPlayState = 'running';
      }
    });
  }
  
  // Allow manual scrolling on the container
  if (generalNoticesContainer) {
    generalNoticesContainer.addEventListener('wheel', function(e) {
      // Prevent default behavior only if inside container
      e.stopPropagation();
      
      // Manual scrolling
      if (e.deltaY > 0) {
        // Scrolling down
        this.scrollTop += 30;
      } else {
        // Scrolling up
        this.scrollTop -= 30;
      }
    });
  }
  
  if (examNoticesContainer) {
    examNoticesContainer.addEventListener('wheel', function(e) {
      // Prevent default behavior only if inside container
      e.stopPropagation();
      
      // Manual scrolling
      if (e.deltaY > 0) {
        // Scrolling down
        this.scrollTop += 30;
      } else {
        // Scrolling up
        this.scrollTop -= 30;
      }
    });
  }
    // Export pause/resume scroll functions for use in HTML
  window.pauseScroll = function() {
    const generalContent = document.querySelector('#generalNoticeContent');
    const examContent = document.querySelector('#examNoticeContent');
    
    if (generalContent && !generalContent.classList.contains('no-scroll')) {
      generalContent.style.animationPlayState = 'paused';
    }
    
    if (examContent && !examContent.classList.contains('no-scroll')) {
      examContent.style.animationPlayState = 'paused';
    }
    
    if (scrollTimer) clearTimeout(scrollTimer);
  };
  
  window.resumeScroll = function() {
    const generalContent = document.querySelector('#generalNoticeContent');
    const examContent = document.querySelector('#examNoticeContent');
    
    scrollTimer = setTimeout(() => {
      if (generalContent && !generalContent.classList.contains('no-scroll')) {
        generalContent.style.animationPlayState = 'running';
      }
      
      if (examContent && !examContent.classList.contains('no-scroll')) {
        examContent.style.animationPlayState = 'running';
      }
    }, 500);
  };
  
  // Export these functions for use in HTML
  window.switchNoticeTab = function(type) {
    // Update tab active state
    document.getElementById('generalNoticeTab').classList.toggle('active', type === 'general');
    document.getElementById('examNoticeTab').classList.toggle('active', type === 'exam');
    
    // Show/hide appropriate container
    document.getElementById('generalNoticesContainer').style.display = type === 'general' ? 'block' : 'none';
    document.getElementById('examNoticesContainer').style.display = type === 'exam' ? 'block' : 'none';
  };
  
  // Add scroll to top buttons for notice containers
  function addScrollToTopButtons() {
    if (generalNoticesContainer) {
      const scrollTopBtn = document.createElement('button');
      scrollTopBtn.className = 'scroll-top-btn';
      scrollTopBtn.innerHTML = '<span class="material-icons">arrow_upward</span>';
      scrollTopBtn.title = 'Scroll to top';
      scrollTopBtn.addEventListener('click', function() {
        generalNoticesContainer.scrollTop = 0;
      });
      generalNoticesContainer.appendChild(scrollTopBtn);
    }
    
    if (examNoticesContainer) {
      const scrollTopBtn = document.createElement('button');
      scrollTopBtn.className = 'scroll-top-btn';
      scrollTopBtn.innerHTML = '<span class="material-icons">arrow_upward</span>';
      scrollTopBtn.title = 'Scroll to top';
      scrollTopBtn.addEventListener('click', function() {
        examNoticesContainer.scrollTop = 0;
      });
      examNoticesContainer.appendChild(scrollTopBtn);
    }
  }
  
  // Call function to add scroll to top buttons
  addScrollToTopButtons();
}

/**
 * Hero caption animation
 */
function initCaptions() {
  const captions = [
    { title: "Join Us Today", text: "Experience world-class education and vibrant campus life." },
    { title: "Your Future Starts Here", text: "Explore endless learning opportunities at Saket College." },
    { title: "Learn, Grow, Succeed", text: "Join a community that fosters innovation and success." },
    { title: "Be a Part of Excellence", text: "Shape your career with our top-notch faculty and resources." }
  ];
  
  let currentIndex = 0;
  
  function changeCaption() {
    const titleElement = document.getElementById("caption-title");
    const textElement = document.getElementById("caption-text");
    
    if (!titleElement || !textElement) return;
    
    currentIndex = (currentIndex + 1) % captions.length;
    
    titleElement.style.opacity = "0";
    textElement.style.opacity = "0";
    
    setTimeout(() => {
      titleElement.textContent = captions[currentIndex].title;
      textElement.textContent = captions[currentIndex].text;
      
      titleElement.style.opacity = "1";
      textElement.style.opacity = "1";
    }, 500);
  }
  
  setInterval(changeCaption, 4000);
}

/**
 * Date and time display functionality
 */
function initDateTime() {
  const dateTimeElement = document.getElementById("dateTime");
  if (!dateTimeElement) return;
  
  function updateDateTime() {
    const now = new Date();
    const options = {
      weekday: 'long',
      year: 'numeric', 
      month: 'long', 
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
      second: '2-digit',
      hour12: true
    };
    
    dateTimeElement.textContent = now.toLocaleString('en-US', options);
  }
  
  setInterval(updateDateTime, 1000);
  updateDateTime(); // Initialize immediately
}

/**
 * Parallax scrolling effect
 */
function initParallax() {
  const parallaxSections = document.querySelectorAll('.parallax-section');
  if (parallaxSections.length === 0) return;
  
  let ticking = false;
  
  function updateParallax() {
    parallaxSections.forEach(section => {
      const scrolled = window.pageYOffset;
      const sectionTop = section.offsetTop;
      const sectionHeight = section.offsetHeight;
      
      // Calculate how far the section is from the viewport top
      const distanceFromTop = sectionTop - scrolled;
      
      // Calculate if section is in the viewport
      const isInView = distanceFromTop < window.innerHeight && distanceFromTop + sectionHeight > 0;
      
      if (isInView) {
        // Calculate a more moderate parallax effect
        // This moves the background more slowly than the section
        const yPos = Math.round((distanceFromTop * 0.4));
        section.style.backgroundPosition = `center ${yPos}px`;
      }
    });
    ticking = false;
  }
  
  window.addEventListener('scroll', () => {
    if (!ticking) {
      window.requestAnimationFrame(() => {
        updateParallax();
        ticking = false;
      });
      ticking = true;
    }
  }, { passive: true });
  
  // Initial update
  updateParallax();
}

/**
 * Leadership photos slideshow functionality
 */
function initLeadershipSlideshow() {
  let currentSlide = 0;
  const slides = document.querySelectorAll('.message-slide');
  const indicators = document.querySelectorAll('.message-indicator');
  
  // Verify that we have slides on the page
  if (!slides || slides.length === 0) {
    console.log("Leadership slideshow slides not found on this page");
    return;
  }

  // Verify that we have indicators on the page
  if (!indicators || indicators.length === 0) {
    console.log("Leadership slideshow indicators not found on this page");
    return;
  }
  
  // Make sure we have the right number of indicators for slides
  console.log(`Found ${slides.length} slides and ${indicators.length} indicators`);
  
  const totalSlides = slides.length;
  
  function showSlide(index) {
    // Make sure index is valid
    if (index < 0 || index >= slides.length) {
      console.error("Invalid slide index:", index);
      return;
    }
    
    // Hide all slides
    for (let i = 0; i < slides.length; i++) {
      if (slides[i] && slides[i].classList) {
        slides[i].classList.remove('active');
      }
    }
    
    // Hide all indicators
    for (let i = 0; i < indicators.length; i++) {
      if (indicators[i] && indicators[i].classList) {
        indicators[i].classList.remove('active');
      }
    }
    
    // Show the current slide
    if (slides[index] && slides[index].classList) {
      slides[index].classList.add('active');
    }
    
    // Highlight the current indicator (if it exists)
    if (index < indicators.length && indicators[index] && indicators[index].classList) {
      indicators[index].classList.add('active');
    }
    
    // Update counter if it exists
    const counter = document.querySelector('.message-count');
    if (counter) {
      counter.textContent = `${index + 1}/${totalSlides}`;
    }
    
    currentSlide = index;
  }
  
  function nextSlide() {
    let next = currentSlide + 1;
    if (next >= totalSlides) next = 0;
    showSlide(next);
  }
  
  function prevSlide() {
    let prev = currentSlide - 1;
    if (prev < 0) prev = totalSlides - 1;
    showSlide(prev);
  }
  
  // Set up indicator clicks
  for (let i = 0; i < indicators.length; i++) {
    if (indicators[i]) {
      indicators[i].addEventListener('click', function() {
        showSlide(i);
      });
    }
  }
  
  // Set up navigation buttons
  const prevBtn = document.querySelector('.message-prev');
  const nextBtn = document.querySelector('.message-next');
  
  if (prevBtn) {
    prevBtn.addEventListener('click', function(e) {
      e.preventDefault();
      prevSlide();
    });
  }
  
  if (nextBtn) {
    nextBtn.addEventListener('click', function(e) {
      e.preventDefault();
      nextSlide();
    });
  }
  
  // Initialize first slide
  showSlide(0);
  
  // Auto-advance slides every 5 seconds
  if (slides.length > 1) {
    try {
      setInterval(function() {
        nextSlide();
      }, 5000);
    } catch (error) {
      console.error("Error in leadership slideshow auto-advance:", error);
    }
  }
}

/**
 * Toggle expandable content for vision and mission sections
 */
window.toggleContent = function(id) {
  const content = document.querySelector(`#${id} .expanded-content`);
  const button = document.querySelector(`#${id} .expand-btn`);
  
  if (!content || !button) return;
  
  if (content.classList.contains('show')) {
    content.classList.remove('show');
    button.textContent = 'Read More';
  } else {
    content.classList.add('show');
    button.textContent = 'Read Less';
  }
}

/**
 * Function to adjust scroll speed based on content length
 */
function adjustScrollSpeed(contentElement, contentHeight, containerHeight) {
  if (!contentElement) return;
  
  // Remove all speed classes first
  contentElement.classList.remove('slow-scroll', 'medium-scroll', 'fast-scroll');
  
  // Calculate the content-to-container ratio
  const ratio = contentHeight / containerHeight;
  
  // Assign appropriate speed class based on content length
  if (ratio > 3) {
    contentElement.classList.add('slow-scroll');
  } else if (ratio > 2) {
    contentElement.classList.add('medium-scroll');
  } else if (ratio > 1) {
    contentElement.classList.add('fast-scroll');
  }
}
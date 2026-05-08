gsap.registerPlugin(ScrollTrigger);

gsap.from('.hero-carousel', {
  opacity: 0,
  y: 100,
  duration: 1,
  ease: 'power3.out'
});

gsap.from('.stat-card', {
  scrollTrigger: {
    trigger: '.stats-container',
    start: 'top center',
    toggleActions: 'play none none reverse'
  },
  opacity: 0,
  y: 50,
  duration: 0.8,
  stagger: 0.2,
  ease: 'power2.out'
});

gsap.set('.feature-card', {
  opacity: 1,
  y: 2,
});

gsap.from('.feature-card', {
  scrollTrigger: {
    trigger: '.features',
    start: 'top bottom-=20%',
    end: 'bottom center',
    toggleActions: 'play none none reverse',
    markers: false
  },
  opacity: 0,
  y: 30,
  duration: 1,
  stagger: {
    amount: 0.6,
    from: "start"
  },
  ease: 'back.out(1.2)'
});

gsap.from('.about-text', {
  scrollTrigger: {
    trigger: '.about-section',
    start: 'top center+=100',
    toggleActions: 'play none none reverse'
  },
  opacity: 0,
  x: -50,
  duration: 1
});

gsap.from('.about-image', {
  scrollTrigger: {
    trigger: '.about-section',
    start: 'top center+=100',
    toggleActions: 'play none none reverse'
  },
  opacity: 0,
  x: 50,
  duration: 1
});

gsap.from('.campus-card', {
  scrollTrigger: {
    trigger: '.campus-life',
    start: 'top center+=100',
    toggleActions: 'play none none reverse'
  },
  opacity: 0,
  scale: 0.8,
  duration: 0.8,
  stagger: 0.2,
  ease: 'power1.out'
});

gsap.from('.vision-mission-content', {
  scrollTrigger: {
    trigger: '.vision',
    start: 'top center+=100',
    toggleActions: 'play none none reverse'
  },
  opacity: 0,
  y: 30,
  duration: 1
});

gsap.from('.message-carousel', {
  scrollTrigger: {
    trigger: '.message-carousel',
    start: 'top center+=100',
    toggleActions: 'play none none reverse'
  },
  opacity: 0,
  scale: 0.9,
  duration: 1,
  ease: 'power2.out'
});

gsap.from('.achievement-card', {
  scrollTrigger: {
    trigger: '.achievements',
    start: 'top center+=100',
    toggleActions: 'play none none reverse'
  },
  opacity: 0,
  y: 5,
  duration: 0.8,
  stagger: 0.2,
  ease: 'power2.out'
});

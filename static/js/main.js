const revealEls = document.querySelectorAll('.reveal');
  const io = new IntersectionObserver((entries)=>{
    entries.forEach(e=>{
      if(e.isIntersecting){ e.target.classList.add('in'); io.unobserve(e.target); }
    });
  },{threshold:0.12});
  revealEls.forEach(el=>io.observe(el));

  document.querySelectorAll('.faq-item').forEach(item=>{
    const question = item.querySelector('.faq-question');
    const answer = item.querySelector('.faq-answer');
    question.addEventListener('click', function(){
      const isOpen = item.classList.contains('open');
      document.querySelectorAll('.faq-item.open').forEach(openItem=>{
        if(openItem !== item){
          openItem.classList.remove('open');
          openItem.querySelector('.faq-answer').style.maxHeight = null;
        }
      });
      if(isOpen){
        item.classList.remove('open');
        answer.style.maxHeight = null;
      } else {
        item.classList.add('open');
        answer.style.maxHeight = answer.scrollHeight + 'px';
      }
    });
  });

  document.querySelectorAll('.logo-mark').forEach(logo=>{
    logo.addEventListener('click', function(e){
      // If the logo points to the page we're already on, just scroll to top
      // smoothly instead of doing a full reload. Otherwise let the browser
      // navigate normally to the linked page.
      const linkPath = new URL(logo.href, window.location.origin).pathname;
      if(linkPath === window.location.pathname){
        e.preventDefault();
        window.scrollTo({top:0, behavior:'smooth'});
      }
    });
  });

  const menuToggle = document.getElementById('menuToggle');
  const mobileMenu = document.getElementById('mobileMenu');
  if(menuToggle && mobileMenu){
    menuToggle.addEventListener('click', function(){
      menuToggle.classList.toggle('active');
      mobileMenu.classList.toggle('open');
    });
    mobileMenu.querySelectorAll('a').forEach(link=>{
      link.addEventListener('click', function(){
        menuToggle.classList.remove('active');
        mobileMenu.classList.remove('open');
      });
    });
  }

  // Reads Django's CSRF token from the hidden input that {% csrf_token %} renders.
  function getCsrfToken(form){
    const input = form.querySelector('input[name="csrfmiddlewaretoken"]');
    return input ? input.value : '';
  }

  const contactForm = document.getElementById('contactForm');
  if(contactForm){
    contactForm.addEventListener('submit', function(e){
      e.preventDefault();
      const note = document.getElementById('contactFormNote');
      const submitBtn = contactForm.querySelector('.form-submit');
      const originalBtnText = submitBtn.textContent;
      submitBtn.disabled = true;
      submitBtn.textContent = 'Sending...';

      fetch(contactForm.action, {
        method: 'POST',
        headers: {
          'X-CSRFToken': getCsrfToken(contactForm),
          'X-Requested-With': 'XMLHttpRequest',
        },
        body: new FormData(contactForm),
      })
      .then(res => res.json().then(data => ({ok: res.ok, data})))
      .then(({ok, data})=>{
        if(ok && data.success){
          contactForm.reset();
          if(note){
            note.textContent = "Thanks — your message is in. We'll reply within one business day.";
            note.style.color = 'var(--red)';
          }
        } else {
          if(note){
            note.textContent = 'Something went wrong. Please check the form and try again.';
            note.style.color = 'var(--red)';
          }
        }
      })
      .catch(()=>{
        if(note){
          note.textContent = "Couldn't send right now — please email hello@easyafrica.com directly.";
          note.style.color = 'var(--red)';
        }
      })
      .finally(()=>{
        submitBtn.disabled = false;
        submitBtn.textContent = originalBtnText;
      });
    });
  }

  const newsletterForm = document.getElementById('newsletterForm');
  if(newsletterForm){
    newsletterForm.addEventListener('submit', function(e){
      e.preventDefault();
      const emailInput = newsletterForm.querySelector('input[type="email"]');
      const button = newsletterForm.querySelector('button');
      const originalText = button.textContent;
      button.disabled = true;

      fetch(newsletterForm.action, {
        method: 'POST',
        headers: {
          'X-CSRFToken': getCsrfToken(newsletterForm),
          'X-Requested-With': 'XMLHttpRequest',
        },
        body: new FormData(newsletterForm),
      })
      .then(res => res.json().then(data => ({ok: res.ok, data})))
      .then(({ok, data})=>{
        if(ok && data.success){
          button.textContent = 'Subscribed ✓';
          emailInput.value = '';
        } else {
          button.textContent = 'Try again';
        }
      })
      .catch(()=>{
        button.textContent = 'Try again';
      })
      .finally(()=>{
        setTimeout(()=>{
          button.textContent = originalText;
          button.disabled = false;
        }, 3000);
      });
    });
  }

  // Work page filter (only runs if #workFilter exists on the page)
  const filterPills = document.querySelectorAll('#workFilter .work-filter-pill');
  const workCards = document.querySelectorAll('#workGrid .work-card');
  filterPills.forEach(pill => {
    pill.addEventListener('click', function(){
      filterPills.forEach(p => p.classList.remove('active'));
      pill.classList.add('active');
      const filter = pill.getAttribute('data-filter');
      workCards.forEach(card => {
        if(filter === 'all' || card.getAttribute('data-category') === filter){
          card.classList.remove('hidden');
        } else {
          card.classList.add('hidden');
        }
      });
    });
  });
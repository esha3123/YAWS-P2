/**
 * Message page functionality
 * Handles the read more/less toggle for leadership messages
 */

function toggleMessage(id) {
    const dots = document.getElementById(`dots-${id}`);
    const moreText = document.getElementById(`more-${id}`);
    const btnText = document.getElementById(`btn-${id}`);
  
    if (moreText.style.display === "block") {
      dots.style.display = "inline";
      btnText.innerHTML = "Read more";
      moreText.style.display = "none";
    } else {
      dots.style.display = "none";
      btnText.innerHTML = "Read less";
      moreText.style.display = "block";
    }
  }
  /*
  document.addEventListener('DOMContentLoaded', function() {
      alert(JSON.stringify({message: 'DOM fully loaded and parsed'}));
      const readMoreButtons = document.querySelectorAll('.read-more-button');
      const closeButtons = document.querySelectorAll('.close-message');
      
      readMoreButtons.forEach(button => {
          alert(JSON.stringify({message: 'Adding click event to read more button'}));
          alert(JSON.stringify({messageId: button.getAttribute('data-message-id')}));
          button.addEventListener('click', function() {
              const messageId = this.getAttribute('data-message-id');
              const fullMessage = document.getElementById(`${messageId}-full-message`);
              fullMessage.style.display = 'block';
              this.style.display = 'none';
          });
      });
  
      closeButtons.forEach(button => {
        
          button.addEventListener('click', function() {
              const fullMessage = this.closest('.full-message');
              const messageContent = fullMessage.parentElement;
              const readMoreButton = messageContent.querySelector('.read-more-button');
              
              fullMessage.style.display = 'none';
              
              readMoreButton.style.display = 'inline-block';
              
              const messageItem = messageContent.closest('.message-item');
              messageItem.scrollIntoView({ behavior: 'smooth' });
          });
      });
  });*/
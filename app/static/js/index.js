
//Navbar toggle
document.addEventListener("DOMContentLoaded", function () {
  const hamburgerIcon = document.querySelector(".hamburger img");
  const hamburgerMenu = document.querySelector(".hamburger .hemburger-menu");

  hamburgerIcon.addEventListener("click", function () {
      // Toggle the visibility of the menu
      if (hamburgerMenu.style.display === "none" || hamburgerMenu.style.display === "") {
          hamburgerMenu.style.display = "block"; // Show the menu
      } else {
          hamburgerMenu.style.display = "none"; // Hide the menu
      }
  });
});

//to make the slider of the detail page
document.addEventListener("DOMContentLoaded", function () {
  let sliderIndex = 0;
  const slides = document.querySelectorAll(".slide");
  const totalSlides = slides.length;
  const slider = document.querySelector(".slider");

  function showSliderSlide(index) {
      if (index >= totalSlides) {
          sliderIndex = 0;
      } else if (index < 0) {
          sliderIndex = totalSlides - 1;
      } else {
          sliderIndex = index;
      }
      slider.style.transform = `translateX(-${sliderIndex * 960}px)`;
  }

  document.querySelector(".next").addEventListener("click", function () {
      showSliderSlide(sliderIndex + 1);
  });

  document.querySelector(".prev").addEventListener("click", function () {
      showSliderSlide(sliderIndex - 1);
  });

  setInterval(() => {
      showSliderSlide(sliderIndex + 1);
  }, 5000);
});

//Home skills typing 
document.addEventListener("DOMContentLoaded", () => {
    const skillText = document.getElementById("skill-text");
    const skills = ["Python Developer", "Web Developer", "Creative Thinker", "Innovative Coder"]; // Add more skills here
    let currentSkill = 0;
    let charIndex = 0;
    let typingSpeed = 100; // Typing speed in milliseconds
    let erasingSpeed = 50; // Erasing speed in milliseconds
    let delayBetweenSkills = 1500; // Delay before typing the next skill
    
    function typeSkill() {
      if (charIndex < skills[currentSkill].length) {
        skillText.textContent += skills[currentSkill].charAt(charIndex);
        charIndex++;
        setTimeout(typeSkill, typingSpeed);
      } else {
        setTimeout(eraseSkill, delayBetweenSkills);
      }
    }
  
    function eraseSkill() {
      if (charIndex > 0) {
        skillText.textContent = skills[currentSkill].substring(0, charIndex - 1);
        charIndex--;
        setTimeout(eraseSkill, erasingSpeed);
      } else {
        currentSkill = (currentSkill + 1) % skills.length; // Loop through the skills array
        setTimeout(typeSkill, typingSpeed);
      }
    }
  
    // Start the typing effect
    setTimeout(typeSkill, delayBetweenSkills);
  });


  
// Function to toggle the active category within its container
function toggleCategory(element) {
    const container = element.closest('.cards-categories'); // Get the parent container
    const categories = container.querySelectorAll('.category'); // Scope to this container
  
    // Remove active class from all categories in this container
    categories.forEach(category => category.classList.remove('active'));
  
    // Add active class to clicked category
    element.classList.add('active');
  }
  
  
  // sort button sort items
  document.addEventListener("DOMContentLoaded", () => {
      // Get all buttons and dropdowns
      const sortButtons = document.querySelectorAll(".cards-sort .outline-btn");
    
      sortButtons.forEach((button) => {
        button.addEventListener("click", (event) => {
          const parent = event.target.closest(".cards-sort");
          const dropdown = parent.querySelector(".sort-items");
    
          // Close other open dropdowns
          document.querySelectorAll(".sort-items").forEach((menu) => {
            if (menu !== dropdown) {
              menu.style.display = "none";
            }
          });
    
          // Toggle the visibility of the current dropdown
          dropdown.style.display = dropdown.style.display === "block" ? "none" : "block";
        });
      });
    
      // Close dropdowns when clicking outside
      document.addEventListener("click", (event) => {
        if (!event.target.closest(".cards-sort")) {
          document.querySelectorAll(".sort-items").forEach((menu) => {
            menu.style.display = "none";
          });
        }
      });
    });
    
    document.addEventListener("DOMContentLoaded", () => {
      // Search Form
      document.querySelector(".search-form").addEventListener("submit", function(event) {
          event.preventDefault();
          const searchInput = document.querySelector(".search-form input").value;
          const url = new URL(window.location);
          url.searchParams.set("search", searchInput);
          window.location.href = url.toString();
      });
  
      // Toggle Categories
      document.querySelectorAll(".category").forEach(category => {
          category.addEventListener("click", function() {
              document.querySelectorAll(".category").forEach(cat => cat.classList.remove("active"));
              this.classList.add("active");
              const selectedCategory = this.dataset.category;
  
              const url = new URL(window.location);
              url.searchParams.set("category", selectedCategory);
              window.location.href = url.toString();
          });
      });
  
      // Sorting
      document.querySelectorAll(".sort-items li").forEach(option => {
          option.addEventListener("click", function() {
              const sortValue = this.getAttribute("onclick").split("'")[1]; // Extract sort type
              const url = new URL(window.location);
              url.searchParams.set("sort", sortValue);
              window.location.href = url.toString();
          });
      });
  });
  

document.addEventListener("DOMContentLoaded", () => {
    const faqCards = document.querySelectorAll(".faq-card");

    faqCards.forEach((card) => {
        const answer = card.querySelector(".answer");
        const toggleIcon = card.querySelector(".faq-toggle");

        // Get static paths from the data attributes
        const openIcon = toggleIcon.dataset.closedIcon;
        const closeIcon = toggleIcon.dataset.openIcon;

        toggleIcon.addEventListener("click", () => {
            if (answer.style.display === "none" || !answer.style.display) {
                answer.style.display = "block";
                toggleIcon.src = closeIcon;
                toggleIcon.alt = "Hide FAQ";
            } else {
                answer.style.display = "none";
                toggleIcon.src = openIcon;
                toggleIcon.alt = "Show FAQ";
            }
        });
    });
});


  //Progreess skill bar
  document.addEventListener("DOMContentLoaded", () => {
    const progressContainers = document.querySelectorAll(".progress-container");

    progressContainers.forEach((container) => {
        const progressValue = container.getAttribute("data-progress");
        const progressBar = container.querySelector(".progress");

        // Ensure the progress value is valid and animate the bar
        if (progressValue && !isNaN(progressValue) && progressValue >= 0 && progressValue <= 100) {
            progressBar.style.width = `${progressValue}%`;
        }
    });
});


//Hobbies slider
let nextDom = document.getElementById('next');
let prevDom = document.getElementById('prev');
let carouselDom = document.querySelector('.carousel');
let SliderDom = carouselDom.querySelector('.carousel .list');
let thumbnailBorderDom = document.querySelector('.carousel .thumbnail');
let thumbnailItemsDom = thumbnailBorderDom.querySelectorAll('.item');
let timeDom = document.querySelector('.carousel .time');

thumbnailBorderDom.appendChild(thumbnailItemsDom[0]);
let timeRunning = 3000;
let timeAutoNext = 7000;

nextDom.onclick = function(){
    showSlider('next');    
}

prevDom.onclick = function(){
    showSlider('prev');    
}
let runTimeOut;
let runNextAuto = setTimeout(() => {
    next.click();
}, timeAutoNext)
function showSlider(type){
    let  SliderItemsDom = SliderDom.querySelectorAll('.carousel .list .item');
    let thumbnailItemsDom = document.querySelectorAll('.carousel .thumbnail .item');
    
    if(type === 'next'){
        SliderDom.appendChild(SliderItemsDom[0]);
        thumbnailBorderDom.appendChild(thumbnailItemsDom[0]);
        carouselDom.classList.add('next');
    }else{
        SliderDom.prepend(SliderItemsDom[SliderItemsDom.length - 1]);
        thumbnailBorderDom.prepend(thumbnailItemsDom[thumbnailItemsDom.length - 1]);
        carouselDom.classList.add('prev');
    }
    clearTimeout(runTimeOut);
    runTimeOut = setTimeout(() => {
        carouselDom.classList.remove('next');
        carouselDom.classList.remove('prev');
    }, timeRunning);

    clearTimeout(runNextAuto);
    runNextAuto = setTimeout(() => {
        next.click();
    }, timeAutoNext)
}


//category filter toggle
document.addEventListener("DOMContentLoaded", () => {
  const menuToggle = document.getElementById("menu-toggle");
  const menuItems = document.getElementById("menu-items");

  menuToggle.addEventListener("click", () => {
      // Toggle the menu's visibility
      menuItems.classList.toggle("open");
  });
});


//freelance card js
const cardWrapper = document.querySelector('.card-wrapper');
const cards = document.querySelectorAll('.card');
const prevBtn = document.querySelector('.prev-btn');
const nextBtn = document.querySelector('.next-btn');
const showAllBtn = document.querySelector('.show-all');

let currentIndex = 1; // Start with the second card as the middle one
const totalCards = cards.length;

// Function to update card positions and middle card
function updateSlider() {
  const offset = -currentIndex * 220; // Adjust based on card width and margin
  cardWrapper.style.transform = `translateX(${offset}px)`;

  // Remove 'middle' class from all cards and add it to the current middle card
  cards.forEach(card => card.classList.remove('middle'));
  cards[currentIndex].classList.add('middle');
}

// Add event listeners for buttons
prevBtn.addEventListener('click', () => {
  if (currentIndex > 0) {
    currentIndex--;
    updateSlider();
  }
});

nextBtn.addEventListener('click', () => {
  if (currentIndex < totalCards - 1) {
    currentIndex++;
    updateSlider();
  }
});

// Show all clients button
showAllBtn.addEventListener('click', () => {
  alert('Display all clients here!');
});

// Initialize slider
updateSlider();



//footer dropdown
// Wait for the DOM to fully load
document.addEventListener("DOMContentLoaded", function () {
  // Select all navigation items
  const navigationItems = document.querySelectorAll(".navigaiton-items");

  navigationItems.forEach((item) => {
      const toggleButton = item.querySelector(".foot-nav-head img"); // Dropdown image
      const dropdownMenu = item.querySelector("ul"); // Corresponding dropdown menu

      toggleButton.addEventListener("click", function () {
          // Toggle the 'active' class on the corresponding dropdown menu
          dropdownMenu.classList.toggle("active");
      });
  });
});

document.addEventListener("DOMContentLoaded", function () {
  let showFormBtn = document.getElementById("showFormBtn");
  let contactForm = document.getElementById("contactForm");

  showFormBtn.addEventListener("click", function () {
      contactForm.style.display = "block";  // Show form
      showFormBtn.style.display = "none";  // Hide the button
  });
});

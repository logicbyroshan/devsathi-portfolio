document.addEventListener("DOMContentLoaded", function () {
  // Navbar toggle
  const hamburgerIcon = document.querySelector(".hamburger img");
  const hamburgerMenu = document.querySelector(".hamburger .hemburger-menu");

  if (hamburgerIcon && hamburgerMenu) {
    hamburgerIcon.addEventListener("click", () => {
      hamburgerMenu.classList.toggle("open");
    });
  }

  // Slider functionality
  let sliderIndex = 0;
  const slides = document.querySelectorAll(".slide");
  const slider = document.querySelector(".slider");

  function showSliderSlide(index) {
    sliderIndex = (index + slides.length) % slides.length;
    slider.style.transform = `translateX(-${sliderIndex * 960}px)`;
  }

  document.querySelector(".next")?.addEventListener("click", () => showSliderSlide(sliderIndex + 1));
  document.querySelector(".prev")?.addEventListener("click", () => showSliderSlide(sliderIndex - 1));
  setInterval(() => showSliderSlide(sliderIndex + 1), 5000);

  // Typing effect
  const skillText = document.getElementById("skill-text");
  const skills = ["Python Developer", "Web Developer", "Creative Thinker", "Innovative Coder"];
  let currentSkill = 0, charIndex = 0;

  function typeSkill() {
    if (charIndex < skills[currentSkill].length) {
      skillText.textContent += skills[currentSkill][charIndex++];
      setTimeout(typeSkill, 100);
    } else {
      setTimeout(eraseSkill, 1500);
    }
  }

  function eraseSkill() {
    if (charIndex > 0) {
      skillText.textContent = skills[currentSkill].substring(0, --charIndex);
      setTimeout(eraseSkill, 50);
    } else {
      currentSkill = (currentSkill + 1) % skills.length;
      setTimeout(typeSkill, 100);
    }
  }

  setTimeout(typeSkill, 1500);

// FAQ Toggle
document.querySelectorAll(".faq-card").forEach(card => {
  const answer = card.querySelector(".answer");
  const toggleIcon = card.querySelector(".faq-toggle");

  // Fetching correct paths from attributes
  const openIcon = toggleIcon.getAttribute("data-closed-icon");  
  const closeIcon = toggleIcon.getAttribute("data-open-icon");   

  toggleIcon.addEventListener("click", () => {
      answer.classList.toggle("visible");
      
      // Force browser to update the image
      toggleIcon.src = answer.classList.contains("visible") ? closeIcon + "?v=" + new Date().getTime() : openIcon + "?v=" + new Date().getTime();
  });
});


  // Progress bar animation
  document.querySelectorAll(".progress-container").forEach(container => {
    const progressBar = container.querySelector(".progress");
    const progressValue = container.dataset.progress;

    if (!isNaN(progressValue) && progressValue >= 0 && progressValue <= 100) {
      progressBar.style.width = `${progressValue}%`;
    }
  });

  // Sorting dropdown toggle
  document.querySelectorAll(".cards-sort .outline-btn").forEach(button => {
    button.addEventListener("click", event => {
      const dropdown = event.target.closest(".cards-sort").querySelector(".sort-items");
      document.querySelectorAll(".sort-items").forEach(menu => menu !== dropdown && menu.classList.remove("open"));
      dropdown.classList.toggle("open");
    });
  });

  document.addEventListener("click", event => {
    if (!event.target.closest(".cards-sort")) {
      document.querySelectorAll(".sort-items").forEach(menu => menu.classList.remove("open"));
    }
  });

  // Search form handling
  document.querySelector(".search-form")?.addEventListener("submit", event => {
    event.preventDefault();
    const searchInput = document.querySelector(".search-form input").value;
    if (searchInput) {
      const url = new URL(window.location);
      url.searchParams.set("search", searchInput);
      window.location.href = url.toString();
    }
  });

  // Footer dropdown
  document.querySelectorAll(".navigaiton-items .foot-nav-head img").forEach(toggleButton => {
    toggleButton.addEventListener("click", function () {
      this.closest(".navigaiton-items").querySelector("ul").classList.toggle("active");
    });
  });

  // Contact form toggle
  document.getElementById("showFormBtn")?.addEventListener("click", () => {
    document.getElementById("contactForm").style.display = "block";
    document.getElementById("showFormBtn").style.display = "none";
  });
});

document.addEventListener("DOMContentLoaded", function () {
    let contactForm = document.getElementById("contactForm");
    if (!contactForm) {
        console.error("❌ contactForm not found!");
        return; // Stop script execution
    }

    contactForm.addEventListener("submit", async function (event) {
        event.preventDefault(); // Stop refresh
        console.log("Form submission started");

        let formData = new FormData(this);
        let responseMessage = document.getElementById("formMessage");

        try {
            let response = await fetch("/contact/", {
                method: "POST",
                body: formData,
                headers: {
                    "X-Requested-With": "XMLHttpRequest"
                }
            });

            let result = await response.json();
            console.log("Response received:", result);

            if (result.success) {
                responseMessage.textContent = "✅ Message sent successfully!";
                responseMessage.style.color = "green";
                this.reset();
            } else {
                responseMessage.textContent = "❌ Failed to send message.";
                responseMessage.style.color = "red";
                console.error("Error:", result.error);
            }
        } catch (error) {
            console.error("Fetch error:", error);
            responseMessage.textContent = "❌ An error occurred.";
            responseMessage.style.color = "red";
        }
    });
});

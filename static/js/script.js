const menuToggle = document.querySelector(".menu-toggle");
const mainNav = document.querySelector("#main-nav");

if (menuToggle && mainNav) {
  menuToggle.addEventListener("click", () => {
    const isOpen = menuToggle.getAttribute("aria-expanded") === "true";
    menuToggle.setAttribute("aria-expanded", String(!isOpen));
    menuToggle.setAttribute("aria-label", isOpen ? "Abrir menú" : "Cerrar menú");
    mainNav.classList.toggle("is-open", !isOpen);
  });

  mainNav.querySelectorAll("a").forEach((link) => {
    link.addEventListener("click", () => {
      menuToggle.setAttribute("aria-expanded", "false");
      menuToggle.setAttribute("aria-label", "Abrir menú");
      mainNav.classList.remove("is-open");
    });
  });
}

const formatSelect = document.querySelector("#formato-select");
document.querySelectorAll("[data-format]").forEach((link) => {
  link.addEventListener("click", () => {
    if (formatSelect) formatSelect.value = link.dataset.format;
  });
});

const observer = "IntersectionObserver" in window
  ? new IntersectionObserver((entries, currentObserver) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add("is-visible");
          currentObserver.unobserve(entry.target);
        }
      });
    }, { threshold: 0.12 })
  : null;

document.querySelectorAll(".reveal").forEach((element) => {
  if (observer) observer.observe(element);
  else element.classList.add("is-visible");
});

const dateInput = document.querySelector('input[name="fecha"]');
if (dateInput) {
  const today = new Date();
  const localToday = new Date(today.getTime() - today.getTimezoneOffset() * 60000)
    .toISOString()
    .slice(0, 10);
  dateInput.min = localToday;
}

const bookingForm = document.querySelector("#booking-form");
const feedback = document.querySelector("#form-feedback");

if (bookingForm && feedback) {
  bookingForm.addEventListener("submit", async (event) => {
    event.preventDefault();
    if (!bookingForm.reportValidity()) return;

    const submitButton = bookingForm.querySelector('button[type="submit"]');
    submitButton.disabled = true;
    feedback.textContent = "Enviando tu solicitud…";
    feedback.className = "form-feedback";

    try {
      const response = await fetch("/reservar", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(Object.fromEntries(new FormData(bookingForm))),
      });
      const result = await response.json();
      if (!response.ok || !result.ok) throw new Error(result.message || "No se pudo enviar la solicitud.");

      feedback.textContent = result.message;
      feedback.classList.add("success");
      bookingForm.reset();
    } catch (error) {
      feedback.textContent = error.message || "No se pudo conectar. Inténtalo de nuevo.";
      feedback.classList.add("error");
    } finally {
      submitButton.disabled = false;
    }
  });
}

const year = document.querySelector("#year");
if (year) year.textContent = new Date().getFullYear();

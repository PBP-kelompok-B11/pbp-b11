document.addEventListener("DOMContentLoaded", function () {
  loadGallery(); // Load gallery otomatis saat halaman dibuka
});

// 1. Fungsi AJAX ambil item gallery
function loadGallery() {
  fetch("/gallery/get-gallery-items/")   // URL Django ke view get_gallery_items
    .then(response => response.json())
    .then(data => {
      const container = document.getElementById("gallery-container");
      container.innerHTML = "";

      data.forEach(item => {
        const card = document.createElement("div");
        card.className = "bg-white rounded-lg shadow-lg overflow-hidden cursor-pointer transform hover:scale-105 transition";
        card.innerHTML = `
          <img src="${item.image_url}" class="w-full h-48 object-cover">
          <div class="p-4">
            <p class="font-bold text-gray-800">${item.deskripsi}</p>
          </div>
        `;
        card.addEventListener("click", () => openModal(item.image_url, item.deskripsi));
        container.appendChild(card);
      });
    })
    .catch(error => console.error("Error loading gallery:", error));
}

// 2. Fungsi Modal
const modal = document.getElementById("gallery-modal");
const modalImg = document.getElementById("modal-image");
const modalDesc = document.getElementById("modal-description");
const closeModalBtn = document.getElementById("close-modal");

function openModal(image, description) {
  modal.classList.remove("hidden");
  modal.classList.add("flex");
  modalImg.src = image;
  modalDesc.textContent = description;
}

closeModalBtn.addEventListener("click", () => {
  modal.classList.add("hidden");
  modal.classList.remove("flex");
});

// Tutup modal jika klik overlay
modal.addEventListener("click", function (e) {
  if (e.target === this) {
    modal.classList.add("hidden");
    modal.classList.remove("flex");
  }
});

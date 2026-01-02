// ===============================
// Pokémon Bag Frontend Logic
// ===============================

// ---------- CONSTANTS ----------
const VISIBLE_ITEMS = 7;
const CATEGORIES = ["Items", "Balls", "Key Items"];

// ---------- STATE ----------
let currentCategory = "Items";
let selectedIndex = 0;
let scrollOffset = 0;
let musicMuted = false;

// ---------- DOM ----------
const bagTitle = document.getElementById("bagTitle");

const bagImage = document.getElementById("bagImage");
const itemList = document.getElementById("itemList");
const itemIcon = document.getElementById("itemIcon");
const itemText = document.getElementById("itemText");
const muteBtn = document.getElementById("muteBtn");
const categoryButtons = document.querySelectorAll("[data-category]");

// ---------- BAG IMAGE MAP ----------
const bagImageMap = {
    "Items": "Items.png",
    "Balls": "PokeBalls.png",
    "Key Items": "keyitems.png",
    "Closed": "Closed.png"
};

// ---------- AUDIO ----------
const clickSound = new Audio("/static/audio/blip.wav");
clickSound.volume = 0.6;

const themeMusic = new Audio("/static/audio/theme.wav");
themeMusic.loop = true;
themeMusic.volume = 0.4;

// Start music after first interaction
document.addEventListener(
    "click",
    () => {
        if (!musicMuted && themeMusic.paused) {
            themeMusic.play().catch(() => {});
        }
    },
    { once: true }
);

// ---------- HELPERS ----------
function playClick() {
    if (musicMuted) return;
    clickSound.currentTime = 0;
    clickSound.play().catch(() => {});
}

function setBagImage(category) {
    const file = bagImageMap[category];
    if (file) {
        bagImage.src = `/static/images/bag/${file}`;
    }
}

function clearDescription() {
    itemIcon.classList.add("hidden");
    itemText.textContent = "Select an item to see its description.";
}

function updateBagTitle(category) {
    if (category === "Items") bagTitle.textContent = "ITEMS POCKET";
    else if (category === "Balls") bagTitle.textContent = "BALLS POCKET";
    else if (category === "Key Items") bagTitle.textContent = "KEY ITEMS POCKET";
}


// ---------- PREVIEW ITEM ----------
function showItem(item) {
    itemText.textContent = item.description || "";

    if (item.icon) {
        itemIcon.src = `/static/images/icons/firered_33_items/${item.icon}`;
        itemIcon.classList.remove("hidden");
    } else {
        itemIcon.classList.add("hidden");
    }
}

// ---------- LOAD CATEGORY ----------
async function loadCategory(category) {
    playClick();
    currentCategory = category;
    updateBagTitle(category);

    clearDescription();
    setBagImage(category);

    itemList.innerHTML = "<li class='placeholder'>Loading...</li>";

    try {
        const res = await fetch(`/api/bag/items/${category}`);
        const items = await res.json();

        itemList.innerHTML = "";

        items.forEach(item => {
            const li = document.createElement("li");
            li.textContent = item.name;

            // Store data for keyboard preview
            li.dataset.item = JSON.stringify(item);

            // Mouse click = activate
            li.addEventListener("click", () => {
                playClick();
                showItem(item);
            });

            itemList.appendChild(li);
        });

        // Reset cursor state
        selectedIndex = 0;
        scrollOffset = 0;
        updateSelection();

        // Highlight active bag button
        categoryButtons.forEach(btn => {
            btn.classList.toggle(
                "active",
                btn.dataset.category === currentCategory
            );
        });

    } catch (err) {
        console.error(err);
        itemList.innerHTML =
            "<li class='placeholder'>Failed to load items</li>";
    }
}

// ---------- UPDATE CURSOR + WINDOW ----------
function updateSelection() {
    const items = document.querySelectorAll("#itemList li");
    if (!items.length) return;

    // Clamp window
    if (selectedIndex < scrollOffset) {
        scrollOffset = selectedIndex;
    }
    if (selectedIndex >= scrollOffset + VISIBLE_ITEMS) {
        scrollOffset = selectedIndex - VISIBLE_ITEMS + 1;
    }

    items.forEach((li, index) => {
        li.classList.toggle("active", index === selectedIndex);
        li.style.display =
            index >= scrollOffset &&
            index < scrollOffset + VISIBLE_ITEMS
                ? "block"
                : "none";
    });

    // Preview item (NO click)
    const data = items[selectedIndex].dataset.item;
    if (data) {
        showItem(JSON.parse(data));
    }
}

// ---------- KEYBOARD CONTROLS ----------
document.addEventListener("keydown", e => {
    const items = document.querySelectorAll("#itemList li");

    // ▲ / ▼ item navigation
    if (e.key === "ArrowDown" && items.length) {
        selectedIndex = (selectedIndex + 1) % items.length;
        playClick();              // 🔊 cursor sound
        updateSelection();
        e.preventDefault();
    }

    if (e.key === "ArrowUp" && items.length) {
        selectedIndex =
            (selectedIndex - 1 + items.length) % items.length;
        playClick();              // 🔊 cursor sound
        updateSelection();
        e.preventDefault();
    }

    // ◀ / ▶ bag switching
    if (e.key === "ArrowRight") {
        playClick();              // 🔊 pocket switch sound
        let i = CATEGORIES.indexOf(currentCategory);
        let next = CATEGORIES[(i + 1) % CATEGORIES.length];
        loadCategory(next);
        e.preventDefault();
    }

    if (e.key === "ArrowLeft") {
        playClick();              // 🔊 pocket switch sound
        let i = CATEGORIES.indexOf(currentCategory);
        let prev =
            CATEGORIES[(i - 1 + CATEGORIES.length) % CATEGORIES.length];
        loadCategory(prev);
        e.preventDefault();
    }
});


// ---------- BUTTON EVENTS ----------
categoryButtons.forEach(btn => {
    btn.addEventListener("click", () => {
        loadCategory(btn.dataset.category);
    });
});

muteBtn.addEventListener("click", () => {
    playClick();
    if (musicMuted) {
        themeMusic.play().catch(() => {});
        muteBtn.textContent = "MUTE";
        musicMuted = false;
    } else {
        themeMusic.pause();
        muteBtn.textContent = "UNMUTE";
        musicMuted = true;
    }
});

// ---------- INIT ----------
updateBagTitle(currentCategory);
setBagImage("Closed");
clearDescription();

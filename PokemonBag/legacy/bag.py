# Description:
# This file handles the complete graphical user interface (GUI) for the Pokémon Bag system.
# It uses Tkinter for window management and layout, PIL for image rendering, and winsound
# for background music and sound effects.
#
# The bag interface supports multiple item categories (Items, Poké Balls, Key Items),
# dynamically displays item icons and descriptions, manages sound toggling,
# and mimics the in-game Pokémon FireRed bag experience.
#
# This module integrates data from external item dictionaries and icon mappings
# and serves as the main interactive entry point for the bag system.

import tkinter as tk
from PIL import Image, ImageTk
import os
import winsound

from items import pokemonItems, keyItems, pokeBalls
from ItemIcons import itemIcons

# ---------------- PATHS ----------------
BASE_PATH = os.path.dirname(os.path.abspath(__file__))

IMAGE_PATH = os.path.join(BASE_PATH, "BagImages")
ICON_PATH = os.path.join(BASE_PATH, "icons", "firered_33_items")
CLICK_SOUND = os.path.join(BASE_PATH, "sound", "blip.wav")
THEME_SOUND = os.path.join(BASE_PATH, "sound", "theme.wav")

# ---------------- DATA ----------------
bagImages = {
    "Closed": "Closed.png",
    "Items": "Items.png",
    "Balls": "PokeBalls.png",
    "Key Items": "keyitems.png"
}

bagData = {
    "Items": pokemonItems,
    "Balls": pokeBalls,
    "Key Items": keyItems
}

# ---------------- STATE ----------------
bagWindow = None
currentImage = None
currentIcon = None
currentCategory = "Items"
musicMuted = False

# ---------------- SOUND (SAFE) ----------------
def playClick():
    if musicMuted:
        return
    try:
        winsound.PlaySound(
            CLICK_SOUND,
            winsound.SND_FILENAME | winsound.SND_ASYNC | winsound.SND_NOSTOP
        )
    except RuntimeError:
        pass

def startTheme():
    try:
        winsound.PlaySound(
            THEME_SOUND,
            winsound.SND_FILENAME | winsound.SND_ASYNC | winsound.SND_LOOP
        )
    except RuntimeError:
        pass

def toggleMusic():
    global musicMuted
    playClick()
    if musicMuted:
        startTheme()
        musicMuted = False
        musicBtn.config(text="MUTE")
    else:
        winsound.PlaySound(None, winsound.SND_PURGE)
        musicMuted = True
        musicBtn.config(text="UNMUTE")

# ---------------- ROOT ----------------
root = tk.Tk()
root.title("Minecraft Pokémon Bag")
root.geometry("520x340")
root.configure(bg="#1e1e1e")

startTheme()

# ---------------- BAG WINDOW ----------------
def openBag():
    global bagWindow, currentImage, currentCategory, currentIcon

    playClick()
    if bagWindow:
        return

    bagWindow = tk.Toplevel(root)
    bagWindow.title("Bag")
    bagWindow.geometry("720x500")
    bagWindow.configure(bg="#1e1e1e")
    bagWindow.grab_set()

    def closeBag():
        global bagWindow
        playClick()
        bagWindow.destroy()
        bagWindow = None

    main = tk.Frame(bagWindow, bg="#1e1e1e")
    main.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)

    # -------- LEFT PANEL --------
    leftPanel = tk.Frame(
        main, bg="#2563eb", width=200, height=340,
        highlightthickness=4, highlightbackground="#000"
    )
    leftPanel.pack(side=tk.LEFT)
    leftPanel.pack_propagate(False)

    imageLabel = tk.Label(leftPanel, bg="#2563eb")
    imageLabel.pack(expand=True)

    def updateBagImage(category):
        global currentImage
        img = Image.open(os.path.join(IMAGE_PATH, bagImages[category]))
        img = img.resize((176, 256), Image.NEAREST)
        currentImage = ImageTk.PhotoImage(img)
        imageLabel.config(image=currentImage)

    # -------- RIGHT PANEL --------
    rightPanel = tk.Frame(
        main, bg="#2a2a2a",
        highlightthickness=4, highlightbackground="#000"
    )
    rightPanel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(8, 0))

    listBox = tk.Listbox(
        rightPanel, bg="#3a3a3a", fg="#e5e7eb",
        font=("Courier New", 11),
        selectbackground="#22c55e",
        selectforeground="#000",
        relief=tk.FLAT, highlightthickness=0, height=10
    )
    listBox.pack(fill=tk.X, padx=6, pady=6)

    descFrame = tk.Frame(
        rightPanel, bg="#1e1e1e",
        highlightthickness=4, highlightbackground="#000"
    )
    descFrame.pack(fill=tk.BOTH, expand=True, padx=6, pady=(0, 6))

    iconLabel = tk.Label(descFrame, bg="#1e1e1e")
    iconLabel.pack(side=tk.LEFT, padx=6, pady=6)

    descLabel = tk.Label(
        descFrame, bg="#1e1e1e", fg="#a7f3d0",
        font=("Courier New", 10),
        wraplength=300, justify="left", anchor="nw"
    )
    descLabel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    def showCategory(category):
        global currentCategory
        playClick()
        currentCategory = category
        listBox.delete(0, tk.END)
        descLabel.config(text="")
        iconLabel.config(image="")
        updateBagImage(category)
        for item in bagData[category]:
            listBox.insert(tk.END, item)

    def showDescription(event):
        global currentIcon
        if not listBox.curselection():
            return
        playClick()
        item = listBox.get(listBox.curselection()[0])
        descLabel.config(text=bagData[currentCategory].get(item, ""))

        iconFile = itemIcons.get(item)
        if iconFile:
            icon = Image.open(os.path.join(ICON_PATH, iconFile))
            icon = icon.resize((48, 48), Image.NEAREST)
            currentIcon = ImageTk.PhotoImage(icon)
            iconLabel.config(image=currentIcon)
        else:
            iconLabel.config(image="")

    listBox.bind("<<ListboxSelect>>", showDescription)

    btnFrame = tk.Frame(bagWindow, bg="#1e1e1e")
    btnFrame.pack(pady=6)

    def pixelButton(text, command):
        return tk.Button(
            btnFrame, text=text,
            command=lambda: (playClick(), command()),
            bg="#4ade80", fg="#000",
            font=("Courier New", 10, "bold"),
            bd=4, width=10, activebackground="#22c55e"
        )

    pixelButton("ITEMS", lambda: showCategory("Items")).pack(side=tk.LEFT, padx=4)
    pixelButton("BALLS", lambda: showCategory("Balls")).pack(side=tk.LEFT, padx=4)
    pixelButton("KEY", lambda: showCategory("Key Items")).pack(side=tk.LEFT, padx=4)
    pixelButton("CLOSE", closeBag).pack(side=tk.LEFT, padx=4)

    updateBagImage("Closed")
    showCategory("Items")

    bagWindow.protocol("WM_DELETE_WINDOW", closeBag)

# ---------------- MAIN MENU ----------------
tk.Label(
    root, text="MINECRAFT-STYLE POKÉMON BAG",
    bg="#1e1e1e", fg="#22c55e",
    font=("Courier New", 14, "bold")
).pack(pady=20)

tk.Button(
    root, text="OPEN BAG",
    font=("Courier New", 12, "bold"),
    bg="#4ade80", fg="#000",
    bd=6, width=20, command=openBag
).pack(pady=6)

musicBtn = tk.Button(
    root, text="MUTE",
    font=("Courier New", 10, "bold"),
    bg="#60a5fa", fg="#000",
    bd=4, width=12, command=toggleMusic
)
musicBtn.pack(pady=6)

root.mainloop()

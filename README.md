# D2 Survivors Save Editor — EXE

**A community-made save editor for D2 Survivors, created by Just a Polish Guy.**

This repository contains the **standalone EXE version for Windows**: download it, double-click it, done. No Python needed.

> ### 🆓 This is the DEMO — the full version is free on Discord
> The EXE here is **v10.9 Demo** and works with D2 Survivors **2026.1102.1**. You can load your save, change gold, see every Charsi upgrade with its cost,
> look at all your items and stash, and check your save with the game's own rules.
> The Item Generator, Runewords, Charms, DEV GENERATION, COPY ITEM, DESIGN, Skills and Belt editors are **previews**.
>
> **👉 Get the full version (free) on our Discord: https://discord.gg/nENzQxTh4**

**[➡️ Download the latest release](https://github.com/justPLguy/D2-Survivors-Save-Editor-EXE/releases/latest)**

---

## 🚀 Choose Your Version

| Version | Description | Repository |
|---|---|---|
| 💻 **EXE** | Standalone Windows application. | [EXE Repository](https://github.com/justPLguy/D2-Survivors-Save-Editor-EXE) |
| 🐍 **Python** | Run the Python script directly. | [Python Repository](https://github.com/justPLguy/D2-Survivors-Save-Editor-PY) |
| 🌐 **Web** | Browser-based version. | [Web Repository](https://github.com/justPLguy/D2-Survivors-Save-Editor-Web) |

- Choose **EXE** for the most straightforward Windows setup.
- Choose **Python** if you want to run the source script yourself.
- Choose **Web** if you prefer a browser-based editor.

Features may differ between versions. Check the relevant repository for details.

## 🆕 What's New Since 10.5

- **10.9: weapon damage, 한국어 game texts and Undo.**
  - Weapon tooltips show **One-Hand / Two-Hand Damage** exactly like the game (checked on 12,905 weapons). Armor, helms and shields show a **Base Defense** line.
  - **한국어 game texts:** in Korean, item names, stat lines and skills are shown like D2 Survivors shows them. The editor reads them from your own game install (`resources\app.asar`); nothing is bundled with the editor or changed in the game.
  - **Undo Last Change** steps back one change at a time.
  - Full version: **Delete item** (with undo), **Copy with a new roll** from a chosen difficulty (Normal, Nightmare, Hell or a Terror tier), and a **50-100% slider** for wanted rolls.
- **10.8: game 2026.1102.1 support.** The editor's tables come from the new game, and every check matches it again.
  - **Second weapon set:** Equipped lists [weapon set I] / [weapon set II], and Check save covers both.
  - Item tooltips show **Required Level** like the game.
  - Bul-Kathos' Sacred Charge, Famine and Naj's Circlet read as legit from both Diablo II and Resurrected files.
  - Full version: weapons and shields can go into either set; runewords on class bases keep the base's property; Civerb's Cudgel and Trang-Oul's Claws come with their new fixed bonuses.
- **10.7: DEV GENERATION** (full version): any unique or set item with up to 48 stats of your choice, values 1-1000, for testing builds offline.
- **10.6: Set values directly beyond the game's ranges** (full version): any value the game still reads, up to ±1000, for testing builds offline.

Items made with DEV GENERATION or Set values directly are always **NOT LEGIT** (red border in the game; worn, they keep runs off the ladder).

## ✨ Features (v10.9)

| Feature | Demo (here) | Full version (Discord) |
|---|:---:|:---:|
| Load / export save codes, automatic backup before every export | ✅ | ✅ |
| **Gold & Charsi**: gold editing, every Charsi upgrade with gold spent, next price and gold to max | ✅ | ✅ |
| **Update notice**: shows when a newer stable version is out on Discord | ✅ | ✅ |
| **6 languages**: English, Polski, Deutsch, Français, 한국어, 简体中文 (globe and flag, top right) | ✅ | ✅ |
| **한국어 game texts** read from your own D2 Survivors install | ✅ | ✅ |
| **Undo Last Change** | ✅ | ✅ |
| Character & Mercenary, active hero bar | ✅ | ✅ |
| **Both weapon sets** shown and checked | ✅ | ✅ |
| Items & Modifiers: every stat, its range and **LEGIT / NOT LEGIT** status | 👁️ view | ✅ edit |
| Item tooltips exactly like in the game (All Resistances, weapon damage, final Defense, set bonuses, Required Level) + Base Defense line | ✅ | ✅ |
| Stash: personal and shared stash tabs | ✅ | ✅ |
| Reference: every unique, set item and runeword with its ranges | ✅ | ✅ |
| Check save with the game's own rules (items + hero builds) | ✅ | ✅ |
| Save Manager | ✅ | ✅ |
| **Item Generator**: unique, set, rare, magic and white items made exactly like the game makes them | 👁️ preview | ✅ |
| **Runewords** and **Charms** generators | 👁️ preview | ✅ |
| **COPY ITEM**: copy an item to any hero's inventory, gear, mercenary or stash | 👁️ preview | ✅ |
| COPY ITEM with a brand new roll, dropped in the difficulty you choose | 👁️ preview | ✅ |
| **Delete item** (Undo brings it back) | 👁️ preview | ✅ |
| Rares with up to 6 chosen affixes (multi-core search), 50-100% slider for wanted rolls | 👁️ preview | ✅ |
| **DESIGN**: pick the picture of rings, amulets and charms | 👁️ preview | ✅ |
| Re-roll items to the values you want (stays legit) | 👁️ preview | ✅ |
| Put weapons and shields into **either weapon set** | 👁️ preview | ✅ |
| **Set values directly**, also beyond the game's ranges (up to ±1000, Not legit) | 👁️ preview | ✅ |
| **DEV GENERATION**: unique or set items with up to 48 stats of your choice (Not legit) | 👁️ preview | ✅ |
| **Skills** editor, **Belt & Potions** editor | 👁️ preview | ✅ |

For the exact changes in each build, check the [release notes](https://github.com/justPLguy/D2-Survivors-Save-Editor-EXE/releases).

## 💻 How to Download and Run

### 1. Download

1. Open the **[latest release](https://github.com/justPLguy/D2-Survivors-Save-Editor-EXE/releases/latest)**.
2. Under **Assets**, download `D2 Survivors Save Editor 10.9 Demo.exe`.
3. Move it to a folder where you want to keep the editor and double-click it.

Download the executable only from this official repository, not from third-party websites.

Works with D2 Survivors **2026.1102.1** (saves from 2026.1101.1 load too).

### 2. Edit Your Save

1. In the game, open **SAVES** and copy your save code (it starts with `D2S1:`).
2. In the editor, click **Paste Clipboard**, then **Load Save Code**.
3. Pick your hero in **Character & Mercenary** and make your changes (for example, gold in the **Gold & Charsi** tab).
4. Click **Generate Save Code**, review the change list and click **Copy Code**.
5. In the game, open **SAVES**, paste the new code and load it.

Not sure where to start? Open the red **HOW TO USE EDITOR** tab inside the editor: it explains every tab and button.
To change the language, click the globe and flag in the top-right corner.
In 한국어 the editor looks for D2 Survivors on its own; if it can't find it, choose the game folder under the globe ("D2 Survivors folder").

**Always keep a copy of your original save code before making changes.**

## ⚠️ Important Warning

The editor is made for **offline fun, not for the ladder**. Edited items or characters may be marked by the game,
and runs made with a marked character may not count towards leaderboards.

Use the editor at your own risk. Keep an untouched copy of your original save code and check your character in-game after editing.

## 🛡️ Windows Security Notice

The EXE is not code-signed, so Windows SmartScreen may show **"Windows protected your PC"** the first time you run it.
If you downloaded it from this repository's Releases page, click **More info → Run anyway**.

If you prefer not to run an unsigned EXE, use the [Python version](https://github.com/justPLguy/D2-Survivors-Save-Editor-PY) instead.

## 🔔 Update Notice

At start-up the editor checks [`version.json`](version.json) in this repository to see which stable version is the newest.
It only reads that version number: **nothing is sent, downloaded or installed.**
Green **UP TO DATE** means you have the newest stable version. A flashing red/orange notice means a new version is waiting on Discord.

## 🔒 Sharing Saves (optional)

After every export the editor asks whether you want to share the save code with the editor's database to help improve the editor.
**Nothing is sent unless you click Yes.** Choosing No keeps everything on your computer.

## 📦 Releases & Patch Notes

Every release has its own patch notes describing changes, new features, fixes, and known issues:

**[➡️ EXE Releases](https://github.com/justPLguy/D2-Survivors-Save-Editor-EXE/releases)**

## 💬 Discord — Full Version, Help and Bug Reports

The **full version is free** on our Discord, together with updates, help and item requests.
Found a bug or have an idea? Report it there, every report helps!

**👉 https://discord.gg/nENzQxTh4**

## 🔗 Other Projects

- 💻 [D2 Survivors Save Editor — EXE](https://github.com/justPLguy/D2-Survivors-Save-Editor-EXE)
- 🐍 [D2 Survivors Save Editor — Python](https://github.com/justPLguy/D2-Survivors-Save-Editor-PY)
- 🌐 [D2 Survivors Save Editor — Web](https://github.com/justPLguy/D2-Survivors-Save-Editor-Web)

## 📺 Follow Just a Polish Guy

Follow my channels for updates, tutorials, gaming content, and more.

- **YouTube:** [@justPLguy](https://www.youtube.com/@justPLguy)
- **Facebook:** [Just a Polish Guy](https://www.facebook.com/justPLguy/)
- **Discord:** [Join the community](https://discord.gg/nENzQxTh4)

## 👤 About the Creator

Created by **Just a Polish Guy** for the D2 Survivors community.

If you find this project useful, consider following my channels and checking out the other versions of the editor.

---

*D2 Survivors Save Editor is an independent community-made project. It is not an official game tool and is not affiliated with the game's developers.*

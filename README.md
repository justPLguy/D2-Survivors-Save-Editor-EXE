# D2 Survivors Save Editor

A community-made save editor for **D2 Survivors**. Version 6.4 adds a separate, side-by-side selector for a character and that character's assigned mercenary.

> **Important:** Back up your save before editing. This is an unofficial community tool and is not affiliated with or endorsed by the creators of D2 Survivors or Diablo II.

## Features

- Load and decode `D2S1:` save codes.
- Edit the shared gold value.
- Browse character classes and equipped items.
- Browse a character's assigned mercenary separately from the character.
- Edit numeric item modifiers.
- Keep pending modifier edits when switching between items.
- Generate a modified `D2S1:` save code and save it to a text file.
- Preserve the existing save data structure when encoding the edited save.

## Download for Windows

Open **GitHub → Releases** and download the latest `D2SurvivorsSaveEditor-vX.Y-Windows.zip`.

1. Download and extract the ZIP.
2. Keep `D2SurvivorsSaveEditor.exe` and the `_internal` folder together.
3. Double-click `D2SurvivorsSaveEditor.exe`.
4. Keep a backup of your original save code before making changes.

The portable `onedir` build requires the complete folder. **Do not move or upload only the EXE** from inside that folder.

## Build from source

Requirements: Windows and Python 3.10+ available on `PATH`.

1. Download `D2_Survivors_Save_Editor.py`.
2. Open Command Prompt in the source directory.
3. Install PyInstaller:

   ```powershell
   python -m pip install --upgrade pyinstaller
   ```

4. Build a portable folder:

   ```powershell
   python -m PyInstaller --noconfirm --clean --onedir --windowed --noupx --name D2SurvivorsSaveEditor D2_Survivors_Save_Editor.py
   ```

5. The application is created in `dist/D2SurvivorsSaveEditor/`. Keep the entire directory together.

To build a single-file EXE instead, remove `--onedir` and use `--onefile`; note that packaging mode can affect antivirus heuristics and startup behavior.

## Antivirus / VirusTotal transparency

Packaged Python executables can receive heuristic detections, but a low detection count does **not** prove a file is safe, and a detection does **not** by itself prove malware.

During initial testing on **22 October 2026**, the developer observed:
- One `onedir` ZIP scan: **1/67** engines flagged the archive.
- The EXE inside that build: **4/71** engines flagged it.

These results are snapshots, not a guarantee of safety, and VirusTotal results can change. The observed report included generic/heuristic labels. No independent security audit has been completed. Users should review the exact release asset and its current scan results themselves. Do not upload personal save files to public scanning services.

## Known limitations

- The editor changes numeric modifiers that are already present on supported item records; it does not create arbitrary new modifiers.
- The mercenary selector lists mercenary data found in the save. It does not edit the mercenary's level, skills, or other character statistics.
- Antivirus behavior varies between products and versions.
- The application has been tested by the maintainer on their own Windows setup; compatibility with every Windows configuration is not guaranteed.

## Support and bug reports

Please open a GitHub Issue and include:
- Windows version,
- editor version,
- a description of the steps that caused the issue,
- the exact error message, if any.

**Never post your full save code publicly** unless you are comfortable sharing all data contained in it. A small redacted example is preferable.

## Credits

Created by **Just a Polish Guy**.

- YouTube: https://www.youtube.com/@justPLguy
- Source repository: add the final repository URL here after creating it.

## License

See [`LICENSE_OPTIONS.md`](LICENSE_OPTIONS.md). Before publishing, choose one license and place its full text in a root-level file named `LICENSE`. Do not publish with multiple competing licenses unless you intentionally want to offer dual licensing.

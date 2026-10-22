# D2 Survivors Save Editor v6.4

**Release type:** Initial public release candidate  
**Build target:** Windows x64 (portable PyInstaller `onedir` package)

## Highlights

- Adds a dedicated mercenary selector beside the character-class selector.
- Displays the mercenary associated with the currently selected character class.
- Keeps character equipment and mercenary equipment in separate browsing contexts.
- Retains existing save-code loading/encoding, gold editing, and numeric item-modifier editing.

## Download and install

Download `D2SurvivorsSaveEditor-v6.4-Windows.zip` from the Assets section below, extract the full archive, and run `D2SurvivorsSaveEditor.exe`.

Keep the `_internal` folder alongside the EXE. Do not extract or distribute only the EXE.

## Important notes

- Back up your save before editing.
- This is an unofficial community tool.
- Initial VirusTotal checks on 22 October 2026 showed 1/67 detections for the portable ZIP and 4/71 for the EXE in that build. These results can change and are not a security guarantee. The application has not undergone an independent security audit.
- If Windows or an antivirus product warns about the file, do not blindly disable protection. Review the source and the exact release asset.

## Known limitations

- Edits numeric modifiers already present on item records; does not create arbitrary new modifiers.
- Does not edit mercenary level, skills, or other mercenary statistics.
- Tested on the maintainer's Windows setup; not verified on every Windows version.

## Source

The Python source is included in the repository.

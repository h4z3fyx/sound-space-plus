# iOS (iPhone and iPad)

[Polska instrukcja pobierania IPA i instalacji przez Sideloadly](iOS-sideload-pl.md).

SSP uses **Godot 3.5.3 stable**, not Godot 4. The iOS target is ARM64,
landscape, with touch controls and a Documents folder exposed in Apple's Files app.

## Build with GitHub Actions

1. Open **Actions → Build iOS IPA (Godot 3.5.3) → Run workflow** on your branch.
2. Download **Rhythia-Xcode** to build and sign locally, or
   **Rhythia-iOS-unsigned** for an IPA that you will sign with your own tooling.

The Linux job imports assets and exports an Xcode project. The macOS job archives
it with signing disabled and packages `Rhythia-unsigned.ipa`. Any failed export,
archive, or missing output fails the workflow. The unsigned IPA cannot be installed
directly and is not an App Store or TestFlight release.

## Install using Xcode

You need a Mac, Xcode with the iOS SDK, an Apple account, and an iPhone/iPad.

1. Extract **Rhythia-Xcode**, keeping all files together, and open
   `Rhythia.xcodeproj`.
2. Select the Rhythia target. In **Signing & Capabilities**, enable automatic
   signing, select your own Team, and use a unique bundle identifier.
   The preset's `0000000000` Team ID is only an export placeholder.
3. Select your connected device and run the app. Enable Developer Mode on the
   device if Xcode requests it. Personal Team signing is subject to Apple's limits;
   distribution through TestFlight/App Store requires the appropriate developer membership.

For a distribution build, archive and export the app using your own signing
certificate and provisioning profile in Xcode. No signing credentials are stored
in this repository.

## Local export

On Linux, install the official Godot 3.5.3 headless editor and place the matching
`iphone.zip` template in `~/.local/share/godot/templates/3.5.3.stable/`.
Then, from the repository root:

```sh
python3 tools/prepare_ios.py /tmp/ssp-ios-source
mkdir -p build/ios
godot --path /tmp/ssp-ios-source --export iOS "$PWD/build/ios/Rhythia.ipa"
```

Use a new destination directory outside the checkout for each preparation. The
script copies the source, substitutes a disabled Discord facade, removes desktop
native addons and their registry entries, and replaces native file dialog scripts
with placeholders so the built-in Godot file selector is used. Desktop sources
are preserved. Godot 3 on Linux exports the Xcode files without running Xcode;
macOS is needed to compile/sign them.

## Controls and data

- Drag to move the cursor. Use the touch pause button to pause, resume, or skip
  a long gap; hold the give-up button to quit a map.
- Buttons respect the screen safe area and the mirror-buttons setting.
- Tap the intro to skip it once skipping becomes available.
- Use **Files → On My iPhone/iPad → Rhythia** to manage maps and other user data.
  Keep maps in the `maps` subfolder and reload content in the game after copying.
- Discord Rich Presence, OpenVR, desktop native dialogs, and the desktop updater
  are unavailable on iOS. Update by installing a newer signed build with the same
  application identity to retain your data.

## Device verification

Before publishing, verify on an actual iPhone and iPad: first launch into the menu,
map download/import through Files, cursor movement, pause/resume/skip/give-up,
mirrored buttons after rotating the device, audio timing, background/foreground
behavior, and persistence after relaunch. Linux export alone does not verify these
or Apple distribution requirements.

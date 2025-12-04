Termux Screensaver (screensaver)
A fun and functional command-line utility to launch a classic Matrix-style screensaver directly in your Termux terminal. It uses the cmatrix utility to provide the visual effect.
🚀 Installation & Setup
 * Save the Script: Place screensaver.sh in your executable scripts directory (e.g., ~/termux-scripts/).
   # [Copy the screensaver.sh file content here]
chmod +x ~/termux-scripts/screensaver.sh

 * Create an Alias (Recommended): Add the following line to your shell configuration file (e.g., ~/.zshrc or ~/.bashrc) to make the command easy to run:
   alias screensaver='~/termux-scripts/screensaver.sh'

   Then run source ~/.zshrc (or .bashrc).
✨ Usage
The first time you run the script, it will check for the required cmatrix package and offer to install it.
Command
screensaver

Workflow
 * Running screensaver opens an interactive menu using fzf.
 * Select a style (e.g., "Matrix Rain" or "Binary Rain").
 * The screensaver begins.
 * To stop the screensaver, press Ctrl+C. The script automatically runs reset to fix any terminal colors or display settings afterward.
🎨 Available Styles
The utility uses fzf to present these options for cmatrix:
| Display Name | Description |
|---|---|
| Matrix Rain (Default) | Standard green matrix code rain. |
| Binary Rain | Classic black and white 1s and 0s. |
| Random Colors | Matrix code rain with a random color scheme. |
| Fast & Intense | A very fast version of the default matrix rain. |


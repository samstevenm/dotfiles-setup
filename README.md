# dotfiles-setup

### Install the `code` Command in PATH

1. **Open VS Code**.
2. **Press `Cmd+Shift+P` to open the Command Palette**.
3. **Type `shell command` and select `Install 'code' command in PATH`**.

After ensuring the `code` command is available, you can rerun the script. However, let's also update the script to check if the `code` command is available and provide a meaningful error message if it is not.
This repository contains a script to set up a development environment on a new machine or periodically back up your settings on an existing machine. The script installs Homebrew, Zsh, Oh My Zsh, zsh-autosuggestions, zsh-syntax-highlighting, and backs up all dotfiles to a "dotfiles" folder within the repository. It also creates symbolic links from your home directory to these backed-up dotfiles. Additionally, it stores a list of installed applications, Homebrew packages, and VSCode configurations, logs each run, and reminds you to commit the log file to the repository.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

The script is intended to be run on a Mac. It uses Homebrew to install packages, so if Homebrew is not already installed, the script will install it. Additionally, ensure that the VSCode CLI (`code` command) is installed and available in your PATH.

### Installing

1. Clone the repository:
    ```sh
    git clone https://github.com/samstevenm/dotfiles-setup.git
    ```

2. Navigate to the repository directory:
    ```sh
    cd dotfiles-setup
    ```

3. Run the script to backup and update your settings:
    ```sh
    python3 terraformer.py
    ```

### Initial Setup on a New Machine

To set up your development environment on a new machine, run the script with the `--setup` argument:
```sh
python3 terraformer.py --setup
```

## Usage

- The default behavior of the script (`python3 terraformer.py`) is to backup your dotfiles and update the logs.
- Use the `--sync` argument to force a backup of your dotfiles and VSCode settings:
    ```sh
    python3 terraformer.py --sync
    ```

The script logs each run

 and reminds you to commit the log file to the repository.

## Files Generated

- `dotfiles/`: Directory containing backed-up dotfiles.
- `dotfiles/vscode/`: Directory containing backed-up VSCode settings and extensions.
- `log.txt`: Log file of the script run, including date, time, hostname, and system information.
- `installed_apps.txt`: List of installed applications in the Applications folder.
- `brew_packages.txt`: List of Homebrew-installed packages.

## License

This project is licensed under the GNU Public license (GPL-3.0)

## Acknowledgments

- Homebrew
- Zsh
- Oh My Zsh
- zsh-autosuggestions
- zsh-syntax-highlighting


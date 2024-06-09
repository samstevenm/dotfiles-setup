# terraformer.py

import os
import subprocess
import sys
from datetime import datetime
import shutil

def install_homebrew():
    """Install Homebrew if it is not installed."""
    if subprocess.run(["which", "brew"], capture_output=True).returncode != 0:
        print("Homebrew not found. Installing Homebrew...")
        subprocess.run(
            '/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"',
            shell=True,
            check=True
        )
    else:
        print("Homebrew already installed.")

def install_zsh():
    """Install zsh if it is not installed."""
    if subprocess.run(["brew", "list", "zsh"], capture_output=True).returncode != 0:
        print("zsh not found. Installing zsh...")
        subprocess.run(["brew", "install", "zsh"], check=True)
    else:
        print("zsh already installed.")

def install_oh_my_zsh():
    """Install Oh My Zsh if it is not installed."""
    if not os.path.exists(os.path.expanduser("~/.oh-my-zsh")):
        print("Oh My Zsh not found. Installing Oh My Zsh...")
        subprocess.run(
            'sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"',
            shell=True,
            check=True
        )
    else:
        print("Oh My Zsh already installed.")

def install_zsh_plugins():
    """Install zsh-autosuggestions and zsh-syntax-highlighting."""
    zsh_custom = os.path.expanduser("~/.oh-my-zsh/custom")

    # zsh-autosuggestions
    zsh_autosuggestions = os.path.join(zsh_custom, "plugins/zsh-autosuggestions")
    if not os.path.exists(zsh_autosuggestions):
        print("zsh-autosuggestions not found. Installing zsh-autosuggestions...")
        subprocess.run(
            ["git", "clone", "https://github.com/zsh-users/zsh-autosuggestions", zsh_autosuggestions],
            check=True
        )
    else:
        print("zsh-autosuggestions already installed.")

    # zsh-syntax-highlighting
    zsh_syntax_highlighting = os.path.join(zsh_custom, "plugins/zsh-syntax-highlighting")
    if not os.path.exists(zsh_syntax_highlighting):
        print("zsh-syntax-highlighting not found. Installing zsh-syntax-highlighting...")
        subprocess.run(
            ["git", "clone", "https://github.com/zsh-users/zsh-syntax-highlighting.git", zsh_syntax_highlighting],
            check=True
        )
    else:
        print("zsh-syntax-highlighting already installed.")

def backup_dotfiles(dotfiles_directory):
    """Backup existing dotfiles to a specified directory and create symlinks."""
    home = os.path.expanduser("~")
    dotfiles = [
        ".zshrc", ".gitconfig", ".vimrc", ".tmux.conf"
    ]

    if not os.path.exists(dotfiles_directory):
        os.makedirs(dotfiles_directory)

    for dotfile in dotfiles:
        src = os.path.join(home, dotfile)
        dst = os.path.join(dotfiles_directory, dotfile)

        if os.path.exists(src):
            print(f"Backing up {src} to {dst}")
            if os.path.exists(dst):
                os.remove(dst)
            os.rename(src, dst)
            os.symlink(dst, src)

def backup_vscode_config(vscode_directory):
    """Backup VSCode settings and extensions."""
    vscode_user_dir = os.path.expanduser("~/Library/Application Support/Code/User")
    vscode_settings = ["settings.json", "keybindings.json", "snippets"]

    if not os.path.exists(vscode_directory):
        os.makedirs(vscode_directory)

    for item in vscode_settings:
        src = os.path.join(vscode_user_dir, item)
        dst = os.path.join(vscode_directory, item)

        if os.path.exists(src):
            print(f"Backing up {src} to {dst}")
            if os.path.exists(dst):
                if os.path.isdir(dst):
                    shutil.rmtree(dst)
                else:
                    os.remove(dst)
            if os.path.isdir(src):
                shutil.copytree(src, dst)
            else:
                shutil.copy2(src, dst)

    # Backup VSCode extensions
    extensions_list = os.path.join(vscode_directory, "extensions.txt")
    if subprocess.run(["which", "code"], capture_output=True).returncode == 0:
        subprocess.run(["code", "--list-extensions"], stdout=open(extensions_list, 'w'))
    else:
        print("VSCode CLI (code) not found. Please install it to backup extensions.")

def log_run(logfile):
    """Log the date, time, hostname, and uname -a to a log file."""
    with open(logfile, 'a') as f:
        f.write(f"{datetime.now()} - {os.uname().nodename} - {os.uname()}\n")

def list_installed_apps(apps_file):
    """List installed applications in the Applications folder."""
    apps_dir = "/Applications"
    installed_apps = [f for f in os.listdir(apps_dir) if os.path.isdir(os.path.join(apps_dir, f))]
    with open(apps_file, 'w') as f:
        for app in installed_apps:
            f.write(f"{app}\n")

def list_brew_packages(brew_file):
    """List installed Homebrew packages."""
    result = subprocess.run(["brew", "list"], capture_output=True, text=True)
    installed_packages = result.stdout.splitlines()
    with open(brew_file, 'w') as f:
        for package in installed_packages:
            f.write(f"{package}\n")

def main(setup=False, sync=False):
    dotfiles_directory = os.path.join(os.getcwd(), "dotfiles")
    vscode_directory = os.path.join(dotfiles_directory, "vscode")
    logfile = os.path.join(os.getcwd(), "log.txt")
    apps_file = os.path.join(os.getcwd(), "installed_apps.txt")
    brew_file = os.path.join(os.getcwd(), "brew_packages.txt")

    if setup:
        install_homebrew()
        install_zsh()
        install_oh_my_zsh()
        install_zsh_plugins()

    if sync or setup:
        backup_dotfiles(dotfiles_directory)
        backup_vscode_config(vscode_directory)

    log_run(logfile)
    list_installed_apps(apps_file)
    list_brew_packages(brew_file)

    print("Setup complete. Please review the changes and commit your settings:")
    print("git add .")
    print('git commit -m "Update settings"')

if __name__ == "__main__":
    setup = "--setup" in sys.argv
    sync = "--sync" in sys.argv
    main(setup, sync)
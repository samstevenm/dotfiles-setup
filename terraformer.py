# /terraformer.py

import os
import subprocess
import sys
from datetime import datetime
import shutil

def run_command(command, verbose=True, capture_output=True):
    """Run a system command and handle errors."""
    try:
        if verbose:
            print(f"🔄 Running command: {' '.join(command) if isinstance(command, list) else command}")
        result = subprocess.run(command, check=True, shell=isinstance(command, str),
                                stdout=subprocess.PIPE if capture_output else None,
                                stderr=subprocess.PIPE if capture_output else None,
                                text=True)
        if capture_output:
            if verbose and result.stdout:
                print(result.stdout)
            return result.stdout if capture_output else None
    except subprocess.CalledProcessError as e:
        if capture_output:
            print(f"❌ Error: {e.stderr if e.stderr else str(e)}")
        else:
            print(f"❌ Command failed with return code {e.returncode}")
        return None

def install_homebrew():
    """Install Homebrew if it is not installed."""
    print("🔍 Checking if Homebrew is installed...")
    if run_command(["which", "brew"], verbose=False, capture_output=False) is None:
        print("🍺 Homebrew not found. Installing Homebrew...")
        run_command('/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"', verbose=True, capture_output=False)
    else:
        print("🍺 Homebrew is already installed.")

def install_zsh():
    """Install zsh if it is not installed."""
    print("🔍 Checking if zsh is installed...")
    if run_command(["brew", "list", "zsh"], verbose=False, capture_output=False) is None:
        print("🐚 zsh not found. Installing zsh...")
        run_command(["brew", "install", "zsh"], verbose=True, capture_output=False)
    else:
        print("🐚 zsh is already installed.")

def install_oh_my_zsh():
    """Install Oh My Zsh if it is not installed."""
    print("🔍 Checking if Oh My Zsh is installed...")
    if not os.path.exists(os.path.expanduser("~/.oh-my-zsh")):
        print("✨ Oh My Zsh not found. Installing Oh My Zsh...")
        run_command('sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"', verbose=True, capture_output=False)
    else:
        print("✨ Oh My Zsh is already installed.")

def install_zsh_plugins():
    """Install zsh-autosuggestions and zsh-syntax-highlighting."""
    zsh_custom = os.path.expanduser("~/.oh-my-zsh/custom")
    print("🔍 Checking if zsh-autosuggestions and zsh-syntax-highlighting are installed...")

    # zsh-autosuggestions
    zsh_autosuggestions = os.path.join(zsh_custom, "plugins/zsh-autosuggestions")
    if not os.path.exists(zsh_autosuggestions):
        print("🔧 zsh-autosuggestions not found. Installing zsh-autosuggestions...")
        run_command(["git", "clone", "https://github.com/zsh-users/zsh-autosuggestions", zsh_autosuggestions], verbose=True, capture_output=False)
    else:
        print("🔧 zsh-autosuggestions is already installed.")

    # zsh-syntax-highlighting
    zsh_syntax_highlighting = os.path.join(zsh_custom, "plugins/zsh-syntax-highlighting")
    if not os.path.exists(zsh_syntax_highlighting):
        print("🔧 zsh-syntax-highlighting not found. Installing zsh-syntax-highlighting...")
        run_command(["git", "clone", "https://github.com/zsh-users/zsh-syntax-highlighting.git", zsh_syntax_highlighting], verbose=True, capture_output=False)
    else:
        print("🔧 zsh-syntax-highlighting is already installed.")

def backup_dotfiles_to_repo(dotfiles_directory):
    """Backup existing dotfiles from the machine to the specified directory in the repo."""
    print("💾 Backing up dotfiles from the machine to the repo...")
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
            if os.path.exists(dst):
                print(f"⚠️ {dst} already exists in the repo. Do you want to overwrite it? (yes/no)")
                if input().strip().lower() != 'yes':
                    print(f"⏭️ Skipping backup for {src}")
                    continue
                os.remove(dst)
            print(f"💾 Backing up {src} to {dst}")
            os.rename(src, dst)
            os.symlink(dst, src)

def push_dotfiles_to_machine(dotfiles_directory):
    """Push dotfiles from the specified directory in the repo to the machine."""
    print("📂 Pushing dotfiles from the repo to the machine...")
    home = os.path.expanduser("~")
    dotfiles = [
        ".zshrc", ".gitconfig", ".vimrc", ".tmux.conf"
    ]

    for dotfile in dotfiles:
        src = os.path.join(dotfiles_directory, dotfile)
        dst = os.path.join(home, dotfile)

        if os.path.exists(src):
            if os.path.exists(dst):
                print(f"⚠️ {dst} already exists on the machine. Do you want to overwrite it? (yes/no)")
                if input().strip().lower() != 'yes':
                    print(f"⏭️ Skipping push for {src}")
                    continue
                os.remove(dst)
            print(f"📂 Pushing {src} to {dst}")
            shutil.copy2(src, dst)

def backup_vscode_config_to_repo(vscode_directory):
    """Backup VSCode settings and extensions from the machine to the repo."""
    print("💾 Backing up VSCode settings and extensions from the machine to the repo...")
    vscode_user_dir = os.path.expanduser("~/Library/Application Support/Code/User")
    vscode_settings = ["settings.json", "keybindings.json", "snippets"]

    if not os.path.exists(vscode_directory):
        os.makedirs(vscode_directory)

    for item in vscode_settings:
        src = os.path.join(vscode_user_dir, item)
        dst = os.path.join(vscode_directory, item)

        if os.path.exists(src):
            if os.path.exists(dst):
                print(f"⚠️ {dst} already exists in the repo. Do you want to overwrite it? (yes/no)")
                if input().strip().lower() != 'yes':
                    print(f"⏭️ Skipping backup for {src}")
                    continue
                if os.path.isdir(dst):
                    shutil.rmtree(dst)
                else:
                    os.remove(dst)
            print(f"💾 Backing up {src} to {dst}")
            if os.path.isdir(src):
                shutil.copytree(src, dst)
            else:
                shutil.copy2(src, dst)

    # Backup VSCode extensions
    extensions_list = os.path.join(vscode_directory, "extensions.txt")
    if run_command(["which", "code"], verbose=False, capture_output=False) is not None:
        print("💾 Backing up VSCode extensions to extensions.txt...")
        with open(extensions_list, 'w') as f:
            subprocess.run(["code", "--list-extensions"], stdout=f, check=True)
    else:
        print("❌ VSCode CLI (code) not found. Please install it to backup extensions.")

def push_vscode_config_to_machine(vscode_directory):
    """Push VSCode settings and extensions from the repo to the machine."""
    print("📂 Pushing VSCode settings and extensions from the repo to the machine...")
    vscode_user_dir = os.path.expanduser("~/Library/Application Support/Code/User")
    vscode_settings = ["settings.json", "keybindings.json", "snippets"]

    for item in vscode_settings:
        src = os.path.join(vscode_directory, item)
        dst = os.path.join(vscode_user_dir, item)

        if os.path.exists(src):
            if os.path.exists(dst):
                print(f"⚠️ {dst} already exists on the machine. Do you want to overwrite it? (yes/no)")
                if input().strip().lower() != 'yes':
                    print(f"⏭️ Skipping push for {src}")
                    continue
                if os.path.isdir(dst):
                    shutil.rmtree(dst)
                else:
                    os.remove(dst)
            print(f"📂 Pushing {src} to {dst}")
            if os.path.isdir(src):
                shutil.copytree(src, dst)
            else:
                shutil.copy2(src, dst)

    # Push VSCode extensions
    extensions_list = os.path.join(vscode_directory, "extensions.txt")
    if os.path.exists(extensions_list):
        print("📂 Installing VSCode extensions from extensions.txt...")
        with open(extensions_list, 'r') as f:
            extensions = f.read().splitlines()
        for extension in extensions:
            print(f"📂 Installing VSCode extension {extension}")
            run_command(["code", "--install-extension", extension], verbose=True, capture_output=False)

def log_run(logfile):
    """Log the date, time, hostname, and uname -a to a log file."""
    print(f"📝 Logging system info to {logfile}...")
    with open(logfile, 'a') as f:
        f.write(f"{datetime.now()} - {os.uname().nodename} - {os.uname()}\n")

def list_installed_apps(apps_file):
    """List installed applications in the Applications folder."""
    print(f"📋 Listing installed applications to {apps_file}...")
    apps_dir = "/Applications"
    installed_apps = [f for f in os.listdir(apps_dir) if os.path.isdir(os.path.join(apps_dir, f))]
    with open(apps_file, 'w') as f:
        for app in installed_apps:
            f.write(f"{app}\n")

def list_brew_packages(brew_file):
    """List installed Homebrew packages."""
    print(f"📋 Listing installed Homebrew packages to {brew_file}...")
    result = run_command(["brew", "list"], verbose=False)
    if result:
        installed_packages = result.splitlines()
        with open(brew_file, 'w') as f:
            for package in installed_packages:
                f.write(f"{package}\n")

def main(backup=False, push=False):
    dotfiles_directory = os.path.join(os.getcwd(), "dotfiles")
    vscode_directory = os.path.join(dotfiles_directory, "vscode")
    logfile = os.path.join(os.getcwd(), "log.txt")
    apps_file = os.path.join(os.getcwd(), "installed_apps.txt")
    brew_file = os.path.join(os.getcwd(), "brew_packages.txt")

    if backup:
        print("🔄 Backup mode: Backing up from machine to repo")
        backup_dotfiles_to_repo(dotfiles_directory)
        backup_vscode_config_to_repo(vscode_directory)
    elif push:
        print("🔄 Push mode: Pushing from repo to machine")
        push_dotfiles_to_machine(dotfiles_directory)
        push_vscode_config_to_machine(vscode_directory)

    log_run(logfile)
    list_installed_apps(apps_file)
    list_brew_packages(brew_file)

    print("✅ Operation complete. Please review the changes and commit your settings:")
    print("git add .")
    print('git commit -m "Update settings"')

if __name__ == "__main__":
    backup = "--backup" in sys.argv
    push = "--push" in sys.argv
    main(backup, push)

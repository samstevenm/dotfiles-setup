import argparse
import os
import subprocess
import sys
import shutil
import platform
import datetime
import glob

# Function to check if a command exists
def command_exists(command):
    return subprocess.call('type ' + command, shell=True, 
        stdout=subprocess.PIPE, stderr=subprocess.PIPE) == 0

# Function to ask for user input
def ask(prompt):
    return input(prompt)

# Function to log errors
def log_error(message):
    print(f"🚨 {message}", file=sys.stderr)

# Function to backup dotfiles and create symlinks
def backup_dotfiles(repo_dir):
    dotfiles = glob.glob(os.path.expanduser('~/*'))
    dotfiles = [file for file in dotfiles if file.startswith('.') and not file.endswith(('.git', '.DS_Store'))]
    for file in dotfiles:
        src = os.path.expanduser('~/' + file)
        dst_dir = os.path.join(repo_dir, 'dotfiles')
        os.makedirs(dst_dir, exist_ok=True)  # create the dotfiles directory if it doesn't exist
        dst = os.path.join(dst_dir, file)
        if os.path.exists(src):
            shutil.copy2(src, dst)
            print(f"🔐 Backed up {file}")
            os.remove(src)  # remove the original file
            os.symlink(dst, src)  # create a symlink from the original location to the backed-up file
            print(f"🔗 Created symlink for {file}")

# Function to commit and push changes
def commit_and_push(repo_dir):
    os.chdir(repo_dir)
    if subprocess.call('git add .', shell=True) != 0:
        log_error("Failed to add files to git")
        sys.exit(1)
    if subprocess.call('git commit -m "Backup dotfiles"', shell=True) != 0:
        log_error("Failed to commit changes")
        sys.exit(1)
    if subprocess.call('git push', shell=True) != 0:
        log_error("Failed to push changes")
        sys.exit(1)

# Function to install Homebrew
def install_homebrew():
    if command_exists('brew'):
        return
    print("🍺 Homebrew is not installed. Installing...")
    subprocess.call('/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"', shell=True)

# Function to install Zsh
def install_zsh():
    if command_exists('zsh'):
        return
    print("🦖 Zsh is not installed. Installing...")
    subprocess.call('brew install zsh', shell=True)

# Function to set Zsh as the default shell
def set_zsh_default():
    subprocess.call('chsh -s "$(which zsh)"', shell=True)

# Function to install Oh My Zsh
def install_oh_my_zsh():
    if os.path.isdir(os.path.expanduser('~/.oh-my-zsh')):
        return
    print("🎩 Oh My Zsh is not installed. Installing...")
    subprocess.call('sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"', shell=True)

# Function to install zsh-autosuggestions
def install_zsh_autosuggestions():
    if os.path.isdir(os.path.expanduser('~/.oh-my-zsh/custom/plugins/zsh-autosuggestions')):
        return
    print("🔍 zsh-autosuggestions is not installed. Installing...")
    subprocess.call('git clone https://github.com/zsh-users/zsh-autosuggestions ~/.oh-my-zsh/custom/plugins/zsh-autosuggestions', shell=True)

# Function to install zsh-syntax-highlighting
def install_zsh_syntax_highlighting():
    if os.path.isdir(os.path.expanduser('~/.oh-my-zsh/custom/plugins/zsh-syntax-highlighting')):
        return
    print("🌈 zsh-syntax-highlighting is not installed. Installing...")
    subprocess.call('git clone https://github.com/zsh-users/zsh-syntax-highlighting.git ~/.oh-my-zsh/custom/plugins/zsh-syntax-highlighting', shell=True)

# Function to enable zsh-autosuggestions and zsh-syntax-highlighting
def enable_zsh_plugins():
    with open(os.path.expanduser('~/.zshrc'), 'a') as file:
        file.write("\nplugins=(zsh-autosuggestions zsh-syntax-highlighting)\n")

# Argument parsing
parser = argparse.ArgumentParser(description='Backup dotfiles to a git repository.')
parser.add_argument('--sync', action='store_true', help='Backup dotfiles to the repository.')
args = parser.parse_args()

# Function to get the repository name
def get_repo_name():
    return os.path.basename(os.getcwd())

# Function to check if the shell is Zsh
def is_zsh():
    return os.environ['SHELL'].endswith('zsh')

# Main function
def main():
    # Configuration
    repo_name = get_repo_name()
    repo_dir = os.getcwd()  # get the current directory

    # Install Homebrew, Zsh, Oh My Zsh, zsh-autosuggestions, and zsh-syntax-highlighting
    install_homebrew()
    if not is_zsh():
        install_zsh()
        set_zsh_default()
    install_oh_my_zsh()
    install_zsh_autosuggestions()
    install_zsh_syntax_highlighting()
    enable_zsh_plugins()

    # Backup dotfiles on subsequent runs
    if args.sync or not is_zsh():
        backup_dotfiles(repo_dir)
        commit_and_push(repo_dir)
        print("🎉 Dotfiles backed up successfully!")
# Run the main function
if __name__ == "__main__":
    main()
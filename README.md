# dotfiles-setup

This repository contains a script to set up a development environment on a new machine. The script installs Homebrew, Zsh, Oh My Zsh, zsh-autosuggestions, zsh-syntax-highlighting, the GitHub CLI, NeoVim, Visual Studio Code, iTerm2, and checks out a specified GitHub repository. It also creates a dotfiles directory and moves your .vimrc, .zshrc, init.vim (NeoVim configuration), settings.json (VS Code configuration), and com.googlecode.iterm2.plist (iTerm2 configuration) files to this directory.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

The script is intended to be run on a Mac with a fresh installation. It uses Homebrew to install packages, so you'll need to have Homebrew installed on your machine.

### Installing

1. Clone the repository:

```bash
git clone https://github.com/samstevenm/dotfiles-setup.git
```

2. Navigate to the repository directory:

```bash
cd dotfiles-setup
```

3. Run the script:

```bash
bash first_run.sh
```

During the execution of the script, you'll be prompted to enter your GitHub repository name. This is the repository that the script will clone.

## Usage

The script is designed to be run once when setting up a new machine. It's not intended to be run multiple times.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* [Homebrew](https://brew.sh/)
* [Zsh](https://www.zsh.org/)
* [Oh My Zsh](https://ohmyz.sh/)
* [zsh-autosuggestions](https://github.com/zsh-users/zsh-autosuggestions)
* [zsh-syntax-highlighting](https://github.com/zsh-users/zsh-syntax-highlighting)
* [GitHub CLI](https://cli.github.com/)

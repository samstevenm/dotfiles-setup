# dotfiles-setup

This repository contains a script to set up a development environment on a new machine. The script installs Homebrew, Zsh, Oh My Zsh, zsh-autosuggestions, zsh-syntax-highlighting, and backs up all dotfiles to a "dotfiles" folder within the repository. It also creates symbolic links from your home directory to these backed-up dotfiles. The script logs each run, including the date, time, hostname, and the output of uname -a, and commits the log file to the repository.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

The script is intended to be run on a Mac. It uses Homebrew to install packages, so if Homebrew is not already installed, the script will install it.

### Installing

1. Clone the repository:
`git clone https://github.com/samstevenm/dotfiles-setup.git`
2. Navigate to the repository directory:
`cd dotfiles-setup`
3. Run the script:
`python3 terraformer.py`

## Usage

The script is designed to be run once when setting up a new machine. If you want to backup your dotfiles again, you can run the script with the --sync argument:

`python3 terraformer.py --sync`

The script logs each run and commits the log file to the repository, even if the --sync argument is not passed.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

This project is licensed under the MIT License - see the LICENSE.md file for details

## Acknowledgments

- Homebrew
- Zsh
- Oh My Zsh
- zsh-autosuggestions
- zsh-syntax-highlighting
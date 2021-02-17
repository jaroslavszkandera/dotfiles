#!/bin/bash


get_help () {
	echo "Usage: $(basename "$0") [OPTIONS] FILE"
	echo "Configure system for optimal use"
	echo "Supply FILE as a list of packages that you want to install"
	echo
	echo "Options:"
	echo "-h, --help      Show brief help"
	echo "-t, --tlp       Install tlp (laptop battery management system)"
	exit 127
}

yay_install () {
	pacman -Qq | grep -q yay && return
	sudo pacman -Syu --needed --noconfirm git openssh base-devel || return
	(
	cd "$CURRENT_FOLDER"                          && \
	git clone https://aur.archlinux.org/yay.git   && \
	cd yay                                        && \
	makepkg -si --needed --noconfirm              && \
	cd ..                                         && \
	rm -rf yay/                                   || return
	)
}

prompt_and_remove_path () {
	if [ -e "$1" ]; then
		printf "%s exists, overwrite? [Y/n] " "$1"
		read -r input
		if [ -z "$input" ] || [ "${input,,}" = 'y' ]; then
			sudo rm -rf "$1"
		else
			return 1
		fi
	fi
}

check_rsa () {
	[ -f "$RSA_PATH" ] && return
	ssh-keygen -t rsa -b 4096 -C 'jirik.sz@gmail.com' -P '' -f "$RSA_PATH"
}

github_key () {
	RSA_GITHUB="${HOME}/github_key.pub"
	cp "${RSA_PATH}.pub" "${RSA_GITHUB}"
	printf '%s\n'                                                       \
		"A copy of an rsa public key has been added to ${RSA_GITHUB}" \
		"Please add this key to github.com"
}

git_init () {
	REPO_PATH="${HOME}/.dotfiles.git"
	prompt_and_remove_path "$REPO_PATH" || return 0
	sudo pacman -Syu --needed --noconfirm openssh git                                            && \
	git clone --bare --recurse-submodules https://github.com/Jirixek/dotfiles.git "$REPO_PATH"   && \
	git --git-dir="$REPO_PATH" --work-tree="$HOME" checkout -f                                   && \
	git --git-dir="$REPO_PATH" config --local status.showUntrackedFiles no                       && \
	git --git-dir="$REPO_PATH" remote set-url origin git@github.com:Jirixek/dotfiles.git         && \
	check_rsa                                                                                    && \
	rm -f ~/.bash_login                                                                          || return
}

borg_init () {
	BACKUP_PATH='/home/backup'
	prompt_and_remove_path "$BACKUP_PATH" || return 0
	sudo borg init --encryption=none "$BACKUP_PATH"
}

link_shell () {
	# change sh shell to dash
	sudo ln -sf /bin/dash /bin/sh
}

add_user_to_groups () {
	sudo usermod -aG wireshark,rfkill,uucp,audio,geoclue,openvpn "$USER"
}

service_enable () {
	# Bash suggestions for unknown packages
	# Bluetooth
	# Cron
	# Firefox profile in memory
	# Lock screen after suspend

	sudo systemctl enable             \
	     pkgfile-update.timer         \
	     bluetooth.service            \
	     cronie.service               \
	     fstrim.timer                 \
           slock@jirik.service
	root_exit=$?

	systemctl --user enable           \
		psd.service                 \
		mpd.service                 \
		syncthing.service           \
		geoclue-agent.service
	user_exit=$?

	return $((root_exit > user_exit ? root_exit : user_exit))
}

# ---------------
#  Init Section
# ---------------
if [ "$(id -u)" -eq 0 ]; then
	echo "Please don't run as root." >&2
	exit 1
fi

CURRENT_FOLDER="$(dirname "$0")"
RSA_PATH="${HOME}/.ssh/id_rsa"
INSTALL_FILE=""

while [ "$#" -gt 0 ]
do
	case "$1" in
		-h|--help)	get_help ;;
		-t|--tlp)
			sudo pacman -Syu --needed --noconfirm tlp tlp-rdw                     && \
			sudo systemctl enable tlp.service NetworkManager-dispatcher.service   && \
			sudo systemctl mask systemd-rfkill.service systemd-rfkill.socket      || exit
			shift
			;;
		*)
			if [ -z "$INSTALL_FILE" ] && [ -f "$1" ]; then
				INSTALL_FILE="$1"
			else
				get_help
			fi
			shift
			;;
	esac
done

[ -z "$INSTALL_FILE" ] && get_help

git_init                                          && \
yay_install                                       && \
"$HOME"/.local/bin/pkgupdate.sh "$INSTALL_FILE"   && \
"$HOME"/.local/bin/linker.sh -w                   && \
service_enable                                    && \
borg_init                                         && \
link_shell                                        && \
add_user_to_groups                                && \
github_key                                        || exit

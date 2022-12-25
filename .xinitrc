#!/bin/sh
# xinit/startx initialization file


# Run all system xinitrc shell scripts
xinitdir="/etc/X11/xinit/xinitrc.d"
if [ -d "$xinitdir" ]; then
	for script in $xinitdir/*; do
		echo "Loading xinit script $script"
		if [ -x "$script" -a ! -d "$script" ]; then
			. "$script"
		fi
	done
fi

[ -f "${HOME}/.zshenv" ] && . "${HOME}/.zshenv"
[ -f "${XDG_CONFIG_HOME}/X11/xprofile" ] && . "${XDG_CONFIG_HOME}/X11/xprofile"

exec startdwm

#!/bin/bash


[ -r ~/.profile ] && . ~/.profile
[[ $- == *i* ]] && [ -r ~/.bashrc ] && . ~/.bashrc

[ -z "${DISPLAY}" ] && [ -n "${XDG_VTNR}" ] && [ "${XDG_VTNR}" -eq 1 ] && \
	exec startx "${XDG_CONFIG_HOME}/X11/xinitrc" -- vt1 -ardelay 300 -arinterval 25 &>/dev/null

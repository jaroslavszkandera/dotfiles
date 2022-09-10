#!/bin/sh


# Path and XDG
echo "$PATH" | grep -qF "${HOME}/.local/scripts/" || \
export PATH="$(find "${HOME}/.local/scripts/" -maxdepth 1 -type d -printf '%p:')$PATH"
export XDG_CONFIG_HOME="${HOME}/.config"
export XDG_CACHE_HOME="${HOME}/.cache"
export XDG_DATA_HOME="${HOME}/.local/share"

# Increase history size
export HISTSIZE=10000
export HISTFILESIZE=10000
export HISTCONTROL=erasedups

# Default programs
export OPENER='mimeopen'
export EDITOR='nvim'
export VISUAL='nvim'
export SUDO_EDITOR='nvim'
export TERMINAL='st'
export BROWSER='firefox'
export READER='evince'
export FILE='lf_wrapper'

# ~/ Clean-up
export GTK2_RC_FILES="${XDG_CONFIG_HOME}/gtk-2.0/gtkrc-2.0"
export LESSHISTFILE='-'
export GNUPGHOME="${XDG_DATA_HOME}/gnupg"
export MATHEMATICA_USERBASE="${XDG_CONFIG_HOME}/mathematica"
export NPM_CONFIG_USERCONFIG="${XDG_CONFIG_HOME}/npm/npmrc"
export WGETRC="${XDG_CONFIG_HOME}/wgetrc"
export XINITRC="${XDG_CONFIG_HOME}/X11/xinitrc"
export GOPATH="${XDG_DATA_HOME}/go"

# Other program settings
export FZF_DEFAULT_OPTS='--layout=reverse --height 40%'
export LESS='-R --use-color --color=d+B$Dug'

# JAVA settings
export _JAVA_AWT_WM_NONREPARENTING=1
export _JAVA_OPTIONS="-Djava.util.prefs.userRoot=${XDG_CONFIG_HOME}/java -Dawt.useSystemAAFontSettings=on -Dswing.aatext=true -Dswing.defaultlaf=com.sun.java.swing.plaf.gtk.GTKLookAndFeel -Dswing.crossplatformlaf=com.sun.java.swing.plaf.gtk.GTKLookAndFeel"

# Git
export GIT_PS1_SHOWDIRTYSTATE=1
export GIT_PS1_SHOWSTASHSTATE=1
export GIT_PS1_SHOWUNTRACKEDFILES=1
export GIT_PS1_SHOWUPSTREAM="auto verbose"

# Make
export MAKEFLAGS="-j$(nproc)"

# CppUTest
export CPPUTEST_HOME="${HOME}/.local/cpputest"

# Qt5 theme
export QT_QPA_PLATFORMTHEME='Matchama-Dark-Azul'
export QT_STYLE_OVERRIDE='kvantum'

# Conda
export CONDARC="${XDG_CONFIG_HOME}/conda/condarc"

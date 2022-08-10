#!/bin/bash
# Initialization for interactive, non-login shells
# This file is used for interactive shell init (no matter if it's login shell or not)
# because it's sourced from .bash_profile


. /usr/share/git/completion/git-prompt.sh
PS1_GIT='$(__git_ps1 "[%s]")\[\033[01;34m\]\$\[\033[00m\]'
PS1='\[\033[01;34m\]\w \[\033[01;33m\]'"$PS1_GIT "
[ "${EUID}" -eq 0 ] && PS1='\[\033[01;31m\]\h\[\033[01;34m\] \W \$\[\033[00m\]'"$PS1_GIT "

# Searching repos for unnamed commands
[ -e "/usr/share/doc/pkgfile/command-not-found.bash" ] && . /usr/share/doc/pkgfile/command-not-found.bash

[ -f ~/.bash_aliases ]   && . "${HOME}/.bash_aliases"
[ -f ~/.bash_functions ] && . "${HOME}/.bash_functions"

[ -z "$TMUX" ] && [ -z "$SSH_CLIENT" ] && tmux-init && tmux attach -t general

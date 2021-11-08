#!/bin/sh


# =================
#  Command mapping
# =================

# XDG Cleanup
alias nvidia-settings='nvidia-settings --config="${XDG_CONFIG_HOME}/nvidia/settings"'
alias wget='wget --hsts-file="${XDG_CACHE_HOME}/wget-hsts"'

# Enable color
alias ls='ls --color=auto'
alias grep='grep --color=auto'
alias fgrep='fgrep --color=auto'
alias egrep='egrep --color=auto'
alias diff='diff --color=auto'
alias watch='watch --color'

# General
alias yt-dlp='yt-dlp -f bestvideo+bestaudio'
alias l='ls -lh'
alias la='ls -lha'
alias df='df -h'

# Dotfiles
alias dfl='git --git-dir="${HOME}/.dotfiles.git/" --work-tree="$HOME"'

# Shortcuts/scripts
alias rsync='rsync-without-trailing-slash'
alias vim='nvim_wrapper'
alias v='nvim_wrapper'
alias g='lf_wrapper'

# ===================
#  Directory mapping
# ===================

. "$HOME"/.local/src/generated/aliases_bash

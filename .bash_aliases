#!/bin/sh


# =================
#  Command mapping
# =================

# XDG Cleanup
alias nvidia-settings='nvidia-settings --config="$XDG_CONFIG_HOME"/nvidia/settings'
alias wget='wget --hsts-file="$XDG_CACHE_HOME/wget-hsts"'

# Enable color
alias ls='ls --color=auto'
alias grep='grep --color=auto'
alias fgrep='fgrep --color=auto'
alias egrep='egrep --color=auto'
alias diff='diff --color=auto'
alias watch='watch --color'

# General
alias youtube-dl='youtube-dl -f bestvideo+bestaudio'
alias l='ls -lh'
alias la='ls -lha'
alias df='df -h'

# Dotfiles
alias dfl='/usr/bin/git --git-dir=$HOME/.dotfiles.git/ --work-tree=$HOME'

# Shortcuts/scripts
alias rsync='rsync-without-trailing-slash'
alias vim='nvim_wrapper'
alias v='nvim_wrapper'
alias g='lf_wrapper'


# ===================
#  Directory mapping
# ===================
# Root
alias gR='cd "/"'
alias ge='cd "/etc/"'
alias gH='cd "/home/"'

alias gm.='cd "/mnt/"'
alias gmm='cd "/mnt/mrdky/"'
alias gmn='cd "/mnt/nas/"'
alias gmw='cd "/mnt/windows/"'

alias gr='cd "/run/media/$USER/"'

alias gV.='cd "/var/"'
alias gVl='cd "/var/lib/lxc/"'

# Home
alias gh='cd "$HOME/"'
alias gc='cd "$HOME/.config/"'

alias gl.='cd "$HOME/.local/"'
alias glb='cd "$HOME/.local/bin/"'
alias glS='cd "$HOME/.local/src/"'
alias gls='cd "$HOME/.local/suckless/"'
alias gla='cd "$HOME/.local/share/Anki2/Jiri Szkandera/collection.media/"'

alias gd.='cd "$HOME/Documents/"'
alias gdc='cd "$HOME/Documents/cvut/"'
alias gdf='cd "$HOME/Documents/faktury/"'
alias gdl='cd "$HOME/Documents/latex/"'
alias gdP='cd "$HOME/Documents/private/"'
alias gdp='cd "$HOME/Documents/programming/"'
alias gdw='cd "$HOME/Documents/workswell/"'

alias gD='cd "$HOME/Downloads/"'
alias gM='cd "$HOME/Music/"'
alias gp.='cd "$HOME/Pictures/"'
alias gps='cd "$HOME/Pictures/screenshots/"'
alias gpm='cd "$HOME/Pictures/memes/"'
alias gv='cd "$HOME/Videos/"'

# ======================
#  Fuzzy finder mapping
# ======================
# Current folder
alias f="fzf_and_open './'"

# Root
alias fR="fzf_and_open '/'"
alias fe="fzf_and_open '/etc/'"
alias fH="fzf_and_open '/home/'"

alias fm.="fzf_and_open '/mnt/'"
alias fmm="fzf_and_open '/mnt/mrdky/'"
alias fmM="fzf_and_open '/mnt/mrdky/Movies/'"
alias fmn="fzf_and_open '/mnt/nas/'"
alias fmw="fzf_and_open '/mnt/windows/'"

alias fr="fzf_and_open \"/run/media/\$USER/\""

alias fv.="fzf_and_open '/var/'"
alias fvl="fzf_and_open '/var/lib/lxc/'"

# Home
alias fh="fzf_and_open \"\$HOME/\""
alias fc="fzf_and_open \"\$HOME/.config/\""

alias fl.="fzf_and_open \"\$HOME/.local/\""
alias flb="fzf_and_open \"\$HOME/.local/bin/\""
alias flS="fzf_and_open \"\$HOME/.local/src/\""
alias fls="fzf_and_open \"\$HOME/.local/suckless/\""
alias fla="fzf_and_open \"\$HOME/.local/share/Anki2/Jiri Szkandera/collection.media/\""

alias fd.="fzf_and_open \"\$HOME/Documents/\""
alias fdc="fzf_and_open \"\$HOME/Documents/cvut/\""
alias fdf="fzf_and_open \"\$HOME/Documents/faktury/\""
alias fdl="fzf_and_open \"\$HOME/Documents/latex/\""
alias fdP="fzf_and_open \"\$HOME/Documents/private/\""
alias fdp="fzf_and_open \"\$HOME/Documents/programming/\""
alias fdw="fzf_and_open \"\$HOME/Documents/workswell/\""

alias fD="fzf_and_open \"\$HOME/Downloads/\""
alias fM="fzf_and_open \"\$HOME/Music/\""
alias fp.="fzf_and_open \"\$HOME/Pictures/\""
alias fps="fzf_and_open \"\$HOME/Pictures/screenshots/\""
alias fpm="fzf_and_open \"\$HOME/Pictures/memes/\""
alias fv="fzf_and_open \"\$HOME/Videos/\""

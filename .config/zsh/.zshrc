# Read when interactive

# Set name of the theme to load.
# Look in ~/.oh-my-zsh/themes/
# Optionally, if you set this to "random", it'll load a random theme each
# time that oh-my-zsh is loaded.
ZSH_THEME="robbyrussell"

# Uncomment the following line to use case-sensitive completion.
# CASE_SENSITIVE="true"

# Uncomment the following line to use hyphen-insensitive completion. Case
# sensitive completion must be off. _ and - will be interchangeable.
# HYPHEN_INSENSITIVE="true"

# Uncomment the following line if pasting URLs and other text is messed up.
DISABLE_MAGIC_FUNCTIONS="true"

# Uncomment the following line to disable bi-weekly auto-update checks.
DISABLE_AUTO_UPDATE="true"

# Uncomment the following line to change how often to auto-update (in days).
# export UPDATE_ZSH_DAYS=13

# Uncomment the following line to enable command auto-correction.
ENABLE_CORRECTION="true"

# Uncomment the following line to display red dots whilst waiting for completion.
COMPLETION_WAITING_DOTS="true"

# Uncomment the following line if you want to disable marking untracked files
# under VCS as dirty. This makes repository status check for large repositories
# much, much faster.
# DISABLE_UNTRACKED_FILES_DIRTY="true"

# Uncomment the following line if you want to change the command execution time
# stamp shown in the history command output.
# The optional three formats: "mm/dd/yyyy"|"dd.mm.yyyy"|"yyyy-mm-dd"
HIST_STAMPS="yyyy-mm-dd"

# Which plugins would you like to load? (plugins can be found in ~/.oh-my-zsh/plugins/*)
# Custom plugins may be added to ~/.oh-my-zsh/custom/plugins/
# Example format: plugins=(rails git textmate ruby lighthouse)
# Add wisely, as too many plugins slow down shell startup.
plugins=(archlinux command-not-found git golang cp colorize)

ZSH_CACHE_DIR="${XDG_CACHE_HOME}/zsh"
[ ! -d "$ZSH_CACHE_DIR" ] && mkdir -p "$ZSH_CACHE_DIR"
#source /usr/share/oh-my-zsh/oh-my-zsh.sh
source ~/.oh-my-zsh/oh-my-zsh.sh


# User configuration
#source /usr/share/zsh/plugins/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh

[ -f "${XDG_CONFIG_HOME}/zsh/.aliases" ]   && source "${XDG_CONFIG_HOME}/zsh/.aliases"
[ -f "${XDG_CONFIG_HOME}/zsh/.functions" ] && source "${XDG_CONFIG_HOME}/zsh/.functions"

# Prompt
GIT_PS1_SHOWDIRTYSTATE=1
GIT_PS1_SHOWSTASHSTATE=1
GIT_PS1_SHOWUNTRACKEDFILES=1
GIT_PS1_SHOWUPSTREAM="auto verbose"
. /usr/share/git/completion/git-prompt.sh

if [ "${EUID}" -eq 0 ]; then
	PS1='%{$fg_bold[red]%}%~ %{$fg_bold[yellow]%}$(__git_ps1 "[%s]")%{$fg_bold[red]%}$ %{$reset_color%}'
else
	PS1='%{$fg_bold[blue]%}%~ %{$fg_bold[yellow]%}$(__git_ps1 "[%s]")%{$fg_bold[blue]%}$ %{$reset_color%}'
fi

# History
setopt histignoredups
setopt inc_append_history
setopt share_history
HISTSIZE=10000
HISTFILE="${ZSH_CACHE_DIR}/history"
HISTFILESIZE=10000

# Ctrl-u doesn't delete whole line
bindkey \^U backward-kill-line

# Other
eval "$(dircolors)"

[ -z "$TMUX" ] && [ -z "$SSH_CLIENT" ] && (tmux-init; tmux attach -t general)

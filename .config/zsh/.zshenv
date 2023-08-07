# Read every time


# Path and XDG
echo "$PATH" | grep -qF "${HOME}/.local/scripts/" || \
	export PATH="$(find "${HOME}/.local/scripts/" -maxdepth 1 -type d -printf '%p:')$PATH"
export XDG_CONFIG_HOME="${HOME}/.config"
export XDG_CACHE_HOME="${HOME}/.cache"
export XDG_DATA_HOME="${HOME}/.local/share"

# Default programs
export OPENER='mimeopen'
export EDITOR='nvim'
export VISUAL='nvim'
export SUDO_EDITOR='nvim'
export TERMINAL='alacritty'
export BROWSER='firefox'
export READER='evince'
export FILE='lfcd'

# ~/ Clean-up
export ZDOTDIR="${XDG_CONFIG_HOME}/zsh"
export GTK2_RC_FILES="${XDG_CONFIG_HOME}/gtk-2.0/gtkrc-2.0"
export LESSHISTFILE='-'
export GNUPGHOME="${XDG_DATA_HOME}/gnupg"
export MATHEMATICA_USERBASE="${XDG_CONFIG_HOME}/mathematica"
export NPM_CONFIG_USERCONFIG="${XDG_CONFIG_HOME}/npm/npmrc"
export WGETRC="${XDG_CONFIG_HOME}/wgetrc"
export XINITRC="${XDG_CONFIG_HOME}/X11/xinitrc"
export GOPATH="${XDG_DATA_HOME}/go"
export CPPUTEST_HOME="${HOME}/.local/cpputest"
export CONDARC="${XDG_CONFIG_HOME}/conda/condarc"

# JAVA settings
export _JAVA_AWT_WM_NONREPARENTING=1
export _JAVA_OPTIONS="-Djava.util.prefs.userRoot=${XDG_CONFIG_HOME}/java -Dawt.useSystemAAFontSettings=on -Dswing.aatext=true -Dswing.defaultlaf=com.sun.java.swing.plaf.gtk.GTKLookAndFeel -Dswing.crossplatformlaf=com.sun.java.swing.plaf.gtk.GTKLookAndFeel"

# Make
export MAKEFLAGS="-j$(nproc)"

# Qt5 theme
#export QT_QPA_PLATFORMTHEME='Matchama-Dark-Azul'
#export QT_STYLE_OVERRIDE='kvantum'

# Ruby
if command -v ruby &>/dev/null; then
	export GEM_HOME="$(ruby -e 'puts Gem.user_dir')"
	export PATH="$PATH:$GEM_HOME/bin"
fi

# LF_BAT_OPTS
export BAT_THEME='Materia-dark-compact'
export LF_BAT_OPTS='-f'

# Other
export FZF_DEFAULT_OPTS='--layout=reverse --height 40%'
export LESS='-R --use-color --color=d+B$Dug'
export MANROFFOPT='-P -c'

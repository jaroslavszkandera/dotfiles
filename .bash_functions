#!/bin/bash


fzf_and_open () {
	if [ -z "$1" ]; then
		SELECTED_FOLDER='./'
	else
		SELECTED_FOLDER="$1"
	fi

	cd "$SELECTED_FOLDER" || return
	SELECTED="$(find "$SELECTED_FOLDER" -mindepth 1 -maxdepth 1 -printf '%f\n' | sort | fzf)" || return
	FILE_TYPE="$(mimetype -ab "$SELECTED")"
	if grep -q 'text/plain' <<<"$FILE_TYPE"; then
		"$EDITOR" "$SELECTED"
	elif grep -qe 'inode' <<<"$FILE_TYPE"; then
		"$FILE" "$SELECTED"
	else
		"$OPENER" "$SELECTED"
	fi
}

lf_wrapper () {
	# setup lf so it changes to the last directory when exited
	tempfile="$(mktemp)" || {
		echo "Can't create tmpfile" >&2
			return 1
		}
	lf -last-dir-path="$tempfile" "$@"
	[ ! -f "$tempfile" ] && return 1

	dir="$(cat "$tempfile")"
	rm -f "$tempfile"
	[ -d "$dir" ] && [ "$dir" != "$PWD" ] && cd "$dir" || return
}

export -f fzf_and_open lf_wrapper

#!/bin/bash
# Initialization for login shells


[ -r ~/.profile ] && . ~/.profile

# Source .bashrc if interactive
[[ $- == *i* ]] && [ -r ~/.bashrc ] && . ~/.bashrc

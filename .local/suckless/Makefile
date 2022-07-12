SUBDIRS := dmenu dwm dwmblocks slock st
JOBS_CHECKOUT := $(addprefix checkout-,${SUBDIRS})
JOBS_INSTALL := $(addprefix install-,${SUBDIRS})
JOBS_PULL := $(addprefix pull-,${SUBDIRS})
JOBS_CLEAN := $(addprefix clean-,${SUBDIRS})

.PHONY: all checkout install pull clean \
	${JOBS_CHECKOUT} ${JOBS_INSTALL} ${JOBS_PULL} ${JOBS_CLEAN}

all: compile

clone: clone-dmenu clone-dwm clone-slock clone-st clone-dwmblocks
clone-dmenu clone-dwm clone-slock clone-st: clone-%:
	git clone https://gitlab.com/jirixek/"$*".git
	git -C "$*" checkout config
	git -C "$*" remote set-url origin git@gitlab.com:jirixek/"$*".git
	git -C "$*" remote add suckless https://git.suckless.org/"$*"
	git -C "$*" fetch --all
clone-dwmblocks: clone-%:
	git clone https://github.com/Jirixek/"$*".git
	git -C "$*" checkout config
	git -C "$*" remote set-url origin git@github.com:Jirixek/"$*".git

checkout: ${JOBS_CHECKOUT}
${JOBS_CHECKOUT}: checkout-%:
	git -C "$*" checkout config

install: ${JOBS_INSTALL}
${JOBS_INSTALL}: install-%:
	sudo $(MAKE) -C "$*" install

pull: ${JOBS_PULL}
${JOBS_PULL}: pull-%:
	# TODO: test the -r option
	git -C "$*" pull

clean: ${JOBS_CLEAN}
${JOBS_CLEAN}: clean-%:
	make -C "$*" clean

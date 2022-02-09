SUBDIRS = dmenu dwm dwmblocks slock st

all: compile

checkout:
	for n in $(SUBDIRS); do git -C "$$n" checkout config || exit; done

compile: checkout
	for n in $(SUBDIRS); do $(MAKE) -C "$$n" || exit; done

install: compile
	for n in $(SUBDIRS); do $(MAKE) -C "$$n" install || exit; done

pull:
	# TODO: test the -r option
	for n in $(SUBDIRS); do git -C "$$n" pull -r || exit; done

clean:
	for n in $(SUBDIRS); do $(MAKE) -C "$$n" clean; done

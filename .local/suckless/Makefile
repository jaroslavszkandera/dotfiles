SUBDIRS = dmenu dwm dwmblocks slock st

all: compile

checkout:
	for n in $(SUBDIRS); do git -C "$$n" checkout config || exit; done

install:
	for n in $(SUBDIRS); do sudo $(MAKE) -C "$$n" install || exit; done

pull:
	# TODO: test the -r option
	for n in $(SUBDIRS); do git -C "$$n" pull -r || exit; done

clean:
	for n in $(SUBDIRS); do $(MAKE) -C "$$n" clean; done

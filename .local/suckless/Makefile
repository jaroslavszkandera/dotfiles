SUBDIRS = dmenu dwm dwmblocks slock st

all: subdirs

subdirs:
	for n in $(SUBDIRS); do $(MAKE) -C $$n || exit 1; done

install:
	for n in $(SUBDIRS); do $(MAKE) -C $$n install || exit 1; done

checkout:
	for n in $(SUBDIRS); do git -C $$n checkout config || exit 1; done

clean:
	for n in $(SUBDIRS); do $(MAKE) -C $$n clean; done

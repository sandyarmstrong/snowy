PROJECT=snowy
VERSION=0.4

dist:
	git archive --prefix=$(PROJECT)/ $(VERSION) | \
	bzip2 > $(PROJECT)-$(VERSION).tar.bz2

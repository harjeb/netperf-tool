SUBDIR = ./tools/netperf-2.7.1
all:
	cd $(SUBDIR) && ./autogen.sh && ./configure && make && make install


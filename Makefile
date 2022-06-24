SUBDIR = ./tools/netperf-2.7.1

install:
	cd $(SUBDIR) && ./autogen.sh && ./configure --prefix=/usr && make && make install


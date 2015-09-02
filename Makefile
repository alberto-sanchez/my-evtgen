include ./config.mk

default: lib_shared lib_archive
#examples


lib_shared:  
	$(MAKE) -C $(SRCDIR) lib_shared

lib_archive: 
	$(MAKE) -C $(SRCDIR) lib_archive

examples: lib_shared dumm pdfdumm
	$(MAKE) -C $(EXAMPLEDIR)

distclean: clean
	rm -rf  tmp/ bin/ lib/
	rm -f config.mk fort.*

clean: 
	$(MAKE) -C $(SRCDIR)      clean
#	$(MAKE) -C $(EXAMPLEDIR)  clean


help:
	@echo "A list of targets to make:"
	@echo ""
	@echo "lib_shared:  compiles EvtGenLHC as a shared library and puts it into ./lib"
	@echo "lib_archive: compiles EvtGenLHC as an archive library and puts it into ./lib/archive"
#	@echo "examples:    compiles example routines from ./examples"
	@echo "default:     lib_shared lib_archive"
	@echo "clean:       removes all libraries, executables and objects"
	@echo "distclean:   same as 'clean' plus removing ./config.mk, tmp/ and lib/ directories"
	@echo ""

.PHONY: examples distclean clean	


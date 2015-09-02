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
	@echo ""
	@echo "lib_shared:  compiles Herwig as a shared library and puts it into ./lib"
	@echo ""
	@echo "lib_archive: compiles Herwig as an archive library and puts it into ./lib/archive"
	@echo ""
	@echo "examples:    compiles example routines from ./examples"
	@echo ""
	@echo "default:     lib_shared lib_archive dumm pdfdumm examples"
	@echo ""
	@echo "clean:       removes all libraries, executables and objects"
	@echo ""
	@echo "distclean:   same as 'clean' plus removing ./config.mk and src/*.[Ff]"
	@echo ""

.PHONY: examples dumm pdfdumm distclean clean tmp	




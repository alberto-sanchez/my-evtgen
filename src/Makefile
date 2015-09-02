include ../config.mk

TMPDIR=../tmp

#objects := $(patsubst %.cpp,%.o,$(wildcard *.cpp))


sources := $(shell find . -type 'f' -name '*.cpp')
sources += $(shell find . -type 'f' -name '*.[Ff]')
objects := $(shell echo $(sources) | sed 's,\./,$(TMPDIR)/,g;s,\.cpp,\.o,g;s,\.F,\.o,g;')
mkfiles := $(shell echo $(sources) | sed 's,\./,$(TMPDIR)/,g;s,\.cpp,\.mk,g;s,\.F,\.mk,g;s,\.f,\.mk,g;')


default: all

all: lib_shared lib_archive

lib_shared: $(LIB_SHARED)

lib_archive: $(LIB_ARCHIVE)


$(LIB_SHARED) : $(objects)
	mkdir -p $(LIBDIR_SHARED)
	@echo creating the shared library $@
	$(CXX) $(LDFLAGSSHARED) $(objects) -o $@ -shared -Wl,-soname,$(notdir $@)

$(LIB_ARCHIVE) : $(objects)
	ar cru $(LIB_ARCHIVE) $(objects)

#---- The following is for dependency checking:

$(TMPDIR)/%.mk:  %.cpp
	$(CXX) -MM $< -I$(INCLUDEDIR) $(INCLUDE_CLHEP) | sed 's,^.*o[ ]*:,$(TMPDIR)/$<:,' | sed 's,cpp:,o:,'  > $@ 

-include $(mkfiles)

#----

$(TMPDIR)/%.o : %.cpp  $(TMPDIR)/%.mk
	$(CXX) $(CXXFLAGS) $(CXXFLAGSSHARED) -c -o $@ $< -I$(INCLUDEDIR) \
	$(INCLUDE_CLHEP)
	
$(TMPDIR)/%.o: %.F
	$(F77) $(FFLAGS) $(FFLAGSSHARED) -c -o $@ $< -I$(INCLUDEDIR) $(INCLUDE_CLHEP)
	
$(TMPDIR)/%.o: %.f
	$(F77) $(FFLAGS) $(FFLAGSSHARED) -c -o $@ $< -I$(INCLUDEDIR) $(INCLUDE_CLHEP)
clean:
	rm -f *~
	rm -f $(objects) 
	rm -f $(LIB_SHARED) 
	rm -f $(LIB_ARCHIVE)

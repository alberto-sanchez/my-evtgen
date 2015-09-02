
_check_cc() {
	local _cc="$1";
	local _cflags="$2";
	echo "int main(void) { 	return 0; }" > .test_cc.c;
	if $_cc $_cflags -o .test_cc .test_cc.c && test -x .test_cc && ./.test_cc ; then
		rm -f .test_cc*;
		return 0;
	else
		rm -f .test_cc*;
		return 1;
	fi;
};

_check_fortran() {
	local _fc="$1";
	local _fflags="$2";
	{
	 echo "        program test";
	 echo "        implicit none";
	 echo "        end";
	} >.test_fortran.f ;
	if $_fc $_fflags -o .test_fortran .test_fortran.f && test -x .test_fortran && ./.test_fortran ; then
		rm -f .test_fortran*;
		return 0;
	else
		rm -f .test_fortran*;
		return 1;
	fi;
};

_check_cxx() {
	local _cxx="$1";
	local _cxxflags="$2";
	{
	echo "	class cl {";
	echo "		public:";
	echo "			 cl();";
	echo "			~cl();";
	echo "			int par(void);";
	echo "			void setpar(int);";
	echo "		private:";
	echo "			int m_par;";
	echo "	};";
	echo "	cl::cl(void) {";
	echo "		m_par = 0;";
	echo "	}";
	echo "	cl::~cl(void) { }";
	echo "	int cl::par(void) {";
	echo "		return m_par;";
	echo "	}";
	echo "	void cl::setpar(int p) {";
	echo "		m_par = p;";
	echo "	}";
	echo "	int main(void) {";
	echo "		cl *c = new cl();";
	echo "		c->setpar(1);";
	echo "		return !c->par();";
	echo "	}";
	} > .test_cxx.cc ;
	if $_cxx $_cxxflags -o .test_cxx .test_cxx.cc && test -x .test_cxx && ./.test_cxx ; then
		rm -f .test_cxx*;
		return 0;
	else
		rm -f .test_cxx*;
		return 1;
	fi;
};


lcg_platform () {
	
local _cc=           ;
local _fc=           ;
local _cxx=          ;

LCG_PLATFORM=        ;

local CFLAGS_GENSER=" -O2 -fPIC "
local CXXFLAGS_GENSER=" -O2 -fPIC -Wall "
local FFLAGS_GENSER=" -O2 -fPIC  -Wuninitialized "

# distribution
if test "x${LCG_OPSYS}" = "x" ; then
	if test -s /etc/redhat-release ; then
		_release=`cat /etc/redhat-release` ; 
		_release_num=`echo ${_release} | sed 's,^.*release[ ][ ]*\([0-9\.][0-9\.]*\) .*$,\1,'` ; 
       		if echo "${_release}" | grep SLC 2>&1 >/dev/null ; then 
			LCG_OPSYS=slc`echo ${_release_num} | sed 's,\([0-9][0-9]*\)\..*$,\1,'`; 
		elif echo "${_release}" |  grep -E "[Rr]ed[Hh]at" 2>&1 >/dev/null ; then 
		        LCG_OPSYS=rh`echo ${_release_num} | sed 's,\.,,g'` ; 
		else 
			LCG_OPSYS=Linux ;
		fi ;
	else 
		LCG_OPSYS=`uname -s` ;
		if test "x${LCG_OPSYS}" = "xDarwin" ; then
			Darwin_kernel=`uname -r` ; 
			if test "x$Darwin_kernel" = "x9.7.0" ; then
				osx_version=105 ; 
				LCG_OPSYS="osx${osx_version}";
			else
				echo "WARNING: guessing Mac OS X version using sysctl" >&2 ;
				kern_osrelease=`sysctl -n kern.osrelease` ;
				kernel_major=`echo $kern_osrelease | sed 's,\..*$,,'`;
				echo "         osrelease: $kern_osrelease">&2;
				lcg_osx_version=10`expr $kernel_major - 4`;
				LCG_OPSYS="mac${lcg_osx_version}" ; 
			fi ; 
		fi ; 
	fi ;
else
	echo "WARNING: LCG_OPSYS was set to ${LCG_OPSYS}. Leaving it intact." >&2 ;
fi ;


# arhitecture
if test "x${MACHINE_ARCH}" = "x" ; then
	if test "x`which sys 2>/dev/null`" != "x" ; then
		MACHINE_ARCH=`sys | sed 's,_.*$,,'` ;
	else
		MACHINE_ARCH=`uname -m` ;
	fi;
fi ;

if test "x${LCG_OPSYS}" = "xslc5" ; then
	_arch=`uname -m` ;
	if test "x$_arch" = "xx86_64" ; then
		if test "x$CROSS32" = "xyes" ; then
			LCG_MACHINE_ARCH=i686;
			ADD_GCC_FLAG=" -m32 ";
			ADD_LD_FLAG=" -m32 ";
			ARCHFLAGS="-arch i386";
		else
			LCG_MACHINE_ARCH=$_arch;
			ADD_GCC_FLAG="";
			ADD_LD_FLAG="";
			ARCHFLAGS="-arch $_arch";
		fi;
	else
		LCG_MACHINE_ARCH=$_arch;
		ADD_GCC_FLAG="";
		ARCHFLAGS="-arch $_arch";
	fi;
elif test "x$LCG_OPSYS" = "xslc4" ; then
	if test "x$MACHINE_ARCH" = "xi386" ; then 
		LCG_MACHINE_ARCH=ia32 ;
		ARCHFLAGS="-arch i386";
	else
		if test "x$CROSS32" = "xyes" ; then
			LCG_MACHINE_ARCH=ia32;
			ADD_GCC_FLAG=" -m32 ";
			ADD_LD_FLAG=" -m32 ";
			ARCHFLAGS="-arch i386";
		else
			LCG_MACHINE_ARCH=$MACHINE_ARCH ; 	
			ADD_GCC_FLAG="";
			ADD_LD_FLAG="";
			ARCHFLAGS="-arch $MACHINE_ARCH";
		fi;
	fi ;
elif echo "$LCG_OPSYS" | grep "osx" 2>&1 >/dev/null ; then
	if test "x$MACHINE_ARCH" = "xi386" ; then 
		LCG_MACHINE_ARCH=ia32 ;
	else
		if test "x$CROSS32" = "xyes" ; then
			LCG_MACHINE_ARCH=ia32;
			ADD_GCC_FLAG=" -m32 ";
			ADD_LD_FLAG=" -m32 ";
			ADD_GCC_LD_FLAG=" -Wl,-flat_namespace ";
			ARCHFLAGS="-arch i386";
		else
			LCG_MACHINE_ARCH=$MACHINE_ARCH ; 	
			ADD_GCC_FLAG="";
			ADD_LD_FLAG="";
			ADD_GCC_LD_FLAG="";
			ARCHFLAGS="-arch $MACHINE_ARCH";
		fi;
	fi ;
elif echo "$LCG_OPSYS" | grep "mac" 2>&1 >/dev/null ; then
	if test "x$MACHINE_ARCH" = "xamd64" ; then
		if test "x$CROSS32" = "xyes" ; then
			LCG_MACHINE_ARCH=i386;
			ADD_GCC_FLAG=" -m32 ";
			ADD_LD_FLAG=" -m32 ";
			ADD_GCC_LD_FLAG=" -Wl,-flat_namespace ";
			ARCHFLAGS="-arch i386";
		else
			LCG_MACHINE_ARCH=x86_64;
			ADD_GCC_FLAG=" -m64 ";
			ADD_LD_FLAG=" -m64 ";
			ADD_GCC_LD_FLAG=" -Wl,-flat_namespace ";
			ARCHFLAGS="-arch x86_64";
		fi;
	elif test "x$MACHINE_ARCH" = "xi386" ; then
		LCG_MACHINE_ARCH=i386;
		ADD_GCC_FLAG=" -m32 ";
		ADD_LD_FLAG=" -m32 ";
		ADD_GCC_LD_FLAG=" -Wl,-flat_namespace ";
		ARCHFLAGS="-arch i386";
	else
		LCG_MACHINE_ARCH=$MACHINE_ARCH;
		ADD_GCC_FLAG="";
		ADD_LD_FLAG="";
		ADD_GCC_LD_FLAG="";
		ARCHFLAGS="-arch $MARCHINE_ARCH";
	fi;
else
	if test "x$MACHINE_ARCH" = "xamd64" ; then
		if test "x$CROSS32" = "xyes" ; then
			LCG_MACHINE_ARCH=i386;
			ADD_GCC_FLAG=" -m32 ";
			ADD_LD_FLAG=" -m32 ";
			ARCHFLAGS="-arch i386";
		else
			LCG_MACHINE_ARCH=x86_64 ;
			ADD_GCC_FLAG="";
			ADD_LD_FLAG="";
			ARCHFLAGS="-arch x86_64";
		fi;
	else 
		LCG_MACHINE_ARCH=`uname -m`;
		ADD_GCC_FLAG="";
		ADD_LD_FLAG="";
		ARCHFLAGS="-arch $MACHINE_ARCH";
	fi;
fi ;

_CC=         ;
_CXX=        ;
_FC=         ;
_CC_args=    ;
_CXX_args=   ;
_FC_args=    ;

_CFLAGS=     ;
_CXXFLAGS=   ;
_FFLAGS=     ;


echo "Checking for CC" >&2;
if test "x$CC" != "x" ; then
	echo "CC=$CC is set in the environment. Hopefully, you know what you're doing." >&2;
	_cc=`echo "$CC" | sed 's, .*$,,'`;
	_CC_args=`echo "$CC" | sed 's,^[^ ][^ ]*[ ]*,,;'` ;
	_cc=`which $_cc 2>/dev/null`;
	if test "x$_cc" != "x" -a -x "$_cc" ; then
		echo "C compiler candidate is $_cc" >&2;
		if test "x$_CC_args" != "x" ; then
			echo "(to be used as $_cc $_CC_args)" >&2;
		fi;
		_CC="$_cc";
	else
		echo "ERROR: missing C compiler you pretend to use. Consider appending the proper path to PATH variable">&2;
		exit 1;
	fi;
else
	_cc_list="gcc cc";
	for _cc in $_cc_list ; do 
		echo "Checking for $_cc ... " >&2;
		_cc=`which $_cc 2>/dev/null`;
		if test "x$_cc" != "x" -a -x "$_cc" ; then
			echo "C compiler candidate is $_cc ... " >&2;
			_CC="$_cc";
			break;
		else
			echo "NOT found" >&2;
		fi;
	done;
fi;
if test "x$_CC" = "x" ; then
	echo "ERROR: can't find C compiler. Stop.">&2;
	exit 1;
fi;

_CC_name=;

_CC_gcc_version=;
_CC_gcc_version_major=;
_CC_gcc_version_minor=;
_CC_gcc_version_minor_minor=;

_CC_version=;
_CC_version_major=;
_CC_version_minor=;
_CC_version_minor_minor=;

if $_CC --version | grep -i GCC 2>&1 >/dev/null ; then
	_CC_gcc_version=`$_CC -dumpversion`;
	_CC_gcc_version_major=`echo "$_CC_gcc_version" | sed 's,^\([0-9][0-9]*\).*$,\1,;'`;
	_CC_gcc_version_minor=`echo "$_CC_gcc_version" | sed 's,^[0-9][0-9]*\.\([0-9][0-9]*\).*$,\1,;'`;
	_CC_gcc_version_minor_minor=`echo "$_CC_gcc_version" | sed 's,^[0-9][0-9]*\.[0-9][0-9]*\.\([0-9][0-9]*\)$,\1,;'`;
	_CC_name=gcc;
	echo "$_CC appears to be gcc $_CC_gcc_version" >&2;
else
	_CC_name=`basename $_cc`;
fi;
_CC_version=$_CC_gcc_version;
_CC_version_major=$_CC_gcc_version_major;
_CC_version_minor=$_CC_gcc_version_minor;
_CC_version_minor_minor=$_CC_gcc_version_minor_minor;


if test "x$CFLAGS" != "x" ; then
	echo "CFLAGS=$CFLAGS is set in the environment. Hopefully, you know what you're doing.">&2;
	_CFLAGS="$_CC_args $CFLAGS";
else
	if test "x$ADD_GCC_FLAG" != "x" ; then
		echo "WARNING: $ADD_GCC_FLAG is added to compiler options." >&2;
	fi;
	_CFLAGS="$_CC_args $ADD_GCC_FLAG";
	LDFLAGS="$LDFLAGS $ADD_LD_FLAG $ADD_GCC_LD_FLAG";
fi;

echo "Checking if $_CC $_CFLAGS can create executables ..." >&2;
if _check_cc "$_cc" "$_CFLAGS" ; then
	echo "it can">&2;
else
	echo "ERROR: $_CC $_CFLAGS can't create an executable. Stop." >&2;
	exit 1;
fi;
echo "Checking if $_CC $_CFLAGS can create executables with GENSER flags: $CFLAGS_GENSER ... " >&2;
if _check_cc "$_cc" "$_CFLAGS $CFLAGS_GENSER" ; then
	echo "it can">&2;
	CC="$_cc";
	CFLAGS="$_CFLAGS $CFLAGS_GENSER";
else
	echo "WARNING: $_cc fails to work with GENSER flags: $CFLAGS_GENSER">&2;
	CC="$_cc";
	CFLAGS="$_CFLAGS";
fi;
echo "Setting CC='$CC'" >&2;
echo "Setting CFLAGS='$CFLAGS'">&2;
export CC CFLAGS;


echo "Checking for FC" >&2;
if test "x$FC" != "x" -o "x$F77" != "x" ; then
	if test "x$FC" != "x" -a "x$F77" != "x" -a "x$FC" != "x$F77" ; then
		echo "ERROR: both FC=$FC and F77=$F77 are set. Stop to avoid clashes." >&2;
		exit 1;
	fi;
	if test "x$FC" != "x" ; then
		echo "FC=$FC is set in the environment. Hopefully, you know what you're doing." >&2;
	else
		echo "F77=$F77 is set in the environment. You are assumed to exactly know what you're doing" >&2;
		FC=$F77;
	fi;
	_fc=`echo "$FC" | sed 's, .*$,,'`;
	_FC_args=`echo "$FC" | sed 's,^[^ ][^ ]*[ ]*,,;'` ;
	_fc=`which $_fc 2>/dev/null`;
	if test "x$_fc" != "x" -a -x "$_fc" ; then
		echo "Fortran compiler candidate is $_fc" >&2;
		if test "x$_FC_args" != "x" ; then
			echo "(to be used as $_fc $_FC_args)" >&2;
		fi;
		_FC="$_fc";
	else
		echo "ERROR: missing Fortran compiler you pretend to use. Consider appending the proper path to PATH variable">&2;
		exit 1;
	fi;
else
	if test "x$_CC_gcc_version" != "x" ; then
		if test $_CC_gcc_version_major -gt 3 ; then
			_fc_list="gfortran g95 f95 f90 fortran g77 f77";
		else
			_fc_list="g77 f77 fortran f90 f95 gfortran";
		fi;
	else
		_fc_list="gfortran g95 f95 f90 fortran g77 f77 ifort fort ifc";
	fi;
	for _fc in $_fc_list ; do 
		echo "Checking for $_fc ... " >&2;
		_fc=`which $_fc 2>/dev/null`;
		if test "x$_fc" != "x" -a -x "$_fc" ; then
			echo "Fortran compiler candidate is $_fc ... " >&2;
			_FC="$_fc";
			break;
		else
			echo "NOT found" >&2;
		fi;
	done;
fi;
if test "x$_FC" = "x" ; then
	echo "ERROR: can't find Fortran compiler. Stop.">&2;
	exit 1;
fi;



if test "x$FFLAGS" != "x" -o "x$FCFLAGS" != "x" ; then
	if test "x$FFLAGS" != "x" -a "x$FCFLAGS" != "x" ; then
		echo "ERROR: both FFLAGS=$FFLAGS and FCFLAGS=$FCFLAGS are set in the environment. Stop to avoid clashes" >&2;
		exit 1;
	fi;
	if test "x$FFLAGS" != "x" ; then
		echo "FFLAGS=$FFLAGS is set in the environment. Hopefully, you know what you're doing.">&2;
	fi;
	if test "x$FCFLAGS" != "x" ; then
		echo "FCFLAGS=$FCFLAGS is set in the environment. Hopefully, you know what you're doing.">&2;
		FFLAGS="$FCFLAGS";
	fi;
	_FFLAGS="$_FC_args $FFLAGS";
else
	if test "x$ADD_GCC_FLAG" != "x" ; then
		echo "WARNING: $ADD_GCC_FLAG is added to compiler options." >&2;
	fi;
	_FFLAGS="$_FC_args $ADD_GCC_FLAG";
fi;

echo "Checking if $_FC $_FFLAGS can create executables ..." >&2;
if _check_fortran "$_fc" "$_FFLAGS" ; then
	echo "it can">&2;
else
	echo "ERROR: $_FC $_FFLAGS can't create an executable. Stop." >&2;
	exit 1;
fi;
echo "Checking if $_FC $_FFLAGS can create executables with GENSER flags: $FFLAGS_GENSER ... " >&2;
if _check_fortran "$_fc" "$_FFLAGS $FFLAGS_GENSER" ; then
	echo "it can">&2;
	FC="$_fc";
	FFLAGS="$_FFLAGS $FFLAGS_GENSER";
else
	echo "WARNING: $_fc fails to work with GENSER flags: $FFLAGS_GENSER">&2;
	FC="$_fc";
	FFLAGS="$_FFLAGS";
fi;

_FC_gcc_version=;
_FC_gcc_version_major=;
_FC_gcc_version_minor=;
_FC_gcc_version_minor_minor=;

if $FC --version | grep GCC 2>&1 >/dev/null ; then
	_FC_gcc_version=`$FC --version 2>/dev/null |  sed '/GCC/!d; s,^.*GCC[^0-9][^0-9]*\([^ ][^ ]*\).*$,\1,;'`;
	_FC_gcc_version_major=`echo "$_FC_gcc_version" | sed 's,^\([0-9][0-9]*\).*$,\1,;'`;
	_FC_gcc_version_minor=`echo "$_FC_gcc_version" | sed 's,^[0-9][0-9]*\.\([0-9][0-9]*\).*$,\1,;'`;
	_FC_gcc_version_minor_minor=`echo "$_FC_gcc_version" | sed 's,^[0-9][0-9]*\.[0-9][0-9]*\.\([0-9][0-9]*\)$,\1,;'`;
	echo "$FC appears to be GNU fortran $_FC_gcc_version" >&2;
	if test "x$_CC_gcc_version" != "x" -a "x$_CC_gcc_version" != "x$_FC_gcc_version" ; then
		echo "WARNING: GNU fortran version $_FC_gcc_version doesn't match GNU C version $_CC_gcc_version" >&2;
	fi;
fi;

echo "Setting FC='$FC'" >&2;
echo "Setting F77='$FC'" >&2;
echo "Setting FFLAGS='$FFLAGS'">&2;
echo "Setting FCFLAGS='$FFLAGS'">&2;
FCFLAGS="$FFLAGS";
export FC F77 FFLAGS FCFLAGS;


echo "Checking for CXX" >&2;
if test "x$CXX" != "x" ; then
	echo "CXX=$CXX is set in the environment. Hopefully, you know what you're doing." >&2;
	_cxx=`echo "$CXX" | sed 's, .*$,,'`;
	_CXX_args=`echo "$CXX" | sed 's,^[^ ][^ ]*[ ]*,,;'` ;
	_cxx=`which $_cxx 2>/dev/null`;
	if test "x$_cxx" != "x" -a -x "$_cxx" ; then
		echo "C++ compiler candidate is $_cxx" >&2;
		if test "x$_CXX_args" != "x" ; then
			echo "(to be used as $_cxx $_CXX_args)" >&2;
		fi;
		_CXX="$_cxx";
	else
		echo "ERROR: missing C++ compiler you pretend to use. Consider appending the proper path to PATH variable">&2;
		exit 1;
	fi;
else
	_cxx_list="g++ c++ cxx";
	for _cxx in $_cxx_list ; do 
		echo "Checking for $_cxx ... " >&2;
		_cxx=`which $_cxx 2>/dev/null`;
		if test "x$_cxx" != "x" -a -x "$_cxx" ; then
			echo "C++ compiler candidate is $_cxx ... " >&2;
			_CXX="$_cxx";
			break;
		else
			echo "NOT found" >&2;
		fi;
	done;
fi;
if test "x$_CXX" = "x" ; then
	echo "ERROR: can't find C++ compiler. Stop.">&2;
	exit 1;
fi;

_CXX_gcc_version=;
_CXX_gcc_version_major=;
_CXX_gcc_version_minor=;
_CXX_gcc_version_minor_minor=;

if $_CXX --version | grep GCC 2>&1 >/dev/null ; then
	_CXX_gcc_version=`$_CXX --version 2>/dev/null |  sed '/GCC/!d; s,^.*GCC[^0-9][^0-9]*\([^ ][^ ]*\).*$,\1,;'`;
	_CXX_gcc_version_major=`echo "$_CXX_gcc_version" | sed 's,^\([0-9][0-9]*\).*$,\1,;'`;
	_CXX_gcc_version_minor=`echo "$_CXX_gcc_version" | sed 's,^[0-9][0-9]*\.\([0-9][0-9]*\).*$,\1,;'`;
	_CXX_gcc_version_minor_minor=`echo "$_CXX_gcc_version" | sed 's,^[0-9][0-9]*\.[0-9][0-9]*\.\([0-9][0-9]*\)$,\1,;'`;
	echo "$_CXX appears to be GNU C++ $_CXX_gcc_version" >&2;
	if test "x$_CC_gcc_version" != "x" -a "x$_CC_gcc_version" != "x$_CXX_gcc_version" ; then
		echo "WARNING: GNU C++ version $_CXX_gcc_version doesn't match GNU C version $_CC_gcc_version" >&2;
	fi;
fi;


if test "x$CXXFLAGS" != "x" ; then
	echo "CXXFLAGS=$CXXFLAGS is set in the environment. Hopefully, you know what you're doing.">&2;
	_CXXFLAGS="$_CXX_args $CXXFLAGS";
else
	if test "x$ADD_GCC_FLAG" != "x" ; then
		echo "WARNING: $ADD_GCC_FLAG is added to compiler options." >&2;
	fi;
	_CXXFLAGS="$_CXX_args $ADD_GCC_FLAG";
fi;

echo "Checking if $_CXX $_CXXFLAGS can create executables ..." >&2;
if _check_cxx "$_cxx" "$_CXXFLAGS" ; then
	echo "it can">&2;
else
	echo "ERROR: $_CXX $_CXXFLAGS can't create an executable. Stop." >&2;
	exit 1;
fi;
echo "Checking if $_CXX $_CXXFLAGS can create executables with GENSER flags: $CXXFLAGS_GENSER ... " >&2;
if _check_cxx "$_cxx" "$_CXXFLAGS $CXXFLAGS_GENSER" ; then
	echo "it can">&2;
	CXX="$_cxx";
	CXXFLAGS="$_CXXFLAGS $CXXFLAGS_GENSER";
else
	echo "WARNING: $_cxx fails to work with GENSER flags: $CXXFLAGS_GENSER">&2;
	CXX="$_cxx";
	CXXFLAGS="$_CXXFLAGS";
fi;
echo "Setting CXX='$CXX'" >&2;
echo "Setting CXXFLAGS='$CXXFLAGS'">&2;
export CXX CXXFLAGS;

if test "x$LDFLAGS" != "x" ; then
	export LDFLAGS;
fi;

if test "x$LCG_OPSYS" = "xslc4" ; then
	LCG_PLATFORM="${LCG_OPSYS}_${LCG_MACHINE_ARCH}_${_CC_name}${_CC_version_major}${_CC_version_minor}";
elif test "x$LCG_OPSYS" = "xosx105" ; then
	LCG_PLATFORM="${LCG_OPSYS}_${LCG_MACHINE_ARCH}_${_CC_name}${_CC_version_major}${_CC_version_minor}${_CC_version_minor_minor}";
else
	LCG_PLATFORM="${LCG_MACHINE_ARCH}-${LCG_OPSYS}-${_CC_name}${_CC_version_major}${_CC_version_minor}-opt";
fi;
echo "Setting LCG_PLATFORM=$LCG_PLATFORM" >&2;

export LCG_PLATFORM;

if test "x$ARCHFLAGS" != "x" ; then
	echo "Setting ARCHFLAGS='$ARCHFLAGS'">&2;
	export ARCHFLAGS;
fi;

};


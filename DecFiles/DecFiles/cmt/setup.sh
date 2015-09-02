# echo "Setting DecFiles v23r1 in /afs/cern.ch/user/j/jback/Gen"

if test "${CMTROOT}" = ""; then
  CMTROOT=/afs/cern.ch/sw/contrib/CMT/v1r20p20090520; export CMTROOT
fi
. ${CMTROOT}/mgr/setup.sh

tempfile=`${CMTROOT}/mgr/cmt -quiet build temporary_name`
if test ! $? = 0 ; then tempfile=/tmp/cmt.$$; fi
${CMTROOT}/mgr/cmt setup -sh -pack=DecFiles -version=v23r1 -path=/afs/cern.ch/user/j/jback/Gen  -no_cleanup $* >${tempfile}; . ${tempfile}
/bin/rm -f ${tempfile}


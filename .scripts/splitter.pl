#!/usr/local/bin/perl

#*******************************************************************************
#
# Program for splitting huge source files in Fortran into separate routine 
# files of the form "name.f", where "name" is the name of the program unit. 
# Standard command (fsplit) sometimes doesn't work so I had to write this one...
#
# Unit types:
#		SUBROUTINE	<name>
#		FUNCTION 		<name>
#		BLOCK DATA 	<name>
#
# We can pass some arguments using the command line:
#
#   perl -w splitter.pl <sourceFile> [<linesCount>]
#
#   <sourceFile>		- the file to split
#   <linesCount> 		- number of lines to proceed. 
#                                 Proceed all file if ommited
#
# ------------------------------------------------------------------------------
#
# RUN EXAMPLE:
#
#   perl -w splitter.pl herwig_6_530.h
#
# Created:	08.09.2003
# Modified:	
#                                         (C) Sergey Makarychev (semak@itep.ru)
#*******************************************************************************

use strict;


#===============================================================
# Variables definition (requred by using 'strict' option)

my $errorCode = 0;	# 0 - no errors
			# 1 - wrong parameters in command line
			# 2 - file open error

my $fileName;		# the name of the file to split
my $linesCount = 0;	# lines to proceed. (0 means all file)

my @linesArray;		# will contain lines of one procedure
my $str;		# the holder for one line from the file
my $counter = 0;	# just a simple line counter
my $fileCounter = 0;	# will count the number of procedures in source file
my $writingMode = 0;	# TRUE if we are storing lines in the separate file

#===============================================================
#===============================================================
#===============================================================
# Program starts

print "\n-> Program started...\n";

# ==================================================================
# Read parameters from command line

if (scalar(@ARGV) < 1){
  print "-> \tERROR: Not enough parameters in command line!\n";
  print "-> \tUSAGE: perl -w splitter.pl <sourceFile> [<linesCount>]\n";
  $errorCode = 1;
  goto ExitPoint;
}

if (scalar(@ARGV) > 2){
  print "-> \tERROR: Too many parameters in command line!\n";
  print "-> \tUSAGE: perl -w splitter.pl <sourceFile> [<linesCount>]\n";
  $errorCode = 1;
  goto ExitPoint;
}

$fileName = $ARGV[0];
$linesCount = $ARGV[1] if (scalar(@ARGV) > 1);

# ==================================================================
# Try to open the source file

if (!open (FILE_IN, "< $fileName")){
  print qq/-> Can't open file "$fileName" for reading!\n/;
  $errorCode = 2;
  goto ExitPoint;
}

# ==================================================================
# ==================================================================
# MAIN LOOP - THROUGH ALL PROCEDURES IN THE FILE...
# ==================================================================
# ==================================================================

print qq/-> This program will try to split the "$fileName" file on subroutines.\n/;

$counter = 0;
$fileCounter = 0;
$#linesArray = -1;		# clear lines array
$writingMode = 0;			# FALSE

print "-> Working...\n";
while ($str = <FILE_IN>)
{  
	# ===============================================================
	# 1) If the line is commented - just write it
	
	if ($str =~ m|^C|i || $str =~ m|^\*|){
		#print $str;
		goto WriteLine;
	}

	# ===============================================================
	#	if we are writting module - we need to check END keyword only
	# otherwise we can find something like string 'STRUCTURE FUNCTION SET ='
	# it could be wrongly considered as begin of new function
	if ($writingMode){
		goto EndKeyword;
	}
		
	# ===============================================================
	# 2) Try to find the START of the routine in current line
	# 	(symbol ^ means start of the line, $ - end of the line,
	#	\s+ means one or more spaces)
	#
	#      (*) if we want to use some found values - we should write it 
	#      in brackets: (..)
	#      after that it could be reffered by $1, $2, etc...
	
	if ($str =~ m|\s+SUBROUTINE\s+(\w+)|i 	|| 
			$str =~ m|^SUBROUTINE\s+(\w+)|i 		||
			$str =~ m|\s+FUNCTION\s+(\w+)|i 		|| 
			$str =~ m|^FUNCTION\s+(\w+)|i			||
			$str =~ m|\s+BLOCK\s+DATA\s+(\w+)|i || 
			$str =~ m|^BLOCK\s+DATA\s+(\w+)|i){
		
		# =============================================================
		# OPEN the new file - start of new routine...

		$fileCounter ++;					
		$fileName = lc ("$1.F");
		
		# Open the new one...
		if (!open (FILE_OUT, "> $fileName")){
		  print qq/-> Can't open file "$fileName" for writting!\n/;
		  $errorCode = 2;
		  goto ExitPoint;
		}

		# information for output...
		print "\t$fileName\t(file $fileCounter, line $counter)\n";
		
		# write lines from memory buffer to file
		push (@linesArray, $str);
		while (scalar(@linesArray) > 0){
				
			$str = shift (@linesArray);
			print FILE_OUT $str;		
		}

		# set writing mode ON
		$writingMode = 1;			# TRUE
		goto SkipLine;

		#print "LINE_$counter: $str";
		#print "Name = $3\n";
	};
	
EndKeyword:
	# ===============================================================
	# 3) Try to find the END of the routine in current line
	# 	(symbol ^ means start of the line, $ - end of the line,
	#	\s+ means one or more spaces)
	
	if ($str =~ m|^\s*\d*\s+END\s+$|i ||
			$str =~ m|^END\s+$|i){

		# =============================================================
		# CLOSE the current file - end of new routine...

		# save the last line (with the END) in the file
		print FILE_OUT $str;
		close (FILE_OUT);

		# clear lines array (just in case, array should be 
                # empty at this moment)
		$#linesArray = -1;
			
		# set writing mode OFF
		$writingMode = 0;			# FALSE
		goto SkipLine;

		#print "LINE_$counter: $str";
		#print "\n";	
	}
	
WriteLine:
	#===============================================================
	# 4) Nothing special found. Store current line (in the file or 
        #    in buffer)

	if ($writingMode){
		# Store current line in the file...
		print FILE_OUT $str;
	}
	else{
		# ...or add this line to the array and wait for routine's start
		push (@linesArray, $str);
	}

SkipLine:	
	#===============================================================
	# Go to the next line...

	$counter++;
  #print "LINE_$counter: $str";         # print file, line by line
		
	#===============================================================
	# Check lines count limit (if defined)
	
	if ($linesCount != 0){
		if ($counter == $linesCount){
			print"\n-> Cancelling at line $counter...\n";
			goto ExitPoint;
		}
	}
}		# end of while {...} (reading from the file to the end)


ExitPoint:
print "->\n";
print "-> $counter lines were processed.\n";
print "-> $fileCounter program units were found and splitted in separate files.\n";

#===============================================================
# Close open files

close (FILE_IN);
close (FILE_OUT);

#===============================================================
# Program ends

print "-> Program finished (errorCode $errorCode)\n\n";
exit ($errorCode);

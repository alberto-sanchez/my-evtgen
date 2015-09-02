#!/usr/bin/env python
import sys,re,mdclient


host = 'lxarda01.cern.ch'
port = 8822
#user = 'anonymous'
user = 'root'
amga_client = mdclient.MDClient(host, port, user)

def usage():
  print 'eventTypeMng [-u|-i  <file name>] | -h | --help\n'
  print 'This tool is used to update or insert new event type.'
  print 'The <file name> list the event on which operate. Each entry  has the following format and is per line.'
  print 'EVTTYPE_ID="<evant id>", DESCRIPTION="<description>", PRIMARY="<primary description>", DECAY="<decay descriptio>"'
  print 'Options:\n   -u: update event type\n   -i: insert event type'
  print '   -h|--help: print this help'


def process_event(eventline):
       EVTTYPE_ID=0
       DESCRIPTION=''
       PRIMARY=''
       DECAY=''
       wrongSyntax=0
       try:
           eventline.index('EVTTYPE_ID')
           eventline.index('DESCRIPTION')
           eventline.index('PRIMARY')
           eventline.index('DECAY')
       except ValueError:
           print '\nthe file syntax is wrong!!!\n'+eventline+'\n\n'
           usage()
           sys.exit(0)
       parameters=eventline.split(',')

       result={}
       ma=re.match("^ *?((?P<id00>EVTTYPE_ID) *?= *?(?P<value00>[0-9]+)|(?P<id01>DESCRIPTION|PRIMARY|DECAY) *?= *?\"(?P<value01>.*?)\") *?, *?((?P<id10>EVTTYPE_ID) *?= *?(?P<value10>[0-9]+)|(?P<id11>DESCRIPTION|PRIMARY|DECAY) *?= *?\"(?P<value11>.*?)\") *?, *?((?P<id20>EVTTYPE_ID) *?= *?(?P<value20>[0-9]+)|(?P<id21>DESCRIPTION|PRIMARY|DECAY) *?= *?\"(?P<value21>.*?)\") *?, *?((?P<id30>EVTTYPE_ID) *?= *?(?P<value30>[0-9]+)|(?P<id31>DESCRIPTION|PRIMARY|DECAY) *?= *?\"(?P<value31>.*?)\") *?$",eventline)

       if not ma:
         print "syntax error at: \n"+eventline
         usage()
         sys.exit(0)         
       else:
         for i in range(4):
           if ma.group('id'+str(i)+'0'):
             if ma.group('id'+str(i)+'0') in result:
                print '\nthe parameter '+ma.group('id'+str(i)+'0')+' cannot appear twice!!!\n'+eventline+'\n\n'
                sys.exit(0)
             else:
               result[ma.group('id'+str(i)+'0')]=ma.group('value'+str(i)+'0')
           else:
             if ma.group('id'+str(i)+'1') in result:
                print '\nthe parameter '+ma.group('id'+str(i)+'1')+' cannot appear twice!!!\n'+eventline+'\n\n'
                sys.exit(0)
             else:
               result[ma.group('id'+str(i)+'1')]=ma.group('value'+str(i)+'1')
             
       return result


def execute(args) :
  import getopt
  raw_arg=sys.argv[1:]
  raw_arg_size=len(raw_arg)
  file=''
  option=''

  if (raw_arg_size==0) or (raw_arg_size>2):
    print 'Too few/many argments.\nUSAGE:\n'
    usage()
    sys.exit(1)

  for a in raw_arg:
       if a[0] != '-' :
          file=a
       else :
           if a not in ['-u','-i','-h','--help']:
                print 'Options not valid.\nUSAGE\n'
                return usage()
           if a in ['-h','--help']:
                return usage()
           option=a

  if len(option)==0:
    print 'No option specified.\nUSAGE:\n'
    usage()
    sys.exit(1)

  if len(file)==0:
    print 'The file name is missing.\nUSAGE:\n'
    usage()
    sys.exit(1)

  try:
     fevt=open(file)
  except Exception,ex:
      print 'cannot open file '+file
      print ex
      return


  filecontents=[]
  tablecontents={}
  eventline=fevt.readline()
  while(eventline):
       if eventline[-1]=='\n':
          eventline=eventline[:-1]
       if not eventline:
           eventline=fevt.readline()
           continue
       filecontents.append(process_event(eventline))
       eventline=fevt.readline()
  error=0
  try:
     amga_client.getattr('/evtTypes/*', ['DESCRIPTION', 'PRIMARY', 'DECAY'])
     while not amga_client.eot():
        fn, values = amga_client.getEntry()
        tablecontents[fn]={'EVTTYPE_ID':fn,'DESCRIPTION':values[0],'PRIMARY':values[1],'DECAY':values[2]}
  except mdclient.CommandException, ex:
            print 'error: '+str(ex)
            amga_client.disconnect()
            return

  try:
   if option=='-i':
    for entry in filecontents:
      if entry['EVTTYPE_ID'] in  tablecontents:
        None
        #print 'event type '+entry['EVTTYPE_ID']+' is present.'
      else:
        print 'event type '+entry['EVTTYPE_ID']+' is missing. Updating table'
        amga_client.addEntry('/evtTypes/'+entry['EVTTYPE_ID'],['DESCRIPTION', 'PRIMARY', 'DECAY','EVTTYPE_ID'],[entry['DESCRIPTION'], entry['PRIMARY'], entry['DECAY'],entry['EVTTYPE_ID']])
        print 'Done!'
   else:
    for entry in filecontents:
      if entry['EVTTYPE_ID'] in  tablecontents:
        if entry==tablecontents[entry['EVTTYPE_ID']]:
           None
           #print 'event type '+entry['EVTTYPE_ID']+' doesn\'t need to be updated'
        else:
           print '\nevent type '+entry['EVTTYPE_ID']+' need to be updated'
           print 'New values:  ',entry,'\n----     -----\nOld values ',tablecontents[entry['EVTTYPE_ID']],'\n'
           if entry['DESCRIPTION']!=tablecontents[entry['EVTTYPE_ID']]['DESCRIPTION']:# update also the files description firing the oracle trigger Trg_AuditAMGA_EvtType
                 amga_client.setAttr('/evtTypes/'+entry['EVTTYPE_ID'],['DESCRIPTION', 'PRIMARY', 'DECAY'],[entry['DESCRIPTION'], entry['PRIMARY'], entry['DECAY']])
           else:
                 amga_client.setAttr('/evtTypes/'+entry['EVTTYPE_ID'],[ 'PRIMARY', 'DECAY'],[ entry['PRIMARY'], entry['DECAY']])
           print 'Updated.'
      else:
        print  'event type '+entry['EVTTYPE_ID']+' is missing'
        error=1
  except mdclient.CommandException, ex:
            print 'error: '+str(ex)
            amga_client.disconnect()
            return
  if not error:        
    print 'All done!!'
  amga_client.disconnect()

       
  #print filecontents
  #print tablecontents     
  #print  file,'\n---\n', options  





if __name__ == "__main__":
  execute(sys.argv[1:])

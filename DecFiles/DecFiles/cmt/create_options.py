#!/usr/bin/env python
#
#  Create_options.py :
#  Author   Manuel Barbera Asin, 14 November 2005
#  Modified Gloria Corti, 20 Nov 2008 to add SUSY and J/Psi particle guns
#
#  create an options file from a decay files
#============================================================================
# 060616 - fixes
#============================================================================
import sys,os,re, string
import time,fileinput

# ---------------------------------------------------------------------------
# Utility function for SUSY model: only for G=4, S=5,6
# ---------------------------------------------------------------------------
def susyOptions(eventType):

    susy = OptionsValue(decdir,"SUSYModel")
    if susy == None: return 0
    if eventType[0:2] != '45' and eventType[0:2] != '46' :
        print "***ERROR: The option SUSYModel can only be used with EventType"
        print " 45dctnxu or 46dctnxu: It is ", eventType, eventType[0:2]
        sys.exit()
    
    optValues = susy.split()
    if len(optValues) != 1 and len(optValues) != 2 :
        print "WARNING: The Keyword SUSY must have one or two values:\n"
        print "         Model and Option (eg. Kaplan_hkk 10ps)"
        return 0

    model = optValues[0]
    choice = model
    if len(optValues) == 2: choice = choice+'_'+optValues[1]
    # include main options for the model: Kaplan or SusyBRpV
    extra = ''
    if OptionsName[1] == '5':
        extra = 'Kaplan'
    elif OptionsName[1] == '6':
        extra = 'SusyBRpV'
    
    optTxt = '#include \"$DECFILESROOT/options/'+extra+'.opts\"\n'    
    if OptionsName[1] == '5':
        optTxt += '#include \"$DECFILESROOT/options/'+model+'.opts\"\n'
        optTxt += 'Generation.Special.PythiaProduction.SLHADecayFile = "'+choice+'.LHdec";\n'
        optTxt += 'Generation.Special.PythiaProduction.PDecayList = {1000022};\n'

    if OptionsName[1] == '6':
        optTxt += 'Generation.Special.PythiaProduction.SLHASpectrumFile = "'+choice+'.LHspc";\n'
        if optValues[0].find('AMSB') != -1:
            optTxt += 'Generation.Special.PythiaLSP.LSPID = { 1000022, 1000024 };\n'

    
    writeOptions(optionsdir,optTxt)
    
# ---------------------------------------------------------------------------
# Utilitty function for Halo from beam gas interactions in LSS and arc
# ---------------------------------------------------------------------------
def beamGasLssArcToolsOptions(evnt):

    # Find all particles to do: Muons, Hadrons or both
    pType = evnt[1]
    cConf = evnt[2]
    bConf = evnt[4]
    pTypes = []
    if (pType != '0' and pType != '2' and pType != '9'):
        print '\n ***ERROR:Only value 0(all), 2(muons), 9(hadrons) allowed in ParticleTypes\n'
        sys.exit()
    else:
        if (pType == '2' or pType == '0'):
            pTypes.append('Muons')
        if (pType == '9' or pType == '0'):
            pTypes.append('Hadrons')

    # Find machine conditions
    iConf = int(cConf)
    if (iConf < 0 or iConf > 2):
        print '\n ***ERROR:Only value from 0 to 2 allowed in Configuration\n'
        sys.exit()
    sDict = {0:'Beta10Startup', 1:'Beta01Startup', 2:'Beta10Scrubbed'}
    source = sDict[iConf]

    # Find beam
    bConf
    if (bConf != '0' and bConf != '1' and bConf != '2'):
        print '\n ***ERROR:Only value from 0 to 2 allowed as Beam type\n'
        sys.exit()
    beams = []
    if (bConf == '0' or bConf == '1'):
        beams.append('Beam1')
    if (bConf == '0' or bConf == '2'):
        beams.append('Beam2')

    # Write all options for the tool to use (may be from 1 to 4)
    pDict = { 'Muons':'mu', 'Hadrons':'h' }

    optTxt = ''
    nickBeam = ''
    for b in beams:
        nickBeam += b
        nickPType = ''
        for p in pTypes:
            nickPType += pDict[p]
            toolName = source+b+p
            optTxt += 'MIBackground.MIBSources  += { "CollimatorSource/'+toolName+'" };\n'
            filename = source+'.'+b+'.'+pDict[p]+'.data'
            optTxt += 'MIBackground.'+toolName+'.ParticleSourceFile   = "'+'$MIBDATAROOT/data/'+filename+'";\n'
            if b == 'Beam2':
                optTxt += 'MIBackground.'+toolName+'.ZParticleOrigin = 19.9*m;\n'
                optTxt += 'MIBackground.'+toolName+'.ZDirection = -1;\n'

    nickTxt = '.'+nickBeam+'.'+source+'.'+nickPType
    return optTxt, nickTxt

# ---------------------------------------------------------------------------
# Utilitty function for Halo on Collimators
# ---------------------------------------------------------------------------
def tctHaloToolsOptions(evnt):

    # Find all particles to do: Muons, Hadrons or both
    pType = evnt[1]
    cConf = evnt[2]
    pTypes = []
    if (pType != '0' and pType != '2' and pType != '9'):
        print '\n ***ERROR:Only value 0(all), 2(muons), 9(hadrons) allowed in ParticleTypes\n'
        sys.exit()
    else:
        if (pType == '2' or pType == '0'): 
            pTypes.append('Muons')
        if (pType == '9' or pType == '0'):
            pTypes.append('Hadrons')
        
    # Find Shield configuration to use (only one possible!)
    iConf = int(cConf)
    if (iConf < 0 or iConf > 8):
        print '\n ***ERROR:Only value from 0 to 8 allowed in Configuration\n'
        sys.exit()
    sDict = {0:'StagedShield', 1:'Shield', 2:'NoShield'}
    ishield = (iConf)/3
    shield = sDict[ishield]

    # Find Collimator source to use (TCTV, TCTH or both)
    tct = (iConf)%3
    tctList = []
    if( tct == 0 or tct == 1 ):
        tctList.append('TCTV')
    if( tct == 0 or tct == 2 ):
        tctList.append('TCTH')

    # Write all options for the tool to use (may be from 1 to 4)
    pDict = { 'Muons':'mu', 'Hadrons':'h' }
    sDict = { 'StagedShield':'staged_shield', 'Shield':'shield', 'NoShield':'no_shield'}

    optTxt = ''
    nickTCT = ''
    for c in tctList:
        nickTCT += c
        nickPType = ''
        for p in pTypes:
            nickPType += pDict[p] 
            toolName = c+shield+p
            optTxt += 'MIBackground.MIBSources  += { "CollimatorSource/'+toolName+'" };\n'
            filename = c+'.'+sDict[shield]+'.'+pDict[p]+'.data'
            optTxt += 'MIBackground.'+toolName+'.ParticleSourceFile   = "'+'$MIBDATAROOT/data/'+filename+'";\n'
        
    
    nickTxt = '.'+nickTCT+'.'+sDict[shield]+'.'+nickPType
    return optTxt, nickTxt

# ---------------------------------------------------------------------------
# Options for Halo on Collimators
# ---------------------------------------------------------------------------
def beamHalo(eventType):

##  EventType = GSDCTNXU, G=6 & C=5 halo on collimators
##  S = particle types generated (similar as for G=5)
##      0: all
##      2: mu
##      9: other (i.e. hadrons)
##  D = special meaning of source configuration (shield and collimator)
##      0: staged shield - Loss on TCTV.4L8.B1 & TCTH.L8.B1
##      1: staged shield - Loss on TCTV.4L8.B1
##      2: staged shield - Loss on TCTH.L8.B1
##      3: design shield - Loss on TCTV.4L8.B1 & TCTH.L8.B1
##      4: design shield - Loss on TCTV.4L8.B1
##      5: design shield - Loss on TCTH.L8.B1
##      6: no shield - Loss on TCTV.4L8.B1 & TCTH.L8.B1
##      7: no shield - Loss on TCTH.L8.B1
##      8: no shield - Loss on TCTH.L8.B1
##  T=0: both beams, T=1: beam1, T=2: beam2
##  N=Num. of bunches traveling (beam1), X=Num. of bunches traveling (beam2)

##  EventType = GSDCTNXU, G=6 & C=4 halo from LSS and arc beam gas
##  S = particle types generated (similar as for G=5)
##      0: all
##      2: mu
##      9: other (i.e. hadrons)
##  D = special meaning of source configuration (Gas densities and beam beta*)
##      0: Startup gas pressure, Beta* = 10m 
##      1: Startup gas pressure, Beta* = 1m
##      2: Scrubbed gas pressure, Beta* = 10m
##  T=0: both beams, T=1: beam1, T=2: beam2

    # If mirror Keyword is present duplicate options as controlled
    # otherwise use eventtype as-is
    configValue = OptionsValue(decdir,"Configuration")
    ptypeValue = OptionsValue(decdir,"ParticleType")
    G = eventType[0]
    CTNXU = eventType[3:8]
    eventList = []
    if (configValue != None):
        configList = configValue.strip().split()
    else:
        configList = [eventType[1]]
        
    if (ptypeValue != None):
        ptypeList = ptypeValue.strip().split()
    else:
        ptypeList = [eventType[2]]
        
    for iconf in configList:
        for ipart in ptypeList:
            eventList.append(G+ipart+iconf+CTNXU)


    # Check for common lines to write
    commonTxt = ''
    # Check if exists ExtraOptions keyword
    incl = OptionsValue(decdir,"ExtraOptions")
    if incl != None:
        if len(incl) == 1:
            print "WARNING: There is an ExtraOptions keyword with no value in "+decdir
	else:
            commonTxt += "#include \"$DECFILESROOT/options/"+string.strip(incl)+".opts\"\n"

    
    commonTxt += 'GaussGen.PrintFreq = 100;\n'
    commonTxt += 'GaussSim.PrintFreq = 100;\n'
    commonTxt += 'GiGaGetEventAlg.OutputLevel = 4;\n'
    
    # Now loop over list of event Type and write the options
    for iev in eventList:
        optionsFile = optionsdirroot+iev+".opts"
        HeaderOptions(optionsFile,iev)
        writeOptions(optionsFile,commonTxt)
        if iev[3] == '4':
            evtTxt, nickTxt = beamGasLssArcToolsOptions(iev)
        elif iev[3] == '5':
            evtTxt, nickTxt = tctHaloToolsOptions(iev)
        else:
            print '\n ***ERROR:Only value 4(Beam Gas LSS) and 5(TCT Halo) allowed as source\n'
        writeOptions(optionsFile,evtTxt)
        evtTxt = 'MIBackground.EventType = '+iev+';\n' 
        writeOptions(optionsFile,evtTxt)
        evtNick = OptionsNick+nickTxt 
        writeBkkTable(iev,AsciiName,evtNick,clean)
        writeSQLTable(iev,AsciiName,evtNick,clean)

    

# ---------------------------------------------------------------------------
# Options for Beam gas
# ---------------------------------------------------------------------------
def beamGasLHCb(eventType):

    Znuclei = [1,  6,  8,  54]
    Anuclei = [1, 12, 16, 131]
    data = ''

    # get the last digits of the event type and check that the event type
    # is providing all necessary info
    NXU = eventType[5:8]
    if eventType[6:8] == '00':
        print '\n ***ERROR:Atomic Number not provided\n'
        
    data+= 'Generation.MinimumBias.HijingProduction.Commands += {\n'
    data+= '  "hijinginit frame LAB",\n'

    # Check that the atomic number is in the list 
    atomicNum=int(NXU)
    
    if not (atomicNum in Znuclei) :
        print '\n ***ERROR:Atomic Number not allowed ( NUX != ',Znuclei,')\n'
        sys.exit()

    if atomicNum!=1:      
        data+='  "hijinginit targ A",\n'
    else:
        data+='  "hijinginit targ P",\n'
          
    beam=int(eventType[4])

    if not (beam in range(0,3)):
        print '\n ***ERROR:beam number not allowed (T can be only 0,1,2)\n'
        sys.exit()
            
    if beam==0:
        beam=beam+12
    data+= '  "hijinginit beam'+str(beam)+'",\n'

    massNum = Anuclei[Znuclei.index(atomicNum)]
    data+= '  "hijinginit iat '+str(massNum)+'",\n'
    data+= '  "hijinginit izt '+str(atomicNum)+'"\n'
    data+= '};\n'

    # set time of interaction, for event with both beam set it to zero
    if beam==12:
        beam=0
    elif beam==2:
        beam=-1

    data+= 'Generation.FlatZSmearVertex.BeamDirection = '+str(beam)+';\n'
    data+= 'Generation.UniformSmearVertex.BeamDirection = '+str(beam)+';\n'
    
    writeOptions(optionsdir,data)


#----------------------------------------------------------------------------
# Options for particle guns
#----------------------------------------------------------------------------
def genParticleGuns(eventType):

    data = ''

    # Momentum Keyword is mandatory
    momentumValues = OptionsValue(decdir,"Momentum")
    range = OptionsValue(decdir,"MomentumRange")
    if momentumValues != None:
        momentumValues = momentumValues.strip().split()
    else:
        print '\nError: There is not a correct value for the keyword Momentum in '+decdir+'\n'
        sys.exit()

    # Check in case of range that only two values are given
    if range != None:
        if len(momentumValues) != 2:
            print '\nError: MomentumRange wants only 2 values: min and max. You have given', len(momentumValues), '\n'
            sys.exit()
        if int(eventType[3]) not in (4,5,6,7):
           print 'ERROR: Momentum range requested but C =',eventType[3],' is not allowed\n'
    else:
        if int(eventType[3]) > 3:
            print 'ERROR: Momentum fix value requested but C =',eventType[3],' is not allowed\n'
            sys.exit()

    
    # Check if exists ExtraOptions keyword
    incl = OptionsValue(decdir,"ExtraOptions")
    if incl != None:
        if len(incl) == 1:
            print "WARNING: There is an ExtraOptions keyword with no value in "+decdir
	else:
            data += "#include \"$DECFILESROOT/options/"+string.strip(incl)+".opts\"\n"

    data += 'ParticleGun.ParticleGunTool = "MomentumRange";\n'

    ## determine absolute pID
    value = pgunPID(eventType)
    
    data += 'ParticleGun.NumberOfParticlesTool = "FlatNParticles";\n'
    data += 'ParticleGun.MomentumRange.PdgCodes = { %s };\n' % value
    data += 'ToolSvc.EvtGenDecay.UserDecayFile = "$DECFILESROOT/dkfiles/%s.dec";\n' % DecayName
    
    # Check if exists ParticleTable keyword
    arg = OptionsValue(decdir,"ParticleTable:")
    if arg != None:
        if len(string.strip(arg)) == 0:
            print "WARNING: The Keyword ParticleTable has no value\n"
        data += "ParticlePropertySvc.OtherFiles = { \"$DECFILESROOT/ppfiles/"+string.strip(arg)+".tbl\" };\n"

    # Check if exists ParticleValue keyword
    arg = OptionsValue(decdir,"ParticleValue")
    if arg != None:
        if len(string.strip(arg)) == 0:
            print "WARNING: The Keyword ParticleValue has no value\n"
        data += "ParticlePropertySvc.Particles = { "+string.strip(arg)+" };\n"

    # pGunType: acceptance, fix momentum or range, (flat eta, flat x-y,
    #                                               not implemented yet)
    acceptance, acc, gType = pGunType( int(eventType[3]) )
    data += acceptance

    # C = 0, 1, 2 or 3: fix list of momentum
    if gType == 1:
        for val in momentumValues:
            pGunMomentum(data, acc, val, val, eventType) 
    elif gType == 2:
        pGunMomentum(data, acc, momentumValues[0], momentumValues[1], eventType)
    else:
        print 'ERROR: Case C >=8 for ParticleGun not implemented yet'
        sys.exit()

#----------------------------------------------------------------------------
#  PID, helper for particlegun
#----------------------------------------------------------------------------
def pgunPID(eventType):

    ## determine absolute pID
    if eventType[1] == '1':
        value = '11'
    elif eventType[1] == '2':
        value = '13'
    elif eventType[1] == '3':
        value = '211'
    elif eventType[1] == '4':
        value = '321'
    elif eventType[1] == '5':
        value = '2212'
    elif eventType[1] == '6':
        value = '22'
    elif eventType[1] == '7':
        value = '111'
    elif eventType[1] == '9':
        value = '0'
    else:
        print 'ERROR: The EventType has S', eventType[1], 'not yet implemented'
        sys.exit()
    
    ## determine if particle or antiparticle or both
    if eventType[2] == '0':
        value = value
    elif eventType[2] == '1':
        value = '-'+value
    elif eventType[2] == '2':
        value = value+', -'+value
    else:
        print "ERROR: The EventType is not correct. D can only be 0, 1 or 2"
        print "The options file for "+DecayName+".dec file can't be generated"
        sys.exit()

    ## special case of "other particle"
    if eventType[1] == '9':
        if eventType[2] == '0':
            value = '443'
        else:
            print 'ERROR: GSD = ', eventType[0:3], 'not implemented yet\n'
            sys.exit()


    return value
    
#----------------------------------------------------------------------------
#  Decode C, i.e. acceptance, GunType( momemtum, eta...) helper for particlegun
#----------------------------------------------------------------------------
def pGunType(cValue):
    
    # C = 0, 2, 4, 6 means in CaloAcceptance, while
    # C = 1, 3, 5, 7 means in TrackersAcceptance
    acceptance = ''
    acc = 0
    if cValue in (0,2,4,6):
        acceptance = "#include \"$DECFILESROOT/options/CaloAcceptance.opts\"\n"
    elif cValue in (1,3,5,7):
        acc = 1
        acceptance = "#include \"$DECFILESROOT/options/TrackersAcceptance.opts\"\n"
    else:
        print '\n ***ERROR:Only value 0 to 7 implemted so far\n'
        sys.exit()

    # C = 0, 1, 2 or 3: fix list of momentum
    gType = 0
    if cValue in range(4):
        gType = 1
    elif cValue in range(4,8):
        gType = 2
    else:
        print 'ERROR: Case C >= 8 for ParticleGun not implemented yet'
        sys.exit()
        
    
    return acceptance, acc, gType

#----------------------------------------------------------------------------
#  helper for particlegun
#----------------------------------------------------------------------------
def pGunMomentum(data, acc, pMin, pMax, eventType):

    dataAux = data

    momentum = '%s' % pMin.split('*')[0]
    unit     = '%s' % pMin.split('*')[1]
    momentumRound = '%0.f' % float(momentum)
    dataAux += 'ParticleGun.MomentumRange.MomentumMin = %s;\n' % pMin

    momentum = '%s' % pMax.split('*')[0]
    unit     = '%s' % pMax.split('*')[1]
    momentumRound = '%0.f' % float(momentum)
    dataAux += 'ParticleGun.MomentumRange.MomentumMax = %s;\n' % pMax
    
    ua = 0
    if unit == 'GeV':
        ua = acc
    elif unit == 'MeV':
        ua = acc + 2
    else:
        print '\n ***ERROR:Units can only be MeV or GeV\n'
        sys.exit()
        
    iEventType = eventType[0:3]+str(ua)+eventType[4:8]
    iEventType = iEventType[0:8-len(momentumRound)]+momentumRound
    dataAux += 'ParticleGun.EventType = %s;\n' % (iEventType)
    OptionsNickAux = OptionsNick+' %s' % pMin
    if pMax != pMin:
        OptionsNickAux += ' - %s' % pMax
    
    OptionsNameAux = iEventType
    file = optionsdirroot + OptionsNameAux + '.opts'
    if os.path.exists(file):
        print "\n *****  The file "+file+" exists. CHECK it ****"
        print " ***** to overwrite it, you should remove it first\n"
    else:
        HeaderOptions(file,OptionsNameAux)
        writeOptions(file,dataAux)
        writeBkkTable(OptionsNameAux,AsciiName,OptionsNickAux,clean)
        writeSQLTable(OptionsNameAux,AsciiName,OptionsNickAux,clean)



#----------------------------------------------------------------------------
#  return the value of the correponding string
#----------------------------------------------------------------------------
def OptionsValue(filename,word):
    fd = open(filename)
    fdlines = fd.readlines()
    for fdline in fdlines:
        if fdline.find(word) != -1:
            # every keyword is at the beginning of the line
            if fdline.strip().split(word)[0].strip() == '#':
                return string.strip(string.split(fdline,":")[1])
 
#----------------------------------------------------------------------------
#  write the options file
#----------------------------------------------------------------------------
def writeOptions(filename,word):
    fd = open(filename,"a+")
    fd.write(word)
    fd.close()
 
#----------------------------------------------------------------------------
#  write the header of the options file
#----------------------------------------------------------------------------
def HeaderOptions(filename,optsName=''):
    if (optsName == ''):
        optsName = OptionsName
        
    fd = open(filename,"w")
    fd.write("// file  "+optsName+".opts generated: "+time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())+"\n")
    fd.write("//\n")
    fd.write("// Event Type:"+optsName+"\n")
    fd.write("//\n")
    fd.write("// ASCII decay Descriptor: "+AsciiName+"\n")
    fd.write("//\n")
    fd.close()
    
 
#----------------------------------------------------------------------------
# write the file to create the entry in the ORACLE database
#----------------------------------------------------------------------------
def writeBkkTable(evttypeid,descriptor,nickname,cleanvalue):
    TableName = os.environ["DECFILESROOT"]+"/doc/table_event.txt"
    if not os.path.exists(TableName):
        os.system("touch "+TableName)
        line = "EventTypeID | NickName | Description\n"
        writeOptions(TableName,line)
         
    insert_event = "true"
    for line in fileinput.input(TableName,inplace=1):
        print line[:-1]
        if line.find(evttypeid) != -1:
            insert_event = "false"


    nick = nickname[:min(len(nickname),255)]
    desc = descriptor[:min(len(descriptor),255)]
    if insert_event == "true":
        if cleanvalue == "true":
            line = evttypeid+" | "+nick+" | "+desc+" (clean)\n"
        else:
            line = evttypeid+" | "+nick+" | "+desc+"\n"
             
        writeOptions(TableName,line)
 
         
#----------------------------------------------------------------------------
# write the file to create the entry in the ORACLE database
#----------------------------------------------------------------------------
def writeSQLTable(evttypeid,descriptor,nickname,cleanvalue):
    TableName = os.environ["DECFILESROOT"]+"/doc/table_event.sql"
    if not os.path.exists(TableName):
        os.system("touch "+TableName)
         
    insert_event = "true"
    for line in fileinput.input(TableName,inplace=1):
        print line[:-1]
        if line.find(evttypeid) != -1:
            insert_event = "false"
            
    # the ORACLE table does not accept names > 256 characters
    # single quote is used in nickname and descriptor so it cannot be used in 'line'
    # use double quotes instead
    nick = nickname[:min(len(nickname),255)]
    desc = descriptor[:min(len(descriptor),255)]
    if insert_event == "true":
        if cleanvalue == "true":
            line = 'EVTTYPEID = '+evttypeid+', DESCRIPTION = "'+nick+'", PRIMARY = "'+desc+'"\n'
#            line = 'svc.addEvtType('+evttypeid+',"'+nick+'","'+desc+'","clean")\n'
        else:
#            line = 'svc.addEvtType('+evttypeid+',"'+nick+'","'+desc+'","")\n'
            line = 'EVTTYPEID = '+evttypeid+', DESCRIPTION = "'+nick+'", PRIMARY = "'+desc+'"\n'
                         
        writeOptions(TableName,line)


#############################################################################
# create an options file corresponding to a single Decay file
#############################################################################
def run_create(clean):
    global optionsdir,OptionsName,AsciiName, decdir, OptionsNick
 
    if clean == "true":
        title = DecayName+" clean"
    else:
        title = DecayName
         
    print "Creation of options file for Decay ",title
     
#  Build the name of the dkfiles
    decdir = os.environ["DECFILESROOT"]+"/dkfiles/"+DecayName+".dec"
 
# check if the Decay files exists
    if not os.path.exists(decdir):
        print "The file "+decdir+" does not exist"
        sys.exit()
             
# Get the equivalent eventtype
# convention add +5 to the last for a clean event..
    OptionsName = OptionsValue(decdir,"EventType")
 
# Check if the Nickname is the correct
    OptionsNick = OptionsValue(decdir,"NickName")
    if OptionsNick != DecayName:
        print "WARNING: The nickname "+OptionsNick+" is not equal to the "+DecayName+".dec"
 
# Check if the Descriptor is correct
    AsciiName = OptionsValue(decdir,"Descriptor")
    if AsciiName is None:
        print "ERROR: The Descriptor is not correct.\nIt must have some value"
        print "The options file for "+DecayName+".dec file can't be generated"
        sys.exit()
 
# Check if EventType is 5xxxxxxxx --> particle guns
    if OptionsName[0] == '5':
        genParticleGuns(OptionsName)
        sys.exit()

# Check if EventType is special source --> MIB (6xx5xxxx)
    if (OptionsName[0] == '6' and OptionsName[3] == '5'):
        beamHalo(OptionsName)
        sys.exit()
    
# Check if EventType is special source --> LSS and arc beam-gas MIB (6xx4xxxx)
    if (OptionsName[0] == '6' and OptionsName[3] == '4'):
        beamHalo(OptionsName)
        sys.exit()
                    

#check if the options file already exist and do not overwrite it
    if clean == 'true':
        optionsdir = optionsdirroot+OptionsName[0:7]+"5.opts"
    else:
        optionsdir = optionsdirroot+OptionsName+".opts"
    if os.path.exists(optionsdir):
        print " *****  The file "+optionsdir+" exists. CHECK it ****"
        print " ***** to overwrite it, you should remove it first\n"
        
        writeBkkTable(OptionsName,AsciiName,OptionsNick,clean)
        writeSQLTable(OptionsName,AsciiName,OptionsNick,clean)
        sys.exit()
 
# EventType must have 8 digits ( GSDCTNXU, G<>0 )
# Check if the EventType is correct
    if OptionsName is None:
        print "ERROR: The EventType is not correct.\nIt must have some value"
        print "The options file for "+DecayName+".dec file can't be generated"
        sys.exit()
    # The EventType mustn't start by zero
    if OptionsName[0] == '0':
        print "ERROR: The EventType is not correct.\nIt mustn't start by 0"
        print "The options file for "+DecayName+".dec file can't be generated"
        sys.exit()
    # The EventType must have at least 8 digits
    if len(OptionsName) < 8:
        print "ERROR: The EventType is not correct.\nIt must have at least 8 digits"
        print "The options file for "+DecayName+".dec file can't be generated"
        sys.exit()
 
    # Check Type
    if OptionsName[0:2] == '30':
        sample = "MinimumBias"
    elif int(OptionsName[0]) in (1, 2, 3, 7):
        if int(OptionsName[1]) in (0, 9):
            # Inclusive
            sample = "Inclusive"
        elif OptionsName[0:2] == '31' :  ## signal tau production
            # SignalPlain
            sample = "SignalPlain"
        elif OptionsName[0:2] == '32': ## Sigma+ production
            # SignalPlain
            sample = "SignalPlain"
        elif OptionsName[0:2] == '33': ## Lambda production
            sample = "SignalPlain"
        elif int(OptionsName[0]) == 1 and int(OptionsName[1]) in (1, 2, 3, 5, 6):
            # SignalRepeatedHadronization
            sample = "SignalRepeatedHadronization"
        elif int(OptionsName[0]) == 2 and int(OptionsName[1]) == 8 and int(OptionsName[6]) == 1:
            sample = "Special"
        elif int(OptionsName[0]) in (2, 7) and int(OptionsName[1]) in (1, 2, 3, 4, 5, 7, 8):
            # SignalPlain
            sample = "SignalPlain"
	elif int(OptionsName[0]) == 1 and int(OptionsName[1]) == 8:
	    # bb resonance: use Special
	    sample = "Special"
        elif int(OptionsName[0]) == 1 and int(OptionsName[1]) == 4:
            # SignalForcedFragmentation
            sample = "SignalForcedFragmentation"
            # Check production
            BcProductionValue = OptionsValue(decdir,"Production")
            if BcProductionValue == "BcVegPy":
                sample = "Special"
        else:
            sample = "otherTreatment"
    elif int(OptionsName[0]) == 4 and int(OptionsName[1]) in range(7):
        sample = "Special"
    elif OptionsName[0] == '6':
        sample = "MinimumBias"
    else:
        sample = "otherTreatment"

    # Check Clean Event
    if clean == "true":
        if sample in ('SignalRepeatedHadronization', 'SignalPlain', 'SignalForcedFragmentation'):
            OptionsName = OptionsName[:-1]+'5'
        else:
            clean = 'false'
            print "ERROR: You are trying to do Clean with a wrong file type.\nThe file must be from a Signal type.\n"
            sys.exit()
 


# Check if Production keyword is correct
    ProductionValue = OptionsValue(decdir,"Production")
    if ProductionValue is None:
        ProductionValue = "Pythia"
    else:
        print "Production: Using %s for %s.dec file" % ( ProductionValue, DecayName )
 
    length = len(ProductionValue.strip().split(' ')) 
    if length > 1:
        engines = []
        for n in range(length):
            engines.append(ProductionValue.strip().split(' ')[n])
        ProductionValue = "Pythia"     
    
# get the first digit of the eventtype
    AB = OptionsName[0:2]
    ABX = OptionsName[0:2]+OptionsName[6]
    ABU = OptionsName[0:2]+OptionsName[7]
 
    HeaderOptions(optionsdir)
    # Polarized Lambda_b
    if ABU == "153" or ABU == "159":
        str = "ToolSvc.EvtGenDecay.PolarizedLambdad = true ;\n"
        writeOptions(optionsdir,str)
 
# Optional lines for all event types --------------------------------- 
# Check if exists ExtraOptions keyword
    incl = OptionsValue(decdir,"ExtraOptions")
    if incl != None:
        if len(incl) == 1:
            print "WARNING: There is an ExtraOptions keyword with no value in "+decdir
	else:
            str = "#include \"$DECFILESROOT/options/"+string.strip(incl)+".opts\"\n"
            writeOptions(optionsdir,str)
 
    # temporary patch for dimuon and dielectron
    if (DecayName.find("incl_b=DiMuon") != -1) or (DecayName.find("incl_b=DiElectron") != -1):
        sample = "RepeatDecay"


# Mandatory lines to write -------------------------------------------
    line = "Generation.EventType = "+OptionsName+";\n"
    writeOptions(optionsdir,line)

    str = "Generation.SampleGenerationTool = \""+string.strip(sample)+"\";\n"
    writeOptions(optionsdir,str)

    # temporary patch for dimuon
    if string.strip(sample) == "RepeatDecay":
        sample = "RepeatDecay.Inclusive"

    #ProductionValue
    str = "Generation."+string.strip(sample)+".ProductionTool = \""+string.strip(ProductionValue)+"Production\";\n"
    writeOptions(optionsdir,str)

    str = "ToolSvc.EvtGenDecay.UserDecayFile = \"$DECFILESROOT/dkfiles/"+DecayName+".dec\";\n"
    writeOptions(optionsdir,str)
 
# Lines for specific event types: Beam gas in LHCb (G=6, C=0,1) ------
    if (OptionsName[0] == '6' and (OptionsName[3] =='0' or OptionsName[3] =='1')):
        beamGasLHCb(OptionsName)
    

# Optional lines depending of existing keywords ----------------------
 
# Check if exists DecayEngine keyword
    DecayEngineValue = OptionsValue(decdir,"DecayEngine")
    if DecayEngineValue != None:
        if len(string.strip(DecayEngineValue)) == 0:
            print "WARNING: The Decay Keyword in "+decdir+" has no value\n"
        str = "Generation.DecayTool = \""+string.strip(DecayEngineValue)+"Decay\";\nGeneration."+string.strip(sample)+".DecayTool = \""+string.strip(DecayEngineValue)+"Decay\";\n"
        writeOptions(optionsdir,str)
 
# Check if exists cuts keyword
    CutsValue = OptionsValue(decdir,"Cuts")
    if CutsValue != None:
        if len(string.strip(CutsValue)) == 0:
            print "INFO: The Cuts Keyword in "+decdir+" has no value\n"
        str = "Generation."+string.strip(sample)+".CutTool = \""+string.strip(CutsValue)+"\";\n"
        writeOptions(optionsdir,str)

# Check if exists cuts option keyword
    CutsOptionsValue = OptionsValue(decdir,"CutsOptions")
    if CutsOptionsValue != None:
        if len(string.strip(CutsOptionsValue)) == 0:
            print "WARNING: The Cuts Options Keyword in "+decdir+" has no value\n"
        for i in range( len(string.strip(CutsOptionsValue).split())/2 ):
           str ="Generation."+string.strip(sample)+"."+string.strip(CutsValue)+"."+string.strip(CutsOptionsValue).split()[2*i]+"="+string.strip(CutsOptionsValue).split()[2*i+1]+";\n"
           writeOptions(optionsdir,str)
 
# Check if exists FullEventCuts keyword
    FullEventCutsValue = OptionsValue(decdir,"FullEventCuts")
    if FullEventCutsValue != None:
        if len(string.strip(FullEventCutsValue)) == 0:
            print "WARNING: The FullEventCuts Keyword in "+decdir+" has no value\n"
        str = "Generation.FullGenEventCutTool = \""+string.strip(FullEventCutsValue)+"\";\n"
        writeOptions(optionsdir,str)
 
# Generation.SAMPLE.GENERATOR.InclusivePIDList
# if Inclusive
    if (sample == 'Inclusive') or (sample == 'RepeatDecay.Inclusive'):
        if OptionsName[0] == '1':
                list = '521, -521, 511, -511, 531, -531, 541, -541, 5122, -5122, 5222, -5222, 5212, -5212, 5112, -5112, 5312, -5312, 5322, -5322, 5332, -5332, 5132, -5132, 5232, -5232'
        elif int(OptionsName[0]) in (2, 7):
                list = '421, -421, 411, -411, 431, -431, 4122, -4122, 443, 4112, -4112, 4212, -4212, 4222, -4222, 4312, -4312, 4322, -4322, 4332, -4332, 4132, -4132, 4232, -4232, 100443, 441, 10441, 20443, 445, 4214, -4214, 4224, -4224, 4314, -4314, 4324, -4324, 4334, -4334, 4412, -4412, 4414,-4414, 4422, -4422, 4424, -4424, 4432, -4432, 4434, -4434, 4444, -4444, 14122, -14122,  14124, -14124, 100441'
        str = "Generation."+string.strip(sample)+".InclusivePIDList = {"+list+"};\n"
        writeOptions(optionsdir,str)
# if Type Signal
    else:
        listing = { '10':'521, -521, 511, -511, 531, -531, 541, -541, 5122, -5122, 5222, -5222, 5212, -5212, 5112, -5112, 5312, -5312, 5322, -5322, 5332, -5332, 5132, -5132, 5232, -5232'
                    , '11':'511,-511'
                    , '12':'521,-521'
                    , '13':'531,-531'
                    , '14':'541,-541'
                    , '15':'5122,-5122'
                    , '19':'521, -521, 511, -511, 531, -531, 541, -541, 5122, -5122, 5332, -5332, 5132, -5132, 5232, -5232'
                    , '20':'421, -421, 411, -411, 431, -431, 4122, -4122, 443, 4112, -4112, 4212, -4212, 4222, -4222, 4312, -4312, 4322, -4322, 4332, -4332, 4132, -4132, 4232, -4232, 100443, 441, 10441, 20443, 445, 4214, -4214, 4224, -4224, 4314, -4314, 4324, -4324, 4334, -4334, 4412, -4412, 4414,-4414, 4422, -4422, 4424, -4424, 4432, -4432, 4434, -4434, 4444, -4444, 14122, -14122,  14124, -14124, 100441'
                    , '21':'411,-411'   
                    , '22':'421,-421'   
                    , '23':'431,-431'   
                    , '24':'443'        
                    , '25':'4122,-4122' 
                    # tau 
                    , '31':'15,-15'
                    # Sigma
                    , '32':'3222,-3222'
                    # Lambda
                    , '33':'3122,-3122'
                    , '70':'421, -421, 411, -411, 431, -431, 4122, -4122, 443, 4112, -4112, 4212, -4212, 4222, -4222, 4312, -4312, 4322, -4322, 4332, -4332, 4132, -4132, 4232, -4232, 100443, 441, 10441, 20443, 445, 4214, -4214, 4224, -4224, 4314, -4314, 4324, -4324, 4334, -4334, 4412, -4412, 4414,-4414, 4422, -4422, 4424, -4424, 4432, -4432, 4434, -4434, 4444, -4444, 14122, -14122,  14124, -14124, 100441'
                    , '71':'411,-411'   
                    , '72':'421,-421'   
                    , '73':'431,-431'   
                    , '74':'443'        
                    , '75':'4122,-4122' 
                   }
        listingExcited = { '270':   '413,-413'
                           , '271': '423,-423'
                           , '272': '433,-433'
                           , '770': '413,-413'
                           , '771': '423,-423'
                           , '772': '433,-433'
                           , '280': '100443'
                           , '281': '9920443'
                           , '282': '10443'
                           , '283': '10441'
                           , '284': '20443'
                           , '285': '445'
                           , '180': '553'
                           , '181': '100553'
                           , '182': '200553'
                           , '183': '300553'
                           , '184': '9000553'
                           , '160': '5112,-5112'
                           , '161': '5212,-5212'
                           , '162': '5222,-5222'
                           , '163': '5132,-5132'
                           , '164': '5232,-5232'
                           , '165': '5332,-5332'}
        if listing.has_key(AB):
            if string.strip(sample) != "Special":
                str = "Generation."+string.strip(sample)+".SignalPIDList = {"+listing[AB]+"};\n"
                writeOptions(optionsdir,str)
        elif listingExcited.has_key(ABX):
            if AB=='18':
                if '' != string.strip(CutsValue):
                    str = "Generation."+string.strip(sample)+"."+string.strip(CutsValue)+".SignalPID = "+listingExcited[ABX]+";\n"
            elif ABX=='281':
                if '' != string.strip(CutsValue):
                    str = "Generation."+string.strip(sample)+"."+string.strip(CutsValue)+".SignalPID = "+listingExcited[ABX]+";\n"
            else:
                str = "Generation."+string.strip(sample)+".SignalPIDList = {"+listingExcited[ABX]+"};\n"
            writeOptions(optionsdir,str)
            
         
# write Clean lines   
    if clean == "true":
        str = "Generation."+sample+".Clean = true;\n"
        str = str + "GeneratorToG4.HepMCEventLocation = \"/Event/Gen/SignalDecayTree\";\n"
        writeOptions(optionsdir,str)

# Check if exists ParticleTable keyword
    arg = OptionsValue(decdir,"ParticleTable")
    if arg != None:
        if len(string.strip(arg)) == 0:
            print "WARNING: The Keyword ParticleTable has no value\n"
        str = "ParticlePropertySvc.OtherFiles = {\"$DECFILESROOT/ppfiles/"+string.strip(arg)+".tbl\"};\n"
        writeOptions(optionsdir,str)

# Check if exists ParticleValue keyword
    arg = OptionsValue(decdir,"ParticleValue")
    if arg != None:
        if len(string.strip(arg)) == 0:
            print "WARNING: The Keyword ParticleValue has no value\n"
        str = "ParticlePropertySvc.Particles = { "+string.strip(arg)+" };\n"
        writeOptions(optionsdir,str)

# Check if exist Model keyword (only applicable for G=4, S=5,6)

    arg = susyOptions(OptionsName)

    writeBkkTable(OptionsName,AsciiName,OptionsNick,clean)
    writeSQLTable(OptionsName,AsciiName,OptionsNick,clean)

#

#----------------------------------------------------------------------------
#  loop in the DKFILES directory to generate the options file
#----------------------------------------------------------------------------
def run_loop():
    files = os.listdir(os.environ["DECFILESROOT"]+"/dkfiles/")
    for f in files:
        res = re.search('.dec',f)
        if res is not None:
            if len(f.split('.dec')[1]) == 0:  
                basefile = f.split('.dec')[0]
                commandline = command+" "+basefile
                os.system(commandline)
 
#############################################################################
#  create the options file
#
#
#----------------------------------------------------------------------------
# give the usage of the command
#----------------------------------------------------------------------------
def usage():
    print "This command should be used with the name of the decay file\n"
    print "create_options.py DECAY_NAME\n\n"
    return 0
 
#############################################################################
#  Main
#############################################################################
 
# test number of argument
#
global optionsdirroot

loop = "false"
clean = "false"
command = sys.argv[0]
# It is defined because it may be change in the future
optionsdirroot = os.environ["DECFILESROOT"]+"/options/"
 
if len(sys.argv) > 3:
    usage()
    sys.exit()
else:
    if len(sys.argv) == 1:
        loop = "true"
    elif len(sys.argv) == 2:
        DecayName = sys.argv[1]
    elif len(sys.argv) == 3:
        DecayName = sys.argv[1]
        if sys.argv[2].lower() == "clean":
            clean = "true"
        else:
            print "Option "+sys.argv[2]+" unknown\n"
            sys.exit(2)
    else:
        usage()
        sys.exit()
         
if loop == "true":
    run_loop()
    sys.exit(0)
else:
    run_create(clean)


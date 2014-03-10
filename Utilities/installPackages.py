#!/usr/bin/python
import sys, os, pwd, commands
import optparse, shlex


def parseOptions():
    
    usage = ('usage: %prog [options] datasetList\n'
             + '%prog -h for help')
    parser = optparse.OptionParser(usage)
    
    parser.add_option('-v', '--version',   dest='version', type='string', default="44X", help='CMSSW release version')
    parser.add_option('-f', '--file',   dest='file', type='string', default="packages_src.txt", help='package source list file')

    # store options and arguments as global variables
    global opt, args
    (opt, args) = parser.parse_args()

    if (opt.version != '53X' and opt.version != '52X' and opt.version != '44X'):
        print opt.version, " is not a possible version, please choose 53X, 52X, or 44X"
        sys.exit()

    if not os.path.exists(opt.file):
        print opt.file, " not found!"
        sys.exit()


def processCmd(cmd):
    print cmd
    status, output = commands.getstatusoutput(cmd)
    if status !=0:
        print 'Error in processing command:\n   ['+cmd+'] \nExiting...'
    return status
        
    
def installPackages():
    global opt

    parseOptions()
    
    for line in open(opt.file,'r'):
        f = line.split()
        if len(f) < 1: continue
        if f[0].startswith("#"): continue

        if len(f) == 2:
            cmd = 'cvs co -r '+f[0]+' '+f[1]
        if len(f) == 3:
            #cmd = 'cvs co -r '+f[0]+' -d '+f[2]+' '+f[1]
            if os.path.isdir(f[2]):
                print f[2],"already exists..."
                continue
            cmd = 'cvs co -r '+f[0]+' '+f[1]
            status = processCmd(cmd)
            cmd = 'mkdir -p '+f[2]
            status = processCmd(cmd)
            cmd = 'mv '+f[1]+'/* '+f[2]
            status = processCmd(cmd)
            cmd = 'rm -r UserCode'

        status = processCmd(cmd)
        if (status != 0):
            print "Trying again..."
            status = processCmd(cmd)
            if (status !=0):
                print "Sorry, something is still wrong, exiting..."
                sys.exit()
            
        

    cmd = 'cvs update -r1.6 PhysicsTools/PatAlgos/plugins/PATPFParticleProducer.cc'
    processCmd(cmd)
    cmd = 'cvs update -r1.8 PhysicsTools/PatAlgos/plugins/PATPFParticleProducer.h'
    processCmd(cmd)
    cmd = 'cvs update -r1.6 PhysicsTools/PatAlgos/plugins/PATCleaner.cc'
    processCmd(cmd)
        
    cmd = 'cvs update -r 1.6 HiggsAnalysis/CombinedLimit/src/HZZ2L2QRooPdfs.cc'
    processCmd(cmd)
    cmd = 'cvs update -r 1.11 HiggsAnalysis/CombinedLimit/src/HZZ4LRooPdfs.cc'
    processCmd(cmd)
    cmd = 'cvs update -r 1.5 HiggsAnalysis/CombinedLimit/interface/HZZ2L2QRooPdfs.h'
    processCmd(cmd)
    cmd = 'cvs update -r 1.10 HiggsAnalysis/CombinedLimit/interface/HZZ4LRooPdfs.h'  
    processCmd(cmd)

    cmd = 'wget www.cern.ch/amapane/H4l/CMSSW/444/HiggsAnalysis/LinkDef.h; mv LinkDef.h HiggsAnalysis/CombinedLimit/src'
    processCmd(cmd)
    
    
    sys.exit()


if __name__ == "__main__":
    installPackages()
        
        




"""
----------------------------
   NAME
----------------------------
 visualinspection.py
----------------------------
   PURPOSE/DESCRIPTION
----------------------------
 GUIs for visual inspection of data products from the Grism Lens-Amplified Survey
 from Space (GLASS) data releases and ancillary data.

 visualinspection.py includes:
    GiG    GLASS inspection GUI                        Details in Treu et al. (2015)
    GiGz   GLASS inspection GUI for redshifts          Details in Treu et al. (2015)
    GiGm   GLASS inspection GUI for morphologies       Details in Vulcani et al. (2016)

 Furthermore, a README with details on all three GiGs is available at
 https://github.com/kasperschmidt/GLASSinspectionGUIs/blob/master/README.pdf
----------------------------
   COMMENTS
----------------------------
 To run the GUIs it is assumed that the following python packages are
 available (most of which should come with the default python install):
     Tkinter, os, sys, glob, datetime, time, numpy, subprocess, pyfits, commands
     re, scipy, matplotlib, PIL

 Also a command line version of ds9 should be available, i.e., the following
 command should open the fitsimage.fits without errors:
     ds9 -geometry 1200x600 -scale zscale fitsimage.fits
----------------------------
   EXAMPLES/USAGE
----------------------------
 First download GLASS data from the GLASS webpage at STScI's MAST server:
 https://archive.stsci.edu/prepds/glass/ and put it in for instance 'data/clusterXXXX/'.
 Then execute the following in python (from the directory containing visualinspection.py
 or add visualinspection.py to your path):

 --- Launch GiG ---
 import visualinspection as vi
 vi.launchgui(directory='data/clusterXXXX/',outputfile='testfile_output_GiG.txt',MASTfiles=True)

 --- Launch GiGz ---
 import visualinspection as vi
 vi.launchgui_z(directory='data/clusterXXXX/',outputfile='testfile_output_GiGz.txt',MASTfiles=True)

 --- Launch GiGm ---
 import visualinspection as vi
 vi.launchgui_m(pstampsdirectory='data/postagestamps/',infofile='./infofile.txt',outputfile='testfile_output_GiGm.txt')

 Note the different directory used for GiGm. This contains postage stamp data. See GiG README at
 for details
"""
#-------------------------------------------------------------------------------------------------------------
__author__      = "K. B. Schmidt (AIP)"
__maintainer__  = "K. B. Schmidt (AIP)"
__email__       = "kbschmidt@aip.de"
__contact__     = "kbschmidt@aip.de"
__version__     = "3.0"
__date__        = "August 1, 2016"
__license__     = "The MIT License (MIT)"
__copyright__   = "Copyright (c) 2014-2016 Kasper B. Schmidt and the GLASS collaboration"
__credits__     = ["The GLASS Collaboration http://glass.astro.ucla.edu"]
__status__      = "Production"
#-------------------------------------------------------------------------------------------------------------
from Tkinter import *
import os
import sys
import glob
import datetime
import time
import numpy as np
import pdb
import subprocess
import pyfits
import re
import scipy.ndimage
import commands
import matplotlib.pyplot as plt
import visualinspection as vi
from PIL import ImageTk, Image
#-------------------------------------------------------------------------------------------------------------
def launchgui(directory='/Users/kasperborelloschmidt/work/GLASS/MACS0717test/vanzellaOBJ/',
              objlist=None,verbose=True,outputfile='DEFAULT',inspectorname='John Doe',
              clobber=False,ds9xpa=False,openfitsauto=False,inGUIimage='zfit',check4duplicates=False,
              outputcheck=False,skipempty=False,MASTfiles=False):
    """
    Launch the inspection GUI for the object inspections Application()
    """
    dir = directory
    if outputfile == 'DEFAULT':
        outfile = dir+'visualinspection_defaultoutput.txt'
    else:
        outfile = dir+outputfile
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # setup and launch GUI
    root = Tk()
    root.title("GLASS Inspection GUI (GiG)")
    root.geometry("1000x700") # size of GUI window
    app = Application(dir,outfile,master=root,objlist=objlist,verbose=verbose,iname=inspectorname,
                      clobber=clobber,ds9xpa=ds9xpa,openfitsauto=openfitsauto,inGUIimage=inGUIimage,
                      check4duplicates=check4duplicates,outputcheck=outputcheck,skipempty=skipempty,
                      MASTfiles=MASTfiles)
    app.mainloop()
    root.destroy()

#-------------------------------------------------------------------------------------------------------------
def launchgui_z(directory='IndvidualObjects/',GiGfile=None,GiGselection='emissionlineobjects',
                objlist=None,outputfile='DEFAULT',inspectorname='John Doe',clobber=False,
                ds9xpa=False,openfitsauto=False,check4duplicates=False,skipempty=False,inGUIimage='zfit',
                outputcheck=False,latexplotlabel=False,autosaveplot=False,verbose=True,MASTfiles=False):
    """
    Launch the inspection GUI for the redshift inspections Application_z()
    """
    dir = directory
    if outputfile == 'DEFAULT':
        outfile = dir+'visualinspection_z_defaultoutput.txt'
    else:
        outfile = dir+outputfile
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # setup and launch GUI
    root = Tk()
    root.title("GLASS Inspection GUI for redshift fit (GiGz)")
    root.geometry("1000x630") # size of GUI window
    app = Application_z(dir,outfile,master=root,GiGfile=GiGfile,GiGselection=GiGselection,
                        objlist=objlist,verbose=verbose,iname=inspectorname,clobber=clobber,ds9xpa=ds9xpa,
                        openfitsauto=openfitsauto,check4duplicates=check4duplicates,outputcheck=outputcheck,
                        latexplotlabel=latexplotlabel,autosaveplot=autosaveplot,skipempty=skipempty,
                        MASTfiles=MASTfiles,inGUIimage=inGUIimage)
    app.mainloop()
    root.destroy()
#-------------------------------------------------------------------------------------------------------------
def launchgui_m(pstampsdirectory='PostageStamps/',objlist=None,clusters=None,infofile=None,
                outputfile='DEFAULT',inspectorname='John Doe',clobber=False,
                ds9xpa=False,openfitsauto=False,skipempty=False,
                outputcheck=False,openpngseperately=False,verbose=True):
    """
    Launch the inspection GUI for the morphology inspections Application_m()
    """
    pdir = pstampsdirectory
    if outputfile == 'DEFAULT':
        outfile = pdir+'visualinspection_m_defaultoutput.txt'
    else:
        outfile = pdir+outputfile
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # setup and launch GUI
    root = Tk()
    root.title("GLASS Inspection GUI for morphology (GiGm)")
    root.geometry("930x530") # size of GUI window
    app = Application_m(pdir,outfile,master=root,infofile=infofile,objlist=objlist,clusters=clusters,
                        verbose=verbose,iname=inspectorname,
                        clobber=clobber,ds9xpa=ds9xpa,openfitsauto=openfitsauto,
                        outputcheck=outputcheck,skipempty=skipempty,openpngseperately=openpngseperately)
    app.mainloop()
    root.destroy()
#-------------------------------------------------------------------------------------------------------------
def getPID(searchstring,verbose=False):
    """
    Return PID of most recent process including the given search string
    Will ignore instances containing 'grep' and with a CPU time stamp of 0 seconds
    """
    cmd = "ps -eo pid,etime,command | grep "+searchstring
    fileobj = os.popen(cmd)            # return file object for ps command
    lines   = fileobj.readlines()      # read ouptu from ps command
    Nproces = len(lines)               # number of prcesses including searchstring

    PIDlist  = []
    time     = []
    for line in lines:
        if 'grep' not in line: # ignore the grep command PID
            ls       = line.split() # etime is [[dd-]hh:]mm:ss
            tsplit   = ls[1].split(':')
            if len(tsplit) == 2:    # if process has been running for minutes & seconds
                timeval = float(tsplit[0])*60. + float(tsplit[1])
            else:
                if '-' in tsplit[0]: # if process has been running for days
                    dayhour = tsplit[0].split('-')
                    timeval = float(dayhour[0])*24*60.*60 + \
                              float(dayhour[1])*60*60     + \
                              float(tsplit[1])*60. + float(tsplit[2])
                else:                # if process has been running for hours
                    timeval = float(tsplit[0])*60.*60     +\
                              float(tsplit[1])*60. + float(tsplit[2])

            if timeval > 0: # ignore 0.00 s instances
                if verbose: print 'Process:',line
                PIDlist.append(int(ls[0]))
                time.append(timeval)
            else:
                if verbose: print ' - Ignoring the following as it has a time stamp of 0s:'
                if verbose: print '   ',line
    if len(PIDlist) == 0:
        if verbose: print ' - No processes with given search string ('+searchstring+') in them. Returning None'
        return None

    if verbose: print 'PIDlist:',PIDlist
    if verbose: print 'time   :',time

    PID = np.array(PIDlist)[time == np.min(time)]
    if len(PID) > 1:
        print ' - Note multiple IDs with the same time stamp were found: ',PID
        print '   Returning the first PID'

    return PID[0]
#-------------------------------------------------------------------------------------------------------------
def getclusterz(filestring):
    """
    Return the redshift of the cluster the object belongs to
    based on the filename.
    """
    if ('A2744' in filestring) or ('a2744' in filestring):
        redshift = 0.308
        cluster  = 'A2744'
    elif ('A370' in filestring) or ('a370' in filestring):
        redshift = 0.375
        cluster  = 'A370'
    elif ('MACS0416.1-2403' in filestring) or ('macs0416' in filestring):
        redshift = 0.396
        cluster  = 'MACS0416.1-2403'
    elif ('MACS0717.5+3745' in filestring) or ('macs0717' in filestring):
        redshift = 0.548
        cluster  = 'MACS0717.5+3745'
    elif ('MACS0744.9+3927' in filestring) or ('macs0744' in filestring):
        redshift = 0.686
        cluster  = 'MACS0744.9+3927'
    elif ('MACS1149.6+2223' in filestring) or ('macs1149' in filestring):
        redshift = 0.544
        cluster  = 'MACS1149.6+2223'
    elif ('MACS1423.8+2404' in filestring) or ('macs1423' in filestring):
        redshift = 0.545
        cluster  = 'MACS1423.8+2404'
    elif ('MACS2129.4-0741' in filestring) or ('macs2129' in filestring):
        redshift = 0.570
        cluster  = 'MACS2129.4-0741'
    elif ('RXJ2248' in filestring) or ('rxj2248' in filestring): # RXJ2248-4431
        redshift = 0.348
        cluster  = 'RXJ2248'
    elif ('RXJ1347.5-1145' in filestring) or ('rxj1347' in filestring):
        redshift = 0.451
        cluster  = 'RXJ1347.5-1145'
    else:
        print " - Did't find any redshift for cluster ("+filestring+"); returning 0.0 "
        redshift = 0.0
        cluster  = 'None'

    return cluster, redshift
#-------------------------------------------------------------------------------------------------------------
def get_objinfo(infofile,objid,cluster):
    """
    Return information on object given an input file
    """
    if infofile == None:
        returndat = None
    else:
        infodat = np.genfromtxt(infofile,dtype=None,names=True,skip_header=0,comments='#')
        objent  = np.where((infodat['id'] == int(objid)) & (infodat['cluster'] == cluster))[0]

        if len(objent) == 0:
            returndat = None
        else:
            returndat = infodat[objent]

    return returndat
#-------------------------------------------------------------------------------------------------------------
def check_idlist(idlist,dir,verbose=True):
    """
    Checking if pngs exist for objects in idlist.
    Returning list of ids with existing files
    """
    if verbose: print ' - Checking ID list to make sure data for objects exists'
    goodids = np.array([])
    for objid in idlist:
        idstr = str("%.5d" % objid)
        pngs  = glob.glob(dir+'*_'+idstr+'*2D.png')
        if len(pngs) > 0:
            goodids = np.append(goodids,objid)

    if (len(goodids) == 0):
        if verbose: print ' - WARNING None of the IDs have data in dir=\n   '+dir

    return goodids
#-------------------------------------------------------------------------------------------------------------
class Application(Frame):
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def __init__(self,dir,outfile,master=None,objlist=None,verbose=True,iname='John Doe',
                 ACSinspection=False,clobber=False,ds9xpa=False,openfitsauto=False,
                 inGUIimage='zfit',check4duplicates=False,outputcheck=False,skipempty=False,
                 MASTfiles=False):
        """
        Intitialize the GUI

        -- INPUT --
        dir               Direcotory containing the data of the objects to inspect.
        outfile           Name of output file to create if it doesn't exists. Use clobber to overwrite.
        master            Provide another 'master' display. If None GUI created from scratch.
        objlist           List of objects to inspect. If 'None' all objects in 'dir' will be
                          inspected.
        verbose           Toggle verbosity.
        iname             Name of inspector to write in output file.
        ACSinspection     If inspecting ACS objects (not enabled as of 160727).
        clobber           Overwrites the output file if it already exists
        ds9xpa            If xpa is availbale for comunicating commands to ds9
                          set this keyword to tru and this will be used instead
                          of opening ds9 everytime the fits files are requested.
        openfitsauto      Automatically load the fits files into the DS9 window
                          when advancing to next (or previous) object.
        inGUIimage        Select what image to display in GUI window (if available)
                          Choices are:
                          'zfit'       The redshift fit output plot (default)
                          'G102stack'  The stacked G102 2D spectra
                          'G141stack'  The stacked G102 2D spectra
        check4duplicates  Loop through output file whenever an object is save to check for
                          and remove duplicate entries
        outputcheck       Checking the written output to see if it contains the expected number
                          of objects etc.
        skipempty         Set to True to ignore unedited objects when writing to output file.
                          Hence, if skipempty = True objects with no comments, flags set or sliders changed
                          will be written to the output
        """
        pp    = subprocess.Popen('ds9 -version',shell=True,executable=os.environ["SHELL"],stdout=subprocess.PIPE)
        ppout = pp.communicate()[0]
        self.ds9version = ppout.split()

        self.now        = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.vb         = verbose
        self.dir        = dir
        self.ds9open    = False # set ds9 indicator (used for ds9xpa = False)
        self.ds9windowopen = False # set ds9 indicator (used for ds9xpa = True)
        self.ACSins     = ACSinspection
        self.quitting   = False
        self.xpa        = ds9xpa # check if user indacetd that xpa was available for ds9
        self.inGUIimage = inGUIimage
        self.duplicates = check4duplicates
        self.fitsauto   = openfitsauto # Open fits files automatically?
        self.outcheck   = outputcheck
        self.skipempty  = skipempty
        self.MASTfiles  = MASTfiles
        if self.xpa:
            #sys.exit(' - XPA DS9 controls not enabled yet; still under construction (use ds9xpa=False)')
            self.ds9windowopen = False

        if os.path.exists(self.dir):
            self.twodfits = glob.glob(self.dir)
        else:
            sys.exit(' - The directory '+self.dir+' does not exist --> ABORTING')

        # -------- GET OBJIDS --------
        if objlist == None:
            if self.MASTfiles:
                searchext = '_2d.png'
                cutent    = [-28,-23]
            else:
                searchext = '.2D.png'
                cutent    = [-17,-12]

            self.file_2Dpng = [f for f in glob.glob(self.dir+'*'+searchext) if 'zfit' not in f]
            self.objlist    = np.asarray([int(self.file_2Dpng[jj][cutent[0]:cutent[1]])
                                          for jj in xrange(len(self.file_2Dpng))])
            self.objlist    = np.unique(self.objlist)
        else:
            if type(objlist) == str:
                self.objlist = np.genfromtxt(objlist,dtype=None,comments='#')
            else:
                self.objlist = np.asarray(objlist)

            self.objlist = vi.check_idlist(self.objlist,self.dir,verbose=self.vb) # check objects exist in dir

        if len(self.objlist) == 0:
            sys.exit('  No valid IDs found \n            Forgot a forward slash after the objdir? \n            Running on MAST files? Then use MASTfiles = True')

        self.currentobj = self.objlist[0]                    # set the first id to look at
        if verbose: print " - Found "+str(len(self.objlist))+' objects to inspect'
        # -------- Get version of MAST data release (assuming all the same) --------
        if self.MASTfiles:
            self.MASTversion = glob.glob(self.dir+'*_2d.png')[0][-11:-7]
        else:
            self.MASTversion = 'None'

        # -------- COUNT PAs FOR ALL IDs --------
        allPAs = []
        for id in self.objlist:
            idstr  = str("%05d" % id)
            if self.MASTfiles:
                searchext = '_1d.png'
            else:
                searchext = '1D.png'
            PAobj  = len(glob.glob(self.dir+'*'+idstr+'*'+searchext))/2. # divide by two to account for grisms
            allPAs.append(PAobj)
        self.Npamax = np.max(allPAs)
        if verbose: print ' - The maximum number of PAs in the objlist was ',self.Npamax

        # -------- OPEN/PREPARE OUTPUT FILE --------
        if os.path.isfile(outfile) & (clobber == True): # check if file is to be overwritten
            overwrite = raw_input(' - clobber==True Are you sure you want to overwrite '+outfile+'? (y/n): ')
            if (overwrite == 'y') or (overwrite == 'yes'):
                print "   Okay, I'll remove the file and start a new one"
                os.remove(outfile)
            elif (overwrite == 'n') or (overwrite == 'no'):
                print "   Okay, I'll append to the existing file, then"
            else:
                sys.exit('   "'+overwrite+'" is not a valid answer --> Aborting')

        if os.path.isfile(outfile):
            newfile   = False
            self.fout = open(outfile,'r')                # open existing file
            IDinspected = np.array([])                  # array to contain IDs in file
            for line in self.fout.readlines():           # loop through file to last line
                lsplit = line.split()
                if lsplit[0] != '#':
                    IDinspected = np.append(IDinspected,float(lsplit[0]))
            if len(IDinspected) == 0:
                sys.exit('Found no inspected objects in '+outfile)
            lastline = line
            self.fout.close()

            lastID = lastline.split()[0]                     # get the last ID in file
            if lastID != '#':
                objent = np.where(self.objlist == float(lastID))[0]
                if self.vb: print ' - The file '+outfile+' already exists (Resuming after last objects in output)'
                try:
                    self.currentobj = self.objlist[objent+1][0]  # change first id to look at
                except:
                    sys.exit(' - The last object in the outputfile is the last in "objlist" --> ABORTING ')
                Nremaining = len(self.objlist[objent+1:])
                Ninspected = len(np.unique(np.sort(IDinspected)))
                if self.vb:
                    print ' - Info from existing output: '
                    print '   '+str(Nremaining)+' of '+str(len(self.objlist))+' IDs still need to be expected'
                    print '   Found '+str(Ninspected)+' IDs already inspected in file'
            else:
                if self.vb: print ' - The file '+outfile+' already exists (append as last row does not contain ID)'
            self.fout     = open(outfile,'a')
        else:
            if self.vb: print ' - The file '+outfile+' was created (did not exist)'
            self.fout     = open(outfile,'w')
            self.fout.write('# Results from Visual Inspection initiated on '+self.now+' \n')
            self.fout.write('# Inspector: '+iname+' \n')
            newfile = True

        self.outfile = outfile

        # -------- ADD LABEL --------
        self.openpngs() # open pngs for first object and set PA variables
        position = [0,0,1]
        self.labelvar = StringVar()
        label = Label(master,textvariable=self.labelvar)
        label.grid(row=position[0],column=position[1],columnspan=position[2],sticky=N)
        self.labelvar.set(self.infostring())

        # -------- CREATE WIDGETS --------
        Frame.__init__(self, master)
        self.grid()
        self.create_widgets()

        # -------- ADD IMAGE WINDOW --------
        self.imgx,self.imgy = 990, 200
        img = ImageTk.PhotoImage(Image.open(self.GUIimage).resize((self.imgx,self.imgy),Image.ANTIALIAS))
        self.imageframe = Label(master, image=img)
        self.imageframe.image = img
        self.imageframe.grid(row = 100, column = 0, columnspan = 1, sticky=S)

        # -------- DRAW SEPERATORS --------
        self.drawsep(900,4,1 ,0,4,0,2,899,4)
        self.drawsep(900,4,29,0,4,0,2,899,4)
        self.drawsep(900,4,60,0,4,0,2,899,4)
        self.drawsep(900,4,80,0,4,0,2,899,4)

        # -------- OPEN FITS FILES FOR FIRST OBJ --------
        if self.fitsauto: # loading fits files automatically
            if self.xpa:
                self.openfits_but_cmd_xpa()
            else:
                self.openfits_but_cmd()

        # -------- FINALIZE --------
        filehdr = '  '.join([key[3:] for key in self.keys])      # create header for output
        if newfile: self.fout.write('# ID PA '+filehdr+' \n') # write header to output

        self.master.bind("<Key>", self.keyboard_cmd) # enable keyboard shortcuts
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def create_widgets(self):
        """
        Arrange the individual parts of the GUI
        postions are given as [row,column,span]
        """

        # -------- 1st PA --------
        self.cbpos = [5,0,1]
        self.checkboxes(self.cbpos)
        self.commentfield([self.cbpos[0]+6,2,1])
        self.wavefieldG102_1([self.cbpos[0]+0,2,1])
        self.wavefieldG141_1([self.cbpos[0]+1,2,1])
        # -------- 1nd PA --------
        self.cbpos2 = [31,0,1]
        if self.Npa == 2:
            self.checkboxes2(self.cbpos2)
        else:
            self.checkboxes2(self.cbpos2,disable=True)
        self.commentfield2([self.cbpos2[0]+6,2,1])
        self.wavefieldG102_2([self.cbpos2[0]+0,2,1])
        self.wavefieldG141_2([self.cbpos2[0]+1,2,1])


        position = [65,0,3]
        #textdisp = " GXXX_zfit_quality:  0: No z-fit,  1: Junk zgrim,  " \
        #           "2: Possible zgrim,  3: Probable zgrism,  4: Secure zgrim"
        textdisp = " GXXX_*_Contamination:  MILD: < 10%,  MODERATE: 10% - 40%,  " \
                   "SEVERE: > 40%"


        label    = StringVar()
        txtlab   = Label(self,textvariable=label)
        label.set(textdisp)
        txtlab.grid(row=position[0],column=position[1],columnspan=position[2],sticky=W)

        self.openfits_but([65,3,1])

        self.prev_but([70,0,1])
        self.quit_but([70,1,1])
        self.skip_but([70,2,1])
        self.next_but([70,3,1])
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def drawsep(self,width,height,row,col,colspan,xleftbottom,yleftbottom,xrighttop,yrighttop):
        """
        Draw a seperator
        """
        cv = Canvas(self, width=width, height=height)
        cv.grid(row = row, column = col, columnspan = colspan, sticky=N)
        cv.create_rectangle(xleftbottom, yleftbottom, xrighttop, yrighttop,fill='black')
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def checkboxes(self,position,disable=False):
        """
        Checkboxes for keywords to assign to object
        """
        self.dirstr = 'direct_'
        if self.ACSins:
            self.gris1 = 'G800L_'
            self.Ncol  = 3.
        else:
            self.gris1 = 'G102_'
            self.gris2 = 'G141_'
            self.Ncol  = 4.

        self.sliders      = [] #['d','D','l','L']
        self.empty        = ['c','C','g','G','d','D','h','H','p','P','t','T','l','L']
        self.calculations = ['c','C','g','G','d','D','h','H','p','P','l','L']
        colors            = self.getcolors()

        # Note that letters in () enables sorting of boxes
        self.keys = {}
        self.keys['(a) '+self.gris1+'Emission_Line']  = 0
        if not self.ACSins: self.keys['(b) '+self.gris2+'Emission_Line']  = 0
        self.keys['(c) G102_Spectral_Coverage']  = 0
        self.keys['(d) G141_Spectral_Coverage']  = 0

        self.keys['(e) '+self.gris1+'Emission_Lines_Multiple']  = 0
        if not self.ACSins: self.keys['(f) '+self.gris2+'Emission_Lines_Multiple']  = 0
        self.keys['(g) G102_Contamination_Level']  = 0
        self.keys['(h) G141_Contamination_Level']  = 0

        self.keys['(i) '+self.gris1+'Defect'] = 0
        if not self.ACSins: self.keys['(j) '+self.gris2+'Defect'] = 0
        self.keys['(k) '+self.gris1+'Contam_Defect']  = 0
        self.keys['(l) Spectral_Coverage_Type']  = 0

        self.keys['(m) '+self.gris1+'Mild_Contamination'] = 0
        if not self.ACSins: self.keys['(n) '+self.gris2+'Mild_Contamination'] = 0
        self.keys['(o) '+self.gris2+'Contam_Defect']  = 0
        self.keys['(p) Contamination_Level_Type']  = 0

        self.keys['(q) '+self.gris1+'Moderate_Contamination'] = 0
        if not self.ACSins: self.keys['(r) '+self.gris2+'Moderate_Contamination'] = 0
        self.keys['(s) '+self.dirstr+'Defect']  = 0
        self.keys['(t) empty7']  = 0

        self.keys['(u) '+self.gris1+'Severe_Contamination'] = 0
        if not self.ACSins: self.keys['(v) '+self.gris2+'Severe_Contamination'] = 0
        self.keys['(w) '+self.dirstr+'Star']  = 0
        self.keys['(x) I_have_no_idea']  = 0

        self.keys['(y) '+self.gris1+'Continuum'] = 0
        if not self.ACSins: self.keys['(z) '+self.gris2+'Continuum'] = 0

        if (sys.version_info[0] == 2) & (sys.version_info[1] == 7): # sort dictionary if running python 2.7
            import collections
            self.keys = collections.OrderedDict(sorted(self.keys.items()))
        else:
            print 'WARNING Python version not 2.7 so not sorting dictionary of keywords(1)'

        Nkey = 0
        self.cbdic     = {}
        self.sliderdic = {}
        for key in self.keys:
            rowval = position[0]+int(np.floor(Nkey/self.Ncol))
            colval = position[1]+int(np.round((Nkey/self.Ncol-np.floor((Nkey/self.Ncol)))*self.Ncol))

            self.keys[key] = Variable()

            if key[1] in self.sliders:
                self.slider = Scale(self, from_=0, to=4,label=key,variable = self.keys[key],
                                    orient=HORIZONTAL,background=colors[key[1]],length=200)
                self.slider.grid(row=rowval,column=colval,columnspan=position[2],rowspan=2,sticky=W)
                self.slider.set(0)

                if disable:
                    self.slider.configure(state='disabled')
                else:
                    self.sliderdic[key] = self.slider
            elif key[1] in self.empty:
                self.cb = Checkbutton(self, text=' ')
                self.cb.grid(row=position[0]+5,column=0,columnspan=1,sticky=W)
                self.cb.deselect()
                self.keys[key].set('-1')
                if key[1] in self.calculations:
                    self.keys[key].set(key)
            else:
                self.cb = Checkbutton(self, text=key, variable=self.keys[key],background=colors[key[1]])
                self.cb.grid(row=rowval,column=colval,columnspan=position[2],sticky=W)
                self.cb.deselect()

                if disable:
                    self.cb.configure(state='disabled')
                else:
                    self.cbdic[key] = self.cb

            Nkey = Nkey + 1
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def checkboxes2(self,position,disable=False):
        """
        Checkboxes for second PA
        """
        # Note that letters in () enables sorting of boxes
        colors     = self.getcolors()
        self.keys2 = {}
        self.keys2['(A) '+self.gris1+'Emission_Line']  = 0
        if not self.ACSins: self.keys2['(B) '+self.gris2+'Emission_Line']  = 0
        self.keys2['(C) G102_Spectral_Coverage']  = 0
        self.keys2['(D) G141_Spectral_Coverage']  = 0

        self.keys2['(E) '+self.gris1+'Emission_Lines_Multiple']  = 0
        if not self.ACSins: self.keys2['(F) '+self.gris2+'Emission_Lines_Multiple']  = 0
        self.keys2['(G) G102_Contamination_Level']  = 0
        self.keys2['(H) G141_Contamination_Level']  = 0

        self.keys2['(I) '+self.gris1+'Defect'] = 0
        if not self.ACSins: self.keys2['(J) '+self.gris2+'Defect'] = 0
        self.keys2['(K) '+self.gris1+'Contam_Defect']  = 0
        self.keys2['(L) Spectral_Coverage_Type']  = 0

        self.keys2['(M) '+self.gris1+'Mild_Contamination'] = 0
        if not self.ACSins: self.keys2['(N) '+self.gris2+'Mild_Contamination'] = 0
        self.keys2['(O) '+self.gris2+'Contam_Defect']  = 0
        self.keys2['(P) Contamination_Level_Type']  = 0

        self.keys2['(Q) '+self.gris1+'Moderate_Contamination'] = 0
        if not self.ACSins: self.keys2['(R) '+self.gris2+'Moderate_Contamination'] = 0
        self.keys2['(S) '+self.dirstr+'Defect']  = 0
        self.keys2['(T) empty7']  = 0

        self.keys2['(U) '+self.gris1+'Severe_Contamination'] = 0
        if not self.ACSins: self.keys2['(V) '+self.gris2+'Severe_Contamination'] = 0
        self.keys2['(W) '+self.dirstr+'Star']  = 0
        self.keys2['(X) I_have_no_idea']  = 0

        self.keys2['(Y) '+self.gris1+'Continuum'] = 0
        if not self.ACSins: self.keys2['(Z) '+self.gris2+'Continuum'] = 0


        if (sys.version_info[0] == 2) & (sys.version_info[1] == 7): # sort dictionary if running python 2.7
            import collections
            self.keys2 = collections.OrderedDict(sorted(self.keys2.items()))
        else:
            print 'WARNING Python version not 2.7 so not sorting dictionary of keywords(2)'

        Nkey = 0
        self.cbdic2     = {}
        self.sliderdic2 = {}
        for key in self.keys2:
            rowval = position[0]+int(np.floor(Nkey/self.Ncol))
            colval = position[1]+int(np.round((Nkey/self.Ncol-np.floor((Nkey/self.Ncol)))*self.Ncol))

            self.keys2[key] = Variable()

            if key[1] in self.sliders:
                self.slider2 = Scale(self, from_=0, to=4,label=key,variable = self.keys2[key],
                                    orient=HORIZONTAL,background=colors[key[1]],length=200)
                self.slider2.grid(row=rowval,column=colval,columnspan=position[2],rowspan=2,sticky=W)
                self.slider2.set(0)

                if disable:
                    self.slider2.configure(state='disabled')
                else:
                    self.sliderdic2[key] = self.slider2
            elif key[1] in self.empty:
                self.cb2 = Checkbutton(self, text=' ')
                self.cb2.grid(row=position[0]+5,column=0,columnspan=1,sticky=W)
                self.cb2.deselect()
                self.keys2[key].set('-1')
                if key[1] in self.calculations:
                    self.keys2[key].set(key)
            else:
                self.cb2 = Checkbutton(self, text=key, variable=self.keys2[key],background=colors[key[1]])
                self.cb2.grid(row=rowval,column=colval,columnspan=position[2],sticky=W)
                self.cb2.deselect()

                if disable:
                    self.cb2.configure(state='disabled')
                else:
                    self.cbdic2[key] = self.cb2

            Nkey = Nkey + 1
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def getcolors(self,):
        """
        Dictionary with colors for keys
        """
        collist = ['orange','red','cyan','magenta','green','white']
        colors  = {}
        colors['a'] = collist[0]
        colors['b'] = collist[1]
        colors['c'] = collist[4]
        colors['d'] = collist[4]
        colors['e'] = collist[0]
        colors['f'] = collist[1]
        colors['g'] = collist[4]
        colors['h'] = collist[4]
        colors['i'] = collist[0]
        colors['j'] = collist[1]
        colors['k'] = collist[0]
        colors['l'] = collist[4]
        colors['m'] = collist[0]
        colors['n'] = collist[1]
        colors['o'] = collist[1]
        colors['p'] = collist[4]
        colors['q'] = collist[0]
        colors['r'] = collist[1]
        colors['s'] = collist[5]
        colors['t'] = collist[4]
        colors['u'] = collist[0]
        colors['v'] = collist[1]
        colors['w'] = collist[5]
        colors['x'] = collist[5]
        colors['y'] = collist[0]
        colors['z'] = collist[1]

        colors['A'] = collist[2]
        colors['B'] = collist[3]
        colors['C'] = collist[4]
        colors['D'] = collist[4]
        colors['E'] = collist[2]
        colors['F'] = collist[3]
        colors['G'] = collist[4]
        colors['H'] = collist[4]
        colors['I'] = collist[2]
        colors['J'] = collist[3]
        colors['K'] = collist[2]
        colors['L'] = collist[4]
        colors['M'] = collist[2]
        colors['N'] = collist[3]
        colors['O'] = collist[3]
        colors['P'] = collist[4]
        colors['Q'] = collist[2]
        colors['R'] = collist[3]
        colors['S'] = collist[5]
        colors['T'] = collist[4]
        colors['U'] = collist[2]
        colors['V'] = collist[3]
        colors['W'] = collist[5]
        colors['X'] = collist[5]
        colors['Y'] = collist[2]
        colors['Z'] = collist[3]

        return colors
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def wavefieldG102_1(self,position):
        """
        Field to provide emission line wavelength
        """
        self.label_G102_1 = Label(self,text='(c) G102 emission line wavelength(s) [A]:  ')
        self.label_G102_1.grid(row=position[0],column=position[1],columnspan=position[2],sticky=W)
        self.linewaveG102_1 = Entry(self)
        self.linewaveG102_1.grid(row=position[0],column=position[1]+position[2],
                                 columnspan=position[2],sticky=W)
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def wavefieldG141_1(self,position):
        """
        Field to provide emission line wavelength
        """
        self.label_G141_1 = Label(self,text='(g) G141 emission line wavelength(s) [A]:  ')
        self.label_G141_1.grid(row=position[0],column=position[1],columnspan=position[2],sticky=W)
        self.linewaveG141_1 = Entry(self)
        self.linewaveG141_1.grid(row=position[0],column=position[1]+position[2],
                                 columnspan=position[2],sticky=W)
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def wavefieldG102_2(self,position):
        """
        Field to provide emission line wavelength
        """
        self.label_G102_2 = Label(self,text='(C) G102 emission line wavelength(s) [A]:  ')
        self.label_G102_2.grid(row=position[0],column=position[1],columnspan=position[2],sticky=W)
        self.linewaveG102_2 = Entry(self)
        self.linewaveG102_2.grid(row=position[0],column=position[1]+position[2],
                                 columnspan=position[2],sticky=W)
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def wavefieldG141_2(self,position):
        """
        Field to provide emission line wavelength
        """
        self.label_G141_2 = Label(self,text='(G) G141 emission line wavelength(s) [A]:  ')
        self.label_G141_2.grid(row=position[0],column=position[1],columnspan=position[2],sticky=W)
        self.linewaveG141_2 = Entry(self)
        self.linewaveG141_2.grid(row=position[0],column=position[1]+position[2],
                                 columnspan=position[2],sticky=W)
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def commentfield(self,position):
        """
        Field to provide comments
        """
        self.label = Label(self,text='(l) Comments ("tab" to move focus):  ')
        self.label.grid(row=position[0],column=position[1],columnspan=position[2],sticky=W)
        self.comments = Entry(self)
        self.comments.grid(row=position[0],column=position[1]+position[2],columnspan=position[2],sticky=W)
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def commentfield2(self,position):
        """
        Field to provide comments for second PA
        """
        self.label2 = Label(self,text='(L) Comments ("tab" to move focus):  ')
        self.label2.grid(row=position[0],column=position[1],columnspan=position[2],sticky=W)
        self.comments2 = Entry(self)
        self.comments2.grid(row=position[0],column=position[1]+position[2],columnspan=position[2],sticky=W)
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def openpngs(self,objid=None):
        """
        Function to open pngs of object
        """
        if objid == None:
            id = self.currentobj
        else:
            id = objid
        idstr     = str("%05d" % id)
        self.pngs = glob.glob(self.dir+'*'+idstr+'*.png')+glob.glob(self.dir+'*'+idstr+'*.pdf')
        if len(self.pngs) == 0:
            sys.exit(' - Did not find any png files to open. Looked for '+
                     self.dir+'*'+idstr+'*.png  --> ABORTING')

        self.file = self.pngs[0].split('/')[-1]

        # order the pngs to display
        if self.MASTfiles:
            G102_1D = [name for name in self.pngs if "g102_"+self.MASTversion+"_1d.png" in name]
            G102_2D = [name for name in self.pngs if "g102_"+self.MASTversion+"_2d.png" in name]
            G141_1D = [name for name in self.pngs if "g141_"+self.MASTversion+"_1d.png" in name]
            G141_2D = [name for name in self.pngs if "g141_"+self.MASTversion+"_2d.png" in name]
            G800_1D = [name for name in self.pngs if "g800l_"+self.MASTversion+"_1d.png" in name]
            G800_2D = [name for name in self.pngs if "g800l_"+self.MASTversion+"_2d.png" in name]
        else:
            G102_1D = [name for name in self.pngs if "G102.1D.png" in name]
            G102_2D = [name for name in self.pngs if "G102.2D.png" in name]
            G141_1D = [name for name in self.pngs if "G141.1D.png" in name]
            G141_2D = [name for name in self.pngs if "G141.2D.png" in name]
            G800_1D = [name for name in self.pngs if "G800L.1D.png" in name]
            G800_2D = [name for name in self.pngs if "G800L.2D.png" in name]

        zfit    = [name for name in self.pngs if "zfit" in name]
        stack   = [name for name in self.pngs if "stack" in name]
        mosaic  = [name for name in self.pngs if "mosaic" in name]
        pngorderedlist = G102_1D + G102_2D + G141_1D + G141_2D + G800_1D + G800_2D + zfit + stack + mosaic
        remaining      = list(set(self.pngs) - set(pngorderedlist)) # get files not accounted for above
        pngorderedlist = pngorderedlist #+ remaining

        self.plat = sys.platform
        if self.plat == 'darwin':
            import platform
            macversion = platform.mac_ver()[0]
            if float(macversion.split('.')[1]) > 6: # check if "open -F" is available (mac OS X 10.7.0 and above)
                opencmd = 'open -n -F '+' '.join(pngorderedlist)
            else:
                opencmd = 'open -n '+' '.join(pngorderedlist)
        elif self.plat == 'linux2' or 'Linux':
            opencmd = 'gthumb '+' '.join(pngorderedlist)+' &'

        # Update the in-GUI image
        self.GUIimage = None
        for png in self.pngs:
            if (self.inGUIimage == 'zfit') & ('zfitplot.png' in png):
                self.GUIimage  = png
            if (self.inGUIimage == 'G102stack') & \
                    (('G102_stack.png' in png) or ('g102_'+self.MASTversion+'_2dstack.png' in png)):
                self.GUIimage  = png
            if (self.inGUIimage == 'G141stack') & \
                    (('G141_stack.png' in png) or ('g141_'+self.MASTversion+'_2dstack.png' in png)):
                self.GUIimage  = png
        if self.GUIimage == None:  # if requested image not found for object use first png figure instead
            self.GUIimage = pngorderedlist[0]

        # Getting number of PAs for current object
        if self.MASTfiles:
            searchext = '_1d.png'
        else:
            searchext = '.1D.png'
        twodpng    = glob.glob(self.dir+'*'+idstr+'*'+searchext)
        self.PAs = np.zeros(len(twodpng))
        for ii in xrange(len(self.PAs)):
            if self.MASTfiles:
                namesplit = os.path.basename(twodpng[ii]).split('-pa')
                self.PAs[ii] = namesplit[-1][:3]
            else:
                namesplit = os.path.basename(twodpng[ii]).split('-')
                self.PAs[ii] = int(namesplit[1])
                if namesplit[0] in ['MACS0416.1','MACS2129.4','RXJ1347.5']: # case of names with negative dec
                    self.PAs[ii] = int(namesplit[2])
        self.PAs  = np.sort(np.unique(self.PAs)) # Make sure the PAs are sorted
        self.Npa  = len(self.PAs)
        self.pPNG = subprocess.Popen(opencmd,shell=True,executable=os.environ["SHELL"])
        time.sleep(1.1)# sleep to make sure png appear in PIDlist
        if self.plat == 'darwin':
            self.pngPID = vi.getPID('Preview.app',verbose=False) # get PID of png process
        elif self.plat == 'linux2' or 'Linux':
            self.pngPID = vi.getPID('gthumb',verbose=False)      # get PID of png process
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def openfits_but(self,position):
        """
        Button to open fits files
        """
        self.fitsb = Button(self)
        self.fitsb["text"] = "(0) Open fits files"
        if self.xpa:
            self.fitsb["command"] = self.openfits_but_cmd_xpa
        else:
            self.fitsb["command"] = self.openfits_but_cmd

        self.fitsb.grid(row=position[0],column=position[1],columnspan=position[2],sticky=W)
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def openfits_but_cmd_xpa(self):
        """
        Command for openfits button
        """
        self.regiontemp = 'temp_ds9_forinspection.reg'
        idstr   = str("%05d" % self.currentobj)
        lockstr = self.lockds9string()
        ds9cmd  = ' '

        if not self.ds9windowopen:
            ds9cmd = ds9cmd+'ds9 -geometry 1200x600 -scale zscale '+\
                     lockstr+' -tile grid layout 4 '+str(2*int(self.Npamax))
            self.pds9   = subprocess.Popen(ds9cmd,shell=True,executable=os.environ["SHELL"])
            time.sleep(1.1)# sleep to make sure ds9 appear in PIDlist
            self.ds9PID = vi.getPID('ds9',verbose=False) # get PID of DS9 process
            self.ds9windowopen = True
            time.sleep(1.0)
            for ii in np.arange(1,17):
                out = commands.getoutput('xpaset -p ds9 frame new')
            out = commands.getoutput('xpaset -p ds9 tile')

        Fstart = 1
        for PA in self.PAs:
            PAstr = '-'+str("%03d" % int(PA))+'-'
            if self.MASTfiles:
                searchexpression = self.dir+'*'+idstr+'*-pa'+PAstr[1:-1]+'_*2d.fits'
            else:
                searchexpression = self.dir+'*'+PAstr+'*'+idstr+'*2D.fits'
            fits_2D = glob.glob(searchexpression)

            for ii in xrange(len(fits_2D)):
                # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
                out = commands.getoutput('xpaset -p ds9 frame '+str(Fstart))
                regionfile = self.regiontemp.replace('.reg',PAstr+'DSCI.reg')
                self.ds9textregion('DSCI PA='+str(int(PA)),filename=regionfile)
                out = commands.getoutput('xpaset -p ds9 file '+fits_2D[ii]+'[DSCI]')
                out = commands.getoutput('xpaset -p ds9 regions '+regionfile)
                Fstart += 1

                # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
                out = commands.getoutput('xpaset -p ds9 frame '+str(Fstart))
                regionfile = self.regiontemp.replace('.reg',PAstr+'SCI.reg')
                self.ds9textregion('SCI PA='+str(int(PA)),filename=regionfile)
                out = commands.getoutput('xpaset -p ds9 file '+fits_2D[ii]+'[SCI]')
                out = commands.getoutput('xpaset -p ds9 regions '+regionfile)
                Fstart += 1

                # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
                out = commands.getoutput('xpaset -p ds9 frame '+str(Fstart))
                regionfile = self.regiontemp.replace('.reg',PAstr+'CONTAM.reg')
                self.ds9textregion('CONTAM PA='+str(int(PA)),filename=regionfile)
                out = commands.getoutput('xpaset -p ds9 file '+fits_2D[ii]+'[CONTAM]')
                out = commands.getoutput('xpaset -p ds9 regions '+regionfile)
                Fstart += 1

                # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
                out = commands.getoutput('xpaset -p ds9 frame '+str(Fstart))
                regionfile = self.regiontemp.replace('.reg',PAstr+'SCI-CONTAM.reg')
                self.ds9textregion('SCI-CONTAM PA='+str(int(PA)),filename=regionfile)
                contamsub = self.subtractcontam(fits_2D[ii]) # creating file with contam. subtracted spectrum
                out = commands.getoutput('xpaset -p ds9 file '+contamsub)
                out = commands.getoutput('xpaset -p ds9 regions '+regionfile)

                # If a sextractor region file for the SCI-CONTAM image exists, show it.
                sexregion = fits_2D[ii].split('.fit')[0]+'_SCI-CONTAM.reg'
                if os.path.exists(sexregion):
                    out = commands.getoutput('xpaset -p ds9 regions '+sexregion)
                Fstart += 1
                # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def openfits_but_cmd(self):
        """
        Command for openfits button
        """
        self.ds9open = True
        self.regiontemp = 'temp_ds9_forinspection.reg'
        idstr   = str("%05d" % self.currentobj)
        lockstr = self.lockds9string()

        ds9cmd  = 'ds9 -geometry 1200x600 -scale zscale '+lockstr+' -tile grid layout 4 '+str(2*int(self.Npa))
        for PA in self.PAs:
            PAstr = '-'+str("%03d" % int(PA))+'-'
            if self.MASTfiles:
                searchext = '2d.fits'
            else:
                searchext = '2D.fits'
            fits_2D = glob.glob(self.dir+'*'+PAstr+'*'+idstr+'*'+searchext)
            for ii in xrange(len(fits_2D)):
                regionfile = self.regiontemp.replace('.reg',PAstr+'DSCI.reg')
                self.ds9textregion('DSCI PA='+str(int(PA)),filename=regionfile)
                ds9cmd = ds9cmd+' "'+fits_2D[ii]+'[DSCI]" -region '+regionfile+' '

                regionfile = self.regiontemp.replace('.reg',PAstr+'SCI.reg')
                self.ds9textregion('SCI PA='+str(int(PA)),filename=regionfile)
                ds9cmd = ds9cmd+' "'+fits_2D[ii]+'[SCI]" -region '+regionfile+' '

                regionfile = self.regiontemp.replace('.reg',PAstr+'CONTAM.reg')
                self.ds9textregion('CONTAM PA='+str(int(PA)),filename=regionfile)
                ds9cmd = ds9cmd+' "'+fits_2D[ii]+'[CONTAM]" -region '+regionfile+' '

                regionfile = self.regiontemp.replace('.reg',PAstr+'SCI-CONTAM.reg')
                self.ds9textregion('SCI-CONTAM PA='+str(int(PA)),filename=regionfile)
                contamsub = self.subtractcontam(fits_2D[ii]) # creating file with contamination subtracted spectrum
                ds9cmd = ds9cmd+' "'+contamsub+'" -region '+regionfile+' '

                # If a sextractor region file for the SCI-CONTAM image exists, show it.
                sexregion = fits_2D[ii].split('.fit')[0]+'_SCI-CONTAM.reg'
                if os.path.exists(sexregion):
                    ds9cmd = ds9cmd+' -region '+sexregion+' '

        self.pds9   = subprocess.Popen(ds9cmd,shell=True,executable=os.environ["SHELL"])
        time.sleep(1.1)# sleep to make sure ds9 appear in PIDlist
        self.ds9PID = vi.getPID('ds9',verbose=False) # get PID of DS9 process
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def lockds9string(self):
        """
        """
        if int(self.ds9version[1].split('.')[0]) >= 7: # only lock if ds9 version is 7 or later
            lockstr = ' -lock frame physical '
        else:
            print ' - WARNING DS9 version older than 7.*; Not locking frames.'
            lockstr = ' '

        return lockstr
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def ds9textregion(self,text,filename='temp.reg'):
        """
        Create ds9 region file with text string
        Note that it's overwriting any existing file!
        """
        regstr = 'physical\n# text(130,10) textangle=0 textrotate=0 font="helvetica 12 normal roman" text={'+text+'}'
        fds9region = open(filename,'w')
        fds9region.write(regstr)
        fds9region.close()

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def updateimage(self):
        """
        update image in GUI
        """
        img = ImageTk.PhotoImage(Image.open(self.GUIimage).resize((self.imgx,self.imgy),Image.ANTIALIAS))
        self.imageframe.configure(image = img)
        self.imageframe.image = img
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def reset(self,skip=False):
        """
        Writing results to output, resetting checkboxes, and closing DS9 and PNG windows

        if skip=True nothing will be written to output file.
        """
        speccovtype   = 1    # type of spectral coverage estimator to return
        contleveltype = 1    # type of contamination level estimator to return
        cutcontam     = 1e-3 # the level above which contamination is counted
        # v v v v v v v v v v v v v v v v v v v v  1st PA v v v v v v v v v v v v v v v v v v v v
        # Make sure single Emission_Line keyword is set if Emission_Lines_Multiple is set
        if self.keys['(e) '+self.gris1+'Emission_Lines_Multiple'].get() == '1':
            self.keys['(a) '+self.gris1+'Emission_Line'].set('1')
        if not self.ACSins:
            if self.keys['(f) '+self.gris2+'Emission_Lines_Multiple'].get() == '1':
                self.keys['(b) '+self.gris2+'Emission_Line'].set('1')

        # Make sure single Emission Line keyword(s) set if wavelength fields not empty
        if len(self.linewaveG102_1.get().split()) == 1:
            self.keys['(a) G102_Emission_Line'].set('1')
        if len(self.linewaveG102_1.get().split()) > 1:
            self.keys['(e) G102_Emission_Lines_Multiple'].set('1')
        if len(self.linewaveG141_1.get().split()) == 1:
            self.keys['(b) G141_Emission_Line'].set('1')
        if len(self.linewaveG141_1.get().split()) > 1:
            self.keys['(f) G141_Emission_Lines_Multiple'].set('1')

        resultstr  = ' '+str("%.5d" % self.currentobj)+' '+str("%.3d" % self.PAs[0])
        defaultstr = resultstr
        for key in self.keys:
            keyval    = self.keys[key].get()
            if keyval == '-1':
                defaultstr = defaultstr+' '+str(keyval)
            elif len(keyval) > 10: # for text keys
                defaultstr = defaultstr+' '+keyval
            else:
                defaultstr = defaultstr+' '+str(0)
            resultstr = resultstr+' '+str(keyval)

        # adding info from comment and wave fields
        defaultstr = defaultstr+'  #G102wave#   #G141wave#   #C#  \n'
        resultstr  = resultstr+'  #G102wave# '+self.linewaveG102_1.get()
        resultstr  = resultstr+'  #G141wave# '+self.linewaveG141_1.get()
        resultstr  = resultstr+'  #C# '+self.comments.get()+' \n'

        skipin = skip # storing original skip value
        if (resultstr == defaultstr) & (self.skipempty == True): skip = True
        if not skip:
            if self.duplicates:
                Ndup = self.removeoutputduplicate(self.currentobj,self.PAs[0])

            # calculating spectral coverage and contamination if not skipping
            speccov       = self.estimate_spectralcoverage(self.currentobj,self.PAs[0],type=speccovtype)
            contlevel     = self.estimate_contaminationlevel(self.currentobj,self.PAs[0],cut=cutcontam,
                                                             type=contleveltype)
            resultstr     = resultstr.replace(self.keys.keys()[2],str("%.5f" % speccov[0]))   # G102
            resultstr     = resultstr.replace(self.keys.keys()[3],str("%.5f" % speccov[1]))   # G141
            resultstr     = resultstr.replace(self.keys.keys()[6],str("%.5f" % contlevel[0])) # G102
            resultstr     = resultstr.replace(self.keys.keys()[7],str("%.5f" % contlevel[1])) # G141
            resultstr     = resultstr.replace(self.keys.keys()[11],str(speccovtype))
            resultstr     = resultstr.replace(self.keys.keys()[15],str(contleveltype))

            self.fout.write(str(resultstr))
        if resultstr == defaultstr: skip = skipin # restoring original skip value

        # v v v v v v v v v v v v v v v v v v v v 2nd PA v v v v v v v v v v v v v v v v v v v v
        if self.Npa == 2: # if the current object has files for two PAs add a second line
            # Make sure single Emission_Line keyword is set if Emission_Lines_Multiple is set
            if self.keys2['(E) '+self.gris1+'Emission_Lines_Multiple'].get() == '1':
                self.keys2['(A) '+self.gris1+'Emission_Line'].set('1')
            if not self.ACSins:
                if self.keys2['(F) '+self.gris2+'Emission_Lines_Multiple'].get() == '1':
                    self.keys2['(B) '+self.gris2+'Emission_Line'].set('1')

            # Make sure single Emission Line keyword(s) set if wavelength fields not empty
            if len(self.linewaveG102_2.get().split()) == 1:
                self.keys2['(A) G102_Emission_Line'].set('1')
            if len(self.linewaveG102_2.get().split()) > 1:
                self.keys2['(E) G102_Emission_Lines_Multiple'].set('1')
            if len(self.linewaveG141_2.get().split()) == 1:
                self.keys2['(B) G141_Emission_Line'].set('1')
            if len(self.linewaveG141_2.get().split()) > 1:
                self.keys2['(F) G141_Emission_Lines_Multiple'].set('1')

            resultstr  = ' '+str("%.5d" % self.currentobj)+' '+str("%.3d" % self.PAs[1])
            defaultstr = resultstr
            for key in self.keys2:
                keyval    = self.keys2[key].get()
                if keyval == '-1':
                    defaultstr = defaultstr+' '+str(keyval)
                elif len(keyval) > 10: # for text keys
                    defaultstr = defaultstr+' '+keyval
                else:
                    defaultstr = defaultstr+' '+str(0)
                resultstr = resultstr+' '+str(keyval)

            # adding info from comment and wave fields
            defaultstr = defaultstr+'  #G102wave#   #G141wave#   #C#  \n'
            resultstr = resultstr+'  #G102wave# '+self.linewaveG102_2.get()
            resultstr = resultstr+'  #G141wave# '+self.linewaveG141_2.get()
            resultstr = resultstr+'  #C# '+self.comments2.get()+' \n'

            if (resultstr == defaultstr) & (self.skipempty == True): skip = True
            if not skip:
                if self.duplicates:
                    Ndup = self.removeoutputduplicate(self.currentobj,self.PAs[1])

                # calculating spectral coverage and contamination if not skipping
                speccov       = self.estimate_spectralcoverage(self.currentobj,self.PAs[1],type=speccovtype)
                contlevel     = self.estimate_contaminationlevel(self.currentobj,self.PAs[1],cut=cutcontam,
                                                                 type=speccovtype)
                resultstr     = resultstr.replace(self.keys2.keys()[2],str("%.5f" % speccov[0]))   # G102
                resultstr     = resultstr.replace(self.keys2.keys()[3],str("%.5f" % speccov[1]))   # G141
                resultstr     = resultstr.replace(self.keys2.keys()[6],str("%.5f" % contlevel[0])) # G102
                resultstr     = resultstr.replace(self.keys2.keys()[7],str("%.5f" % contlevel[1])) # G141
                resultstr     = resultstr.replace(self.keys2.keys()[11],str(speccovtype))
                resultstr     = resultstr.replace(self.keys2.keys()[15],str(contleveltype))

                self.fout.write(str(resultstr))
            if resultstr == defaultstr: skip = skipin # restoring original skip value

        # --- close and re-open output file so inspection is saved ---
        self.fout.close()
        self.fout = open(self.outfile,'a')

        # --- resetting widgets and closing windows ---
        self.comments.delete(0,END) # reset comment field
        self.comments2.delete(0,END) # reset comment field

        self.linewaveG102_1.delete(0,END) # reset wave field
        self.linewaveG141_1.delete(0,END) # reset wave field
        self.linewaveG102_2.delete(0,END) # reset wave field
        self.linewaveG141_2.delete(0,END) # reset wave field

        self.checkboxes(self.cbpos) # reset check boxes
        self.checkboxes2(self.cbpos2) # reset check boxes

        self.closewindows()

        self.ds9open = False # resetting ds9 indicator
        self.focus_set() # set focus to main window
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def removeoutputduplicate(self,id,pa):
        """
        Subtract continuum from science fram
        """
        self.fout.close()
        idstr       = str("%.5d" % id)
        pastr       = str("%.3d" % pa)
        stringstart = ' '+idstr+' '+pastr
        file        = open(self.outfile,'r')
        lines       = file.readlines()
        file.close()
        file = open(self.outfile,"w")

        Ndup        = 0
        for line in lines:
            if line[0:10] != stringstart:
                file.write(line)
            else:
                if self.vb: print ' - Found dublicate entry for ID '+idstr+' PA '+pastr+' deleting it!'
                Ndup = Ndup+1

        file.close()
        self.fout = open(self.outfile,'a')
        return Ndup
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def estimate_spectralcoverage(self,objid,PA,type=1):
        """
        Estimating the spectral coverage for the current object
        """
        idstr     = str("%05d" % objid)
        PAstr     = '-'+str("%03d" % int(PA))+'-'
        globstr   = self.dir+'*'+PAstr+'*'+idstr+'*1D.fits'
        file1D    = glob.glob(globstr)

        if len(file1D) > 2:
            if self.vb: print ' - WARNING Found more than 2 file globbing for '+globstr

        speccovG102 = speccovG141 = 9.99
        for f in file1D:
            dat    = pyfits.open(f)[1].data
            et     = dat['etrace']
            Npix   = float(len(et))
            Nzero  = float(len(et[et==0]))

            if Npix == 0:
                if 'G102' in f:
                    speccovG102 = -99
                elif 'G141' in f:
                    speccovG141 = -99
            else:
                if type == 1:
                    SCvalue     = 1.0 - Nzero/Npix
                else:
                    sys.exit(' - Invalid type ('+str(type)+') in estimate_spectralcoverage')

                if 'G102' in f:
                    speccovG102 = SCvalue
                elif 'G141' in f:
                    speccovG141 = SCvalue

        return speccovG102, speccovG141
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def estimate_contaminationlevel(self,objid,PA,cut=1e-3,type=1):
        """
        Estimating the contamination level for the current object
        """
        idstr     = str("%05d" % objid)
        PAstr     = '-'+str("%03d" % int(PA))+'-'
        file2D    = glob.glob(self.dir+'*'+PAstr+'*'+idstr+'*2D.fits')

        contlevelG102 = contlevelG141 = 9.99
        for f in file2D:
            hduimg      = pyfits.open(f) # Load the FITS hdulist
            model       = hduimg[6].data
            #scimodel    = hduimg[4].data[model != 0]
            contammodel = hduimg[7].data[model != 0]

            Nbad        = float(len(contammodel[np.abs(contammodel) > cut]) )
            Npix        = float(len(contammodel))

            if Npix == 0:
                if 'G102' in f:
                    contlevelG102 = -99
                elif 'G141' in f:
                    contlevelG141 = -99
            else:
                if type == 1:
                    CLvalue  = Nbad/Npix
                else:
                    sys.exit(' - Invalid type ('+str(type)+') in estimate_contaminationlevel')

                if 'G102' in f:
                    contlevelG102 = CLvalue
                elif 'G141' in f:
                    contlevelG141 = CLvalue

        return contlevelG102, contlevelG141
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def closewindows(self):
        """
        Close PNG and DS9 windows
        """
        killsignal = 1     # see bash> man kill
        PIDkill    = True
        if PIDkill:
            try:
                os.kill(self.pngPID,killsignal)                  # close PNG window for currentobj
            except:
                print '   WARNING error occurred while trying to close PNG window(s)'

            if np.logical_or(((self.ds9open == True) & (self.xpa == False)),
                             ((self.xpa == True) & (self.quitting == True) & (self.ds9windowopen == True))):
                try:
                    os.kill(self.ds9PID,killsignal)                  # close DS9 window for currentobj
                except:
                    if self.vb: print ' - WARNING: Could not kill DS9 process id ',self.ds9PID
                rmout = commands.getoutput('rm '+self.regiontemp.replace('.reg','*.reg')) # removing ds9 region file
        else:
            print '=== WHAT ARE YOU DOING HERE?? ==='
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def skip_but(self,position):
        self.skip = Button(self)
        self.skip["text"] = "Skip object"
        self.skip["command"] = self.skip_but_cmd
        self.skip.grid(row=position[0],column=position[1],columnspan=position[2],sticky=W)
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def skip_but_cmd(self):
        """
        Command for skip button
        """
        self.reset(skip=True)

        if self.currentobj == self.objlist[-1]:
            if self.vb: print ' - Object',self.currentobj,' was the last in the list.\n   Quitting GUI.'
            self.quitting = True
            self.quit_but_cmd()
        else:
            newent = np.where(self.objlist == self.currentobj)[0]+1
            self.currentobj = self.objlist[newent][0]
            self.openpngs()
            self.labelvar.set(self.infostring())
            self.updateimage()
            if self.Npa != 2: self.checkboxes2(self.cbpos2,disable=True) # disable checkboxes2 if Npa not 2

            if self.fitsauto: # loading fits files automatically
                if self.xpa:
                    self.openfits_but_cmd_xpa()
                else:
                    self.openfits_but_cmd()
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def next_but(self,position):
        self.next = Button(self)
        self.next["text"] = "(8) Next object (save)"
        self.next["command"] = self.next_but_cmd
        self.next.grid(row=position[0],column=position[1],columnspan=position[2],sticky=W)
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def next_but_cmd(self):
        """
        Command for next button
        """
        self.reset()

        if self.currentobj == self.objlist[-1]:
            if self.vb: print ' - Object',self.currentobj,' was the last in the list.\n   Quitting GUI.'
            self.quitting = True
            self.quit_but_cmd()
        else:
            newent = np.where(self.objlist == self.currentobj)[0]+1
            self.currentobj = self.objlist[newent][0]
            self.openpngs()
            self.labelvar.set(self.infostring())
            self.updateimage()
            if self.Npa != 2: self.checkboxes2(self.cbpos2,disable=True) # disable checkboxes2 if Npa not 2

            if self.fitsauto: # loading fits files automatically
                if self.xpa:
                    self.openfits_but_cmd_xpa()
                else:
                    self.openfits_but_cmd()
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def prev_but(self,position):
        self.prev= Button(self)
        self.prev["text"] = "(7) Previous object"
        self.prev["command"] = self.prev_but_cmd
        self.prev.grid(row=position[0],column=position[1],columnspan=position[2],sticky=W)
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def prev_but_cmd(self):
        """
        Command for previous button
        """
        self.reset()

        if self.currentobj == self.objlist[0]:
            if self.vb: print ' - At first object of list...'
        else:
            newent = np.where(self.objlist == self.currentobj)[0]-1
            self.currentobj = self.objlist[newent][0]
            self.openpngs()
            self.labelvar.set(self.infostring())
            self.updateimage()
            if self.Npa != 2: self.checkboxes2(self.cbpos2,disable=True) # disable checkboxes2 if Npa not 2

            if self.fitsauto: # loading fits files automatically
                if self.xpa:
                    self.openfits_but_cmd_xpa()
                else:
                    self.openfits_but_cmd()
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def quit_but(self,position):
        """
        Set up the quit button
        """
        self.QUIT = Button(self)
        self.QUIT["text"] = "QUIT GiG"
        self.QUIT["command"] = self.quit_but_cmd
        self.QUIT.grid(row=position[0],column=position[1],columnspan=position[2],sticky=W)
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def quit_but_cmd(self):
        """
        Command for quit button
        """
        if self.quitting == False: self.reset() # Only reset if quit_but_cmd was activated by quit button
        self.quitting = True
        self.fout.close()
        self.closewindows()
        if self.outcheck: self.checkoutput()
        self.quit()
        if self.vb: print ' - Quit GiG successfully'
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def checkoutput(self):
        """
        Checking the output to see if it is as expected
        """
        data      = np.genfromtxt(self.outfile,comments='#',skip_header=2,names=True)
        Nobjout   = len(np.unique(data['ID']))
        Npaout    = len(np.unique(data['PA']))

        if self.vb: print ' - OUTPUTCHECK: Found '+str(Nobjout)+' objects in output. '+\
                          'Input objlist contained '+str(len(self.objlist))+' objects'
        if self.vb: print ' - OUTPUTCHECK: Found '+str(Npaout)+' PAs in output. '+\
                          'Input objlist had '+str(self.Npamax)+' PAs'
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def subtractcontam(self,twodfits):
        """
        Subtract continuum from science fram
        """
        filename, fileext =  os.path.splitext(twodfits)
        output = filename+'_SCI-CONTAM'+fileext

        if os.path.isfile(output): # check if file already exists
            if self.vb: print ' - ',output,' already exists'
        else:
            if self.vb: print ' - Create ',output
            hduimg  = pyfits.open(twodfits) # Load the FITS hdulist
            hdrsci  = hduimg['SCI'].header    # extracting science header
            sci     = hduimg['SCI'].data
            contam  = hduimg['CONTAM'].data
            pyfits.writeto(output, sci-contam, hdrsci, clobber=False)

        return output
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def keyboard_cmd(self,event):
        """
        Commands for keyboard shortcuts
        """
        cmd = event.char

        focuson = self.focus_get() # check where the focus is
        if  (focuson == self.comments) or (focuson == self.comments2) or \
            (focuson == self.linewaveG102_1) or (focuson == self.linewaveG141_1) or \
            (focuson == self.linewaveG102_2) or (focuson == self.linewaveG141_2):
            pass
        else:
            keycmd    = []
            keynames  = []
            keynumber = []
            for ii, key in enumerate(self.keys):
                keycmd.append(key[1])
                keynames.append(key)
                keynumber.append(ii)

            keycmd2    = []
            keynames2  = []
            keynumber2 = []
            for ii, key2 in enumerate(self.keys2):
                keycmd2.append(key2[1])
                keynames2.append(key2)
                keynumber2.append(ii)

            if cmd in keycmd:
                thiskey = keynames[np.where(np.asarray(cmd) == np.asarray(keycmd))[0]]
                if cmd in self.sliders:
                    sliderval = int(self.keys[thiskey].get())
                    if sliderval == 4:
                        self.sliderdic[thiskey].set(0)
                    else:
                        self.sliderdic[thiskey].set(sliderval+1)
                elif cmd == 'l':
                    self.comments.focus_set()
                elif cmd == 'c':
                    self.linewaveG102_1.focus_set()
                elif cmd == 'g':
                    self.linewaveG141_1.focus_set()
                elif cmd in self.empty:
                    pass
                else:
                    self.cbdic[thiskey].toggle()

            elif (cmd in keycmd2) & (self.Npa == 2):
                thiskey2 = keynames2[np.where(np.asarray(cmd) == np.asarray(keycmd2))[0]]
                if cmd in self.sliders:
                    sliderval2 = int(self.keys2[thiskey2].get())
                    if sliderval2 == 4:
                        self.sliderdic2[thiskey2].set(0)
                    else:
                        self.sliderdic2[thiskey2].set(sliderval2+1)
                elif cmd == 'L':
                    self.comments2.focus_set()
                elif cmd == 'C':
                    self.linewaveG102_2.focus_set()
                elif cmd == 'G':
                    self.linewaveG141_2.focus_set()
                elif cmd in self.empty:
                    pass
                else:
                    self.cbdic2[thiskey2].toggle()

            elif cmd == '0':
                if self.xpa:
                    self.openfits_but_cmd_xpa()
                else:
                    self.openfits_but_cmd()

            elif cmd == '7':
                self.prev_but_cmd()

            elif cmd == '8':
                self.next_but_cmd()

            else:
                pass
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def infostring(self):
        """
        Return string with information to display in GUI window
        """
        cluster, redshift = vi.getclusterz(self.file)
        infostr = "--- Currently looking at object "+str(self.currentobj)+\
                  ', PA(s) = '+str(self.PAs)+\
                  '  ('+cluster+' redshift = '+str(redshift)+') ---'

        return infostr
#-------------------------------------------------------------------------------------------------------------
class Application_z(Frame):
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def __init__(self,dir,outfile,master=None,GiGfile=None,GiGselection='emissionlineobjects',
                 objlist=None,verbose=True,iname='John Doe',latexplotlabel=False,
                 ACSinspection=False,clobber=False,ds9xpa=False,openfitsauto=False,skipempty=False,
                 inGUIimage='zfit',check4duplicates=False,outputcheck=False,autosaveplot=False,
                 MASTfiles=False):
        """
        Intitialize the GUI for redshift fit

        -- INPUT --
        dir               Direcotory containing the data of the objects to inspect.
        outfile           Name of output file to create if it doesn't exists. Use clobber to overwrite.
        master            Provide another 'master' display. If None GUI created from scratch.
        GiGfile           File name of GiG inspectionn output if available. Will enable displaying
                          emission lines noted in the GiG output on the interactive plot as well as
                          selecting objects based on inspections.
        GiGselection      The selection to apply to the GiG catalog prior to performing inspection.
                          Only objects satisfying the GiGselection will be inspected unless an objlist was provided.
        objlist           List of objects to inspect. If 'None' all objects in 'dir' will be
                          inspected.
        verbose           Toggle verbosity.
        iname             Name of inspector to write in output file.
        latexplotlabel    Render plotting lables with latex; requires latex compiler.
        ACSinspection     If inspecting ACS objects (not enabled as of 150423).
        clobber           Overwrites the output file if it already exists
        ds9xpa            If xpa is availbale for comunicating commands to ds9
                          set this keyword to tru and this will be used instead
                          of opening ds9 everytime the fits files are requested.
        openfitsauto      Automatically load the fits files into the DS9 window
                          when advancing to next (or previous) object.
        skipempty         Set to True to ignore unedited objects when writing to output file.
                          Hence, if skipempty = True objects with no comments, flags set or sliders changed
                          will be written to the output
        inGUIimage        Select what image to display in GUI window (if available)
                          Choices are:
                          'zfit'       The redshift fit output plot (default)
                          'G102stack'  The stacked G102 2D spectra
                          'G141stack'  The stacked G102 2D spectra
        check4duplicates  Loop through output file whenever an object is save to check for
                          and remove duplicate entries
        outputcheck       Checking the written output to see if it contains the expected number
                          of objects etc.
        autosaveplot      Saving of the 1Dspec plot automatically when advancing to next object
        """
        pp    = subprocess.Popen('ds9 -version',shell=True,executable=os.environ["SHELL"],stdout=subprocess.PIPE)
        ppout = pp.communicate()[0]
        self.ds9version = ppout.split()

        self.now           = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.vb            = verbose
        self.dir           = dir
        self.ds9open       = False # set ds9 indicator (used for ds9xpa = False)
        self.ds9windowopen = False # set ds9 indicator (used for ds9xpa = True)
        self.ACSins        = ACSinspection
        self.quitting      = False
        self.xpa           = ds9xpa # check if user indacetd that xpa was available for ds9
        self.inGUIimage    = inGUIimage
        self.duplicates    = check4duplicates
        self.fitsauto      = openfitsauto # Open fits files automatically?
        self.outcheck      = outputcheck
        self.GiGf          = GiGfile
        self.latex         = latexplotlabel
        self.autosaveplot  = autosaveplot
        self.skipempty     = skipempty
        self.MASTfiles     = MASTfiles
        if self.xpa:
            #sys.exit(' - XPA DS9 controls not enabled yet; still under construction (use ds9xpa=False)')
            self.ds9windowopen = False

        if os.path.exists(self.dir):
            self.twodfits = glob.glob(self.dir)
        else:
            sys.exit(' - The directory '+self.dir+' does not exist --> ABORTING')

        # -------- LOAD GiG INFO IF FILE PROVIDED --------
        if self.GiGf != None:
            GiGfile_open  = open(GiGfile,'r')
            self.GiGlines = GiGfile_open.readlines()
            GiGfile_open.close()

            GiGsel         = GiGselection
            self.GiGobjID  = self.selectonGiG(GiGfile,GiGsel)

        # -------- GET OBJIDS --------
        if objlist == None:
            if self.GiGf != None:
                self.objlist = self.GiGobjID
            else:
                if self.MASTfiles:
                    searchext = '_2d.png'
                    cutent    = [-28,-23]
                else:
                    searchext = '.2D.png'
                    cutent    = [-17,-12]

                self.file_2Dpng = [f for f in glob.glob(self.dir+'*'+searchext) if 'zfit' not in f]
                self.objlist    = np.asarray([int(self.file_2Dpng[jj][cutent[0]:cutent[1]])
                                              for jj in xrange(len(self.file_2Dpng))])
                self.objlist    = np.unique(self.objlist)
        else:
            if type(objlist) == str:
                self.objlist = np.genfromtxt(objlist,dtype=None,comments='#')
            else:
                self.objlist = np.asarray(objlist)

            self.objlist = vi.check_idlist(self.objlist,self.dir,verbose=self.vb) # check objects exist in dir

        if len(self.objlist) == 0:
            sys.exit(' No valid IDs found \n             Forgot a forward slash after the objdir? \n             Running on MAST files? Then use MASTfiles = True')

        self.currentobj = self.objlist[0]                    # set the first id to look at
        if verbose: print " - Found "+str(len(self.objlist))+' objects to inspect'
        # -------- Get version of MAST data release (assuming all the same) --------
        if self.MASTfiles:
            self.MASTversion = glob.glob(self.dir+'*_2d.png')[0][-11:-7]
        else:
            self.MASTversion = 'None'
        # -------- COUNT PAs FOR ALL IDs --------
        allPAs = []
        for id in self.objlist:
            idstr  = str("%05d" % id)
            if self.MASTfiles:
                searchext = '_1d.png'
            else:
                searchext = '1D.png'
            PAobj  = len(glob.glob(self.dir+'*'+idstr+'*'+searchext))/2. # divide by two to account for grisms
            allPAs.append(PAobj)
        self.Npamax = np.max(allPAs)
        if verbose: print ' - The maximum number of PAs in the objlist was ',self.Npamax

        # -------- OPEN/PREPARE OUTPUT FILE --------
        if os.path.isfile(outfile) & (clobber == True): # check if file is to be overwritten
            overwrite = raw_input(' - clobber==True Are you sure you want to overwrite '+outfile+'? (y/n): ')
            if (overwrite == 'y') or (overwrite == 'yes'):
                print "   Okay, I'll remove the file and start a new one"
                os.remove(outfile)
            elif (overwrite == 'n') or (overwrite == 'no'):
                print "   Okay, I'll append to the existing file, then"
            else:
                sys.exit('   "'+overwrite+'" is not a valid answer --> Aborting')

        if os.path.isfile(outfile):
            newfile   = False
            self.fout = open(outfile,'r')                # open existing file
            IDinspected = np.array([])                   # array to contain IDs in file
            for line in self.fout.readlines():           # loop through file to last line
                lsplit = line.split()
                if lsplit[0] != '#':
                    IDinspected = np.append(IDinspected,float(lsplit[0]))
            if len(IDinspected) == 0:
                sys.exit('Found no inspected objects in '+outfile)
            lastline = line
            self.fout.close()

            lastID = lastline.split()[0]                     # get the last ID in file
            if lastID != '#':
                objent = np.where(self.objlist == float(lastID))[0]
                if self.vb: print ' - The file '+outfile+' already exists (Resuming after last objects in output)'
                try:
                    self.currentobj = self.objlist[objent+1][0]  # change first id to look at
                except:
                    sys.exit(' - The last object in the outputfile is the last in "objlist" --> ABORTING ')
                Nremaining = len(self.objlist[objent+1:])
                Ninspected = len(np.unique(np.sort(IDinspected)))
                if self.vb:
                    print ' - Info from existing output: '
                    print '   '+str(Nremaining)+' of '+str(len(self.objlist))+' IDs still need to be expected'
                    print '   Found '+str(Ninspected)+' IDs already inspected in file'

            else:
                if self.vb: print ' - The file '+outfile+' already exists (append as last row does not contain ID)'
            self.fout     = open(outfile,'a')
        else:
            if self.vb: print ' - The file '+outfile+' was created (did not exist)'
            self.fout     = open(outfile,'w')
            self.fout.write('# Results from Visual Inspection of zfits initiated on '+self.now+' \n')
            self.fout.write('# Inspector: '+iname+' \n')
            newfile = True

        self.outfile = outfile

        # -------- ADD LABEL --------
        self.openpngs() # open pngs for first object and set PA variables
        position = [0,0,1]
        self.labelvar = StringVar()
        label = Label(master,textvariable=self.labelvar)
        label.grid(row=position[0],column=position[1],columnspan=position[2],sticky=N)
        self.labelvar.set(self.infostring())

        # -------- CREATE WIDGETS --------
        Frame.__init__(self, master)
        self.grid()
        self.create_widgets()

        # -------- SETUP DATAPLOT --------
        self.dataPlot_init(xsize=1200,ysize=100)
        self.dataPlot_loaddata()
        self.dataPlot_plot(refresh=False,newobj=True)
        self.DPxlow_full, self.DPxhigh_full, self.DPylow_full, self.DPyhigh_full = \
            self.dataPlot_getwindowinfo() # store first full window

        # -------- ADD IMAGE WINDOW --------
        self.imgx,self.imgy = 990, 200
        img = ImageTk.PhotoImage(Image.open(self.GUIimage).resize((self.imgx,self.imgy),Image.ANTIALIAS))
        self.imageframe = Label(master, image=img)
        self.imageframe.image = img
        self.imageframe.grid(row = 150, column = 0, columnspan = 1, sticky=S)

        # -------- DRAW SEPERATORS --------
        self.drawsep(900,4,1 ,0,4,0,2,899,4)
        self.drawsep(900,4,29,0,4,0,2,899,4)
        self.drawsep(900,4,40,0,4,0,2,899,4)
        self.drawsep(900,4,60,0,4,0,2,899,4)
        self.drawsep(900,4,80,0,4,0,2,899,4)

        # -------- OPEN FITS FILES FOR FIRST OBJ --------
        if self.fitsauto: # loading fits files automatically
            if self.xpa:
                self.openfits_but_cmd_xpa()
            else:
                self.openfits_but_cmd()

        # -------- FINALIZE --------
        filehdr = '  '.join([key[3:] for key in self.keys])      # create header for output
        if newfile: self.fout.write('# ID PA '+filehdr+' byhandredshift byhandredshift_quality '
                                                       'multiple_redshift_solutions  \n')

        self.master.bind("<Key>", self.keyboard_cmd) # enable keyboard shortcuts
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def create_widgets(self):
        """
        Arrange the individual parts of the GUI
        postions are given as [row,column,span]
        """

        # -------- 1st PA --------
        self.cbpos = [5,0,1]
        self.checkboxes(self.cbpos)
        self.commentfield([self.cbpos[0]+5,2,1])
        # -------- 1nd PA --------
        self.cbpos2 = [31,0,1]
        if self.Npa == 2:
            self.checkboxes2(self.cbpos2)
        else:
            self.checkboxes2(self.cbpos2,disable=True)
        self.commentfield2([self.cbpos2[0]+5,2,1])

        position = [65,0,3]
        textdisp = " G***_zfit_quality:      0: No zfit/uninformative   1: Junk zfit   2: Possible zfit" \
                   "   3: Probable zfit   4: Secure zfit"
        label    = StringVar()
        txtlab   = Label(self,textvariable=label)
        label.set(textdisp)
        txtlab.grid(row=position[0],column=position[1],columnspan=position[2],sticky=W)

        self.openfits_but([65,3,1])

        self.prev_but([70,0,1])
        self.quit_but([70,1,1])
        self.skip_but([70,2,1])
        self.next_but([70,3,1])
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def drawsep(self,width,height,row,col,colspan,xleftbottom,yleftbottom,xrighttop,yrighttop):
        """
        Draw a seperator
        """
        cv = Canvas(self, width=width, height=height)
        cv.grid(row = row, column = col, columnspan = colspan, sticky=N)
        cv.create_rectangle(xleftbottom, yleftbottom, xrighttop, yrighttop,fill='black')
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def checkboxes(self,position,disable=False):
        """
        Checkboxes for keywords to assign to object
        """
        self.dirstr = 'direct_'
        self.gris1 = 'G102_'
        self.gris2 = 'G141_'
        self.Ncol  = 4.

        self.sliders      = ['a','A','b','B']
        self.empty        = ['e','E','f','F',#'g','G','h','H',
                             #'c','C','d','D',
                             #'i','I','j','J','k','K','l','L',
                             'm','M','n','N','o','O','p','P',
                             'q','Q','r','R','s','S','t','T',
                             'u','U','v','V','w','W','x','X',
                             'y','Y','z','Z']
        self.calculations = []#['c','C','g','G','d','D','h','H','p','P','l','L']
        colors            = self.getcolors()

        # Note that letters in () enables sorting of boxes
        self.keys = {}
        self.keys['(a) '+self.gris1+'zfit_quality']  = 0
        self.keys['(b) '+self.gris2+'zfit_quality']  = 0
        self.keys['(c) MgII_detection']  = 0
        self.keys['(d) OII_detection']  = 0

        self.keys['(e) empty1']  = 0
        self.keys['(f) empty2']  = 0
        self.keys['(g) OIII_detection']  = 0
        self.keys['(h) Ha_detection']  = 0

        if (sys.version_info[0] == 2) & (sys.version_info[1] == 7): # sort dictionary if running python 2.7
            import collections
            self.keys = collections.OrderedDict(sorted(self.keys.items()))
        else:
            print 'WARNING Python version not 2.7 so not sorting dictionary of keywords(1)'

        Nkey = 0
        self.cbdic     = {}
        self.sliderdic = {}
        for key in self.keys:
            rowval = position[0]+int(np.floor(Nkey/self.Ncol))
            colval = position[1]+int(np.round((Nkey/self.Ncol-np.floor((Nkey/self.Ncol)))*self.Ncol))

            self.keys[key] = Variable()

            if key[1] in self.sliders:
                self.slider = Scale(self, from_=0, to=4,label=key,variable = self.keys[key],
                                    orient=HORIZONTAL,background=colors[key[1]],length=200)
                self.slider.grid(row=rowval,column=colval,columnspan=position[2],rowspan=2,sticky=W)
                self.slider.set(0)

                if disable:
                    self.slider.configure(state='disabled')
                else:
                    self.sliderdic[key] = self.slider
            elif key[1] in self.empty:
                self.cb = Checkbutton(self, text='emptyXX')
                self.cb.deselect()
                self.keys[key].set('-1')
                if key[1] in self.calculations:
                    self.keys[key].set(key)
            else:
                self.cb = Checkbutton(self, text=key, variable=self.keys[key],background=colors[key[1]])
                self.cb.grid(row=rowval,column=colval,columnspan=position[2],sticky=W)
                self.cb.deselect()

                if disable:
                    self.cb.configure(state='disabled')
                else:
                    self.cbdic[key] = self.cb

            Nkey = Nkey + 1
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def checkboxes2(self,position,disable=False):
        """
        Checkboxes for second PA
        """
        # Note that letters in () enables sorting of boxes
        colors     = self.getcolors()
        self.keys2 = {}
        self.keys2['(A) '+self.gris1+'zfit_quality']  = 0
        self.keys2['(B) '+self.gris2+'zfit_quality']  = 0
        self.keys2['(C) MgII_detection']  = 0
        self.keys2['(D) OII_detection']  = 0

        self.keys2['(E) empty1']  = 0
        self.keys2['(F) empty2']  = 0
        self.keys2['(G) OIII_detection']  = 0
        self.keys2['(H) Ha_detection']  = 0

        if (sys.version_info[0] == 2) & (sys.version_info[1] == 7): # sort dictionary if running python 2.7
            import collections
            self.keys2 = collections.OrderedDict(sorted(self.keys2.items()))
        else:
            print 'WARNING Python version not 2.7 so not sorting dictionary of keywords(2)'

        Nkey = 0
        self.cbdic2     = {}
        self.sliderdic2 = {}

        for key in self.keys2:
            rowval = position[0]+int(np.floor(Nkey/self.Ncol))
            colval = position[1]+int(np.round((Nkey/self.Ncol-np.floor((Nkey/self.Ncol)))*self.Ncol))

            self.keys2[key] = Variable()

            if key[1] in self.sliders:
                self.slider2 = Scale(self, from_=0, to=4,label=key,variable = self.keys2[key],
                                    orient=HORIZONTAL,background=colors[key[1]],length=200)
                self.slider2.grid(row=rowval,column=colval,columnspan=position[2],rowspan=2,sticky=W)
                self.slider2.set(0)

                if disable:
                    self.slider2.configure(state='disabled')
                else:
                    self.sliderdic2[key] = self.slider2
            elif key[1] in self.empty:
                self.cb2 = Checkbutton(self, text='emptyXX')
                self.cb2.deselect()
                self.keys2[key].set('-1')
                if key[1] in self.calculations:
                    self.keys2[key].set(key)
            else:
                self.cb2 = Checkbutton(self, text=key, variable=self.keys2[key],background=colors[key[1]])
                self.cb2.grid(row=rowval,column=colval,columnspan=position[2],sticky=W)
                self.cb2.deselect()

                if disable:
                    self.cb2.configure(state='disabled')
                else:
                    self.cbdic2[key] = self.cb2

            Nkey = Nkey + 1
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def selectonGiG(self,GiGfile,GiGsel,verbose=True):
        """
        Returning object list of selection from GiG catalog
        """
        self.GiGdata = np.genfromtxt(GiGfile,comments='#',skip_header=2,names=True)

        if GiGsel == 'emissionlineobjects':
            selection = self.GiGdata[np.logical_or(np.logical_or(self.GiGdata['G102_Emission_Line'] == 1,
                                                                 self.GiGdata['G141_Emission_Line'] == 1),
                                                   np.logical_or(self.GiGdata['G102_Continuum'] == 1,
                                                                 self.GiGdata['G141_Continuum'] == 1))]
            objlist   = np.unique(np.sort(selection['ID']))
            Nid       = len(objlist)
            if verbose: print ' - Found ',Nid,' objects with emission lines and/or continuum in ',GiGfile
        elif (GiGsel == 'allentries') or (GiGsel == None) or (GiGsel == 'all'):
            objlist = np.unique(np.sort(self.GiGdata['ID']))
            Nid       = len(objlist)
            if verbose: print ' - Found ',Nid,' objects (all objects) in ',GiGfile
        else:
            print ' - WARNING the GiGselection keyword (',GiGsel,') is not valid;'
            print '   Returning all IDs in the GiG catalog ',GiGfile
            objlist = np.unique(np.sort(self.GiGdata['ID']))

        return objlist

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def getcolors(self,):
        """
        Dictionary with colors for keys
        """
        collist = ['orange','red','cyan','magenta','green','white']
        colors  = {}
        colors['a'] = collist[0]
        colors['b'] = collist[1]
        colors['c'] = collist[5]
        colors['d'] = collist[5]
        colors['e'] = collist[4]
        colors['f'] = collist[4]
        colors['g'] = collist[5]
        colors['h'] = collist[5]
        colors['i'] = collist[4]
        colors['j'] = collist[4]
        colors['k'] = collist[4]
        colors['l'] = collist[4]
        colors['m'] = collist[4]
        colors['n'] = collist[4]
        colors['o'] = collist[4]
        colors['p'] = collist[4]
        colors['q'] = collist[4]
        colors['r'] = collist[4]
        colors['s'] = collist[4]
        colors['t'] = collist[4]
        colors['u'] = collist[4]
        colors['v'] = collist[4]
        colors['w'] = collist[4]
        colors['x'] = collist[4]
        colors['y'] = collist[4]
        colors['z'] = collist[4]

        colors['A'] = collist[2]
        colors['B'] = collist[3]
        colors['C'] = collist[5]
        colors['D'] = collist[5]
        colors['E'] = collist[4]
        colors['F'] = collist[4]
        colors['G'] = collist[5]
        colors['H'] = collist[5]
        colors['I'] = collist[4]
        colors['J'] = collist[4]
        colors['K'] = collist[4]
        colors['L'] = collist[4]
        colors['M'] = collist[4]
        colors['N'] = collist[4]
        colors['O'] = collist[4]
        colors['P'] = collist[4]
        colors['Q'] = collist[4]
        colors['R'] = collist[4]
        colors['S'] = collist[4]
        colors['T'] = collist[4]
        colors['U'] = collist[4]
        colors['V'] = collist[4]
        colors['W'] = collist[4]
        colors['X'] = collist[4]
        colors['Y'] = collist[4]
        colors['Z'] = collist[4]

        return colors


    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def dataPlot_init(self,xsize=500,ysize=150,rowval=45):
        """
        Inititalize the data plot window (also used to kill it when exiting)
        """
        #----------------- Plot setup -----------------
        plt.ioff()                                                 # turn off interactive plotting
        plt.ion()                                                  # enable interactive plotting
        self.DPFsize  = 16
        self.DPlwidth = 2
        self.DPxscale = 1e4
        self.DPg102range_cut  = [8000,11250]
        self.DPg141range_cut  = [11000,16500]
        self.DPg102range_full = [7600,11700]
        self.DPg141range_full = [10500,17000]
        self.DPg102col   = ['orange','cyan']
        self.DPg141col   = ['red','magenta']
        self.DPxrange    = [0.78,1.67]
        if self.latex:
            plt.rc('text', usetex=True)                            # enabling LaTex rendering of text
        else:
            plt.rc('text', usetex=False)                           # disabling LaTex rendering of text
        plt.rc('font' , family='serif',size=self.DPFsize)          # setting text font
        plt.rc('xtick', labelsize=self.DPFsize)
        plt.rc('ytick', labelsize=self.DPFsize)

        self.dataPlot_fig    = plt.figure()
        self.dataPlot_fig.canvas.set_window_title('GLASS 1D spectra of object '+str(self.currentobj))
        self.dataPlot_fig.subplots_adjust(wspace=0.2, hspace=0.2,left=0.1, right=0.98, bottom=0.15, top=0.95)
        self.dataPlot_ax     = self.dataPlot_fig.add_subplot(111)
        self.dataPlotManager = plt.get_current_fig_manager()  # get plotting canvas
        self.dataPlotManager.resize(xsize,ysize)

        # ==== SLIDERS =====
        cluster, cluster_z = vi.getclusterz(self.file)

        self.varsliderz = DoubleVar()
        self.sliderz  = Scale(self, from_=0.00, to=15.0,label='Redshift (n)+ (N)-',variable = self.varsliderz,
                              orient=HORIZONTAL,background='gray',length=200,resolution=0.001)
        self.sliderz.grid(row=rowval,column=0,columnspan=1,rowspan=1,sticky=W)
        self.varsliderz.set(cluster_z) # set intial value of slider

        self.varslidersmooth  = DoubleVar()
        self.slidersmooth= Scale(self, from_=0, to=10,label='Gauss smooth (m)+ (M)-',
                                 variable = self.varslidersmooth,
                                 orient=HORIZONTAL,background='gray',length=200,resolution=0.1)
        self.slidersmooth.grid(row=rowval,column=1,columnspan=1,rowspan=1,sticky=W)
        self.varslidersmooth.set(0) # set intial value of slider

        self.varsliderzqual = DoubleVar()
        self.sliderzqual    = Scale(self, from_=0, to=4.0,label='(q) By-hand redshift quality',
                                    variable = self.varsliderzqual,orient=HORIZONTAL,background='yellow',
                                    length=200,resolution=1.0)
        self.sliderzqual.grid(row=rowval,column=2,columnspan=1,rowspan=1,sticky=W)
        self.varsliderzqual.set(0) # set intial value of slider


        # ==== COMMENT FIELD ====
        self.byhandzlabel = Label(self,text='(u) By-hand redshift:  ',background='yellow')
        self.byhandzlabel.grid(row=rowval,column=3,columnspan=1,sticky=NW)
        self.byhandz = Entry(self)
        self.byhandz.grid(row=rowval,column=3,columnspan=1,sticky=SW)

        # ==== CHECK BOX ====
        self.modelboxvar = Variable()
        self.modelbox = Checkbutton(self, text='(o) Remove models', variable=self.modelboxvar,background='gray')
        self.modelbox.grid(row=rowval+1,column=0,columnspan=1,sticky=W)
        self.modelbox.deselect()

        self.GiGlinesboxvar = Variable()
        self.GiGlinesbox = Checkbutton(self, text='(p) Show GiG lines', variable=self.GiGlinesboxvar,
                                       background='gray')
        self.GiGlinesbox.grid(row=rowval+1,column=1,columnspan=1,sticky=W)
        self.GiGlinesbox.deselect()
        if (self.GiGf == None): self.GiGlinesbox.configure(state='disabled')

        self.mzsboxvar = Variable()
        self.mzsbox    = Checkbutton(self, text='(t) Multiple Redshift Solutions', variable=self.mzsboxvar,
                                     background='yellow')
        self.mzsbox.grid(row=rowval+1,column=2,columnspan=1,sticky=W)
        self.mzsbox.deselect()

        # ==== BUTTONS ====
        self.dataPlot_fullzoombutton([rowval+2,0,1])
        self.dataPlot_redrawbutton([rowval+2,1,1])
        self.dataPlot_savebutton([rowval+2,3,1])

        self.DPxlow, self.DPxhigh, self.DPylow, self.DPyhigh = self.dataPlot_getwindowinfo() # store window
        # self.dataPlotManager.destroy()
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def dataPlot_redrawbutton(self,position):
        """
        Button to redraw plot
        """
        self.dpbut_redraw = Button(self)
        self.dpbut_redraw["text"] = "(r) Redraw"
        self.dpbut_redraw["command"] = self.dataPlot_redrawbutton_cmd
        self.dpbut_redraw.grid(row=position[0],column=position[1],columnspan=position[2],sticky=W)
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def dataPlot_redrawbutton_cmd(self):
        """
        Command for redrawing the plot
        """
        self.DPxlow, self.DPxhigh, self.DPylow, self.DPyhigh = self.dataPlot_getwindowinfo() # store window
        self.dataPlot_plot(refresh=True,verbose=True)
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def dataPlot_fullzoombutton(self,position):
        """
        Button to go to full zoom in the plot
        """
        self.dpbut_fullzoom = Button(self)
        self.dpbut_fullzoom["text"] = "(z) full zoom"
        self.dpbut_fullzoom["command"] = self.dataPlot_fullzoombutton_cmd
        self.dpbut_fullzoom.grid(row=position[0],column=position[1],columnspan=position[2],sticky=W)
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def dataPlot_fullzoombutton_cmd(self):
        """
        Command for going back to full zoom in the plot
        """
        self.DPxlow, self.DPxhigh, self.DPylow, self.DPyhigh = self.dataPlot_getwindowinfo() # store window
        self.dataPlot_plot(refresh=True,fullzoom=True,verbose=True)

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def dataPlot_savebutton(self,position):
        """
        Button to save the plot using default naming
        """
        self.dpbut_save = Button(self)
        self.dpbut_save["text"] = "(s) Quick save plot"
        if self.autosaveplot: self.dpbut_save["text"] = "(s) Autosave Enabled"
        self.dpbut_save["command"] = self.dataPlot_savebutton_cmd
        self.dpbut_save.grid(row=position[0],column=position[1],columnspan=position[2],sticky=W)
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def dataPlot_savebutton_cmd(self):
        """
        Command for saving the created plot
        """
        plotname = self.dir+self.cluster+'_'+str("%.5d" % self.currentobj)+'_GiGz_1Dspecplot.pdf'
        self.dataPlot_fig.savefig(plotname)
        print ' - Saved GiGz plot window to \n   '+plotname
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def dataPlot_loaddata(self,verbose=False):
        """
        Loading the data for dataPlot so it's only necessary to load data once

        """
        self.DPidstr    = str("%.5d" % self.currentobj)
        if self.MASTfiles:
            searchext = '1d.fits'
        else:
            searchext = '1D.fits'
        fits1Dfound     = glob.glob(self.dir+'*'+self.DPidstr+'*'+searchext)
        self.DPfits1D   = []
        self.DPPAs      = []
        for f1D in fits1Dfound:
            try:
                if self.MASTfiles:
                    self.DPPAs.append(re.search(r'(-pa..._)', f1D).group()[3:6])
                else:
                    self.DPPAs.append(re.search(r'(-...-)', f1D).group()[1:4])

                self.DPfits1D.append(f1D)
            except:
                pass

        self.DPNfiles   = len(self.DPfits1D)
        self.DPPAs      = np.sort(np.unique(np.asarray(self.DPPAs)))
        if verbose: print ' - Found the PAs ',self.DPPAs

        # check if EAZY fit pickle exist and load that data
        self.eazydicexists = False
        eazydicfile        = glob.glob(self.dir+'*'+self.DPidstr+'*EAZYzfit_all.pickle')
        if (len(eazydicfile) > 0):
            eazydicfile = eazydicfile[0]
            if os.path.isfile(eazydicfile):
                import pickle
                with open(eazydicfile, 'rb') as handle:
                    self.eazydic = pickle.load(handle)

                if verbose: print ' - Attempt to load dictionary in ',eazydicfile
                try:
                    keys     = self.eazydic.keys()
                    for key in keys:
                        if key.endswith('2D.fits'):
                            eazykey = key

                    if verbose: print ' - Loading EAZY photo-z info from key ',eazykey
                    lambdaz, temp_sed, lci, obs_sed, fobs, efobs = self.eazydic[eazykey]
                    self.goodzfitload = True
                except:
                    self.goodzfitload = False

                if verbose: print ' - Loading results from zfit (in *zfit.dat)'
                self.zfitdataALL = []
                idstr            = str("%.5d" % self.currentobj)
                zfitfiles        = np.sort(glob.glob(self.dir+'/*_'+idstr+'*zfit.dat'))
                for zfitfile in zfitfiles:
                    zfitdata  = np.genfromtxt(zfitfile,dtype=None)
                    if (self.zfitdataALL == []):
                        self.zfitdataALL = zfitdata
                    else:
                        self.zfitdataALL = np.append(self.zfitdataALL,zfitdata)

                self.eazydicexists = True
            else:
                if verbose: print ' No EAZY dictionary found when looking for ',eazydicfile
        else:
            self.goodzfitload = False
    # = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
    def dataPlot_plot(self,verbose=False,refresh=False,newobj=False,fullzoom=False):
        """
        Plotting the 1D spectra loaded in dataPlot_loaddata
        Code taken from runzfit.plotcombinedresults on 141024 and modified.

        Eazydicfile ends on MACS1423.8+2404_00111_EAZYzfit_all.pickle

        """
        self.dataPlot_fig.canvas.set_window_title('GLASS 1D spectra of object '+str(self.currentobj))
        xlow, xhigh, ylow, yhigh = self.dataPlot_getwindowinfo()
        if fullzoom:
            xlow, xhigh, ylow, yhigh =  self.DPxlow_full, self.DPxhigh_full, self.DPylow_full, self.DPyhigh_full
        #----------------- Define emission line list -----------------
        #Lines from http://www.sdss.org/dr7/algorithms/linestable.html and
        # http://adsabs.harvard.edu/abs/2008ApJS..174..282L
        linelist = np.asarray([1216 ,1335 ,1402  ,1549 ,1908. ,2795. ,3726.03 ,
                    4101.74   ,4340.47  ,4861.33 ,4959.,5007. ,
                    6548, 6562.8, 6583.5,
                    6718,6732,
                    9071.1,   9533.2])
        linename = ['Lya','CII','SiIV','CIV','CIII]','MgII',"[OII]" ,
                    '$H\delta$','H$\gamma$','H$\\beta$',''   ,'[OIII]',
                    ''  ,'H$\\alpha$+NII',' '   ,
                    ' ' ,'SII',
                    '[SIII]','[SIII]']
        #----------------- Refreshing plot window-----------------
        if refresh:
            self.dataPlot_fig.clf() # clearing figure
            self.dataPlot_ax     = self.dataPlot_fig.add_subplot(111)
        #----------------- Grab infor from sliders -----------------
        smoothlevel  = float(self.varslidersmooth.get())
        if verbose: print ' - Grabbed the Gauss smooth level ',smoothlevel,' from the slider'
        redshift     = float(self.varsliderz.get())
        if verbose: print ' - Grabbed the redshift ',redshift,' from the slider'

        try:
            zbyhand      = float(self.byhandz.get())
            if type(zbyhand) == float:
                redshift = zbyhand
                if verbose: print '   But the redshift',zbyhand,'was found in "by-hand" field so using that instead '
            self.varsliderz.set(zbyhand)
        except:
            pass

        #----------------- Flambda spec -----------------
        xrangeflam = self.DPxrange
        ymax   = []
        ymin   = []

        for ii in range(self.DPNfiles):
            dat1D   = pyfits.open(self.DPfits1D[ii])[1].data
            if ('G102' in self.DPfits1D[ii]) or ('g102' in self.DPfits1D[ii]):
                goodent = np.where((dat1D['WAVE'] > self.DPg102range_full[0]) &
                                   (dat1D['WAVE'] < self.DPg102range_full[1]))[0]
                color   = self.DPg102col[0]
                if len(self.DPPAs) == 2:
                    if '-'+self.DPPAs[1]+'-' in self.DPfits1D[ii]: color = self.DPg102col[1] # second PA color
            elif ('G141' in self.DPfits1D[ii]) or 'g141' in self.DPfits1D[ii]:
                goodent = np.where((dat1D['WAVE'] > self.DPg141range_full[0]) &
                                   (dat1D['WAVE'] < self.DPg141range_full[1]))[0]
                color   = self.DPg141col[0]
                if len(self.DPPAs) == 2:
                    if '-'+self.DPPAs[1]+'-' in self.DPfits1D[ii]: color = self.DPg141col[1] # second PA color


            wave1D = dat1D['WAVE'][goodent]/self.DPxscale
            flux1D = (dat1D['FLUX'][goodent] - dat1D['CONTAM'][goodent])/dat1D['SENSITIVITY'][goodent]

            if len(flux1D) >= 1:
                self.dataPlot_ax.plot(wave1D, flux1D, color=color,linestyle='-',
                                      linewidth=self.DPlwidth*1.5, alpha=0.2)

                ymax.append(np.max(dat1D['FLUX'][(dat1D['WAVE'] > self.DPg102range_cut[0]) &
                                                 (dat1D['WAVE'] < self.DPg102range_cut[1])]))
                ymin.append(np.min(dat1D['FLUX'][(dat1D['WAVE'] > self.DPg102range_cut[0]) &
                                                 (dat1D['WAVE'] < self.DPg102range_cut[1])]))

                # Smoothed versions
                filtersigma   = smoothlevel
                flux1D_smooth = scipy.ndimage.filters.gaussian_filter1d(flux1D, filtersigma,cval=0.0)
                self.dataPlot_ax.plot(wave1D, flux1D_smooth, color=color,linestyle='-',
                                      linewidth=self.DPlwidth*1.5, alpha=0.7)

                frange  = [np.min(flux1D),np.max(flux1D)]
                dfrange = np.max(flux1D)-np.min(flux1D)

                # ======= Plotting the GiG catalog lines if any there for object =======
                if (self.GiGf != None) & (self.GiGlinesboxvar.get() != '0'):
                    objPA = float(self.DPPAs[0])
                    if (len(self.DPPAs) == 2):
                        if ('-'+self.DPPAs[1]+'-' in self.DPfits1D[ii]): # 2nd PA
                            objPA = float(self.DPPAs[1])

                    if ('G102' in self.DPfits1D[ii]) or ('g102' in self.DPfits1D[ii]):
                        ents = np.where((self.GiGdata['ID'] == self.currentobj) &
                                        (self.GiGdata['PA'] == objPA) ) # first PA match

                        if (len(ents[0]) > 0):
                            for ent in ents:
                                objGiGdat = self.GiGlines[ent+3]
                                G102waves = objGiGdat.split('#G102wave#')[-1].split('#G141wave#')[0].replace(',',' ').split()
                                for wave in G102waves:
                                    wave = float(wave)
                                    if wave < 2.0: wave = wave*1.e4 # in case of wave given in micron
                                    dwave = np.abs(wave1D-wave/self.DPxscale)
                                    GiGlineflux = flux1D_smooth[dwave == np.min(dwave)]
                                    self.dataPlot_ax.plot(wave/self.DPxscale,GiGlineflux,marker='o',
                                                          markerfacecolor=color,markeredgecolor='black',
                                                          markeredgewidth=self.DPlwidth/1.5,
                                                          markersize=8)
                                if len(G102waves) == 0: # No G102 lines marked
                                    if verbose:
                                        print ' - No G102 line wavelengths found for',self.currentobj,'at PA =',objPA
                                    textpos = wave1D[int(len(wave1D)/2.)]
                                    if (textpos > xrangeflam[0]) & (textpos < xrangeflam[1]):
                                        ypos = flux1D[wave1D == textpos]
                                        self.dataPlot_ax.text(textpos,ypos,
                                                              'No line wavelengths found in GiG catalog',
                                                              color=color,size=self.DPFsize-3.,
                                                              horizontalalignment='center',
                                                              verticalalignment='center',alpha=0.8)
                        else:
                            if verbose: print ' - No entry for',self.currentobj,'at PA =',objPA,'in GiG catalog'



                    if ('G141' in self.DPfits1D[ii]) or ('g141' in self.DPfits1D[ii]):
                        ents = np.where((self.GiGdata['ID'] == self.currentobj) &
                                        (self.GiGdata['PA'] == objPA) ) # first PA match

                        if (len(ents[0]) > 0):
                            for ent in ents:
                                objGiGdat = self.GiGlines[ent+3]
                                G141waves = objGiGdat.split('#G141wave#')[-1].split('#C#')[0].replace(',',' ').split()
                                for wave in G141waves:
                                    wave = float(wave)
                                    if wave < 2.0: wave = wave*1.e4 # in case of wave given in micron
                                    dwave = np.abs(wave1D-wave/self.DPxscale)
                                    GiGlineflux = flux1D_smooth[dwave == np.min(dwave)]
                                    self.dataPlot_ax.plot(wave/self.DPxscale,GiGlineflux,marker='o',
                                                          markerfacecolor=color,markeredgecolor='black',
                                                          markeredgewidth=self.DPlwidth/1.5,
                                                          markersize=8)
                                if len(G141waves) == 0: # No G141 lines marked
                                    if verbose:
                                        print ' - No G141 line wavelengths found for',self.currentobj,'at PA =',objPA
                                    textpos = wave1D[int(len(wave1D)/2.)]
                                    if (textpos > xrangeflam[0]) & (textpos < xrangeflam[1]):
                                        ypos = flux1D[wave1D == textpos]
                                        self.dataPlot_ax.text(textpos,ypos,
                                                              'No line wavelengths found in GiG catalog',
                                                              color=color,size=self.DPFsize-3.,
                                                              horizontalalignment='center',
                                                              verticalalignment='center',alpha=0.8)
                        else:
                            if verbose: print ' - No entry for',self.currentobj,'at PA =',objPA,'in GiG catalog'

            # ======= Plot zfit models on top of spectra =======
            if self.eazydicexists & (self.modelboxvar.get() == '0') & (self.goodzfitload == True):
                # plot wavelength solutions for zfit
                ent = np.where(self.zfitdataALL['f0'] == self.DPfits1D[ii].split('/')[-1].split('.1D.')[0])
                if len(ent[0]) == 0:
                    pass
                else:
                    zfitredshift = self.zfitdataALL['f6'][ent]
                    for ll in range(len(linelist)):
                        try:
                            self.dataPlot_ax.plot(np.zeros(2)+linelist[ll]/self.DPxscale*(zfitredshift+1.0),
                                                  frange,color=color,alpha=0.6,
                                                  linestyle='--',linewidth=self.DPlwidth)
                            textpos = linelist[ll]/self.DPxscale*(zfitredshift+1.0)
                        except:
                            pdb.set_trace()

                        if (textpos > xrangeflam[0]) & (textpos < xrangeflam[1]):
                            self.dataPlot_ax.text(textpos,frange[0]+dfrange*0.05,
                                                  linename[ll],color=color,size=self.DPFsize-3.,
                                                  rotation='vertical',horizontalalignment='right',
                                                  verticalalignment='bottom',alpha=0.6)

                    # plot model for given redshift
                    oned_wave = self.eazydic[self.DPfits1D[ii].split('/')[-1].replace('.1D.','.2D.')+'_oned_wave']
                    model_1D  = self.eazydic[self.DPfits1D[ii].split('/')[-1].replace('.1D.','.2D.')+'_model_1D']/\
                                dat1D['SENSITIVITY']
                    if oned_wave[0] != -99:
                        self.dataPlot_ax.plot(oned_wave[goodent]/self.DPxscale, model_1D[goodent],
                                              color='white',linestyle='-',
                                              linewidth=self.DPlwidth*2,alpha=1.0,zorder=50+ii,)

                        self.dataPlot_ax.plot(oned_wave[goodent]/self.DPxscale, model_1D[goodent],
                                              color=color,linestyle='-',
                                              linewidth=self.DPlwidth,alpha=1.0,zorder=50+ii,
                                              label='zfit model (zfit='+str("%.3f" % zfitredshift)+')')

            if self.eazydicexists & (self.modelboxvar.get() == '1'): # add legend if no models shown
                ent = np.where(self.zfitdataALL['f0'] == self.DPfits1D[ii].split('/')[-1].split('.1D.')[0])
                zfitredshift = self.zfitdataALL['f6'][ent]
                self.dataPlot_ax.plot([],[],color=color,linestyle='-',linewidth=self.DPlwidth,
                                            alpha=1.0,label='zfit ='+str("%.3f" % zfitredshift))

        # set ranges based on spectra
        if (len(ymin) != 0) & (len(ymax) != 0):
            yrangeflam = [0.95*min(ymin), 1.05*max(ymax)]
            if yrangeflam[0] < -0.01: yrangeflam[0] = -0.01
            if yrangeflam[1] >  10.0: yrangeflam[1] =  10.0
        else:
            yrangeflam = 0.0, 1.0
        if not newobj: # only check window if not plotting new object
            if (ylow != yrangeflam[0]) or (yhigh != yrangeflam[1]):
                yrangeflam = [ylow,yhigh]
        Dyrange    = yrangeflam[1]-yrangeflam[0]
        self.dataPlot_ax.set_ylim(yrangeflam)

        if not newobj: # only check window if not plotting new object
            if (xlow != xrangeflam[0]) or (xhigh != xrangeflam[1]):
                xrangeflam = [xlow,xhigh]
        self.dataPlot_ax.set_xlim(xrangeflam)
        self.dataPlot_ax.fill_between([1.105,1.16],[yrangeflam[0],yrangeflam[0]],[yrangeflam[1],yrangeflam[1]],
                                      alpha=0.20,color='k')

        if self.latex:
            xlab = '$\lambda / [\mu\mathrm{m}]$'
            ylab = '$f_\lambda / [10^{-17}\mathrm{erg}/\mathrm{s}/\mathrm{cm}^2/\mathrm{\AA}]$'
        else:
            xlab = 'lambda / [micron]'
            ylab = 'f_lambda / [10**-17/erg/s/cm2/A]'

        self.dataPlot_ax.set_xlabel(xlab)
        self.dataPlot_ax.set_ylabel(ylab)

        self.dataPlotManager.canvas.draw()

        # === plot emission lines for scale ===
        for ii in range(len(linelist)):
            self.dataPlot_ax.plot(np.zeros(2)+linelist[ii]/self.DPxscale*(redshift+1.0),
                                  yrangeflam,color='#006600',alpha=0.7,
                                  linestyle='-',linewidth=self.DPlwidth)
            textpos = linelist[ii]/self.DPxscale*(redshift+1.0)

            if (textpos > xrangeflam[0]) & (textpos < xrangeflam[1]):
                self.dataPlot_ax.text(textpos,yrangeflam[0]+Dyrange*0.05,
                                      linename[ii],color='#006600',size=self.DPFsize-3.,rotation='vertical',
                                      horizontalalignment='right',verticalalignment='bottom')

        # === position legend ===
        box = self.dataPlot_ax.get_position()
        self.dataPlot_ax.set_position([box.x0, box.y0, box.width, box.height * 0.83])
        self.dataPlot_ax.plot(0,0,'orange',label='G102 PA='+self.DPPAs[0],linewidth=self.DPlwidth*2)
        self.dataPlot_ax.plot(0,0,'red',label='G141 PA='+self.DPPAs[0],linewidth=self.DPlwidth*2)
        if len(self.DPPAs) == 2:
            self.dataPlot_ax.plot(0,0,'cyan',label='G102 PA='+self.DPPAs[1],linewidth=self.DPlwidth*2)
            self.dataPlot_ax.plot(0,0,'magenta',label='G141 PA='+self.DPPAs[1],linewidth=self.DPlwidth*2)
        self.dataPlot_ax.plot(0,0,'green',label='Lines at z='+str("%.3f" % redshift),linewidth=self.DPlwidth*2)
        if (self.GiGf != None) & (self.GiGlinesboxvar.get() != '0'):
            self.dataPlot_ax.plot(0,0,label='GiG marked lines',marker='o',markerfacecolor='white',linestyle='',
                                  markeredgecolor='black',markeredgewidth=self.DPlwidth/1.5,markersize=8)
        leg = self.dataPlot_ax.legend(fancybox=True, loc='upper center',numpoints=1,prop={'size':self.DPFsize-3.},
                                      ncol=5,bbox_to_anchor=(0.5, 1.27))
        #leg.get_frame().set_alpha(0.7)

        self.dataPlotManager.canvas.draw()
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def dataPlot_getwindowinfo(self):
        """
        get information about window after zoom etc.
        """
        xmin  = self.dataPlot_ax.get_xbound()[0]
        xmax  = self.dataPlot_ax.get_xbound()[1]
        ymin  = self.dataPlot_ax.get_ybound()[0]
        ymax  = self.dataPlot_ax.get_ybound()[1]

        return xmin, xmax, ymin, ymax
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def commentfield(self,position):
        """
        Field to provide comments
        """
        self.label = Label(self,text='(l) Comments ("tab" to move focus):  ')
        self.label.grid(row=position[0],column=position[1],columnspan=position[2],sticky=W)
        self.comments = Entry(self)
        self.comments.grid(row=position[0],column=position[1]+position[2],columnspan=position[2],sticky=W)
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def commentfield2(self,position):
        """
        Field to provide comments for second PA
        """
        self.label2 = Label(self,text='(L) Comments ("tab" to move focus):  ')
        self.label2.grid(row=position[0],column=position[1],columnspan=position[2],sticky=W)
        self.comments2 = Entry(self)
        self.comments2.grid(row=position[0],column=position[1]+position[2],columnspan=position[2],sticky=W)
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def openpngs(self,objid=None):
        """
        Function to open pngs of object
        """
        if objid == None:
            id = self.currentobj
        else:
            id = objid
        idstr     = str("%05d" % id)
        self.pngs = glob.glob(self.dir+'*'+idstr+'*.png')+glob.glob(self.dir+'*'+idstr+'*.pdf')
        if len(self.pngs) == 0:
            sys.exit(' - Did not find any png files to open. Looked for '+
                     self.dir+'*'+idstr+'*.png  --> ABORTING')

        self.file = self.pngs[0].split('/')[-1]

        # order the pngs to display
        G102_1D = [name for name in self.pngs if "G102.1D.png" in name]
        G102_2D = [name for name in self.pngs if "G102.2D.png" in name]
        G141_1D = [name for name in self.pngs if "G141.1D.png" in name]
        G141_2D = [name for name in self.pngs if "G141.2D.png" in name]
        G800_1D = [name for name in self.pngs if "G800L.1D.png" in name]
        G800_2D = [name for name in self.pngs if "G800L.2D.png" in name]
        zfit    = [name for name in self.pngs if "zfit" in name]
        stack   = [name for name in self.pngs if "stack" in name]
        mosaic  = [name for name in self.pngs if "mosaic" in name]
        pngorderedlist = G102_1D + G102_2D + G141_1D + G141_2D + G800_1D + G800_2D + zfit + stack + mosaic
        remaining      = list(set(self.pngs) - set(pngorderedlist)) # get files not accounted for above
        pngorderedlist = pngorderedlist #+ remaining

        self.plat = sys.platform
        if self.plat == 'darwin':
            import platform
            macversion = platform.mac_ver()[0]
            if float(macversion.split('.')[1]) > 6: # check if "open -F" is available (mac OS X 10.7.0 and above)
                opencmd = 'open -n -F '+' '.join(pngorderedlist)
            else:
                opencmd = 'open -n '+' '.join(pngorderedlist)
        elif self.plat == 'linux2' or 'Linux':
            opencmd = 'gthumb '+' '.join(pngorderedlist)+' &'

        # Update the in-GUI image
        self.GUIimage = None
        for png in self.pngs:
            if (self.inGUIimage == 'zfit') & ('zfitplot.png' in png):
                self.GUIimage  = png
            if (self.inGUIimage == 'G102stack') & \
                    (('G102_stack.png' in png) or ('g102_'+self.MASTversion+'_2dstack.png' in png)):
                self.GUIimage  = png
            if (self.inGUIimage == 'G141stack') & \
                    (('G141_stack.png' in png) or ('g141_'+self.MASTversion+'_2dstack.png' in png)):
                self.GUIimage  = png
        if self.GUIimage == None:  # if requested image not found for object use first png figure instead
            self.GUIimage = pngorderedlist[0]

        # Getting number of PAs for current object
        if self.MASTfiles:
            searchext = '_1d.png'
        else:
            searchext = '.1D.png'
        twodpng    = glob.glob(self.dir+'*'+idstr+'*'+searchext)
        self.PAs = np.zeros(len(twodpng))
        for ii in xrange(len(self.PAs)):
            if self.MASTfiles:
                namesplit = os.path.basename(twodpng[ii]).split('-pa')
                self.PAs[ii] = namesplit[-1][:3]
            else:
                namesplit = os.path.basename(twodpng[ii]).split('-')
                self.PAs[ii] = int(namesplit[1])
                if namesplit[0] in ['MACS0416.1','MACS2129.4','RXJ1347.5']: # case of names with negative dec
                    self.PAs[ii] = int(namesplit[2])
        self.PAs  = np.sort(np.unique(self.PAs)) # Make sure the PAs are sorted
        self.Npa  = len(self.PAs)
        self.pPNG = subprocess.Popen(opencmd,shell=True,executable=os.environ["SHELL"])
        time.sleep(1.1)# sleep to make sure png appear in PIDlist
        if self.plat == 'darwin':
            self.pngPID = vi.getPID('Preview.app',verbose=False) # get PID of png process
        elif self.plat == 'linux2' or 'Linux':
            self.pngPID = vi.getPID('gthumb',verbose=False)      # get PID of png process
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def openfits_but(self,position):
        """
        Button to open fits files
        """
        self.fitsb = Button(self)
        self.fitsb["text"] = "(0) Open fits files"
        if self.xpa:
            self.fitsb["command"] = self.openfits_but_cmd_xpa
        else:
            self.fitsb["command"] = self.openfits_but_cmd

        self.fitsb.grid(row=position[0],column=position[1],columnspan=position[2],sticky=W)
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def openfits_but_cmd_xpa(self):
        """
        Command for openfits button
        """
        self.regiontemp = 'temp_ds9_forinspection.reg'
        idstr   = str("%05d" % self.currentobj)
        lockstr = self.lockds9string()
        ds9cmd  = ' '

        if not self.ds9windowopen:
            ds9cmd = ds9cmd+'ds9 -geometry 1200x600 -scale zscale '+\
                     lockstr+' -tile grid layout 4 '+str(2*int(self.Npamax))
            self.pds9   = subprocess.Popen(ds9cmd,shell=True,executable=os.environ["SHELL"])
            time.sleep(1.1)# sleep to make sure ds9 appear in PIDlist
            self.ds9PID = vi.getPID('ds9',verbose=False) # get PID of DS9 process
            self.ds9windowopen = True
            time.sleep(1.0)
            for ii in np.arange(1,17):
                out = commands.getoutput('xpaset -p ds9 frame new')
            out = commands.getoutput('xpaset -p ds9 tile')

        Fstart = 1
        for PA in self.PAs:
            PAstr = '-'+str("%03d" % int(PA))+'-'
            if self.MASTfiles:
                searchexpression = self.dir+'*'+idstr+'*-pa'+PAstr[1:-1]+'_*2d.fits'
            else:
                searchexpression = self.dir+'*'+PAstr+'*'+idstr+'*2D.fits'
            fits_2D = glob.glob(searchexpression)

            for ii in xrange(len(fits_2D)):
                # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
                out = commands.getoutput('xpaset -p ds9 frame '+str(Fstart))
                regionfile = self.regiontemp.replace('.reg',PAstr+'DSCI.reg')
                self.ds9textregion('DSCI PA='+str(int(PA)),filename=regionfile)
                out = commands.getoutput('xpaset -p ds9 file '+fits_2D[ii]+'[DSCI]')
                out = commands.getoutput('xpaset -p ds9 regions '+regionfile)
                Fstart += 1

                # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
                out = commands.getoutput('xpaset -p ds9 frame '+str(Fstart))
                regionfile = self.regiontemp.replace('.reg',PAstr+'SCI.reg')
                self.ds9textregion('SCI PA='+str(int(PA)),filename=regionfile)
                out = commands.getoutput('xpaset -p ds9 file '+fits_2D[ii]+'[SCI]')
                out = commands.getoutput('xpaset -p ds9 regions '+regionfile)
                Fstart += 1

                # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
                out = commands.getoutput('xpaset -p ds9 frame '+str(Fstart))
                regionfile = self.regiontemp.replace('.reg',PAstr+'CONTAM.reg')
                self.ds9textregion('CONTAM PA='+str(int(PA)),filename=regionfile)
                out = commands.getoutput('xpaset -p ds9 file '+fits_2D[ii]+'[CONTAM]')
                out = commands.getoutput('xpaset -p ds9 regions '+regionfile)
                Fstart += 1

                # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
                out = commands.getoutput('xpaset -p ds9 frame '+str(Fstart))
                regionfile = self.regiontemp.replace('.reg',PAstr+'SCI-CONTAM.reg')
                self.ds9textregion('SCI-CONTAM PA='+str(int(PA)),filename=regionfile)
                contamsub = self.subtractcontam(fits_2D[ii]) # creating file with contam. subtracted spectrum
                out = commands.getoutput('xpaset -p ds9 file '+contamsub)
                out = commands.getoutput('xpaset -p ds9 regions '+regionfile)

                # If a sextractor region file for the SCI-CONTAM image exists, show it.
                sexregion = fits_2D[ii].split('.fit')[0]+'_SCI-CONTAM.reg'
                if os.path.exists(sexregion):
                    out = commands.getoutput('xpaset -p ds9 regions '+sexregion)
                Fstart += 1
                # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def openfits_but_cmd(self):
        """
        Command for openfits button
        """
        self.ds9open = True
        self.regiontemp = 'temp_ds9_forinspection.reg'
        idstr   = str("%05d" % self.currentobj)
        lockstr = self.lockds9string()

        ds9cmd  = 'ds9 -geometry 1200x600 -scale zscale '+lockstr+' -tile grid layout 4 '+str(2*int(self.Npa))
        for PA in self.PAs:
            PAstr = '-'+str("%03d" % int(PA))+'-'
            if self.MASTfiles:
                searchext = '2d.fits'
            else:
                searchext = '2D.fits'
            fits_2D = glob.glob(self.dir+'*'+PAstr+'*'+idstr+'*'+searchext)
            for ii in xrange(len(fits_2D)):
                regionfile = self.regiontemp.replace('.reg',PAstr+'DSCI.reg')
                self.ds9textregion('DSCI PA='+str(int(PA)),filename=regionfile)
                ds9cmd = ds9cmd+' "'+fits_2D[ii]+'[DSCI]" -region '+regionfile+' '

                regionfile = self.regiontemp.replace('.reg',PAstr+'SCI.reg')
                self.ds9textregion('SCI PA='+str(int(PA)),filename=regionfile)
                ds9cmd = ds9cmd+' "'+fits_2D[ii]+'[SCI]" -region '+regionfile+' '

                regionfile = self.regiontemp.replace('.reg',PAstr+'CONTAM.reg')
                self.ds9textregion('CONTAM PA='+str(int(PA)),filename=regionfile)
                ds9cmd = ds9cmd+' "'+fits_2D[ii]+'[CONTAM]" -region '+regionfile+' '

                regionfile = self.regiontemp.replace('.reg',PAstr+'SCI-CONTAM.reg')
                self.ds9textregion('SCI-CONTAM PA='+str(int(PA)),filename=regionfile)
                contamsub = self.subtractcontam(fits_2D[ii]) # creating file with contamination subtracted spectrum
                ds9cmd = ds9cmd+' "'+contamsub+'" -region '+regionfile+' '

                # If a sextractor region file for the SCI-CONTAM image exists, show it.
                sexregion = fits_2D[ii].split('.fit')[0]+'_SCI-CONTAM.reg'
                if os.path.exists(sexregion):
                    ds9cmd = ds9cmd+' -region '+sexregion+' '

        self.pds9   = subprocess.Popen(ds9cmd,shell=True,executable=os.environ["SHELL"])
        time.sleep(1.1)# sleep to make sure ds9 appear in PIDlist
        self.ds9PID = vi.getPID('ds9',verbose=False) # get PID of DS9 process
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def lockds9string(self):
        """
        """
        if int(self.ds9version[1].split('.')[0]) >= 7: # only lock if ds9 version is 7 or later
            lockstr = ' -lock frame physical '
        else:
            print ' - WARNING DS9 version older than 7.*; Not locking frames.'
            lockstr = ' '

        return lockstr
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def ds9textregion(self,text,filename='temp.reg'):
        """
        Create ds9 region file with text string
        Note that it's overwriting any existing file!
        """
        regstr = 'physical\n# text(130,10) textangle=0 textrotate=0 font="helvetica 12 normal roman" text={'+text+'}'
        fds9region = open(filename,'w')
        fds9region.write(regstr)
        fds9region.close()

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def updateimage(self):
        """
        update image in GUI
        """
        img = ImageTk.PhotoImage(Image.open(self.GUIimage).resize((self.imgx,self.imgy),Image.ANTIALIAS))
        self.imageframe.configure(image = img)
        self.imageframe.image = img
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def reset(self,skip=False):
        """
        Writing results to output, resetting checkboxes, and closing DS9 and PNG windows

        if skip=True nothing will be written to output file.
        """
        if (self.autosaveplot) & (skip==False): self.dataPlot_savebutton_cmd() # saving plot before resetting

        try: # checking that the input can be converted to a float
            zbyhand      = str(float(self.byhandz.get()))+' '
        except:
            zbyhand      = '-99 '
            if (str(self.byhandz.get()) != ''):
                print ' - WARNING: by-hand redshift field ('+str(self.byhandz.get())+\
                      ') could not be converted to float. Using -99.'
        zbyhand = zbyhand+str(int(self.varsliderzqual.get()))
        # v v v v v v v v v v v v v v v v v v v v  1st PA v v v v v v v v v v v v v v v v v v v v
        resultstr  = ' '+str("%.5d" % self.currentobj)+' '+str("%.3d" % self.PAs[0])
        defaultstr = resultstr
        for key in self.keys:
            keyval    = str(self.keys[key].get())
            if keyval == '-1':
                defaultstr = defaultstr+' '+str(keyval)
            elif len(keyval) > 10: # for text keys
                defaultstr = defaultstr+' '+keyval
            else:
                defaultstr = defaultstr+' '+str(0)
            resultstr = resultstr+' '+str(keyval)

        # by-hand redshift info
        defaultstr = defaultstr+' -99 0'
        resultstr  = resultstr+' '+zbyhand

        # Multiple redshift solutions?
        defaultstr = defaultstr+' 0'
        resultstr  = resultstr+' '+self.mzsboxvar.get()

        # adding info from comment and wave fields
        defaultstr = defaultstr +'  #C#  \n'
        resultstr  = resultstr  +'  #C# '+self.comments.get()+' \n'

        skipin = skip # storing original skip value
        if (resultstr == defaultstr) & (self.skipempty == True): skip = True
        if not skip:
            if self.duplicates:
                Ndup = self.removeoutputduplicate(self.currentobj,self.PAs[0])

            self.fout.write(str(resultstr))
        if resultstr == defaultstr: skip = skipin # restoring original skip value

        # v v v v v v v v v v v v v v v v v v v v 2nd PA v v v v v v v v v v v v v v v v v v v v
        if self.Npa == 2: # if the current object has files for two PAs add a second line
            resultstr  = ' '+str("%.5d" % self.currentobj)+' '+str("%.3d" % self.PAs[1])

            defaultstr = resultstr
            for key in self.keys2:
                keyval    = str(self.keys2[key].get())
                if keyval == '-1':
                    defaultstr = defaultstr+' '+str(keyval)
                elif len(keyval) > 10: # for text keys
                    defaultstr = defaultstr+' '+keyval
                else:
                    defaultstr = defaultstr+' '+str(0)
                resultstr = resultstr+' '+str(keyval)

            # by-hand redshift info
            defaultstr = defaultstr+' -99 0'
            resultstr  = resultstr +' '+zbyhand

            # Multiple redshift solutions?
            defaultstr = defaultstr+' 0'
            resultstr  = resultstr+' '+self.mzsboxvar.get()

            # adding info from comment and wave fields
            defaultstr = defaultstr+'  #C#  \n'
            resultstr = resultstr  +'  #C# '+self.comments2.get()+' \n'

            if (resultstr == defaultstr) & (self.skipempty == True): skip = True
            if not skip:
                if self.duplicates:
                    Ndup = self.removeoutputduplicate(self.currentobj,self.PAs[1])

                self.fout.write(str(resultstr))
            if resultstr == defaultstr: skip = skipin # restoring original skip value

        # --- close and re-open output file so inspection is saved ---
        self.fout.close()
        self.fout = open(self.outfile,'a')

        # --- resetting widgets and closing windows ---
        self.comments.delete(0,END) # reset comment field
        self.comments2.delete(0,END) # reset comment field
        self.byhandz.delete(0,END)

        cluster, cluster_z = vi.getclusterz(self.file)
        self.varsliderz.set(cluster_z) # set intial value of slider
        self.varslidersmooth.set(0)    # set intial value of slider
        self.varsliderzqual.set(0)     # set intial value of slider

        self.checkboxes(self.cbpos) # reset check boxes
        self.checkboxes2(self.cbpos2) # reset check boxes
        self.modelbox.deselect()
        self.GiGlinesbox.deselect()
        self.mzsbox.deselect()

        self.closewindows()

        self.ds9open = False # resetting ds9 indicator
        self.focus_set() # set focus to main window
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def removeoutputduplicate(self,id,pa):
        """
        Subtract continuum from science fram
        """
        self.fout.close()
        idstr       = str("%.5d" % id)
        pastr       = str("%.3d" % pa)
        stringstart = ' '+idstr+' '+pastr
        file        = open(self.outfile,'r')
        lines       = file.readlines()
        file.close()
        file = open(self.outfile,"w")

        Ndup        = 0
        for line in lines:
            if line[0:10] != stringstart:
                file.write(line)
            else:
                if self.vb: print ' - Found dublicate entry for ID '+idstr+' PA '+pastr+' deleting it!'
                Ndup = Ndup+1

        file.close()
        self.fout = open(self.outfile,'a')
        return Ndup
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def closewindows(self):
        """
        Close PNG and DS9 windows
        """
        killsignal = 1     # see bash> man kill
        PIDkill    = True
        if PIDkill:
            try:
                os.kill(self.pngPID,killsignal)                  # close PNG window for currentobj
            except:
                print '   WARNING error occurred while trying to close PNG window(s)'

            if np.logical_or(((self.ds9open == True) & (self.xpa == False)),
                             ((self.xpa == True) & (self.quitting == True) & (self.ds9windowopen == True))):
                try:
                    os.kill(self.ds9PID,killsignal)                  # close DS9 window for currentobj
                except:
                    if self.vb: print ' - WARNING: Could not kill DS9 process id ',self.ds9PID
                rmout = commands.getoutput('rm '+self.regiontemp.replace('.reg','*.reg')) # removing ds9 region file
        else:
            print '=== WHAT ARE YOU DOING HERE?? ==='
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def skip_but(self,position):
        self.skip = Button(self)
        self.skip["text"] = "Skip object"
        self.skip["command"] = self.skip_but_cmd
        self.skip.grid(row=position[0],column=position[1],columnspan=position[2],sticky=W)
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def skip_but_cmd(self):
        """
        Command for skip button
        """
        self.reset(skip=True)

        if self.currentobj == self.objlist[-1]:
            if self.vb: print ' - Object',self.currentobj,' was the last in the list.\n   Quitting GUI.'
            self.quitting = True
            self.quit_but_cmd()
        else:
            newent = np.where(self.objlist == self.currentobj)[0]+1
            self.currentobj = self.objlist[newent][0]
            self.openpngs()
            self.labelvar.set(self.infostring())
            self.updateimage()
            if self.Npa != 2: self.checkboxes2(self.cbpos2,disable=True) # disable checkboxes2 if Npa not 2

            # load new data for plot and replot
            self.dataPlot_loaddata()
            self.dataPlot_plot(refresh=True,newobj=True)
            self.DPxlow_full, self.DPxhigh_full, self.DPylow_full, self.DPyhigh_full = \
                self.dataPlot_getwindowinfo() # store full window

            if self.fitsauto: # loading fits files automatically
                if self.xpa:
                    self.openfits_but_cmd_xpa()
                else:
                    self.openfits_but_cmd()
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def next_but(self,position):
        self.next = Button(self)
        self.next["text"] = "(8) Next object (save)"
        self.next["command"] = self.next_but_cmd
        self.next.grid(row=position[0],column=position[1],columnspan=position[2],sticky=W)
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def next_but_cmd(self):
        """
        Command for next button
        """
        self.reset()

        if self.currentobj == self.objlist[-1]:
            if self.vb: print ' - Object',self.currentobj,' was the last in the list.\n   Quitting GUI.'
            self.quitting = True
            self.quit_but_cmd()
        else:
            newent = np.where(self.objlist == self.currentobj)[0]+1
            self.currentobj = self.objlist[newent][0]
            self.openpngs()
            self.labelvar.set(self.infostring())
            self.updateimage()
            if self.Npa != 2: self.checkboxes2(self.cbpos2,disable=True) # disable checkboxes2 if Npa not 2

            # load new data for plot and replot
            self.dataPlot_loaddata()
            self.dataPlot_plot(refresh=True,newobj=True)
            self.DPxlow_full, self.DPxhigh_full, self.DPylow_full, self.DPyhigh_full = \
                self.dataPlot_getwindowinfo() # store full window

            if self.fitsauto: # loading fits files automatically
                if self.xpa:
                    self.openfits_but_cmd_xpa()
                else:
                    self.openfits_but_cmd()
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def prev_but(self,position):
        self.prev= Button(self)
        self.prev["text"] = "(7) Previous object"
        self.prev["command"] = self.prev_but_cmd
        self.prev.grid(row=position[0],column=position[1],columnspan=position[2],sticky=W)
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def prev_but_cmd(self):
        """
        Command for previous button
        """
        self.reset()

        if self.currentobj == self.objlist[0]:
            if self.vb: print ' - At first object of list...'
        else:
            newent = np.where(self.objlist == self.currentobj)[0]-1
            self.currentobj = self.objlist[newent][0]
            self.openpngs()
            self.labelvar.set(self.infostring())
            self.updateimage()
            if self.Npa != 2: self.checkboxes2(self.cbpos2,disable=True) # disable checkboxes2 if Npa not 2

            # load new data for plot and replot
            self.dataPlot_loaddata()
            self.dataPlot_plot(refresh=True,newobj=True)
            self.DPxlow_full, self.DPxhigh_full, self.DPylow_full, self.DPyhigh_full = \
                self.dataPlot_getwindowinfo() # store full window

            if self.fitsauto: # loading fits files automatically
                if self.xpa:
                    self.openfits_but_cmd_xpa()
                else:
                    self.openfits_but_cmd()
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def quit_but(self,position):
        """
        Set up the quit button
        """
        self.QUIT = Button(self)
        self.QUIT["text"] = "QUIT GiGz"
        self.QUIT["command"] = self.quit_but_cmd
        self.QUIT.grid(row=position[0],column=position[1],columnspan=position[2],sticky=W)
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def quit_but_cmd(self):
        """
        Command for quit button
        """
        if self.quitting == False: self.reset() # Only reset if quit_but_cmd was activated by quit button
        self.quitting = True
        self.fout.close()
        self.closewindows()
        self.dataPlotManager.destroy()
        if self.outcheck: self.checkoutput()
        self.quit()
        if self.vb: print ' - Quit GiGz successfully'
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def checkoutput(self):
        """
        Checking the output to see if it is as expected
        """
        data      = np.genfromtxt(self.outfile,comments='#',skip_header=2,names=True)
        Nobjout   = len(np.unique(data['ID']))
        Npaout    = len(np.unique(data['PA']))

        if self.vb: print ' - OUTPUTCHECK: Found '+str(Nobjout)+' objects in output. '+\
                          'Input objlist contained '+str(len(self.objlist))+' objects'
        if self.vb: print ' - OUTPUTCHECK: Found '+str(Npaout)+' PAs in output. '+\
                          'Input objlist had '+str(self.Npamax)+' PAs'
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def subtractcontam(self,twodfits):
        """
        Subtract continuum from science fram
        """
        filename, fileext =  os.path.splitext(twodfits)
        output = filename+'_SCI-CONTAM'+fileext

        if os.path.isfile(output): # check if file already exists
            if self.vb: print ' - ',output,' already exists'
        else:
            if self.vb: print ' - Create ',output
            hduimg  = pyfits.open(twodfits) # Load the FITS hdulist
            hdrsci  = hduimg['SCI'].header    # extracting science header
            sci     = hduimg['SCI'].data
            contam  = hduimg['CONTAM'].data
            pyfits.writeto(output, sci-contam, hdrsci, clobber=False)

        return output
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def keyboard_cmd(self,event):
        """
        Commands for keyboard shortcuts
        """
        cmd = event.char

        focuson = self.focus_get() # check where the focus is
        if  (focuson == self.comments) or (focuson == self.comments2) or \
            (focuson == self.byhandz):
            pass
        else:
            keycmd    = []
            keynames  = []
            keynumber = []
            for ii, key in enumerate(self.keys):
                keycmd.append(key[1])
                keynames.append(key)
                keynumber.append(ii)

            keycmd2    = []
            keynames2  = []
            keynumber2 = []
            for ii, key2 in enumerate(self.keys2):
                keycmd2.append(key2[1])
                keynames2.append(key2)
                keynumber2.append(ii)

            if cmd in keycmd:
                thiskey = keynames[np.where(np.asarray(cmd) == np.asarray(keycmd))[0]]
                if cmd in self.sliders:
                    sliderval = int(self.keys[thiskey].get())
                    if sliderval == 4:
                        self.sliderdic[thiskey].set(0)
                    else:
                        self.sliderdic[thiskey].set(sliderval+1)
                elif cmd in self.empty:
                    pass
                else:
                    self.cbdic[thiskey].toggle()

            elif (cmd in keycmd2) & (self.Npa == 2):
                thiskey2 = keynames2[np.where(np.asarray(cmd) == np.asarray(keycmd2))[0]]
                if cmd in self.sliders:
                    sliderval2 = int(self.keys2[thiskey2].get())
                    if sliderval2 == 4:
                        self.sliderdic2[thiskey2].set(0)
                    else:
                        self.sliderdic2[thiskey2].set(sliderval2+1)
                elif cmd in self.empty:
                    pass
                else:
                    self.cbdic2[thiskey2].toggle()

            elif cmd == 'l':
                self.comments.focus_set()

            elif cmd == 'L':
                self.comments2.focus_set()

            elif cmd == 'm':
                sliderval = float(self.slidersmooth.get())
                self.slidersmooth.set(sliderval+0.1)
            elif cmd == 'M':
                sliderval = float(self.slidersmooth.get())
                self.slidersmooth.set(sliderval-0.1)

            elif cmd == 'n':
                sliderval = float(self.sliderz.get())
                self.sliderz.set(sliderval+0.1)
            elif cmd == 'N':
                sliderval = float(self.sliderz.get())
                self.sliderz.set(sliderval-0.1)

            elif cmd == 'o':
                self.modelbox.toggle()

            elif cmd == 'p':
                self.GiGlinesbox.toggle()

            elif cmd == 'q':
                sliderval = int(self.sliderzqual.get())
                if sliderval == 4:
                    self.sliderzqual.set(0)
                else:
                    self.sliderzqual.set(sliderval+1)

            elif cmd == 'r':
                self.dataPlot_redrawbutton_cmd()

            elif cmd == 's':
                self.dataPlot_savebutton_cmd()

            elif cmd == 't':
                self.mzsbox.toggle()

            elif cmd == 'u':
                self.byhandz.focus_set()

            elif cmd == 'z':
                self.dataPlot_fullzoombutton_cmd()

            elif cmd == '0':
                if self.xpa:
                    self.openfits_but_cmd_xpa()
                else:
                    self.openfits_but_cmd()

            elif cmd == '7':
                self.prev_but_cmd()

            elif cmd == '8':
                self.next_but_cmd()

            else:
                pass
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def infostring(self):
        """
        Return string with information to display in GUI window
        """
        self.cluster, redshift = vi.getclusterz(self.file)
        infostr = "--- Currently looking at object "+str(self.currentobj)+\
                  ', PA(s) = '+str(self.PAs)+\
                  '  ('+self.cluster+' redshift = '+str(redshift)+') ---'

        return infostr
#-------------------------------------------------------------------------------------------------------------
class Application_m(Frame):
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def __init__(self,pdir,outfile,master=None,infofile=None,objlist=None,clusters=None,verbose=True,iname='John Doe',
                 ACSinspection=False,clobber=False,ds9xpa=False,openfitsauto=False,outputcheck=False,skipempty=False,
                 openpngseperately=False):
        """
        Intitialize the GUI

        -- INPUT --
        pdir              Directory containing the postage stamps
        outfile           Name of output file to create if it doesn't exists. Use clobber to overwrite.
        master            Provide another 'master' display. If None GUI created from scratch.
        objlist           List of objects to inspect. If 'None' all objects in 'dir' will be
                          inspected.
        clusters          If objlist is not None, provide the list of clusters the IDs correspond to
        verbose           Toggle verbosity.
        iname             Name of inspector to write in output file.
        ACSinspection     If inspecting ACS objects (not enabled as of 150423).
        clobber           Overwrites the output file if it already exists
        ds9xpa            If xpa is availbale for comunicating commands to ds9
                          set this keyword to tru and this will be used instead
                          of opening ds9 everytime the fits files are requested.

                          NB! XPA fix the number of frames. If more than Nframes images are available they
                              will not be shown. If all objects only have Nframes that's not a proble.
                              otherwise set ds9xpa = False

        openfitsauto      Automatically load the fits files into the DS9 window
                          when advancing to next (or previous) object.
        outputcheck       Checking the written output to see if it contains the expected number
                          of objects etc.
        skipempty         Set to True to ignore unedited objects when writing to output file.
                          Hence, if skipempty = True objects with no comments, flags set or sliders changed
                          will be written to the output
        openpngseperately By default the pngs are not opened in Preview/GThumb to avoid biasing the inspections
                          However, setting this keyword to true, will do that.
        """
        pp    = subprocess.Popen('ds9 -version',shell=True,executable=os.environ["SHELL"],stdout=subprocess.PIPE)
        ppout = pp.communicate()[0]
        self.ds9version = ppout.split()

        self.now         = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.vb          = verbose
        self.pdir        = pdir
        self.master      = master
        self.infofile    = infofile
        self.ds9open     = False # set ds9 indicator (used for ds9xpa = False)
        self.ds9windowopen = False # set ds9 indicator (used for ds9xpa = True)
        self.ACSins      = ACSinspection
        self.quitting    = False
        self.xpa         = ds9xpa # check if user indacetd that xpa was available for ds9
        self.fitsauto    = openfitsauto # Open fits files automatically?
        self.outcheck    = outputcheck
        self.skipempty   = skipempty
        self.openpngssep = openpngseperately
        if self.xpa:
            self.ds9windowopen = False

        if os.path.exists(self.pdir):
            self.twodfits = glob.glob(self.pdir)
        else:
            sys.exit(' - The directory '+self.pdir+' does not exist --> ABORTING')

        # -------- GET OBJIDS --------
        if objlist == None:
            searchext = '_rgb.png'

            self.file_2Dpng  = glob.glob(self.pdir+'*'+searchext)
            self.clusterlist = np.asarray([self.file_2Dpng[jj].split('/')[-1].split('_')[0]
                                           for jj in xrange(len(self.file_2Dpng))])
            self.objlist     = np.asarray([int(self.file_2Dpng[jj].split('/')[-1].split('_')[1])
                                           for jj in xrange(len(self.file_2Dpng))])
        else:
            if type(objlist) == str:
                self.objlist, self.clusterlist = np.genfromtxt(objlist,dtype=None,comments='#')
            else:
                self.objlist     = np.asarray(objlist)
                self.clusterlist = np.asarray(clusters)

        # ---- sort ids
        entsort = np.argsort(self.objlist)
        self.objlist = self.objlist[entsort]
        self.clusterlist = self.clusterlist[entsort]

        if len(self.objlist) == 0:
            sys.exit('  No valid IDs found \n            Forgot a forward slash after the objdir?')

        self.currentobj = self.objlist[0]                    # set the first id to look at
        self.currentcl  = self.clusterlist[0]

        if verbose: print " - Found "+str(len(self.objlist))+' objects to inspect'

        # -------- OPEN/PREPARE OUTPUT FILE --------
        if os.path.isfile(outfile) & (clobber == True): # check if file is to be overwritten
            overwrite = raw_input(' - clobber==True Are you sure you want to overwrite '+outfile+'? (y/n): ')
            if (overwrite == 'y') or (overwrite == 'yes'):
                print "   Okay, I'll remove the file and start a new one"
                os.remove(outfile)
            elif (overwrite == 'n') or (overwrite == 'no'):
                print "   Okay, I'll append to the existing file, then"
            else:
                sys.exit('   "'+overwrite+'" is not a valid answer --> Aborting')

        if os.path.isfile(outfile):
            newfile   = False
            self.fout = open(outfile,'r')                # open existing file
            IDinspected = np.array([])                  # array to contain IDs in file
            for line in self.fout.readlines():           # loop through file to last line
                lsplit = line.split()
                if lsplit[0] != '#':
                    IDinspected = np.append(IDinspected,float(lsplit[0]))
            if len(IDinspected) == 0:
                sys.exit('Found no inspected objects in '+outfile)
            lastline = line
            self.fout.close()

            lastID = lastline.split()[0]                     # get the last ID in file
            lastCL = lastline.split()[1]                     # get the last cluster in file

            if lastID != '#':
                objent = np.where((self.objlist == float(lastID)) & (self.clusterlist == lastCL))[0]
                if self.vb: print ' - The file '+outfile+' already exists (Resuming after last objects in output)'
                try:
                    self.currentobj = self.objlist[objent+1][0]      # change first id to look at
                    self.currentcl  = self.clusterlist[objent+1][0]  # change cluster for first id
                except:
                    sys.exit(' - The last object in the outputfile is the last in "objlist" --> ABORTING ')
                Nremaining = len(self.objlist[objent+1:])
                Ninspected = len(np.sort(IDinspected))
                if self.vb:
                    print ' - Info from existing output: '
                    print '   '+str(Nremaining)+' of '+str(len(self.objlist))+' objects still need to be expected'
                    print '   Found '+str(Ninspected)+' objects already inspected in file'
            else:
                if self.vb: print ' - The file '+outfile+' already exists (append as last row does not contain ID)'
            self.fout     = open(outfile,'a')
        else:
            if self.vb: print ' - The file '+outfile+' was created (did not exist)'
            self.fout     = open(outfile,'w')
            self.fout.write('# Results from Visual Inspection initiated on '+self.now+' \n')
            self.fout.write('# Inspector: '+iname+' \n')
            newfile = True

        self.outfile = outfile

        # -------- ADD LABEL --------
        self.openpngs() # open pngs for first object and set PA variables
        self.showingHamaps = False
        position = [0,0,1]
        self.labelvar = StringVar()
        label = Label(self.master,textvariable=self.labelvar)
        label.grid(row=position[0],column=position[1],columnspan=position[2],sticky=N)
        self.labelvar.set(self.infostring())

        # -------- CREATE WIDGETS --------
        fmain = Frame.__init__(self, self.master, bg="white")
        self.grid()
        self.create_widgets()

        # -------- ADD IMAGE WINDOWS --------
        self.updatepstamps()

        # -------- DRAW SEPERATORS --------
        self.drawsep(900,4,1  ,0,4,0, 2,899,4)
        self.drawsep(900,4,29 ,0,4,0, 2,899,4)
        #self.drawsep(900,4,60 ,0,4,0, 2,899,4)
        self.drawsep(900,4,80 ,0,4,0, 2,899,4)
        self.drawsep(900,4,110,0,4,0, 2,899,4)

        # -------- OPEN FITS FILES FOR FIRST OBJ --------
        if self.fitsauto: # loading fits files automatically
            if self.xpa:
                self.openfits_but_cmd_xpa()
            else:
                self.openfits_but_cmd()

        # -------- FINALIZE --------
        filehdr = '  '.join([key[3:] for key in self.keys])      # create header for output
        if newfile: self.fout.write('# ID cluster '+filehdr.replace(': ','_')+filehdr.replace('/','_')+' \n') # write header to output

        self.master.bind("<Key>", self.keyboard_cmd) # enable keyboard shortcuts
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def create_widgets(self):
        """
        Arrange the individual parts of the GUI
        postions are given as [row,column,span]
        """

        # -------- 1st PA --------
        self.cbpos = [5,0,1]
        self.checkboxes(self.cbpos)
        self.commentfield([self.cbpos[0]+6,2,1])

        self.openfits_but([65,3,1])

        self.prev_but([70,0,1])
        self.quit_but([70,1,1])
        self.skip_but([70,2,1])
        self.next_but([70,3,1])
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def drawsep(self,width,height,row,col,colspan,xleftbottom,yleftbottom,xrighttop,yrighttop):
        """
        Draw a seperator
        """
        cv = Canvas(self, width=width, height=height)
        cv.grid(row = row, column = col, columnspan = colspan, sticky=N)
        cv.create_rectangle(xleftbottom, yleftbottom, xrighttop, yrighttop,fill='black')
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def checkboxes(self,position,disable=False):
        """
        Checkboxes for keywords to assign to object
        """
        self.dirstr = 'direct_'
        self.Ncol  = 4.

        self.sliders      = [] #['d','D','l','L']
        self.empty        = ['o','p','v','w','y','z']
        self.Haboxes      = ['i','j','k','l','m','n','q','r','s','t','u']
        self.calculations = []
        colors            = self.getcolors()

        # Note that letters in () enables sorting of boxes
        self.keys = {}
        self.keys['(a) Img: Elliptical']  = 0
        self.keys['(b) Img: S0']  = 0
        self.keys['(c) Img: Spiral']  = 0
        self.keys['(d) Img: Hubble_Unclassified']  = 0

        self.keys['(e) Img: Irregular']  = 0
        self.keys['(f) Img: Merging']  = 0
        self.keys['(g) Img: Do_not_know']  = 0
        self.keys['(h) Img: Star/Defect']  = 0

        self.keys['(i) Ha: Regular'] = 0
        self.keys['(j) Ha: Clumpy'] = 0
        self.keys['(k) Ha: Concentrated']  = 0
        self.keys['(l) Ha: Assymmetric_Jellyfish']  = 0

        self.keys['(m) Ha: Other'] = 0
        self.keys['(n) Ha: No_Halpha'] = 0
        self.keys['(o) empty1']  = 0
        self.keys['(p) empty2']  = 0

        self.keys['(q) Process: Regular'] = 0
        self.keys['(r) Process: Ram_Pressure'] = 0
        self.keys['(s) Process: Major_Merger']  = 0
        self.keys['(t) Process: Minor_Merger']  = 0

        self.keys['(u) Process: Other']  = 0
        #self.keys['(v) empty3'] = 0
        #self.keys['(w) empty4']  = 0
        self.keys['(x) Uncertain'] = 0

        #self.keys['(y) empty5'] = 0
        #self.keys['(z) empty6'] = 0

        if (sys.version_info[0] == 2) & (sys.version_info[1] == 7): # sort dictionary if running python 2.7
            import collections
            self.keys = collections.OrderedDict(sorted(self.keys.items()))
        else:
            print 'WARNING Python version not 2.7 so not sorting dictionary of keywords(1)'

        Nkey = 0
        self.cbdic     = {}
        self.sliderdic = {}
        for key in self.keys:
            rowval = position[0]+int(np.floor(Nkey/self.Ncol))
            colval = position[1]+int(np.round((Nkey/self.Ncol-np.floor((Nkey/self.Ncol)))*self.Ncol))

            self.keys[key] = Variable()

            if key[1] in self.sliders:
                self.slider = Scale(self, from_=0, to=4,label=key,variable = self.keys[key],
                                    orient=HORIZONTAL,background=colors[key[1]],length=200)
                self.slider.grid(row=rowval,column=colval,columnspan=position[2],rowspan=2,sticky=W)
                self.slider.set(0)

                if disable:
                    self.slider.configure(state='disabled')
                else:
                    self.sliderdic[key] = self.slider
            elif key[1] in self.empty:
                self.cb = Checkbutton(self, text=' ')
                self.cb.grid(row=position[0]+5,column=0,columnspan=1,sticky=W)
                self.cb.deselect()
                self.keys[key].set('-1')
                if key[1] in self.calculations:
                    self.keys[key].set(key)
            else:
                self.cb = Checkbutton(self, text=key, variable=self.keys[key],background=colors[key[1]])
                if key[1] == 'x': # manually shifting the 'uncertain' checkbox
                    rowval = rowval+1

                self.cb.grid(row=rowval,column=colval,columnspan=position[2],sticky=W)
                self.cb.deselect()

                if disable:
                    self.cb.configure(state='disabled')
                elif key[1] in self.Haboxes:
                    self.cb.configure(state='disabled')
                    self.keys[key].set('-1')
                else:
                    self.cbdic[key] = self.cb

            Nkey = Nkey + 1
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def enableHaboxes(self,position):
        """
        Enable Ha-related checkboxes
        """
        colors = self.getcolors()
        Nkey = 0
        for key in self.keys:
            rowval = position[0]+int(np.floor(Nkey/self.Ncol))
            colval = position[1]+int(np.round((Nkey/self.Ncol-np.floor((Nkey/self.Ncol)))*self.Ncol))
            if key[1] in self.Haboxes:
                self.keys[key] = Variable()
                self.cb = Checkbutton(self, text=key, variable=self.keys[key],background=colors[key[1]])
                self.cb.grid(row=rowval,column=colval,columnspan=position[2],sticky=W)
                self.cb.configure(state='active')
                self.cb.deselect()
                self.cbdic[key] = self.cb
            Nkey = Nkey + 1

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def getcolors(self,):
        """
        Dictionary with colors for keys
        """
        collist = ['orange','red','cyan','magenta','green','white']
        colors  = {}
        colors['a'] = collist[4]
        colors['b'] = collist[4]
        colors['c'] = collist[4]
        colors['d'] = collist[4]
        colors['e'] = collist[4]
        colors['f'] = collist[4]
        colors['g'] = collist[4]
        colors['h'] = collist[0]
        colors['i'] = collist[1]
        colors['j'] = collist[1]
        colors['k'] = collist[1]
        colors['l'] = collist[1]
        colors['m'] = collist[1]
        colors['n'] = collist[1]
        colors['o'] = collist[1]
        colors['p'] = collist[3]
        colors['q'] = collist[2]
        colors['r'] = collist[2]
        colors['s'] = collist[2]
        colors['t'] = collist[2]
        colors['u'] = collist[2]
        colors['v'] = collist[3]
        colors['w'] = collist[3]
        colors['x'] = collist[0]
        colors['y'] = collist[3]
        colors['z'] = collist[3]

        return colors
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def commentfield(self,position):
        """
        Field to provide comments
        """
        self.label = Label(self,text='(p) Comments ("tab" to move focus):  ')
        self.label.grid(row=position[0],column=position[1],columnspan=position[2],sticky=W)
        self.comments = Entry(self)
        self.comments.grid(row=position[0],column=position[1]+position[2],columnspan=position[2],sticky=W)
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def openpngs(self):
        """
        Function to open pngs of object
        """
        self.objhasHa = False # resetting Halpha flag

        idstr = str("%05d" % self.currentobj)
        self.pstamplist = glob.glob(self.pdir+self.currentcl+'_'+idstr+'*.png')
        self.Nstamps = len(self.pstamplist)

        self.Hamap = self.pdir+self.currentcl+'_'+idstr+'_ha.png'
        if self.Hamap in self.pstamplist:
            self.objhasHa = True

        if len(self.pstamplist) == 0:
            sys.exit(' - Did not find any png files to open. Looked for '+
                     self.pdir+self.currentcl+'_'+idstr+'*.png  --> ABORTING')

        self.file = self.pstamplist[0].split('/')[-1]


        rgbs    = [name for name in self.pstamplist if name.endswith("rgb.png")]
        f475s   = [name for name in self.pstamplist if name.endswith("f475w.png")]
        f105s   = [name for name in self.pstamplist if name.endswith("f105w.png")]
        f140s   = [name for name in self.pstamplist if name.endswith("f140w.png")]
        f160s   = [name for name in self.pstamplist if name.endswith("f160w.png")]
        f475Has = [name for name in self.pstamplist if name.endswith("f475w_ha.png")]
        f105Has = [name for name in self.pstamplist if name.endswith("f105w_ha.png")]
        f140Has = [name for name in self.pstamplist if name.endswith("f140w_ha.png")]
        f160Has = [name for name in self.pstamplist if name.endswith("f160w_ha.png")]

        pngorderedlist  = rgbs + f475s + f105s + f105s + f140s + f160s + f475Has + f105Has + f105Has + f140Has + f160Has
        remaining       = list(set(self.pstamplist) - set(pngorderedlist)) # get files not accounted for above (ha map)
        self.pstamplist = pngorderedlist + remaining                       # save ordered list as main file list

        if self.openpngssep:
            pngorderedlist  = self.pstamplist
            self.plat = sys.platform
            if self.plat == 'darwin':
                import platform
                macversion = platform.mac_ver()[0]
                if float(macversion.split('.')[1]) > 6: # check if "open -F" is available (mac OS X 10.7.0 and above)
                    opencmd = 'open -n -F '+' '.join(pngorderedlist)
                else:
                    opencmd = 'open -n '+' '.join(pngorderedlist)
            elif self.plat == 'linux2' or 'Linux':
                opencmd = 'gthumb '+' '.join(pngorderedlist)+' &'

            self.pPNG = subprocess.Popen(opencmd,shell=True,executable=os.environ["SHELL"])
            time.sleep(1.1)# sleep to make sure png appear in PIDlist
            if self.plat == 'darwin':
                self.pngPID = vi.getPID('Preview.app',verbose=False) # get PID of png process
            elif self.plat == 'linux2' or 'Linux':
                self.pngPID = vi.getPID('gthumb',verbose=False)      # get PID of png process
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def openfits_but(self,position):
        """
        Button to open fits files
        """
        self.fitsb = Button(self)
        self.fitsb["text"] = "(0) Open fits files"
        if self.xpa:
            self.fitsb["command"] = self.openfits_but_cmd_xpa
        else:
            self.fitsb["command"] = self.openfits_but_cmd

        self.fitsb.grid(row=position[0],column=position[1],columnspan=position[2],sticky=W)
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def openfits_but_cmd_xpa(self):
        """
        Command for openfits button
        """
        self.regiontemp = 'temp_ds9_forinspection.reg'
        idstr   = str("%05d" % self.currentobj)
        lockstr = self.lockds9string()
        ds9cmd  = ' '

        if not self.ds9windowopen:
            ds9cmd = ds9cmd+'ds9 -geometry 1000x600 -scale zscale '+lockstr+' -tile grid layout 4 1'
            self.pds9   = subprocess.Popen(ds9cmd,shell=True,executable=os.environ["SHELL"])
            time.sleep(1.1)# sleep to make sure ds9 appear in PIDlist
            self.ds9PID = vi.getPID('ds9',verbose=False) # get PID of DS9 process
            self.ds9windowopen = True
            time.sleep(1.0)
            out = commands.getoutput('xpaset -p ds9 frame new rgb')
            out = commands.getoutput('xpaset -p ds9 frame new')
            out = commands.getoutput('xpaset -p ds9 frame new')
            out = commands.getoutput('xpaset -p ds9 frame new')
            out = commands.getoutput('xpaset -p ds9 frame 1')
            out = commands.getoutput('xpaset -p ds9 frame hide')

            out = commands.getoutput('xpaset -p ds9 tile')

        Fstart = 2
        for pstamp in self.pstamplist:
            pstampname = '_'.join(pstamp.split('.')[0].split('_')[2:])
            fitsstamp  = pstamp.replace('.png','.fits')

            if fitsstamp.endswith('_ha.fits'):
                pass
            else:
                out = commands.getoutput('xpaset -p ds9 frame '+str(Fstart))
                if 'rgb' in fitsstamp:
                    out = commands.getoutput('xpaset -p ds9 rgb red')
                    out = commands.getoutput('xpaset -p ds9 file '+fitsstamp.replace('rgb','rgb_r')+'[0]')
                    out = commands.getoutput('xpaset -p ds9 rgb green')
                    out = commands.getoutput('xpaset -p ds9 file '+fitsstamp.replace('rgb','rgb_g')+'[0]')
                    out = commands.getoutput('xpaset -p ds9 rgb blue')
                    out = commands.getoutput('xpaset -p ds9 file '+fitsstamp.replace('rgb','rgb_b')+'[0]')
                else:
                    regionfile = self.regiontemp.replace('.reg',pstampname+'.reg')
                    self.ds9textregion(pstampname,filename=regionfile)
                    out = commands.getoutput('xpaset -p ds9 file '+fitsstamp+'[0]')
                    out = commands.getoutput('xpaset -p ds9 regions '+regionfile)
                Fstart += 1

        out = commands.getoutput('xpaset -p ds9 zoom to fit')

        if self.showingHamaps: # sho the Halpha map fits file
            pstampname = 'Halpha'
            fitsstamp  = self.Hamap.replace('.png','.fits')
            out = commands.getoutput('xpaset -p ds9 frame '+str(Fstart))
            regionfile = self.regiontemp.replace('.reg',pstampname+'.reg')
            self.ds9textregion(pstampname,filename=regionfile)
            out = commands.getoutput('xpaset -p ds9 file '+fitsstamp+'[0]')
            out = commands.getoutput('xpaset -p ds9 regions '+regionfile)
            Fstart += 1
        else:
            out = commands.getoutput('xpaset -p ds9 frame '+str(Fstart))
            out = commands.getoutput('xpaset -p ds9 frame clear')
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def openfits_but_cmd(self):
        """
        Command for openfits button
        """
        self.ds9open = True
        self.regiontemp = 'temp_ds9_forinspection.reg'
        idstr   = str("%05d" % self.currentobj)
        lockstr = self.lockds9string()

        ds9cmd  = 'ds9 -rgb -geometry 1000x600 -scale zscale '+lockstr+' -tile grid layout 4 1 -frame 1 -frame hide '

        Fstart = 2
        for pstamp in self.pstamplist:
            pstampname = '_'.join(pstamp.split('.')[0].split('_')[2:])
            fitsstamp  = pstamp.replace('.png','.fits')
            if fitsstamp.endswith('_ha.fits'):
                pass
            else:
                if 'rgb' in fitsstamp:
                    ds9cmd = ds9cmd+' -frame '+str(Fstart)+' -red "'+fitsstamp.replace('rgb','rgb_r')+'[0]" '+\
                             ' -frame '+str(Fstart)+' -green "'+fitsstamp.replace('rgb','rgb_g')+'[0]" '+\
                             ' -frame '+str(Fstart)+' -blue "'+fitsstamp.replace('rgb','rgb_b')+'[0]" '
                else:
                    regionfile = self.regiontemp.replace('.reg',pstampname+'.reg')
                    self.ds9textregion(pstampname,filename=regionfile)
                    ds9cmd = ds9cmd+' -frame '+str(Fstart)+' "'+fitsstamp+'[0]" '+\
                             ' -frame '+str(Fstart)+' -region '+regionfile+' '
                Fstart += 1

        if self.showingHamaps: # sho the Halpha map fits file
            pstampname = 'Halpha'
            fitsstamp  = self.Hamap.replace('.png','.fits')
            regionfile = self.regiontemp.replace('.reg',pstampname+'.reg')
            self.ds9textregion(pstampname,filename=regionfile)
            ds9cmd = ds9cmd+' -frame '+str(Fstart)+' "'+fitsstamp+'[0]" '+\
                     ' -frame '+str(Fstart)+' -region '+regionfile+' '
        ds9cmd = ds9cmd+' -tile yes -zoom to fit'
        print ds9cmd
        self.pds9   = subprocess.Popen(ds9cmd,shell=True,executable=os.environ["SHELL"])
        time.sleep(1.1)# sleep to make sure ds9 appear in PIDlist
        self.ds9PID = vi.getPID('ds9',verbose=False) # get PID of DS9 process
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def lockds9string(self):
        """
        """
        if int(self.ds9version[1].split('.')[0]) >= 7: # only lock if ds9 version is 7 or later
            lockstr = ' -lock frame physical '
        else:
            print ' - WARNING DS9 version older than 7.*; Not locking frames.'
            lockstr = ' '

        return lockstr
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def ds9textregion(self,text,filename='temp.reg'):
        """
        Create ds9 region file with text string
        Note that it's overwriting any existing file!
        """
        regstr = 'physical\n# text(30,5) textangle=0 textrotate=0 font="helvetica 12 normal roman" text={'+text+'}'
        fds9region = open(filename,'w')
        fds9region.write(regstr)
        fds9region.close()
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def set_imgmap(self,position,namekey):
        imgname = self.pstamplist[0] # setting default imgname (just the first in list of images)
        for pstamp in self.pstamplist:
            if namekey in pstamp: imgname = pstamp
        img = ImageTk.PhotoImage(Image.open(imgname).resize((self.imgx,self.imgy),Image.ANTIALIAS))
        self.imageframe = Label(self, image=img)
        self.imageframe.image = img
        self.imageframe.grid(row = position[0], column = position[1], columnspan = position[2], sticky=N+W+E+S)

        return self.imageframe
    # - - - - - - - - - - - - - - - - -  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def updatepstamps(self,ha=False):
        """
        update postage stamp images in GUI
        """
        self.imgx,self.imgy = 220, 220
        rownumberstart = 100
        if ha:
            self.f475wHa_imgframe  = self.set_imgmap([rownumberstart + 0,1,1],'_f475w_ha')
            self.f105wHa_imgframe  = self.set_imgmap([rownumberstart + 0,2,1],'_f140w_ha')
            self.ha_imgframe       = self.set_imgmap([rownumberstart + 0,3,1],'_ha')
        else:
            self.rgb_imgframe      = self.set_imgmap([rownumberstart + 0,0,1],'_rgb.')
            self.f475w_imgframe    = self.set_imgmap([rownumberstart + 0,1,1],'_f475w.')
            self.f105w_imgframe    = self.set_imgmap([rownumberstart + 0,2,1],'_f140w.')
            try:
                self.ha_imgframe.grid_forget()
            except:
                pass

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def reset(self,skip=False):
        """
        Writing results to output, resetting checkboxes, and closing DS9 and PNG windows

        if skip=True nothing will be written to output file.
        """
        resultstr  = ' '+str("%.5d" % self.currentobj)+' '+str(self.currentcl)
        defaultstr = resultstr
        for key in self.keys:
            keyval    = self.keys[key].get()
            if keyval == '-1':
                defaultstr = defaultstr+' '+str(keyval)
            elif len(keyval) > 10: # for text keys
                defaultstr = defaultstr+' '+keyval
            else:
                defaultstr = defaultstr+' '+str(0)
            resultstr = resultstr+' '+str(keyval)

        # adding info from comment and wave fields
        resultstr  = resultstr+'  #C# '+self.comments.get()+' \n'

        # check if format of ouput is good (i.e., is more than one value set in each category?)
        self.goodformat = True
        resultsplit = resultstr.split(' ')
        if resultsplit[3:10].count('1')  != 1: self.goodformat = False  # img checkboxes
        if (resultsplit[11:17].count('1') != 1) & ('-1' not in resultsplit[11:17]): self.goodformat = False  # Ha CBs
        if (resultsplit[19:24].count('1') != 1) & ('-1' not in resultsplit[11:17]): self.goodformat = False  # process CBs

        if self.goodformat or skip:
            skipin = skip # storing original skip value
            if (resultstr == defaultstr) & (self.skipempty == True): skip = True
            if not skip:
                self.fout.write(str(resultstr))
            if resultstr == defaultstr: skip = skipin # restoring original skip value

            # --- close and re-open output file so inspection is saved ---
            self.fout.close()
            self.fout = open(self.outfile,'a')

            # --- resetting widgets and closing windows ---
            self.comments.delete(0,END) # reset comment field

            self.checkboxes(self.cbpos) # reset check boxes

            self.closewindows()

            self.ds9open = False # resetting ds9 indicator
            self.focus_set() # set focus to main window
        else:
            print ' WARNING: You should set at least one, but only one, checkbox in each category - Fix before advancing.'
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def removeoutputduplicate(self,id):
        """
        Subtract continuum from science fram
        """
        self.fout.close()
        idstr       = str("%.5d" % id)
        stringstart = ' '+idstr
        file        = open(self.outfile,'r')
        lines       = file.readlines()
        file.close()
        file = open(self.outfile,"w")

        Ndup        = 0
        for line in lines:
            if line.startswith(stringstart):
                file.write(line)
            else:
                if self.vb: print ' - Found dublicate entry for ID '+idstr+' deleting it!'
                Ndup = Ndup+1

        file.close()
        self.fout = open(self.outfile,'a')
        return Ndup

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def closewindows(self):
        """
        Close PNG and DS9 windows
        """
        killsignal = 1     # see bash> man kill
        PIDkill    = True
        if PIDkill:
            if self.openpngssep:
                try:
                    os.kill(self.pngPID,killsignal)                  # close PNG window for currentobj
                except:
                    print '   WARNING error occurred while trying to close PNG window(s)'

            if np.logical_or(((self.ds9open == True) & (self.xpa == False)),
                             ((self.xpa == True) & (self.quitting == True) & (self.ds9windowopen == True))):
                try:
                    os.kill(self.ds9PID,killsignal)                  # close DS9 window for currentobj
                except:
                    if self.vb: print ' - WARNING: Could not kill DS9 process id ',self.ds9PID
                rmout = commands.getoutput('rm '+self.regiontemp.replace('.reg','*.reg')) # removing ds9 region file
        else:
            print '=== WHAT ARE YOU DOING HERE?? ==='
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def skip_but(self,position):
        self.skip = Button(self)
        self.skip["text"] = "Skip object"
        self.skip["command"] = self.skip_but_cmd
        self.skip.grid(row=position[0],column=position[1],columnspan=position[2],sticky=W)
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def skip_but_cmd(self):
        """
        Command for skip button
        """
        self.reset(skip=True)

        if self.currentobj == self.objlist[-1]:
            if self.vb: print ' - Object',self.currentobj,' was the last in the list.\n   Quitting GUI.'
            self.quitting = True
            self.quit_but_cmd(skip=True)
        else:
            newent = np.where((self.objlist == self.currentobj) & (self.clusterlist == self.currentcl))[0]+1
            self.currentobj = self.objlist[newent][0]
            self.currentcl  = self.clusterlist[newent][0]
            self.openpngs()
            self.showingHamaps = False
            self.labelvar.set(self.infostring())
            self.updatepstamps()

            if self.fitsauto: # loading fits files automatically
                if self.xpa:
                    self.openfits_but_cmd_xpa()
                else:
                    self.openfits_but_cmd()
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def next_but(self,position):
        self.next = Button(self)
        self.next["text"] = "(8) Next object (save)"
        self.next["command"] = self.next_but_cmd
        self.next.grid(row=position[0],column=position[1],columnspan=position[2],sticky=W)
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def next_but_cmd(self):
        """
        Command for next button
        """
        if (self.currentobj == self.objlist[-1]) & (self.currentcl == self.clusterlist[-1]):
            if self.vb: print ' - Object '+self.currentcl+'_'+str("%.5d" % self.currentobj)+\
                              ' was the last in the list.\n   Quitting GUI.'
            self.reset()
            if self.goodformat:
                self.quitting = True
                self.quit_but_cmd()
        else:
            if self.objhasHa:
                self.showingHamaps = True
                self.updatepstamps(ha=True)
                self.enableHaboxes(self.cbpos)
                self.objhasHa = False # resetting Halpha flag
            else:
                self.reset()
                if self.goodformat:
                    newent = np.where((self.objlist == self.currentobj) & (self.clusterlist == self.currentcl))[0]+1
                    self.currentobj = self.objlist[newent][0]
                    self.currentcl  = self.clusterlist[newent][0]
                    self.openpngs()
                    self.showingHamaps = False

                    self.labelvar.set(self.infostring())
                    self.updatepstamps()

                    if self.fitsauto: # loading fits files automatically
                        if self.xpa:
                            self.openfits_but_cmd_xpa()
                        else:
                            self.openfits_but_cmd()
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def prev_but(self,position):
        self.prev= Button(self)
        self.prev["text"] = "(7) Previous object"
        self.prev["command"] = self.prev_but_cmd
        self.prev.grid(row=position[0],column=position[1],columnspan=position[2],sticky=W)
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def prev_but_cmd(self):
        """
        Command for previous button
        """
        self.reset()
        if self.goodformat:
            if (self.currentobj == self.objlist[0]) & (self.currentcl == self.clusterlist[0]):
                if self.vb: print ' - At first object of list...'
            else:
                newent = np.where((self.objlist == self.currentobj) & (self.clusterlist == self.currentcl))[0]-1
                self.currentobj = self.objlist[newent][0]
                self.currentcl  = self.clusterlist[newent][0]
                self.openpngs()
                self.showingHamaps = False
                self.labelvar.set(self.infostring())
                self.updatepstamps()

                if self.fitsauto: # loading fits files automatically
                    if self.xpa:
                        self.openfits_but_cmd_xpa()
                    else:
                        self.openfits_but_cmd()
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def quit_but(self,position):
        """
        Set up the quit button
        """
        self.QUIT = Button(self)
        self.QUIT["text"] = "QUIT GiG"
        self.QUIT["command"] = self.quit_but_cmd
        self.QUIT.grid(row=position[0],column=position[1],columnspan=position[2],sticky=W)
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def quit_but_cmd(self,skip=False):
        """
        Command for quit button
        """
        if self.quitting == False: self.reset() # Only reset if quit_but_cmd was activated by quit button
        if self.goodformat or skip:
            self.quitting = True
            self.fout.close()
            self.closewindows()
            if self.outcheck: self.checkoutput()
            self.quit()
            if self.vb: print ' - Quit GiG successfully'
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def checkoutput(self):
        """
        Checking the output to see if it is as expected
        """
        data      = np.genfromtxt(self.outfile,comments='#',skip_header=2,names=True)
        Nobjout   = len(np.unique(data['ID']))

        if self.vb: print ' - OUTPUTCHECK: Found '+str(Nobjout)+' objects in output. '+\
                          'Input objlist contained '+str(len(self.objlist))+' objects'
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def subtractcontam(self,twodfits):
        """
        Subtract continuum from science fram
        """
        filename, fileext =  os.path.splitext(twodfits)
        output = filename+'_SCI-CONTAM'+fileext

        if os.path.isfile(output): # check if file already exists
            if self.vb: print ' - ',output,' already exists'
        else:
            if self.vb: print ' - Create ',output
            hduimg  = pyfits.open(twodfits) # Load the FITS hdulist
            hdrsci  = hduimg['SCI'].header    # extracting science header
            sci     = hduimg['SCI'].data
            contam  = hduimg['CONTAM'].data
            pyfits.writeto(output, sci-contam, hdrsci, clobber=False)

        return output
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def keyboard_cmd(self,event):
        """
        Commands for keyboard shortcuts
        """
        cmd = event.char

        focuson = self.focus_get() # check where the focus is
        if  (focuson == self.comments):
            pass
        else:
            keycmd    = []
            keynames  = []
            keynumber = []
            for ii, key in enumerate(self.keys):
                keycmd.append(key[1])
                keynames.append(key)
                keynumber.append(ii)

            if cmd in keycmd:
                thiskey = keynames[int(np.where(np.asarray(cmd) == np.asarray(keycmd))[0])]
                if cmd in self.sliders:
                    sliderval = int(self.keys[thiskey].get())
                    if sliderval == 4:
                        self.sliderdic[thiskey].set(0)
                    else:
                        self.sliderdic[thiskey].set(sliderval+1)
                elif cmd == 'p':
                    self.comments.focus_set()
                elif cmd in self.empty:
                    pass
                elif (cmd in self.Haboxes) & (not self.showingHamaps):
                    pass
                else:
                    self.cbdic[thiskey].toggle()

            elif cmd == '0':
                if self.xpa:
                    self.openfits_but_cmd_xpa()
                else:
                    self.openfits_but_cmd()

            elif cmd == '7':
                self.prev_but_cmd()

            elif cmd == '8':
                self.next_but_cmd()

            else:
                pass
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def infostring(self):
        """
        Return string with information to display in GUI window
        """
        objinfo           = vi.get_objinfo(self.infofile,self.currentobj,self.currentcl)

        if objinfo == None:
            infostr = "--- Currently looking at object "+self.currentcl+'_'+str("%.5d" % int(self.currentobj))+\
                      ':: Environment = None, redshift = None, mag = None ---'
        else:
            infostr = "--- Currently looking at object "+self.currentcl+'_'+str("%.5d" % int(self.currentobj))+\
                      ':: Environment = '+str(objinfo['environment'][0])+\
                      ', redshift = '+str(objinfo['redshift'][0])+\
                      ', '+str(objinfo['mag_band'][0])+'  = '+\
                      str("%.2f" % objinfo['mag'])+'+/-'+str("%.2f" % objinfo['mag_err'])+' ---'

        return infostr

#-------------------------------------------------------------------------------------------------------------
#                                                      END
#-------------------------------------------------------------------------------------------------------------


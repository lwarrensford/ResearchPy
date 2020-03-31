"""
Automates the retrieval of files necessary for ZINC files from a given list
of ZINC IDs. Also automates the dynamics and evaluates the energies. 

-Luke Warrensford 10/19
"""

import os
import time
import os.path

import urllib.request
import httplib2
from bs4 import BeautifulSoup, SoupStrainer

capture = False

def GetLink():
    # uses a module, might not work right now
    http = httplib2.Http()
    status, response = http.request('http://www.zinc.docking.org/substance/' + zincs[i][5,] + '.com')
    first_link = soup.a
    return first_link

def PullFiles():
    os.system('mkdir ' + zincs[i])
    os.system('cp -r master/. /work/l/lwarrensford/' + zincs[i] + '/.')
    os.chdir('/work/l/lwarrensford/' + zincs[i])
    os.system('source setup-charmm.sh')
    
    # NEED TO FIND A WAY TO IMPORT MOL2 FILE *** WIP ***
    GetLink()
    urllib.request.urlretrieve(first_link, '/work/l/lwarrensford/' + zincs[i] + '.mol2')
    
    os.system('babel -imol2 ' + zincs[i] + '.mol2 -opdb ' + zincs[i] + '.pdb')
    os.system('vim ' + zincs[i])
    os.system(':%s/<0>/MOL/g')
    os.system(':%s/ A /   /g')
    os.system(':x')

    # Copies the relevant part of the master stream file to create zinc
    # specific stream file. *** Work in progress, not yet tested ***
    os.system('touch ' + zincs[i] + '.str')
    with open("maybhit_all.str", r) as all_strs:
        lines = all_strs.readlines()
        for line in range(0, len(lines)):
            lines[line] = str(lines[line])
            line = lines[line].split()
            try:
                if line[0][9:17] == zincs[i]:
                    capture = True
                else:
                    continue
            except IndexError:
                continue
            try:
                if capture == True and line != 'END':
                        with open(zincs[i] + '.str', w) as stream:
                        stream.append(line[0])
                elif capture == True and line[0] == 'END':
                    capture = False
                    continue
                else:
                    continue
            except IndexError:
                continue

def RunMM():
    os.system('$CHARMM stream=' + zincs[i] + ' name=mol -i generate.inp -o generate.out')
    time.sleep(20)
    if os.path.isfile('generate.out'):
        os.system('sbatch dyna.slu ' + zincs[i] + ' mol')
        print("Dynamics of " + zincs[i] + " running...")
    else:
        print("Generation of " + zincs[i] + " failed!")

def Eval():
    if os.path.isfile('dyna-mol.out'):
        os.chdir('/work/l/lwarrensford/' + zincs[i])
        os.system('sbatch eval_mm.slu ' + zincs[i] + ' mol mm')
        os.system('sbatch eval_3ob.slu ' + zincs[i] + 'mol mm')
        print("Evaluations of " + zincs[i] + " running...")
    else:
        print("Dynamics of " + zincs[i] + " failed!")

def Fep():
    if os.path.isfile('eval_mol-mm-3ob.out'):
        os.system("paste energy/mol.mm.mm.ene energy/mol.mm.3ob.ene | awk '{printf%.5f\n\",$4-$2}' > mol.mm.3ob.fw")
        os.system('/bin/bash scripts/fep-bot.sh mol.mm.3ob.fw > da-fep-mm-3ob.dat')
    else:
        print("Either evaluations have failed or are incomplete!")

zincs = ['ZINC_01042543']

for i in range(0, len(zincs)):
    PullFiles()
    RunMM()
    time.sleep(1800)
    Eval()
    time.sleep(600)
    Fep()

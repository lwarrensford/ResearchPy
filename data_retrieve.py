import os
import os.path
import glob

"""
Retrieves temp files from various nodes on the computing cluster by 
checking the SLURM output files.

-Luke Warrensford 8/18
"""

# Put the names of your ZINC molecules in this list
zincs = ['zinc_00061095', 'zinc_00077329', 'zinc_00079729', 'zinc_00086442', 
    'zinc_00087557', 'zinc_00095858', 'zinc_00107550', 'zinc_00107778', 
    'zinc_00123162', 'zinc_00133435', 'zinc_00138607', 'zinc_00140610', 
    'zinc_00164361', 'zinc_00167648', 'zinc_01036618'
    ]

for i in range(0, len(zincs)):
# loops through outputs and uses that info for scp
    os.chdir(zincs[i])
    os.system('mkdir switches')
    for filename in glob.glob('slurm*.out'):
        with open(filename) as readOutput:
            oLines = readOutput.readlines()
            for line in range(0, len(oLines)):
                oLines[line] = str(oLines[line])
                oLine = oLines[line].split()
                try:
                    if oLine[0][0:3] == 'svc':
                        node = str(oLine)
                        print('NODE FOUND')
                        keep = True
                    elif oLine[0][0:4] == 'zinc' and keep:
                        zincID = str(oLine[0])
                        randID = str(oLine[2])
                        start = str(oLine[3])
                        finish = str(oLine[4])
                        keep = False
                        os.system('scp lwarrensford@' + node + ':/tmp/' + zincs[i] + 
                            '-' + randID + '-fswi-' + start + '-' + finish + '/switches-' + 
                            zincs[i] + '-' + randID + '-' + start + '-' + finish + 
                            '.tar.gz /work/l/lwarrensford/hipen23/' + zincs[i] + '/switches/.'
                            )
                        print("COPYING TAR...")
                        os.system('scp -r lwarrensford@' + node + ':/tmp/' + zincs[i] + 
                            '-' + randID + '-fswi-' + start + '-' + finish + 
                            '/data/ /work/l/lwarrensford/hipen23/' + zincs[i] + '/.'
                            )
                        print("COPYING FOLDER...")
                        os.chdir('/work/l/lwarrensford/hipen23/' + zincs[i])
                    else:
                        continue
                except IndexError:
                    continue
    os.chdir('/work/l/lwarrensford/hipen23')

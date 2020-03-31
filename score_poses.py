"""
Script for taking poses generated from docking (tailored to CIFDock in this case)
and score them directly from the command line using Schrodinger's built-in
Glide Python script.

-Luke Warrensford 2/14/2020
"""

import os
import os.path
import glob
import time

pdbs = []

# Collects the pose numbers from the list of filenames
for filename in glob.glob('poses/protein*.pdb'):
    if len(filename) == 18:
        pdbs.append(str(filename[-5:-4]))
    elif len(filename) == 19:
        pdbs.append(str(filename[-6:-4]))
    elif len(filename) == 20:
        pdbs.append(str(filename[-7:-4]))
    else:
        continue

# Create directories for each pose and generate Schrodinger input file
for pdb in pdbs:
    os.system("mkdir pose_" + str(pdb))
    os.system("cp poses/protein" + str(pdb) + ".pdb pose_" + str(pdb) + "/.")
    with open("pose_" + str(pdb) + "/score_" + str(pdb) + ".in", 'w') as schrod_in:
        schrod_in.write("COMPLEX\tprotein" + str(pdb) + ".pdb")
        # Change any of the below variables if you want to adjust the way Schrodginer prepares the complex
        schrod_in.write("\nPPREP\tFALSE\nDOCK_DOCKING_METHOD\tinplace\nDOCK_PRECISION\tXP")

# Runs Glide for each pose
for pdb in pdbs:
    os.chdir("pose_" + str(pdb))
    os.system("$SCHRODINGER/run xglide.py score_" + str(pdb) + ".in")
    os.chdir("..")

# Waits for Glide to finish, then returns the Glide score from each pose's output files
for pdb in pdbs:
    while not os.path.exists("pose_" + str(pdb) + "/score_" + str(pdb) + "__protein" + str(pdb) + "__dock_lib.maegz"):
        time.sleep(1)
    if os.path.isfile("pose_" + str(pdb) + "/score_" + str(pdb) + "__protein" + str(pdb) + "__dock_lib.maegz"):
        gotIt = False
        with open("pose_" + str(pdb) + "/score_" + str(pdb) + ".log") as schrod_out:
            lines = schrod_out.readlines()
            for line in range(0, len(lines)):
                lines[line] = str(lines[line])
                line = lines[line].split()
                try:    
                    if line[0] == "protein" + str(pdb) and not gotIt:
                        with open("pose_score_list.dat", 'a') as outfile:
                            outfile.write("\nPose #" + str(pdb) + " Glide score = " + line[-1][0:-1])
                            gotIt = True
                    else:
                        continue
                except IndexError:
                    continue
    else:
        pass

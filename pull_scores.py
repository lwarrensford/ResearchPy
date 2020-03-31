import os
import os.path
import glob
import time

"""
Retrieve list of Glide scores

-Luke Warrensford 2/20
"""

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

for pdb in pdbs:
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

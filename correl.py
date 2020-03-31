"""
Py script for determining the correlation of the positions of atoms from two different
coordinate files.

-Luke Warrensford 1/20
"""

import math

pre_pdb = []
post_pdb = []

# Open the pre-dynamics cor file and extract the positions
with open("sgld_charmmsp-stu1_mini_init.pdb", 'r') as pre_cor:
    lines = pre_cor.readlines()
    for line in range(0, len(lines)):
        lines[line] = str(lines[line])
        line = lines[line].split()
        try:
            if float(line[5]):
                atom = {
                    "id": int(line[1]),
                    "x_val": float(line[5]),
                    "y_val": float(line[6]),
                    "z_val": float(line[7]),
                }
                pre_pdb.append(atom)
            else:
                continue
        except ValueError:
            continue
        except IndexError:
            continue

# Open the post-dynamics cor file and extract the positions
with open("sgld_charmmsp-stu1_final.pdb", 'r') as post_cor:
    lines = post_cor.readlines()
    for line in range(0, len(lines)):
        lines[line] = str(lines[line])
        line = lines[line].split()
        try:
            if float(line[5]):
                atom = {
                    "id": int(line[1]),
                    "x_val": float(line[5]),
                    "y_val": float(line[6]),
                    "z_val": float(line[7]),
                }
                post_pdb.append(atom)
            else:
                continue
        except ValueError:
            continue
        except IndexError:
            continue

pre_R = []
post_R = []

# Calculate the R coordinate value for each atom in the molecule
for i in range(0, len(pre_pdb)):
    i = math.sqrt((pre_pdb[i]["x_val"] ** 2) + (pre_pdb[i]["y_val"] ** 2) + (pre_pdb[i]["z_val"] ** 2))
    pre_R.append(i)

for i in range(0, len(post_pdb)):
    i = math.sqrt((post_pdb[i]["x_val"] ** 2) + (post_pdb[i]["y_val"] ** 2) + (post_pdb[i]["z_val"] ** 2))
    post_R.append(i)

# Calculate the ensemble values of the pre and post dynamics coordinates
pre_ensemble = sum(pre_R) / len(pre_R)

post_ensemble = sum(post_R) / len(post_R)

cor_correl = []

# Calculate the correlated coordinates
for i in range(0, len(pre_pdb)):
    correl = pre_R[i] * post_R[i]
    cor_correl.append(correl)

# Calculate the uncorrelated coordinates and the correlation function
correl_ensemble = sum(cor_correl) / len(cor_correl)

C = correl_ensemble - (pre_ensemble * post_ensemble)

C = 2 * (C / len(cor_correl))

print(C)

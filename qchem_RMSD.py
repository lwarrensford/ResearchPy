from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_error
from math import sqrt
import os

"""
Retrieve output data from Q-Chem jobs and evaluate RMSD

-Luke Warrensford 7/18
"""

methods = ["B3LYP", "BLYP", "CAM-B3LYP", "HF", "M06-2X", "w-B97M-V", "wB97X-D", "wB97X-V"]
basis_sets = ["6-31G*", "6-31+G*", "6-311G**", "6-311+G**"]
solvs = ["NONE", "PCM", "SM8", "SMD"]
mols = ['ACEM', 'BUTA', 'DMSO', 'EMS', 'ETHA', 'ETOH', 'ETSH', 'IBUT', 'MEOH', 'MESH', 'MIMI', 'MIND', 'PCRO', 'PRAM', 'PRO2', 'PRPA', 'THF', 'THIP', 'TOLU']

def isfloat(value):
  try:
    float(value)
    return True
  except ValueError:
    return False

def RMSE():
    with open(mol + '.out') as f_obj:
        lines = f_obj.readlines()

    with open('/Users/lukewarrensford/Desktop/ref_mol/' + mol + '.txt') as r_obj:
        ref_lines = r_obj.readlines()

    ref = []

    for i in range(0, len(ref_lines)):
        ref_lines[i] = (str(ref_lines[i]))
        ref_line = ref_lines[i].split()
        if len(ref_line) == 3:
            ref.append(float(ref_line[2]))
            
    current_charges = []

    j=1
    k=0
    types = ['Mulliken', 'ChElPG', 'Hirshfeld', 'CM5', 'CM5_S', 'RESP', 'Stewart']
    comparing = False

    with open(mol + '_analyzed.txt', 'a') as out_file:
        out_file.write('ANALYSIS OF ' + mol)
        out_file.write('\n----------------------------------------')

    for i in range(200, len(lines)):
        # loop through the lines to search for the goods
        lines[i] = (str(lines[i]))
        line = lines[i].split()
        if len(line) != 3 and j != len(ref):
            continue
        elif line[0] == '1' and not isfloat(line[1]):
            # identifies charge section and begins adding them to list
            with open(mol + '_analyzed.txt', 'a') as out_file:
                out_file.write('\n----------------------------------------')
                out_file.write('\n' + types[k])
                out_file.write('\n----------------------------------------')
                out_file.write('\nAtom\tQChem_Charge\tRef_Charge')
                out_file.write('\n----------------------------------------')
                out_file.write('\n' + line[1] + '\t' + line[2] + '\t' + str(ref[0]))
            print('----------------------------------------')
            print(types[k])
            print('----------------------------------------')
            print('Atom\tQChem_Charge\tRef_Charge')
            print('----------------------------------------')
            # compare that line's value to the ref value
            comparing = True
            print(line[1] + '\t' + line[2] + '\t' + str(ref[0]))
            current_charges.append(float(line[2]))
            k += 1
        elif len(line) == 3 and comparing and j <= len(ref)-1:
            # continues to add values to list after IDing charge section
            current_charges.append(float(line[2]))
            with open(mol + '_analyzed.txt', 'a') as out_file:
                out_file.write('\n' + line[1] + '\t' + line[2] + '\t' + str(ref[j]))
            print(line[1] + '\t' + line[2] + '\t' + str(ref[j]))
            j += 1
        elif len(line) != 3 and j == len(ref):
            # when gets to end of charge section, calc RMSE and reset counters and list
            rms = sqrt(mean_squared_error(current_charges, ref))
            mae = mean_absolute_error(current_charges, ref)
            with open(mol + '_analyzed.txt', 'a') as out_file:
                out_file.write('\n\n' + mol + ' ' + types[k-1] + ' RMSE: ' + str(rms))
                out_file.write('\n\n' + mol + ' ' + types[k-1] + ' MAE: ' + str(mae))
            comparing = False
            j = 1
            current_charges = []
            continue
        else:
            # legacy
            comparing = False
            j = 1

for i in range(0, 1):
    method = methods[i]
    for j in range(0, len(basis_sets)):
        basis = basis_sets[j]
        for k in range(0, len(solvs)):
            solv = solvs[k]
            for l in range(0, len(mols)):
                mol = mols[l]
                os.chdir('/Users/lukewarrensford/Desktop/mol_charge/' + method.lower() + '/' + basis.lower() + '/' + solv.lower() + '/' + mol)
                os.system('rm *.txt')
                try:
                    RMSE()
                except FileNotFoundError:
                    pass
            os.chdir('/Users/lukewarrensford/Desktop/mol_charge')

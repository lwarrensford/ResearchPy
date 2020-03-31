import os

"""
Creates a nice looking output file for the AA Q-Chem data

-Luke Warrensford 6/18
"""

mols = ['ACEM', 'BUTA', 'DMSO', 'EMS', 'ETHA', 'ETOH', 'ETSH', 'IBUT', 'MEOH', 'MESH', 'MIMI', 'MIND', 'PCRO', 'PRAM', 'PRO2', 'PRPA', 'THF', 'THIP', 'TOLU']

with open('/Users/lukewarrensford/Desktop/mol_final_list.txt', 'a') as log:
    log.write('Optimal scenario to produce most-similar Charmm charges for the selected molecules.')
    log.write('\n-------------------------------------------------------------------------------------')
    log.write('\nMolecule\tMethod\tBasis Set\tSolvent\tCharge Type\tRMSE')
    log.write('\n-------------------------------------------------------------------------------------')


for i in range(0, len(mols)):
    mol = mols[i]
    os.chdir('/Users/lukewarrensford/Desktop/mol_final/' + mol)
    with open(mol + '_optimal.out', 'r') as f_obj:
        lines = f_obj.readlines()
        for a in range(1, len(lines)):
            lines[a] = (str(lines[a]))
            line = lines[a].split()
            with open('/Users/lukewarrensford/Desktop/mol_final_list.txt', 'a') as log:
                log.write('\n' + mol + '\t' + line[8] + '\t' + line[11] + '\t' + line[14] + '\t' + line[17] + '\t' + line[-1])
    os.chdir('/Users/lukewarrensford/Desktop/mol_final')

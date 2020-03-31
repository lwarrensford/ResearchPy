import os

"""
Automates the generation of Q-Chem scripts for the various AA analogues

-Luke Warrensford 6/18
"""

methods = ["B3LYP", "BLYP", "CAM-B3LYP", "HF", "M06-2X", "w-B97M-V", "wB97X-D", "wB97X-V"]
basis_sets = ["6-31G*", "6-31+G*", "6-311G**", "6-311+G**"]
solvs = ["NONE", "PCM", "SM8", "SMD"]
mols = ['ACEM', 'BUTA', 'DMSO', 'EMS', 'ETHA', 'ETOH', 'ETSH', 'IBUT', 'MEOH', 'MESH', 'MIMI', 'MIND', 'PCRO', 'PRAM', 'PRO2', 'PRPA', 'THF', 'THIP', 'TOLU']

for i in range(1, len(methods)):
    method = methods[i]
    for j in range(0, len(basis_sets)):
        basis = basis_sets[j]
        for k in range(0, len(solvs)):
            solv = solvs[k]
            for l in range(0, len(mols)):
                mol = mols[l]
                os.chdir('/Users/lukewarrensford/Desktop/mol_charges/' + method.lower() + '/' + basis.lower() + '/' + solv.lower() + '/' + mol)
                if solv == 'SM8' and basis == '6-311G**':
                    continue
                elif solv == 'SM8' or solv == 'SMD':
                    with open('/Users/lukewarrensford/Desktop/mol_charges/' + method.lower() + '/' + basis.lower() + '/' + solv.lower() + '/' + mol + '/' + mol + '.inp', 'a') as inp_file:
                        inp_file.write('METHOD = ' + method)
                        inp_file.write('\nBASIS = ' + basis)
                        inp_file.write('\nSOLVENT_METHOD = ' + solv)
                        inp_file.write('\n$END')
                        inp_file.write('\n' + '\n$SMX' + '\nSOLVENT WATER' + '\n$END')
                elif solv == 'PCM':
                    with open('/Users/lukewarrensford/Desktop/mol_charges/' + method.lower() + '/' + basis.lower() + '/' + solv.lower() + '/' + mol + '/' + mol + '.inp', 'a') as inp_file:
                        inp_file.write('METHOD = ' + method)
                        inp_file.write('\nBASIS = ' + basis)
                        inp_file.write('\nSOLVENT_METHOD = ' + solv)
                        inp_file.write('\n$END')
                else:
                    with open('/Users/lukewarrensford/Desktop/mol_charges/' + method.lower() + '/' + basis.lower() + '/' + solv.lower() + '/' + mol + '/' + mol + '.inp', 'a') as inp_file:
                        inp_file.write('METHOD = ' + method)
                        inp_file.write('\nBASIS = ' + basis)
                        inp_file.write('\n$END')

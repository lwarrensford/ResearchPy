import os

"""
Automates the submission of Q-Chem jobs to the computing cluster

-Luke Warrensford 6/18
"""

methods = ["B3LYP", "BLYP", "CAM-B3LYP", "HF", "M06-2X", "RIMP2", "w-B97M-V", "wB97X-D", "wB97X-V"]
basis_sets = ["6-31G*", "6-31+G*", "6-311G**", "6-311+G**"]
solvs = ["NONE", "PCM", "SM8", "SMD"]
mols = ['ACEM', 'BUTA', 'DMSO', 'EMS', 'ETHA', 'ETOH', 'ETSH', 'IBUT', 'MEOH', 'MESH', 'MIMI', 'MIND', 'PCRO', 'PRAM', 'PRO2', 'PRPA', 'THF', 'THIP', 'TOLU']

for i in range(6, 10):
    method = methods[i]
    for j in range(0,len(basis_sets)):
        basis = basis_sets[j]
        for k in range(0,len(solvs)):
            solv = solvs[k]
            for m in range(0,len(mols)):
                mol = mols[m]
                os.chdir(method.lower() + "/" + basis.lower() + "/" + solv.lower() + "/" + mol)
                os.system("sbatch /work/l/lwarrensford/mol_charges/aa_qchem.slu " + mol.lower())
                os.chdir("/work/l/lwarrensford/mol_charges")

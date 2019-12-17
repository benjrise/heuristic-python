# Install through "pip install pymatgen" in python console
from pymatgen import MPRester
import time
import csv
import numpy as np

ALL_ELEMENTS = ["H", "He", "Li", "Be", "B", "C", "N", "O", "F", "Ne", "Na", "Mg", "Al", "Si", "P", "S", "Cl", "Ar", "K", "Ca", "Sc", "Ti", "V", "Cr", "Mn", "Fe", "Co", "Ni", "Cu", "Zn", "Ga", "Ge", "As", "Se", "Br", "Kr", "Rb", "Sr", "Y", "Zr", "Nb", "Mo", "Tc", "Ru",
                "Rh", "Pd", "Ag", "Cd", "In", "Sn", "Sb", "Te", "I", "Xe", "Cs", "Ba", "La", "Ce", "Pr", "Nd", "Pm", "Sm", "Eu", "Gd", "Tb", "Dy", "Ho", "Er", "Tm", "Yb", "Lu", "Hf", "Ta", "W", "Re", "Os", "Ir", "Pt", "Au", "Hg", "Tl", "Pb", "Bi", "Ac", "Th", "Pa", "U", "Np", "Pu", "Am"]
start_time = time.time()
# Key generated from dashboard onF materials project website
m = MPRester("LK17Ip5a6B3yfG9o")
ALL_MATS = m.query(criteria={"elements": {"$in": ALL_ELEMENTS}}, properties=[
                   "material_id", "total_magnetization", "e_above_hull", "elements", "unit_cell_formula", "band_gap"])
print("--- %s seconds ---" % (time.time() - start_time))
materials_properties = ["material_id", "total_magnetization",
                        "e_above_hull", "elements", "unit_cell_formula", "band_gap", "formula"]
csv_file = "materials.csv"


def find_gcd2(x, y):
    while(y):
        x, y = y, x % y
    return x


def find_gcdn(arr):
    num1 = arr[0]
    num2 = arr[1]
    gcd = find_gcd2(num1, num2)
    for i in range(2, len(arr)):
        gcd = find_gcd2(gcd, arr[i])
    return gcd


for mat in ALL_MATS:
    if len(mat["elements"]) == 1:
        temp1 = {}
        temp1[mat["elements"][0]] = 1
        mat["formula"] = temp1
        continue
    formula_arr = []
    for element in mat["elements"]:
        formula_arr.append(mat["unit_cell_formula"][element])
    x = find_gcdn(formula_arr)
    simple_arr = np.array(formula_arr)/x
    tempDict = {}
    for i in range(0, len(simple_arr)):
        tempDict[mat["elements"][i]] = simple_arr[i]
    mat["formula"] = tempDict


try:
    with open(csv_file, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=materials_properties)
        writer.writeheader()
        for data in ALL_MATS:
            writer.writerow(data)
except IOError:
    print("I/O error")

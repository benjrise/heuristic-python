import ast
import csv
import numpy as np

ALL_MATS = []


def parse_array(str_array):
    string = str_array[1:-1]
    string = string.replace("'", "")
    arr = string.split(", ")
    return arr


def parse_dict(str_dict):
    pdict = ast.literal_eval(str_dict)
    return pdict


with open('material_data.csv', mode='r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
        row["elements"] = parse_array(row["elements"])
        row["unit_cell_formula"] = parse_dict(row["unit_cell_formula"])
        row["e_above_hull"] = float(row["e_above_hull"])
        ALL_MATS.append(row)

print(ALL_MATS)


"""
Heusler compounds [X2, Y, Z]
"""

X_H = ["Li", "Mg", "Mn", "Fe", "Co", "Ni", "Cu",
       "Ru", "Rh", "Pd", "Ag", "Cd", "Ir", "Pt", "Au"]
Y_H = ["Li", "Be", "Sc", "Ti", "V", "Cr", "Mn", "Fe", "Co", "Ni", "Zn", "Y", "Zr", "Nb", "Mo", "Hf", "W", "La", "Ce", "Pr", "Nd", "Sm", "Gd", "Tb" "Dy", "Ho",
       "Er", "Tm", "Yb", "Lu"]
Z_H = ["Mg", "Zn", "B", "Al", "Si", "Ga",
       "Ge", "As", "In", "Sn", "Sb", "Pb", "Bi"]


def heusler_compounds(matsin, X_H, Y_H, Z_H):

    heusler_comps = []

    for mat in matsin:

        noofels = 0
        for element in mat["elements"]:
            noofels += mat["unit_cell_formula"][element]

        if noofels != 4.0 or len(mat["elements"]) != 3:
            continue

        X = []
        Y_Z1 = []
        Y_Z2 = []

        i = 1
        for element in mat["elements"]:
            if mat["unit_cell_formula"][element] == 2.0:
                X.append(element)
                continue
            if i == 1:
                Y_Z1.append(element)
                i += 1
                continue
            if i == 2:
                Y_Z2.append(element)
                i = 1
                continue

        if set(Y_Z1).issubset(set(Y_H)) == True and set(Y_Z2).issubset(set(Z_H)) == True and set(X).issubset(set(X_H)) == True:
            heusler_comps.append(mat)

        if set(Y_Z2).issubset(set(Y_H)) == True and set(Y_Z1).issubset(set(Z_H)) == True and set(X).issubset(set(X_H)) == True:
            heusler_comps.append(mat)

    return heusler_comps


def halfheusler_compounds(matsin, X_H, Y_H, Z_H):

    heusler_comps = []

    for mat in matsin:

        noofels = 0
        for element in mat["elements"]:
            noofels += mat["unit_cell_formula"][element]

        if noofels != 3.0 or len(mat["elements"]) != 3:
            continue

        XYZ1 = []
        XYZ2 = []
        XYZ3 = []

        i = 1
        for element in mat["elements"]:
            if i == 1:
                XYZ1.append(element)
                i += 1
                continue
            if i == 2:
                XYZ2.append(element)
                i += 1
                continue
            if i == 3:
                XYZ3.append(element)
                i = 1

        if set(XYZ1).issubset(X_H):
            if (set(XYZ2).issubset(set(Y_H)) == True and (set(XYZ3).issubset(set(Z_H)) == True))\
                    or \
                    ((set(XYZ3).issubset(set(Y_H))) == True and (set(XYZ1).issubset(set(Z_H))) == True):
                heusler_comps.append(mat)

        if set(XYZ1).issubset(Y_H):
            if (set(XYZ2).issubset(set(X_H)) == True and set(XYZ3).issubset(set(Z_H)) == True)\
                    or \
                    (set(XYZ3).issubset(set(X_H)) == True and (set(XYZ1).issubset(set(Z_H)) == True)):
                heusler_comps.append(mat)

        if set(XYZ1).issubset(Z_H):
            if (set(XYZ2).issubset(set(Y_H)) == True and set(XYZ3).issubset(set(X_H)) == True)\
                    or \
                    (set(XYZ3).issubset(set(Y_H)) == True and set(XYZ1).issubset(set(X_H)) == True):
                heusler_comps.append(mat)

    return heusler_comps

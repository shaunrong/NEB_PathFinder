#!/usr/bin/env python
import argparse
from pymatgen import Element
from pymatgen.io.vaspio import Poscar, Chgcar
import os

__author__ = 'Shaun Rong'
__version__ = '0.1'
__maintainer__ = 'Shaun Rong'
__email__ = 'rongzq08@gmail.com'

from PathFinder.pathFinder import NEBPathfinder, ChgcarPotential

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-s1', type=str, help='starting point CONTCAR')
    parser.add_argument('-s2', type=str, help='ending point CONTCAR')
    parser.add_argument('-e', type=str, help='diffusing cation')
    parser.add_argument('-n', type=int, default=8, help='number of interpolated images')
    parser.add_argument('-chg', type=str, help='CHGCAR for pathFinder')
    arg = parser.parse_args()

    s1 = Poscar.from_file(arg.s1).structure
    s2 = Poscar.from_file(arg.s2).structure
    chg = Chgcar.from_file(arg.chg)

    relax_sites = []
    for i, site in enumerate(s1.sites):
        if site.specie == Element(arg.e):
            relax_sites.append(i)

    pf = NEBPathfinder(s1, s2, relax_sites=relax_sites, v=ChgcarPotential(chg).get_v(), n_images=(3*arg.n))

    images = pf.images

    for i, image in enumerate(images):
        if i % 3 == 0:
            p = Poscar(image)
            directory = "0" + str(i/3)
            if not os.path.exists(directory):
                os.makedirs(directory)
            p.write_file("{}/POSCAR".format(directory))
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 21 01:16:20 2022

@author: cnncn
"""


def genall(path):
    """
    convert all POSCARs in path to cif
    
    Parameters
    ----------
    path : str
        path of the directory that contains all POSCAR files
        
    """
    
    from pymatgen.core import Structure
    from pymatgen.symmetry.analyzer import SpacegroupAnalyzer
    import os
    
    allfile = os.listdir(path)
    for f in allfile:
        # The name of POSCAR files must start with "POSCAR" 
        if f.startswith('POSCAR'):
            name = os.path.join(path,f)
            structure = Structure.from_file(name)
            asp = SpacegroupAnalyzer(structure,symprec=0.001, angle_tolerance=1.0)
            prmstructure = asp.get_primitive_standard_structure()
            cifname =  name + '.cif'
            print(cifname)
            prmstructure.to(filename=cifname)


def plot_ele_band(path):
    """
    plot projected electronic band structure
    Please change the Klabels, path and rgb_labels
        
    """
    
    from pymatgen.io.vasp.outputs import Vasprun
    from pymatgen.electronic_structure.plotter import BSDOSPlotter
    import os
    
    xmlname = os.path.join(path, 'vasprun.xml') 
    kpt_name = os.path.join(path, 'KPOINTS')
    vaspout = Vasprun(xmlname, parse_projected_eigen=True)
    bandstr = vaspout.get_band_structure(kpoints_filename=kpt_name,line_mode=True)
    pbandpdos_fig = BSDOSPlotter(bs_projection='elements',
                                 dos_projection='elements',
                                 vb_energy_range=5,
                                 cb_energy_range=5,
                                 tick_fontsize=25,
                                 legend_fontsize=25,
                                 rgb_legend=False)
    pbandpdos_fig.get_plot(bandstr).savefig(os.path.join(path, 'band.pdf'))
            

def plot_phonon_band():     
    from pymatgen.io.phonopy import get_ph_bs_symm_line
    from pymatgen.phonon.plotter import PhononBSPlotter
    
    Klabels = {'\u0393':[0.0,0.0,0.0],'X':[0.0,0.5,0.0],'M':[0.5,0.5,0.0],'\u0393':[0.0,0.0,0.0],'R':[0.5,0.5,0.5]}
    bs = get_ph_bs_symm_line('../tests/band.yaml',has_nac=False, labels_dict=Klabels)
    bsplt = PhononBSPlotter(bs)
    bsplt.show_proj(site_comb=[[0],[1],[2,3,4]], units='cm-1', rgb_labels = ("Sr","Ti","O"))
    bsplt.save_proj_plot('../tests/phobandstr.pdf', img_format="pdf", site_comb=[[0],[1],[2,3,4]], units='cm-1',rgb_labels = ("Sr","Ti","O"))


if __name__ == "__main__":
    # genall(r'../tests/POSCAR_to_cif')
    # plot_ele_band(r'../tests/ele_band')
    plot_phonon_band()
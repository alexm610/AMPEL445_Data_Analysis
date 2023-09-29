import pya
from SiEPIC.utils import get_technology_by_name

'''
Author: Alex Manak (UBC)
alexm610@ece.ubc.ca
September 29, 2023

This file is intended to be used as a module 
within custom layout scripts. For users to import this module, 
a copy of this file must be placed in 
the 'python' folder of the user's KLayout 
installation. 
A hardlink is recommended, in case
the user wishes to modify this file in their
working folder.
Locations this file is to be added to:
    - MacOS:
        /Users/<username>/.klayout/python
    - Windows:
        C:\Users\<username>\AppData\Roaming\KLayout\python

It is recommended to users to run their layout scripts 
from within the KLayout Macro IDE, as running KLayout via 
the system CLI has traditionally been buggy. 

Version history:
September 29, 2023
    - Initial version completed
'''

class generate_layout:
    '''
    This class contains useful automations for users writing 
    scripted layout routines. It is initially setup for the 
    'SiEPICfab_EBeam_ZEP' technology, but this can be easily 
    changed below. 
    '''
    def __init__(self):
        self.technology_name = 'SiEPICfab_EBeam_ZEP'
        self.mw = pya.Application().instance().main_window()
        self.ly = self.mw.create_layout(self.technology_name, 1).layout()
        self.cell = self.ly.create_cell('TOP')
        self.lv = self.mw.current_view()
        self.lv.select_cell(self.cell.cell_index(), 0)
        self.dbu = self.ly.dbu
        self.TECHNOLOGY = get_technology_by_name(self.technology_name)
    
    def place_cell(self, cell_name, x_pos, y_pos, rotation):
        #t = pya.Trans.from_s('%s, %s, %s' % (rotation, x_pos / self.dbu, y_pos / self.dbu))
        t = pya.Trans(0, False, x_pos / self.dbu, y_pos / self.dbu)
        cell_instance = self.cell.insert(pya.CellInstArray(cell_name.cell_index(), t))

    def load_cells(self, pcell_def):
        return self.ly.create_cell('%s' % pcell_def, self.technology_name)

    def create_floorplan(self, bottom_corner, top_corner):
        floor_plan = self.cell.layout().layer(self.TECHNOLOGY['FloorPlan'])
        self.cell.shapes(floor_plan).insert(pya.Box(bottom_corner[0] / self.dbu, bottom_corner[1] / self.dbu, top_corner[0] / self.dbu, top_corner[1] / self.dbu))

    def screenshot(self, filename):
        self.lv.clear_object_selection()
        self.lv.zoom_fit()
        self.lv.max_hier()
        dir_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '%s.png' % filename)
        self.lv.save_screenshot(dir_path)

    def save_layout(self, filename):
        # save the layout, without PCell information, for fabrication
        save_options = pya.SaveLayoutOptions()
        save_options.write_context_info = False
        save_options.format = 'OASIS'
        save_options.oasis_compression_level = 10
        output_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), "%s.%s" % (filename, save_options.format[0:3]))
        print("Saving output %s: %s" % (save_options.format, output_file))
        self.ly.write(output_file, save_options)

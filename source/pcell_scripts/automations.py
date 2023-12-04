import pya, os
from SiEPIC.utils import get_technology_by_name

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
        self.shapes = self.cell.shapes
        self.LayerSi_etch = self.cell.layout().layer(self.TECHNOLOGY['Si_etch_highres'])
        self.LayerMetal = self.cell.layout().layer(self.TECHNOLOGY['M1'])
        self.PinRecN = self.cell.layout().layer(self.TECHNOLOGY['PinRec'])
        self.DevRecN = self.cell.layout().layer(self.TECHNOLOGY['DevRec'])
        self.oxideopen = self.cell.layout().layer(self.TECHNOLOGY['Oxide open (to BOX)'])
        self.Si_Core = self.cell.layout().layer(self.TECHNOLOGY['Si_core'])
        self.Si_Clad = self.cell.layout().layer(self.TECHNOLOGY['Si_clad'])
        self.LayerSi_etch_lowres = self.cell.layout().layer(self.TECHNOLOGY['Si_etch_lowres'])
        self.DeepTrench = self.cell.layout().layer(self.TECHNOLOGY['Deep Trench'])
        self.WaveGuide = self.cell.layout().layer(self.TECHNOLOGY['Waveguide'])
        self.FloorPlan = self.cell.layout().layer(self.TECHNOLOGY['FloorPlan'])
        self.TextLayer = self.cell.layout().layer(self.TECHNOLOGY['Text'])

    def return_layer(self, n) -> pya.LayerInfo:
        if n == 0: return self.LayerSi_etch
        elif n == 1: return self.LayerMetal
        elif n == 2: return self.PinRecN
        elif n == 3: return self.DevRecN
        elif n == 4: return self.oxideopen
        elif n == 5: return self.Si_Core
        elif n == 6: return self.Si_Clad
        elif n == 7: return self.LayerSi_etch_lowres
        elif n == 8: return self.DeepTrench
        elif n == 9: return self.WaveGuide
        elif n == 10: return self.FloorPlan
        else: return self.LayerSi_etch

    def generate_geometry(self, points, input_layer):
        polygon = pya.DPolygon(points)
        geometry = pya.Polygon.from_dpoly(polygon * (1 / self.dbu))
        if input_layer == 0:
            layer_in = self.LayerSi_etch
        elif input_layer == 1:
            layer_in = self.return_layer(1)
        elif input_layer == 2:
            layer_in = self.PinRecN
        elif input_layer == 3:
            layer_in = self.DevRecN
        elif input_layer == 4:
            layer_in = self.oxideopen
        else:
            layer_in = self.LayerSi_etch
        self.cell.shapes(layer_in).insert(geometry)

    def draw_rectangle(self, x, y, layer):
        points = []
        for i in range(len(x)):
            points.append(pya.DPoint(x[i], y[i]))
        self.generate_geometry(points, layer)

    def place_cell(self, cell_name, x_pos, y_pos, rotation):
        t = pya.Trans(rotation, False, x_pos / self.dbu, y_pos / self.dbu) # rotation must be a positive integer, corresponding to multiples of 90 degrees
        return self.cell.insert(pya.CellInstArray(cell_name.cell_index(), t))

    def load_gds_cell(self, cell_def):
        return self.ly.create_cell('%s' % cell_def, self.technology_name)

    def load_cells(self, pcell_def, pcell_param):
        return self.ly.create_cell('%s' % pcell_def, self.technology_name, pcell_param)

    def create_floorplan(self, bottom_corner, top_corner):
        floor_plan = self.FloorPlan
        self.cell.shapes(floor_plan).insert(pya.Box(bottom_corner[0] / self.dbu, bottom_corner[1] / self.dbu, top_corner[0] / self.dbu, top_corner[1] / self.dbu))

    def place_label(self, x, y, rotation, text):
        t = pya.Trans(rotation, False, x / self.dbu, y / self.dbu)
        text_label = pya.Text("opt_in_TE_1550_device_%s" % (text), t)
        text_shape = self.cell.shapes(self.TextLayer).insert(text_label)
        text_shape.text_size = 1 / self.dbu

    def screenshot(self, filename, dir_path):
        self.lv.clear_object_selection()
        self.lv.zoom_fit()
        self.lv.max_hier()
        #dir_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '%s.png' % filename)
        file_path = os.path.join(dir_path, "%s.png" % (filename))
        print("Saving screenshot: %s.png" % (filename))
        self.lv.save_screenshot(file_path)

    def save_layout(self, filename, file_path):
        # save the layout, without PCell information, for fabrication
        save_options = pya.SaveLayoutOptions()
        save_options.write_context_info = False
        save_options.format = 'OASIS'
        save_options.oasis_compression_level = 10
        #output_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), "%s.%s" % (filename, save_options.format[0:3]))
        output_file = os.path.join(file_path, "%s.%s" % (filename, save_options.format[0:3]))
        print("Saving output %s: %s" % (save_options.format, output_file))
        self.ly.write(output_file, save_options)

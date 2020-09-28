""" QLAr.py

Original Author: P. Koller, University of Bern

"""

import gegede.builder
from duneggd.LocalTools import localtools as ltools
from gegede import Quantity as Q


class QLArBuilder(gegede.builder.Builder):
    """ Class to build QLAr geometry.

    """

    def configure(self,QLAr_dimension,**kwargs):

        # Read dimensions form config file
        self.QLAr_dx             = QLAr_dimension['dx']
        self.QLAr_dy             = QLAr_dimension['dy']
        self.QLAr_dz             = QLAr_dimension['dz']

        # Material definitons

        self.Material           = 'LAr'

    def construct(self,geom):
        """ Construct the geometry.

        """

        self.halfDimension  = { 'dx':   self.QLAr_dx,
                                'dy':   self.QLAr_dy,
                                'dz':   self.QLAr_dz}

        main_lv, main_hDim = ltools.main_lv(self,geom,'Box')
        print('QLArBuilder::construct()')
        print('main_lv = '+main_lv.name)
        self.add_volume(main_lv)


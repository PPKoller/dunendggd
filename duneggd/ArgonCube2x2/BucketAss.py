""" BucketAss.py

Original Author: P. Koller, University of Bern

"""

import gegede.builder
from duneggd.LocalTools import localtools as ltools
from gegede import Quantity as Q


class BucketAssBuilder(gegede.builder.Builder):
    """ Class to build BucketAss geometry.

    """

    def configure(self,Bucket_dimension,LAr_level,G10Bottom_dimension,LArVol1_dimension,LArVol2_dimension,**kwargs):

        # Read dimensions form config file
        self.Bucket_dx          = Bucket_dimension['dx']
        self.Bucket_dy          = Bucket_dimension['dy']
        self.Bucket_dz          = Bucket_dimension['dz']
        self.Bucket_dd          = Bucket_dimension['dd']

        self.G10Bottom_dx       = G10Bottom_dimension['dx']
        self.G10Bottom_dy       = G10Bottom_dimension['dy']
        self.G10Bottom_dz       = G10Bottom_dimension['dz']

        self.LArVol1_dx         = LArVol1_dimension['dx']
        self.LArVol1_dy         = LArVol1_dimension['dy']
        self.LArVol1_dz         = LArVol1_dimension['dz']

        self.LArVol2_dx         = LArVol2_dimension['dx']
        self.LArVol2_dy         = LArVol2_dimension['dy']
        self.LArVol2_dz         = LArVol2_dimension['dz']

        self.LAr_dy             = LAr_level
        self.GAr_dy             = self.Bucket_dy-self.LAr_dy

        # Material definitons
        self.Bucket_Material    = 'G10'
        self.LArPhase_Material  = 'LAr'
        self.GArPhase_Material  = 'GAr'

        self.Material           = 'G10'

    def construct(self,geom):
        """ Construct the geometry.

        """

        #innerDetector_builder   = self.get_builder('InnerDetector')

        self.halfDimension  = { 'dx':   self.Bucket_dx,
                                'dy':   self.Bucket_dy,
                                'dz':   self.Bucket_dz}

        main_lv, main_hDim = ltools.main_lv(self,geom,'Box')
        print('BucketAssBuilder::construct()')
        print('main_lv = '+main_lv.name)
        self.add_volume(main_lv)

        # Construct LAr Phase Volume
        larPhase_shape = geom.shapes.Box('LArPhase',
                                        dx = self.Bucket_dx-self.Bucket_dd*2,
                                        dy = self.LAr_dy,
                                        dz = self.Bucket_dz-self.Bucket_dd*2)

        larPhase_lv = geom.structure.Volume('volLArPhase',
                                        material=self.LArPhase_Material,
                                        shape=larPhase_shape)

        # Place LAr Phase Volume inside Bucket volume
        pos = [Q('0cm'),-self.GAr_dy,Q('0cm')]

        larPhase_pos = geom.structure.Position('larPhase_pos',
                                                pos[0],pos[1],pos[2])

        larPhase_pla = geom.structure.Placement('larPhase_pla',
                                                volume=larPhase_lv,
                                                pos=larPhase_pos)

        main_lv.placements.append(larPhase_pla.name)

        # Construct GAr Phase Volume
        garPhase_shape = geom.shapes.Box('GArPhase',
                                        dx = self.Bucket_dx-self.Bucket_dd*2,
                                        dy = self.GAr_dy,
                                        dz = self.Bucket_dz-self.Bucket_dd*2)

        garPhase_lv = geom.structure.Volume('volGArPhase',
                                        material=self.GArPhase_Material,
                                        shape=garPhase_shape)

        # Place GAr Phase Volume inside Bucket volume
        pos = [Q('0cm'),self.LAr_dy,Q('0cm')]

        garPhase_pos = geom.structure.Position('garPhase_pos',
                                                pos[0],pos[1],pos[2])

        garPhase_pla = geom.structure.Placement('garPhase_pla',
                                                volume=garPhase_lv,
                                                pos=garPhase_pos)

        main_lv.placements.append(garPhase_pla.name)

        # Construct G10 Bottom Volume
        G10bottom_shape = geom.shapes.Box('G10Bottom',
                                        dx = self.G10Bottom_dx,
                                        dy = self.G10Bottom_dy,
                                        dz = self.G10Bottom_dz)

        G10bottom_lv = geom.structure.Volume('volG10Bottom',
                                        material=self.Bucket_Material,
                                        shape=G10bottom_shape)

        # Place G10 Bottom Volume inside Bucket volume
        pos = [Q('0cm'),-self.Bucket_dy+self.G10Bottom_dy,Q('0cm')]

        G10bottom_pos = geom.structure.Position('G10bottom_pos',
                                                pos[0],pos[1],pos[2])

        G10bottom_pla = geom.structure.Placement('G10bottom_pla',
                                                volume=G10bottom_lv,
                                                pos=G10bottom_pos)

        main_lv.placements.append(G10bottom_pla.name)

        # Construct LAr Volume 1
        larVol1_shape = geom.shapes.Box('LArVol1',
                                        dx = self.LArVol1_dx,
                                        dy = self.LArVol1_dy+self.LArVol2_dy,
                                        dz = self.LArVol1_dz)

        larVol1_lv = geom.structure.Volume('volLArVol1',
                                        material=self.LArPhase_Material,
                                        shape=larVol1_shape)

        # Place LAr Volume 1 inside Bucket volume
        pos = [Q('0cm'),-self.Bucket_dy+self.LArVol1_dy+self.LArVol2_dy,Q('0cm')]

        larVol1_pos = geom.structure.Position('larVol1_pos',
                                                pos[0],pos[1],pos[2])

        larVol1_pla = geom.structure.Placement('larVol1_pla',
                                                volume=larVol1_lv,
                                                pos=larVol1_pos)

        main_lv.placements.append(larVol1_pla.name)

        # Construct LAr Volume 2
        larVol2_shape = geom.shapes.Box('LArVol2',
                                        dx = self.LArVol2_dx,
                                        dy = self.LArVol2_dy,
                                        dz = self.LArVol2_dz)

        larVol2_lv = geom.structure.Volume('volLArVol2',
                                        material=self.LArPhase_Material,
                                        shape=larVol2_shape)

        # Place LAr Volume 2 inside Bucket volume
        pos = [Q('0cm'),-self.Bucket_dy+self.LArVol2_dy,Q('0cm')]

        larVol2_pos = geom.structure.Position('larVol2_pos',
                                                pos[0],pos[1],pos[2])

        larVol2_pla = geom.structure.Placement('larVol2_pla',
                                                volume=larVol2_lv,
                                                pos=larVol2_pos)

        main_lv.placements.append(larVol2_pla.name)

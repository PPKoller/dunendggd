""" LCM.py

Original Author: P. Koller, University of Bern

"""

import gegede.builder
from duneggd.LocalTools import localtools as ltools
from gegede import Quantity as Q


class LCMBuilder(gegede.builder.Builder):
    """ Class to build LCM geometry.

    """

    def configure(self,Fiber_dimension,SiPM_LCM_dimension,SiPM_LCM_Mask,SiPM_LCM_PCB,N_Fiber_LCM,N_SiPM_LCM,N_Mask_LCM,**kwargs):

        # Read dimensions form config file
        self.Fiber_rmin             = Fiber_dimension['rmin']
        self.Fiber_rmax             = Fiber_dimension['rmax']
        self.Fiber_dz               = Fiber_dimension['dz']
        self.Fiber_pitch            = Fiber_dimension['pitch']
        self.Fiber_dd               = Fiber_dimension['dd']

        self.SiPM_LCM_dx            = SiPM_LCM_dimension['dx']
        self.SiPM_LCM_dy            = SiPM_LCM_dimension['dy']
        self.SiPM_LCM_dz            = SiPM_LCM_dimension['dz']
        self.SiPM_LCM_pitch         = SiPM_LCM_dimension['pitch']

        self.SiPM_LCM_Mask_dx       = SiPM_LCM_Mask['dx']
        self.SiPM_LCM_Mask_dy       = SiPM_LCM_Mask['dy']
        self.SiPM_LCM_Mask_dz       = SiPM_LCM_Mask['dz']
        self.SiPM_LCM_Mask_pitch    = SiPM_LCM_Mask['pitch']

        self.SiPM_LCM_PCB_dx        = SiPM_LCM_PCB['dx']
        self.SiPM_LCM_PCB_dy        = SiPM_LCM_PCB['dy']
        self.SiPM_LCM_PCB_dz        = SiPM_LCM_PCB['dz']
        self.SiPM_LCM_PCB_pitch     = SiPM_LCM_PCB['pitch']

        self.N_Fiber_LCM            = int(N_Fiber_LCM)
        self.N_SiPM_LCM             = int(N_SiPM_LCM)
        self.N_Mask_LCM             = int(N_Mask_LCM)

        # Material definitons
        self.Fiber_Material         = 'EJ280WLS'
        self.SiPM_LCM_Material      = 'Silicon'
        self.SiPM_LCM_Mask_Material = 'PVT'
        self.SiPM_LCM_PCB_Material  = 'FR4'

        self.Material               = 'LAr'

    def construct(self,geom):
        """ Construct the geometry.

        """

        self.halfDimension      = { 'dx':   self.Fiber_dz
                                            +self.SiPM_LCM_Mask_dx
                                            +self.SiPM_LCM_PCB_dx,

                                    'dy':   self.SiPM_LCM_PCB_dy,

                                    'dz':   self.SiPM_LCM_PCB_dz}

        main_lv, main_hDim = ltools.main_lv(self,geom,'Box')
        print('LCMBuilder::construct()')
        print('main_lv = '+main_lv.name)
        self.add_volume(main_lv)

        # Construct fiber panel
        Fiber_shape = geom.shapes.Tubs('Fiber_panel_shape',
                                       rmin = self.Fiber_rmin,
                                       rmax = self.Fiber_rmax,
                                       dz = self.Fiber_dz-self.SiPM_LCM_Mask_dx)

        Fiber_lv = geom.structure.Volume('volFiber',
                                            material=self.Fiber_Material,
                                            shape=Fiber_shape)

        # Place LCM Fibers
        pos = [self.SiPM_LCM_PCB_dx,-self.Fiber_dd-2*self.N_Fiber_LCM*self.Fiber_pitch,Q('0cm')]
        for i in range(self.N_Fiber_LCM):
            pos[1] = pos[1] + 2*self.Fiber_pitch

            rot = [Q('0.0deg'),Q('90.0deg'),Q('0.0deg')]

            Fiber_pos = geom.structure.Position('Fiber_pos_center_'+str(i),
                                                    pos[0],pos[1],pos[2])

            Fiber_rot = geom.structure.Rotation('Fiber_rot_center_'+str(i),
                                                    rot[0],rot[1],rot[2])

            Fiber_pla = geom.structure.Placement('Fiber_pla_center_'+str(i),
                                                    volume=Fiber_lv,
                                                    pos=Fiber_pos,
                                                    rot=Fiber_rot)

            main_lv.placements.append(Fiber_pla.name)

        pos = [self.SiPM_LCM_PCB_dx,+self.Fiber_dd-2*self.Fiber_pitch,Q('0cm')]
        for i in range(self.N_Fiber_LCM,2*self.N_Fiber_LCM):
            pos[1] = pos[1] + 2*self.Fiber_pitch

            rot = [Q('0.0deg'),Q('90.0deg'),Q('0.0deg')]

            Fiber_pos = geom.structure.Position('Fiber_pos_center_'+str(i),
                                                    pos[0],pos[1],pos[2])

            Fiber_rot = geom.structure.Rotation('Fiber_rot_center_'+str(i),
                                                    rot[0],rot[1],rot[2])

            Fiber_pla = geom.structure.Placement('Fiber_pla_center_'+str(i),
                                                    volume=Fiber_lv,
                                                    pos=Fiber_pos,
                                                    rot=Fiber_rot)

            main_lv.placements.append(Fiber_pla.name)

        # Construct and place SiPMs and the corresponding Masks
        SiPM_LCM_Mask_shape = geom.shapes.Box('SiPM_LCM_Mask_shape',
                                       dx = self.SiPM_LCM_Mask_dx,
                                       dy = self.SiPM_LCM_Mask_dy,
                                       dz = self.SiPM_LCM_Mask_dz)

        SiPM_LCM_Mask_lv = geom.structure.Volume('volSiPM_LCM_Mask',
                                            material=self.SiPM_LCM_Mask_Material,
                                            shape=SiPM_LCM_Mask_shape)

        # Place Mask LV near end
        pos = [-self.Fiber_dz+self.SiPM_LCM_PCB_dx,Q('0mm'),Q('0mm')]

        SiPM_LCM_Mask_pos = geom.structure.Position('SiPM_LCM_Mask_pos_near',
                                                pos[0],pos[1],pos[2])

        SiPM_LCM_Mask_pla = geom.structure.Placement('SiPM_LCM_Mask_pla_near',
                                                volume=SiPM_LCM_Mask_lv,
                                                pos=SiPM_LCM_Mask_pos)

        main_lv.placements.append(SiPM_LCM_Mask_pla.name)

        # Place Mask LV far end
        pos = [self.halfDimension['dx']-self.SiPM_LCM_Mask_dx,Q('0mm'),Q('0mm')]

        rot = ['0.deg','180.deg','0.deg']

        SiPM_LCM_Mask_pos = geom.structure.Position('SiPM_LCM_Mask_pos_far',
                                                pos[0],pos[1],pos[2])

        SiPM_LCM_Mask_rot = geom.structure.Rotation('SiPM_LCM_Mask_rot_far',
                                                rot[0],rot[1],rot[2])

        SiPM_LCM_Mask_pla = geom.structure.Placement('SiPM_LCM_Mask_pla_far',
                                                volume=SiPM_LCM_Mask_lv,
                                                pos=SiPM_LCM_Mask_pos,
                                                rot=SiPM_LCM_Mask_rot)

        main_lv.placements.append(SiPM_LCM_Mask_pla.name)

        # Construct SiPM LV
        SiPM_LCM_shape = geom.shapes.Box('SiPM_LCM_shape',
                                       dx = self.SiPM_LCM_dx,
                                       dy = 2*self.SiPM_LCM_dy,
                                       dz = self.SiPM_LCM_dz)

        SiPM_LCM_lv = geom.structure.Volume('volSiPM_LCM',
                                            material=self.SiPM_LCM_Material,
                                            shape=SiPM_LCM_shape)

        # Place SiPMs next to Fiber plane
        posipm = [self.SiPM_LCM_Mask_dx-self.SiPM_LCM_dx,Q('0cm'),Q('0cm')]

        SiPM_LCM_pos = geom.structure.Position('SiPM_LCM_pos',
                                                posipm[0],posipm[1],posipm[2])

        SiPM_LCM_pla = geom.structure.Placement('SiPM_LCM_pla',
                                                volume=SiPM_LCM_lv,
                                                pos=SiPM_LCM_pos)

        SiPM_LCM_Mask_lv.placements.append(SiPM_LCM_pla.name)

        # Construct and place SiPM PCBs
        SiPM_LCM_PCB_shape = geom.shapes.Box('SiPM_LCM_PCB_shape',
                                       dx = self.SiPM_LCM_PCB_dx,
                                       dy = self.SiPM_LCM_PCB_dy,
                                       dz = self.SiPM_LCM_PCB_dz)

        SiPM_LCM_PCB_lv = geom.structure.Volume('volSiPM_LCM_PCB',
                                            material=self.SiPM_LCM_PCB_Material,
                                            shape=SiPM_LCM_PCB_shape)

        # Place SiPM PCBs next to SiPM Masks
        pos = [-self.Fiber_dz-self.SiPM_LCM_Mask_dx,Q('0cm'),Q('0cm')]

        SiPM_LCM_PCB_pos = geom.structure.Position('SiPM_LCM_PCB_pos',
                                                pos[0],pos[1],pos[2])

        SiPM_LCM_PCB_pla = geom.structure.Placement('SiPM_LCM_PCB_pla',
                                                volume=SiPM_LCM_PCB_lv,
                                                pos=SiPM_LCM_PCB_pos)

        main_lv.placements.append(SiPM_LCM_PCB_pla.name)

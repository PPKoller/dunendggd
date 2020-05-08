""" LCM.py

Original Author: P. Koller, University of Bern

"""

import gegede.builder
from duneggd.LocalTools import localtools as ltools
from gegede import Quantity as Q


class LCMBuilder(gegede.builder.Builder):
    """ Class to build LCM geometry.

    """

    def configure(self,Fibre_dimension,SiPM_LCM_dimension,SiPM_LCM_Mask,SiPM_LCM_PCB,N_Fibre_LCM,N_SiPM_LCM,N_Mask_LCM,**kwargs):

        # Read dimensions form config file
        self.Fibre_rmin             = Fibre_dimension['rmin']
        self.Fibre_rmax             = Fibre_dimension['rmax']
        self.Fibre_dz               = Fibre_dimension['dz']
        self.Fibre_pitch            = Fibre_dimension['pitch']
        self.Fibre_dd               = Fibre_dimension['dd']

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

        self.N_Fibre_LCM            = int(N_Fibre_LCM)
        self.N_SiPM_LCM             = int(N_SiPM_LCM)
        self.N_Mask_LCM             = int(N_Mask_LCM)

        # Material definitons
        self.Fibre_Material         = 'EJ280WLS'
        self.SiPM_LCM_Material      = 'Silicon'
        self.SiPM_LCM_Mask_Material = 'PVT'
        self.SiPM_LCM_PCB_Material  = 'FR4'

        self.Material               = 'LAr'

    def construct(self,geom):
        """ Construct the geometry.

        """

        self.halfDimension      = { 'dx':   self.Fibre_dz
                                            +self.SiPM_LCM_Mask_dx
                                            +self.SiPM_LCM_PCB_dx,

                                    'dy':   self.SiPM_LCM_PCB_dy
                                            +(self.N_Mask_LCM-1)*self.SiPM_LCM_PCB_pitch,

                                    'dz':   self.SiPM_LCM_PCB_dz}

        main_lv, main_hDim = ltools.main_lv(self,geom,'Box')
        print('LCMBuilder::construct()')
        print('main_lv = '+main_lv.name)
        self.add_volume(main_lv)

        # Construct fibre panel
        Fibre_shape = geom.shapes.Tubs('Fibre_panel_shape',
                                       rmin = self.Fibre_rmin,
                                       rmax = self.Fibre_rmax,
                                       #dz = self.Fibre_dz
                                       dz = self.Fibre_dz-self.SiPM_LCM_Mask_dx)

        Fibre_lv = geom.structure.Volume('volFibre',
                                            material=self.Fibre_Material,
                                            shape=Fibre_shape)

        # Place bottom LCM Fibres
        pos = [self.SiPM_LCM_PCB_dx,-2*self.SiPM_LCM_Mask_pitch-self.Fibre_dd-2*self.N_Fibre_LCM*self.Fibre_pitch,Q('0cm')]
        #pos = [self.SiPM_LCM_Mask_dx+self.SiPM_LCM_PCB_dx,-2*self.SiPM_LCM_Mask_pitch-self.Fibre_dd-2*self.N_Fibre_LCM*self.Fibre_pitch,Q('0cm')]
        for i in range(self.N_Fibre_LCM):
            pos[1] = pos[1] + 2*self.Fibre_pitch

            rot = [Q('0.0deg'),Q('90.0deg'),Q('0.0deg')]

            Fibre_pos = geom.structure.Position('Fibre_pos_btm_'+str(i),
                                                    pos[0],pos[1],pos[2])

            Fibre_rot = geom.structure.Rotation('Fibre_rot_btm_'+str(i),
                                                    rot[0],rot[1],rot[2])

            Fibre_pla = geom.structure.Placement('Fibre_pla_btm_'+str(i),
                                                    volume=Fibre_lv,
                                                    pos=Fibre_pos,
                                                    rot=Fibre_rot)

            main_lv.placements.append(Fibre_pla.name)

        pos = [self.SiPM_LCM_PCB_dx,-2*self.SiPM_LCM_Mask_pitch+self.Fibre_dd-2*self.Fibre_pitch,Q('0cm')]
        #pos = [self.SiPM_LCM_Mask_dx+self.SiPM_LCM_PCB_dx,-2*self.SiPM_LCM_Mask_pitch+self.Fibre_dd-2*self.Fibre_pitch,Q('0cm')]
        for i in range(self.N_Fibre_LCM,2*self.N_Fibre_LCM):
            pos[1] = pos[1] + 2*self.Fibre_pitch

            rot = [Q('0.0deg'),Q('90.0deg'),Q('0.0deg')]

            Fibre_pos = geom.structure.Position('Fibre_pos_btm_'+str(i),
                                                    pos[0],pos[1],pos[2])

            Fibre_rot = geom.structure.Rotation('Fibre_rot_btm_'+str(i),
                                                    rot[0],rot[1],rot[2])

            Fibre_pla = geom.structure.Placement('Fibre_pla_btm_'+str(i),
                                                    volume=Fibre_lv,
                                                    pos=Fibre_pos,
                                                    rot=Fibre_rot)

            main_lv.placements.append(Fibre_pla.name)

        # Place center LCM Fibres
        pos = [self.SiPM_LCM_PCB_dx,-self.Fibre_dd-2*self.N_Fibre_LCM*self.Fibre_pitch,Q('0cm')]
        #pos = [self.SiPM_LCM_Mask_dx+self.SiPM_LCM_PCB_dx,-self.Fibre_dd-2*self.N_Fibre_LCM*self.Fibre_pitch,Q('0cm')]
        for i in range(self.N_Fibre_LCM):
            pos[1] = pos[1] + 2*self.Fibre_pitch

            rot = [Q('0.0deg'),Q('90.0deg'),Q('0.0deg')]

            Fibre_pos = geom.structure.Position('Fibre_pos_center_'+str(i),
                                                    pos[0],pos[1],pos[2])

            Fibre_rot = geom.structure.Rotation('Fibre_rot_center_'+str(i),
                                                    rot[0],rot[1],rot[2])

            Fibre_pla = geom.structure.Placement('Fibre_pla_center_'+str(i),
                                                    volume=Fibre_lv,
                                                    pos=Fibre_pos,
                                                    rot=Fibre_rot)

            main_lv.placements.append(Fibre_pla.name)

        pos = [self.SiPM_LCM_PCB_dx,+self.Fibre_dd-2*self.Fibre_pitch,Q('0cm')]
        #pos = [self.SiPM_LCM_Mask_dx+self.SiPM_LCM_PCB_dx,+self.Fibre_dd-2*self.Fibre_pitch,Q('0cm')]
        for i in range(self.N_Fibre_LCM,2*self.N_Fibre_LCM):
            pos[1] = pos[1] + 2*self.Fibre_pitch

            rot = [Q('0.0deg'),Q('90.0deg'),Q('0.0deg')]

            Fibre_pos = geom.structure.Position('Fibre_pos_center_'+str(i),
                                                    pos[0],pos[1],pos[2])

            Fibre_rot = geom.structure.Rotation('Fibre_rot_center_'+str(i),
                                                    rot[0],rot[1],rot[2])

            Fibre_pla = geom.structure.Placement('Fibre_pla_center_'+str(i),
                                                    volume=Fibre_lv,
                                                    pos=Fibre_pos,
                                                    rot=Fibre_rot)

            main_lv.placements.append(Fibre_pla.name)

        # Place top LCM Fibres
        pos = [self.SiPM_LCM_PCB_dx,2*self.SiPM_LCM_Mask_pitch-self.Fibre_dd-2*self.N_Fibre_LCM*self.Fibre_pitch,Q('0cm')]
        #pos = [self.SiPM_LCM_Mask_dx+self.SiPM_LCM_PCB_dx,2*self.SiPM_LCM_Mask_pitch-self.Fibre_dd-2*self.N_Fibre_LCM*self.Fibre_pitch,Q('0cm')]
        for i in range(self.N_Fibre_LCM):
            pos[1] = pos[1] + 2*self.Fibre_pitch

            rot = [Q('0.0deg'),Q('90.0deg'),Q('0.0deg')]

            Fibre_pos = geom.structure.Position('Fibre_pos_top_'+str(i),
                                                    pos[0],pos[1],pos[2])

            Fibre_rot = geom.structure.Rotation('Fibre_rot_top_'+str(i),
                                                    rot[0],rot[1],rot[2])

            Fibre_pla = geom.structure.Placement('Fibre_pla_top_'+str(i),
                                                    volume=Fibre_lv,
                                                    pos=Fibre_pos,
                                                    rot=Fibre_rot)

            main_lv.placements.append(Fibre_pla.name)

        pos = [self.SiPM_LCM_PCB_dx,2*self.SiPM_LCM_Mask_pitch+self.Fibre_dd-2*self.Fibre_pitch,Q('0cm')]
        #pos = [self.SiPM_LCM_Mask_dx+self.SiPM_LCM_PCB_dx,2*self.SiPM_LCM_Mask_pitch+self.Fibre_dd-2*self.Fibre_pitch,Q('0cm')]
        for i in range(self.N_Fibre_LCM,2*self.N_Fibre_LCM):
            pos[1] = pos[1] + 2*self.Fibre_pitch

            rot = [Q('0.0deg'),Q('90.0deg'),Q('0.0deg')]

            Fibre_pos = geom.structure.Position('Fibre_pos_top_'+str(i),
                                                    pos[0],pos[1],pos[2])

            Fibre_rot = geom.structure.Rotation('Fibre_rot_top_'+str(i),
                                                    rot[0],rot[1],rot[2])

            Fibre_pla = geom.structure.Placement('Fibre_pla_top_'+str(i),
                                                    volume=Fibre_lv,
                                                    pos=Fibre_pos,
                                                    rot=Fibre_rot)

            main_lv.placements.append(Fibre_pla.name)

        # Construct and place SiPMs and the corresponding Masks
        SiPM_LCM_Mask_shape = geom.shapes.Box('SiPM_LCM_Mask_shape',
                                       dx = self.SiPM_LCM_Mask_dx,
                                       dy = self.SiPM_LCM_Mask_dy,
                                       dz = self.SiPM_LCM_Mask_dz)

        SiPM_LCM_Mask_lv = geom.structure.Volume('volSiPM_LCM_Mask',
                                            material=self.SiPM_LCM_Mask_Material,
                                            shape=SiPM_LCM_Mask_shape)

        #for n in range(self.N_Mask_LCM):
            # Place Mask LV next to Fibre plane
            #pos = [-self.Fibre_dz+self.SiPM_LCM_PCB_dx,-(self.N_Mask_LCM-1)*self.SiPM_LCM_Mask_pitch+(2*n)*self.SiPM_LCM_Mask_pitch,Q('0mm')]

            #SiPM_LCM_Mask_pos = geom.structure.Position('SiPM_LCM_Mask_pos_'+str(n),
            #                                        pos[0],pos[1],pos[2])

            #SiPM_LCM_Mask_pla = geom.structure.Placement('SiPM_LCM_Mask_pla_'+str(n),
            #                                        volume=SiPM_LCM_Mask_lv,
            #                                        pos=SiPM_LCM_Mask_pos)

            #main_lv.placements.append(SiPM_LCM_Mask_pla.name)

        for n in range(self.N_Mask_LCM):
            # Place Mask LV near end
            pos = [-self.Fibre_dz+self.SiPM_LCM_PCB_dx,-(self.N_Mask_LCM-1)*self.SiPM_LCM_Mask_pitch+(2*n)*self.SiPM_LCM_Mask_pitch,Q('0mm')]

            SiPM_LCM_Mask_pos = geom.structure.Position('SiPM_LCM_Mask_pos_near_'+str(n),
                                                    pos[0],pos[1],pos[2])

            SiPM_LCM_Mask_pla = geom.structure.Placement('SiPM_LCM_Mask_pla_near_'+str(n),
                                                    volume=SiPM_LCM_Mask_lv,
                                                    pos=SiPM_LCM_Mask_pos)

            main_lv.placements.append(SiPM_LCM_Mask_pla.name)

            # Place Mask LV far end
            pos = [self.halfDimension['dx']-self.SiPM_LCM_Mask_dx,-(self.N_Mask_LCM-1)*self.SiPM_LCM_Mask_pitch+(2*n)*self.SiPM_LCM_Mask_pitch,Q('0mm')]

            rot = ['0.deg','180.deg','0.deg']

            SiPM_LCM_Mask_pos = geom.structure.Position('SiPM_LCM_Mask_pos_far_'+str(n),
                                                    pos[0],pos[1],pos[2])

            SiPM_LCM_Mask_rot = geom.structure.Rotation('SiPM_LCM_Mask_rot_far_'+str(n),
                                                    rot[0],rot[1],rot[2])

            SiPM_LCM_Mask_pla = geom.structure.Placement('SiPM_LCM_Mask_pla_far_'+str(n),
                                                    volume=SiPM_LCM_Mask_lv,
                                                    pos=SiPM_LCM_Mask_pos,
                                                    rot=SiPM_LCM_Mask_rot)

            main_lv.placements.append(SiPM_LCM_Mask_pla.name)

        # Construct SiPM LV
        SiPM_LCM_shape = geom.shapes.Box('SiPM_LCM_shape',
                                       dx = self.SiPM_LCM_dx,
                                       #dy = self.SiPM_LCM_dy,
                                       dy = 2*self.SiPM_LCM_dy,
                                       dz = self.SiPM_LCM_dz)

        SiPM_LCM_lv = geom.structure.Volume('volSiPM_LCM',
                                            material=self.SiPM_LCM_Material,
                                            shape=SiPM_LCM_shape)

        #for n in range(int(self.N_SiPM_LCM/self.N_Mask_LCM)):
            # Place SiPMs next to Fibre plane
            #posipm = [self.SiPM_LCM_Mask_dx-self.SiPM_LCM_dx,-(self.N_SiPM_LCM/self.N_Mask_LCM-1)*self.SiPM_LCM_pitch+(2*n)*self.SiPM_LCM_pitch,Q('0cm')]

            #SiPM_LCM_pos = geom.structure.Position('SiPM_LCM_pos_'+str(n),
            #                                        posipm[0],posipm[1],posipm[2])

            #SiPM_LCM_pla = geom.structure.Placement('SiPM_LCM_pla_'+str(n),
            #                                        volume=SiPM_LCM_lv,
            #                                        pos=SiPM_LCM_pos)

            #SiPM_LCM_Mask_lv.placements.append(SiPM_LCM_pla.name)

        # Place SiPMs next to Fibre plane
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

        for n in range(self.N_Mask_LCM):
            # Place SiPM PCBs next to SiPM Masks
            pos = [-self.Fibre_dz-self.SiPM_LCM_Mask_dx,-(self.N_Mask_LCM-1)*self.SiPM_LCM_PCB_pitch+(2*n)*self.SiPM_LCM_PCB_pitch,Q('0cm')]

            SiPM_LCM_PCB_pos = geom.structure.Position('SiPM_LCM_PCB_pos_'+str(n),
                                                    pos[0],pos[1],pos[2])

            SiPM_LCM_PCB_pla = geom.structure.Placement('SiPM_LCM_PCB_pla_'+str(n),
                                                    volume=SiPM_LCM_PCB_lv,
                                                    pos=SiPM_LCM_PCB_pos)

            main_lv.placements.append(SiPM_LCM_PCB_pla.name)

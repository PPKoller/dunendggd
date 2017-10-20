""" GArTPC.py

A basic builder for a gas TPC consisting of a cylindrical chamber 
with two back-to-back rectangular active volmes.

TO DO:

Start splitting the various volumes into separate builders or 
use equivalent existing builders whenever possible.

Validate that rotations for x and y drift are in the correct
direction.

Add in electric field?

"""

import gegede.builder
from duneggd.LocalTools import localtools as ltools
from gegede import Quantity as Q


class GArTPCBuilder(gegede.builder.Builder):
    """ Class to build a gaseous argon TPC geometry.

    Attributes:
        ChamberRadius: Outer radius of the vacuum vessel.
        ChamberLength: Full length of the vacuum vessel.
        EndCapThickness: Thickness of the flat ends of the vessel.
        WallThickness: Thickness of the rounded wall of the vessel.
        ChamberMaterial: Material used to build the vacuum vessel.
        BField: Magnetic field in the volume.
        Material: Name of gas material.
        GasDensity: Density of gas (only used for custom gas mixes).
        Composition: Composition of a custom gas mixture.
        halfDimension: Dimensions of volume holding the TPC geometry.
        tpcDimension: Dimensions of each rectangular TPC volume.
        HalfX: Half length of TPC in x-direction
        HalfY: Half length of TPC in y-direction
        HalfZ: Half of drift distance.
        Drift: Drift axis
        TPCGap: Half of spacing between TPCs. Reset when central 
                electrode is created.
        SmallGap: A small distance to help prevent overlaps
        PadThickness: Thickness of PCB holding readout pads
        PadMaterial: Material of PCB holding readout pads
        PadOffset: Offset from TPC active volume (due to wire grids)
        PadFrameThickness: Thickness of support structure behind PCB
        PadFrameMaterial: Material of support structure.
        CentElectrodeHCThickness: Thickness of honeycomb or similar
                structure separating two electrode sheets
        CentElectrodeThickness: Thickness of mylar (or similar)
                sheet used to make the central electrode

    """

    def configure(self,chamberDimension,tpcDimension,
                  halfDimension,Material,bfield=None,drift='z',**kwargs):

        """ Set the configuration for the geometry.

            The keywords MaterialName and Density should only be used
            if Material is a dict-type rather than a string.

            Args:
                chamberDimension: Outer dimensions of vauum vessel.
                    Dict. with keys 'r' and 'dz'
                tpcDimension: Dimensions of each TPC.
                    Dict with keys 'dx','dy','dz'
                halfDimension: Half-dimensions of bounding volume.
                    Dict with keys 'rmin', 'rmax' and 'dz' (dz=half of length)
                Material: Gas material. String if using a standard
                    material, dict in the form {material:mass_fraction,...}
                bfield: Magnetic field (3D array-like). Don't use if a
                    magnetic field was set in a parent volume.
                drift: The drift direction. (x, y, or z)
                kwargs: Additional keyword arguments. Allowed are:
                    EndCapThickness, WallThickness, 
                    ChamberMaterial, MaterialName, Density,
                    PadThickness, PadMaterial, PadOffset,
                    PadFrameThickness,PadFrameMaterial
                    CentElectrodeHCThickness,        
                    CentElectrodeThickness
        """

        # The vacuum chamber is a G4Tubs for now
        self.ChamberRadius = chamberDimension['r']
        self.ChamberLength = chamberDimension['dz']

        self.EndCapThickness = Q("1cm")
        self.WallThickness = Q("1cm")
        self.ChamberMaterial = "Steel"

        if "EndCapThickness" in kwargs.keys():
            self.EndCapThickness = kwargs['EndCapThickness']
        if 'WallThickness' in kwargs.keys():
            self.WallThiciness = kwargs['WallThickness']
        if 'ChamberMaterial' in kwargs.keys():
            self.ChamberMaterial = kwargs['ChamberMaterial']

        # Should be a 3D array Quantity objects
        # Will support dipole and solenoid type fields
        # Really should be set with a magnet builder but here for testing
        # Not currently used
        self.BField = bfield
        
        # The gas
        if type(Material)==str:
            # Set from a pre-defined material
            self.Material = Material
            self.GasDensity = None
            self.Composition = None
        else:
            # Set from a dictionary of materials & mass fractions
            comp = []
            for k in Material.keys():
                comp.append( (k,Material[k]) )
            self.Composition = tuple(comp)
            self.Material = kwargs['MaterialName']
            self.GasDensity = kwargs['Density']
 
        self.halfDimension = halfDimension
        # The TPCs: Boxes at the center of the vacuum chamber
        self.tpcDimension = tpcDimension
        self.HalfX = tpcDimension['dx']/2 
        self.HalfY = tpcDimension['dy']/2
        self.HalfZ = tpcDimension['dz']/2
        self.Drift = drift
        # A bit of space for the central electrode

        self.TPCGap = Q('2mm') 
        self.SmallGap = Q('0.001mm')
        self.CentElectrodeHCThickness = Q('6mm')
        self.CentElectrodeThickness = Q('0.02mm')

        # Readout Pad Stuff

        self.PadThickness = Q('5mm')
        self.PadMaterial = 'FR4'
        self.PadOffset = Q('9mm')
        self.PadFrameThickness = Q('1.5cm')
        self.PadFrameMaterial = 'Aluminum'

        if 'PadThickness' in kwargs.keys():
            self.PadThickness = kwargs['PadThickness']
        if 'PadMaterial' in kwargs.keys():
            self.PadMaterial = kwargs['PadMaterial']
        if 'PadFrameThickness' in kwargs.keys():
            self.PadFrameThickness = kwargs['PadFrameThickness']
        if 'PadFrameMaterial' in kwargs.keys():
            self.PadFrameMaterial = kwargs['PadFrameMaterial']
        if 'PadOffset' in kwargs.keys():
            self.PadOffset = kwargs['PadOffset']
        if 'CentElectrodeHCThickness' in kwargs.keys():
            self.CentElectrodeHCThickness = \
                 kwargs['CentElectrodeHCThickness']
        if 'CentElectrodeThickness' in kwargs.keys():
            self.CentElectrodeThickness = \
                 kwargs['CentElectrodeThickness']


    def construct(self,geom):
        """ Construct the geometry.

        The standard geometry consists of a cylindrical vessel 
        filled with gas. Two TPC sensitive volumes are placed
        within the gas, as is a central electrode.
        After that, a readout plane and field cage are added 
        to each TPC.

        args:
            geom: The geometry

        """

        # If using a custom gas, define here
        if self.Composition is not None:
            geom.matter.Mixture(self.Material,density=self.GasDensity,components=self.Composition)

        main_lv, main_hDim = ltools.main_lv(self,geom,'Tubs')
        print('GasTPCBuilder::construct()')
        print('main_lv = ',main_lv.name)
        self.add_volume(main_lv)

        # Construct the chamber
        tpc_chamber_shape = geom.shapes.Tubs('TPCChamber',
                                       rmax = self.ChamberRadius,
                                       dz = self.ChamberLength*0.5)
        tpc_chamber_lv = geom.structure.Volume('TPCChamber_vol',
                                               material=self.ChamberMaterial,
                                               shape=tpc_chamber_shape)

        if self.BField is not None:
            tpc_chamber_lv.params.append(('BField',self.BField))
        # Place into main LV
        pos = [Q('0m'),Q('0m'),Q('0m')]
        tpc_chamber_pos = geom.structure.Position('TPCChamber_pos',
                                                  pos[0],pos[1],pos[2])
        tpc_chamber_pla = geom.structure.Placement('TPCChamber_pla',
                                                   volume=tpc_chamber_lv,
                                                   pos=tpc_chamber_pos)
        main_lv.placements.append(tpc_chamber_pla.name)

  
        # Add in the gas volume
        tpc_gas_shape = geom.shapes.Tubs('TPCGas',
                             rmax=self.ChamberRadius-self.WallThickness,
                             dz=0.5*self.ChamberLength - self.EndCapThickness)

        tpc_gas_lv = geom.structure.Volume('TPCGas_vol',
                                           material='GAr',#self.Material,
                                           shape=tpc_gas_shape)

        # Place gas into the chamber
        pos = [Q('0m'),Q('0m'),Q('0m')]
        tpc_gas_pos = geom.structure.Position('TPCGas_pos',
                                              pos[0],pos[1],pos[2])
        tpc_gas_pla = geom.structure.Placement('TPCGas_pla',
                                               volume=tpc_gas_lv,
                                               pos=tpc_gas_pos)
        tpc_chamber_lv.placements.append(tpc_gas_pla.name)

        
        # Construct the TPCs
        self.construct_tpcs(geom,tpc_gas_lv)
        

    def construct_tpcs(self,geom,lv):
        """ Construct the two TPCs along with their 
        field cages and readout plaen

        args:
            geom: The geometry:
            tpc_gas_lv: The vessel gas volume where
                want to place the TPCs

        """

        pos1 = []
        pos2 = []
        rot1 = []
        rot2 = []
        
        if self.Drift == 'y':

            pos1 = [0,1,0]
            pos2 = [0,-1,0]
            rot1 = [Q('270deg'),Q('0deg'),Q('0deg')]
            rot2 = [Q('90deg'),Q('0deg'),Q('0deg')]

        elif self.Drift == 'x':

            pos1 = [1,0,0]
            pos2 = [-1,0,0]
            rot1 = [Q('0deg'),Q('90deg'),Q('0deg')]
            rot2 = [Q('0deg'),Q('270deg'),Q('0deg')]

        else:
            pos1 = [0,0,-1]
            pos2 = [0,0,1]
            rot1 = [Q('0deg'),Q('0deg'),Q('0deg')]
            rot2 = [Q('180deg'),Q('0deg'),Q('0deg')]

        self.construct_central_electrode(geom,rot1,lv)
        self.construct_tpc(geom,"TPC1",pos1,rot1,lv)
        self.construct_tpc(geom,"TPC2",pos2,rot2,lv)

    def construct_central_electrode(self,geom,rot,lv):
        """ Create the central electrode

        Currently is similar to the ALICE design.
        The electrode consists of two thin layers
        of mylar with a thicker layer of a honeycomb
        structure to support things without providing
        much material.

        Implemented as two nested boxes.

        Args:
            geom: The geometry
            rot: A 3D array giving the rotation
            lv: The logical volume where we want to
                place the electrode.

        """
        

        # Create the shape and logical volume
        
        cent_hc_dx = self.CentElectrodeHCThickness
        cent_my_dx = self.CentElectrodeThickness

        cent_elec_shape = geom.shapes.Box('cent_elec_shape',
                                          self.HalfX,
                                          self.HalfY,
                                          cent_hc_dx/2+cent_my_dx)
        cent_elec_lv = geom.structure.Volume('cent_elec_vol',material = 'Mylar',
                                       shape=cent_elec_shape)

        elec_rot = geom.structure.Rotation('cent_elec_rot',rot[0],rot[1],rot[2])
        # Create a placement
        cent_elec_pla = geom.structure.Placement('cent_elec_pla',
                                            volume=cent_elec_lv,
                                            rot=elec_rot
                                           )

        lv.placements.append(cent_elec_pla.name)

        # The honeycomb structure

        cent_hc_shape = geom.shapes.Box('cent_hc_shape',
                                          self.HalfX-self.SmallGap,
                                          self.HalfY-self.SmallGap,
                                          cent_hc_dx/2)
        cent_hc_lv = geom.structure.Volume('cent_hc_vol',material = 'NomexHoneycomb',
                                       shape=cent_hc_shape)

        elec_rot = geom.structure.Rotation('cent_hc_rot',rot[0],rot[1],rot[2])
        # Create a placement
        cent_hc_pla = geom.structure.Placement('cent_hc_pla',
                                            volume=cent_hc_lv,
                                            rot=elec_rot
                                           )

        cent_elec_lv.placements.append(cent_hc_pla.name)
 
        self.TPCGap = cent_hc_dx/2+cent_my_dx+self.SmallGap

    def construct_tpc(self,geom,name,pos_vec,rot,lv):
        """ Construct a TPC. Each TPC includes the gas volume,
            a field cage, and a readout plane.

        Args:

            geom: The geometry.
            name: The name of the TPC. Should be unique.
            pos_vec: A unit vector giving the direction about
                     which the TPC should be translated. 
                     Array-like.
            rot: A rotation vector. Array-like
            lv: The parent volume.

        """
        # First, set up the main rotation and position to be used for the TPC
        tpc_rot = geom.structure.Rotation(name+'_rot',rot[0],rot[1],rot[2])
        pos = [ x*(self.HalfZ + self.TPCGap) for x in pos_vec]
        tpc_pos = geom.structure.Position(name+'_pos',pos[0],pos[1],pos[2])
 
        # Create the shape and logical volume
        tpc_shape = geom.shapes.Box(name+'_shape',self.HalfX,self.HalfY,self.HalfZ)
        tpc_lv = geom.structure.Volume(name+'_vol',material = self.Material,
                                       shape=tpc_shape)

        # Create a placement
        tpc_pla = geom.structure.Placement(name+'_pla',
                                            volume=tpc_lv,
                                            pos=tpc_pos,
                                            rot=tpc_rot
                                           )

        # The gas volumes are sensitive detectors
        tpc_lv.params.append(('SensDet',name))

        # Place in the main gas volume
        lv.placements.append(tpc_pla.name)

        self.construct_readout_plane(geom,name,pos_vec,tpc_rot,lv)
        self.construct_fieldcage(geom,name,tpc_pos,tpc_rot,lv)

    def construct_readout_plane(self,geom,name,pos_vec,tpc_rot,lv):
        """ Construct a readout plane.

        This creates a PCB volume which holds the readout pads and
        a support structure (modeled just as a box in this simplified
        geometry). Wires, readout pad electrodes, and support structures
        such as posts to hold wires or edges of readout regions are not
        modeled. Based on ALICE TPC specs.

        Args:
            geom: The geometry.
            name: The name of the TPC.
            pos_vec: A unit vector pointing in the direction which this
                     should be moved from the center. Array-like.
            tpc_rot: The rotation for this TPC. A Rotation object. 
            lv: The parent volume.

        """
        padpos = [x*(self.TPCGap+2*self.HalfZ+self.PadOffset
                  +self.PadThickness/2) for x in pos_vec]
        pad_pos = geom.structure.Position(name+'pad_pos',
                                          padpos[0],
                                          padpos[1],
                                          padpos[2])

        pad_shape = geom.shapes.Box(name+'pad_shape',
                                    self.HalfX,
                                    self.HalfY,
                                    self.PadThickness/2)
        pad_lv = geom.structure.Volume(name+'pad_vol',
                                       material=self.PadMaterial,
                                       shape=pad_shape)
        pad_pla = geom.structure.Placement(name+'pad_pla',volume=pad_lv,
                                           pos=pad_pos,
                                           rot=tpc_rot)

        lv.placements.append(pad_pla.name)

        
 
        # Pad support frame
        padframepos = [padpos[x] + pos_vec[x]*(self.SmallGap
                       +self.PadFrameThickness/2) for x in range(3)]

        padframe_pos = geom.structure.Position(name+'padframe_pos',
                                               padpos[0],
                                               padpos[1],
                                               padpos[2])

        padframe_shape = geom.shapes.Box(name+'padframe_shape',
                                         self.HalfX,
                                         self.HalfY,
                                         self.PadFrameThickness/2)
        padframe_lv = geom.structure.Volume(name+'padframe_vol',
                                            material=self.PadFrameMaterial,
                                            shape=padframe_shape)
        padframe_pla = geom.structure.Placement(name+'padframe_pla',
                                                volume=padframe_lv,
                                                pos=padframe_pos,
                                                rot=tpc_rot)

        lv.placements.append(padframe_pla.name)

    def construct_fieldcage(self,geom,name,tpc_pos,tpc_rot,lv):
        """ Construct the field cage for a TPC.

        Currently constructs the support structures for the field 
        cage. This is based on the ALICE TPC design. The field cage
        structure consists of a central honeycomb structure 
        surrounded on both sides by kevlar and then tedlar.

        Field cage posts and conductive strips are not currently 
        modeled.
 
        Args:
            geom: The geometry 
            name: The name of the TPC
            tpc_pos: The position of the TPC center. A Position object.
            tpc_rot: The rotation of this TPC. A Rotation object. 
            lv: The parent volume.

        """
        # Outer Tedlar layers
        fc_dx = Q('21.3mm')
        fc_out_x = self.HalfX + fc_dx + self.SmallGap
        fc_out_y = self.HalfY + fc_dx + self.SmallGap
        fc_in_x = self.HalfX + self.SmallGap
        fc_in_y = self.HalfY + self.SmallGap
        cvf_dx = Q('0.05mm')

        fc_cvf_1 = geom.shapes.Box(name+'fc_cvf1_shape',
                                   fc_out_x,fc_out_y,self.HalfZ)
        fc_cvf_0 = geom.shapes.Box(name+'fc_cvf0_shape',
                                   fc_in_x,fc_in_y,self.HalfZ+Q('1mm'))
        fc_cvf_shape = geom.shapes.Boolean(name+'fc_cvf_shape',
                                           type='subtraction',
                                           first=fc_cvf_1,
                                           second=fc_cvf_0)
        fc_cvf_lv = geom.structure.Volume(name+'fc_cvf_vol',
                                          material='CVF',
                                          shape=fc_cvf_shape)
        fc_cvf_pla = geom.structure.Placement(name+'fc_cvf_pla',
                                             volume=fc_cvf_lv,
                                             pos=tpc_pos,
                                             rot=tpc_rot)
        lv.placements.append(fc_cvf_pla.name)

        # Kevlar Prepreg (Kevlar/epoxy mixture) layers
        kev_dx = Q('0.6mm')
        fc_kev_1 = geom.shapes.Box(name+'fc_kev1_shape',
                                   fc_out_x-cvf_dx,
                                   fc_out_y-cvf_dx,
                                   self.HalfZ-2*self.SmallGap)
        fc_kev_0 = geom.shapes.Box(name+'fc_kev0_shape',
                                   fc_in_x+cvf_dx,
                                   fc_in_y+cvf_dx,
                                   self.HalfZ-self.SmallGap)
        fc_kev_shape = geom.shapes.Boolean(name+'fc_kev_shape',
                                           type='subtraction', 
                                           first=fc_kev_1,
                                           second=fc_kev_0)
        fc_kev_lv = geom.structure.Volume(name+'fc_kev_vol',
                                          material='KevlarPrepreg',
                                          shape=fc_kev_shape)
        fc_kev_pla = geom.structure.Placement(name+'fc_kev_pla',
                                              volume=fc_kev_lv)
        fc_cvf_lv.placements.append(fc_kev_pla.name)

        # Nomex Honeycomb layer
        fc_hc_1 = geom.shapes.Box(name+'fc_hc1_shape',
                                   fc_out_x-cvf_dx-kev_dx,
                                   fc_out_y-cvf_dx-kev_dx,
                                   self.HalfZ-4*self.SmallGap)
        fc_hc_0 = geom.shapes.Box(name+'fc_hc0_shape',
                                   fc_in_x+cvf_dx+kev_dx,
                                   fc_in_y+cvf_dx+kev_dx,
                                   self.HalfZ-3*self.SmallGap)
        fc_hc_shape = geom.shapes.Boolean(name+'fc_hc_shape',
                                           type='subtraction',
                                           first=fc_hc_1,
                                           second=fc_hc_0)
        fc_hc_lv = geom.structure.Volume(name+'fc_hc_vol',
                                          material='NomexHoneycomb',
                                          shape=fc_hc_shape)
        fc_hc_pla = geom.structure.Placement(name+'fc_hc_pla',
                                              volume=fc_hc_lv)
        fc_kev_lv.placements.append(fc_hc_pla.name)

import numpy as np

class beamPath(object):

	"""
	-- beamPath --

    	A beam path object consists of a few things:
    
        * A seed beam. This defines the "input beam" of your system.
                When calculating the beam properties somewhere in a beam
                path, this is the origin of the beam which is propagated 
                around the system. It is defined by a beamq object which is
                stored in the beamPath.seedq property, also the location
                of the seed beam in the beam path is defined by the 
                beamPath.seedz property. This beam can be defined anywhere
                in the beam path and need not be at the "beginning."
     
        * A target beam. This defines the "output beam" of your system.
                This is the beam which you would like to match into.
                It is defined similarly to the seed beam by the properties
                beamPath.targetq and beamPath.targetz. It is also used by 
                the various optimization routines when trying to maximize 
                the mode overlap with the seed beam.
     
        * Components. These are the various optical components in the beam
                path which affect the propagation of beams in the path.
                It is a vector array of objects in the component class.
                Each component has a certain transfer matrix and position,
                these properties are stored in the component class.
                The beamPath class stores the array of components in the 
                beamPath.components array. The ordering of the elements in 
                this array is always by increasing z position. This means
                that the array index of components in the component array
                may change if the z positions are changed. The component
                class also has a 'label' property, which allows a component
                to be indexed unambiguously. See beamPath.component below.
     
    	The beamPath class also has methods which facilitate in calculating 
        beam propagation and laying out your beam path.
    """

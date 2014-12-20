import numpy as np

class component:
	
	'''
	-- component --

		The component class is used to represent optical components.
        The properties associated with a component object are: the 
        position (z), the ray transfer matrix, or ABCD matrix (M) and the
        label. Component objects used with the special constructors also
        have a 'parameters' property.

        Methods:
        component - The component constructor, for making a component
    	            object. The arguments are (M,z,label)
		component.duplicate - creates and identical component object.
 		component.lens - creates a lens component.
    	component.dielectric - creates a dielectric (thick lens) component.
    	component.curvedMirror - creates a curved mirror object.
    	component.flatMirror - creates flat mirror object.
    	component.propagator - creates free space propagator object.
    	component.combine - creates a composit component object with a 
    						tranfer matrix which is the product of the 
    						components in the calling array. 
    '''
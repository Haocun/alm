import numpy as np

class component:
    
    """
    -- component --

        The component class is used to represent optical components.
        The properties associated with a component object are: the 
        position (z), the ray transfer matrix, or ABCD matrix (M) and the
        label. Component objects used with the special constructors also
        have a 'parameters' property.

        Methods:
        component - The component constructor, for making a component
                    object. The arguments are (M,z,label)
        component.duplicate - creates an identical component object.
        component.lens - creates a lens component.
        component.dielectric - creates a dielectric (thick lens) component.
        component.curvedMirror - creates a curved mirror object.
        component.flatMirror - creates flat mirror object.
        component.propagator - creates free space propagator object.
        component.combine - creates a composit component object with a 
                            tranfer matrix which is the product of the 
                            components in the calling array. 
    """


    # these methods are to construct different types of components

    def __init__ (self, label = "none", z = 0):

        self.label = label
        self.z = z


    @staticmethod
    def lens (focalLength, Z = 0, label = 0):

        #   -- component.lens --
        # Create a lens component object.
        # Example:
        # component.lens(f,z,label);
        # This creates a lens component with focal length f at position
        # z. label is a string which is used to identify the component.

        numcomps = len(focalLength)

        if numcomps > 1:
            zlength = len(Z)

            if zlength != numcomps:
                if zlength != 1:
                    raise Exception ("List of focal lengths must be the\
                                    same length as list of z positions.")                
                Z = Z[0:numcomps]

            if label != 0:
                lablength = len(label)

                if isinstance(label, str):
                    lablength = 1

                if lablength != numcomps:
                    if zlength != 1:
                        raise Exception ("List of focal lengths must be the\
                                        same length as list of labels.") 
                    
                    singlabel = label
                    label = []

                    for jj in xrange(1,numcomps+1):
                        label.append(singlabel)

#line77



















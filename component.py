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


    def lens (self, focalLength, Z = 0, label = 0):

        #   -- component.lens --
        # Create a lens component object.
        # Example:
        # component.lens(f,z,label);
        # This creates a lens component with focal length f at position
        # z. label is a string which is used to identify the component.

        self.focalLength = focalLength
        self.Z = Z
        self.label = label

        self.numcomps = len(self.focalLength)

        if self.numcomps > 1:
            self.zlength = len(Z)

            if self.zlength != self.numcomps:
                if self.zlength != 1:
                    raise Exception ("List of focal lengths must be the\
                                    same length as list of z positions.")
                else:
                    self.Z = self.Z[0:self.numcomps]

            if self.label != 0:
                self.lablength = len(self.label)

                if isinstance(self.label, str):
                    self.lablength = 1

                if self.lablength != self.numcomps:
                    if self.zlength != 1:
                        raise Exception ("List of focal lengths must be the\
                                        same length as list of labels.") 
                    
                    else:
                        self.singlabel = self.label
                        self.label = []

                        for jj in xrange(1,self.numcomps+1):
                            self.label.append(self.singlabel)

#line77




















    def flatMirror (self, Z = 0, label):

        #   -- component.flatMirror --
        # Create a flat Mirror component object.
        # Example:
        # component.flatMirror(z,label);
        # This creates a flat mirror component at position z.
        # Label is a string which is used to identify the component.

        self.M = [ 1, 0; 0, 1];
        
        self.type = 'flat mirror'
        self.label = label



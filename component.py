import numpy as np
import numpy.lib.recfunctions as nprf

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

    def __init__ (self, M = np.matrix([[1,0],[0,1]]), Z = 0, label = None):

        self.M = M
        self.z = Z
        self.type = 'other'
        self.parameters = [0]
        
        if label is not None:
            self.label = label


    @staticmethod
    def lens (focalLength = [0], Z = [0], label = None):

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
                Z = Z*numcomps

            if label is not None:
                lablength = len(label)

                if lablength != numcomps:
                    if lablength != 1:
                        raise Exception ("List of focal lengths must be the\
                                        same length as list of labels.") 
                    label = label*numcomps

            lenslist = [[0,0,0]] # make the count start from 1
            for n in range(numcomps):
                c = component()
                if label is not None:
                    cl = c.lens([focalLength[n]],[Z[n]],[label[n]])
                else:
                    cl = c.lens([focalLength[n]],[Z[n]])
                lenslist.append(cl)
            return lenslist 


        M = np.matrix([[1,0],[-1/focalLength[0],1]])        

        o = component(M, Z)
        o.type = 'lens'
        o.parameters = nprf.rec_append_fields(o.parameters,'focalLength',[fl],dtypes = [(float)])
        if label is not None:
            o.label = label[0]
        else:
            o.label = 'no label'
        return o


#Example:
#A = component.lens([2,3],[4,5],['lb1','lb2'])
#print (A[1].type, A[1].parameters.focalLength, A[1].label)


    @staticmethod
    def curvedMirror (radiusOfCurvature = [0], Z = [0], label = None):

        # -- component.curvedMirror --
        # Create a curved mirror component object.
        # Example:
        # mylens = component.curvedMirror(ROC,z,label);
        # This creates a lens component with radius of curvature ROC at position
        # z. label is a string which is used to identify the component.

        numcomps = len(radiusOfCurvature)

        if numcomps > 1:
            zlength = len(Z)

            if zlength != numcomps:
                if zlength != 1:
                    raise Exception ("List of radii must be the\
                                    same length as list of z positions.")                
                Z = Z*numcomps

            if label is not None:
                lablength = len(label)

                if lablength != numcomps:
                    if lablength != 1:
                        raise Exception ("List of radii must be the\
                                        same length as list of labels.") 
                    label = label*numcomps

            curvedMirrorlist = [[0,0,0]] # make the count start from 1
            for n in range(numcomps):
                c = component()
                if label is not None:
                    ccm = c.curvedMirror([radiusOfCurvature[n]],[Z[n]],[label[n]])
                else:
                    ccm = c.curvedMirror([radiusOfCurvature[n]],[Z[n]])
                curvedMirrorlist.append(ccm)
            return curvedMirrorlist


        M = np.matrix([[1,0],[-2/radiusOfCurvature[0],1]])        

        o = component(M, Z)
        o.type = 'curved mirror'
        o.parameters = nprf.rec_append_fields(o.parameters,'ROC',[radii],dtypes = [(float)])
        if label is not None:
            o.label = label[0]
        else:
            o.label = 'no label'
        return o


#Example:
#B = component.curvedMirror([10,20],[40,60],['cM1','cM2'])
#print (B[2].type, B[1].parameters.ROC, B[1].label)


    @staticmethod
    def flatMirror (Z = 0, label = None):

        #   -- component.flatMirror --
        # Create a flat Mirror component object.
        # There can only be one flat mirror in an optical path.
        # Example:
        # component.flatMirror(z,label);
        # This creates a flat mirror component at position z.
        # Label is a string which is used to identify the component.

        M = np.matrix([[1, 0],[0, 1]]) 
        
        o = component(M, Z)
        o.type = 'flat mirror'
        if label is not None:
            o.label = label
        else:
            o.label = 'no label'
        return o
 
#Example:
#C = component.flatMirror(60,'fm1')
#print (C.type, C.z, C.label)


    @staticmethod
    def dielectric (R1, R2, thickness = 0, n = 1, Z = 0, label = None):
        # -- component.dielectric --
        # Create a dielectric component object.
        # Example:
        # mylens = component.dielectric(R1, R2, thickness, n, Z, label);
        # This creates a dielectric (thick lens) component at position
        # z. label is a string which is used to identify the component.
        
        dist = np.matrix([[1, thickness],[0, 1]])
        refract1 = np.matrix([[1, 0], [(n-1)/R2, n]])
        refract2 = np.matrix([[1, 0], [(1-n)/(R1*n), 1/n]])
        M = refract1*dist*refract2 

        o = component(M, Z)
        o.type = 'dielectric'
        o.parameters = nprf.rec_append_fields(o.parameters,'length',[thickness],dtypes = [(float)])
        if label is not None:
            o.label = label
        else:
            o.label = 'no label'
        return o

#Example:
#D = component.dielectric(1,2,0.1,1.3,5,'fm1')
#print (D.type, D.parameters.length, D.label)

       
    @staticmethod
    def propagator (DZ = 0, Z = 0, label = None):

        # -- component.propagator --
        # Create a free-space propagator component object.
        # Example:
        # mylens = component.propagator(dz,z,label);
        # This creates a propagator component with length dz at position
        # z. label is a string which is used to identify the component.

        M = np.matrix([[1, DZ], [0, 1]]) 

        o = component(M, Z)
        o.type = 'propagator'
        o.parameters = nprf.rec_append_fields(o.parameters,'length',[DZ],dtypes = [(float)])
        if label is not None:
            o.label = label
        else:
            o.label = 'no label'
        return o

#Example:
E = component.propagator(0.5, 2, 'prop1')
print (E.type, E.parameters.length, E.label)


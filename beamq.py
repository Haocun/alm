import numpy as np
import matplotlib.pyplot as plt

class beamq:
    
    """
    -- beamq --
    
        The beamq class is used for calculating the properties of a 
        gaussian beam. It stores the complex beam q parameter used to 
        chatacterize a gaussian beam. By setting the 'q' and 'wavelength' 
        properties of a beamq object, it can return various properties
        of the beam.

        Constructor Methods:
            Note: The default value of wavelength is 1064nm.
            beamq(q,wavelength) - returns a beamq object with the defined q
                value for wavelength (in meters).
            beamq.beamWaistAndZ(w0,Z,wavelength) - returns a beamq object
                with a waist of w0 (in meters) at position Z (in meters)
                with wavelength (in meters).
            beamq.beamWaistAndR(w0,R,wavelength) - returns a beamq object
                with a waist of w0 (in meters) and a radius of R (in meters)
                at Z=0 with wavelength (in meters). 
            beamq.beamWidthAndR(w,R,wavelength) - returns a beamq object
                with a beam width of w (in meters) at Z=0 and a radius of 
                R (in meters) Z=0 with wavelength (in meters).

        Properties:
            beamWidth - the 1/e electric field amplitude radius.
            waistSize - the beam width at the waist of the beam.
            waistZ - the relative distance from the beam waist, this is
                    also the real part of the q parameter.
            divergenceAngle - the angle between the propagation axis and
                    the diverging radius of the beam in the far field.
            radiusOfCurvature - The radius of curvature of the constant 
                    phase front of the beam.
            rayleighRange - The axial length scale of the beam focus,
                    this is also the imaginary part of the q parameter.
    """
    
    def __init__(self, q, wavelength = 1064e-9):
        
        self.q = q
        self.wavelength = wavelength
        
    

    @staticmethod
    def beamWaistAandZ(w0, Z, wavelength = 1064e-9):
        
        ZR = np.pi*w0**2/wavelength
        q = Z+1j*ZR
        
        return beamq(q, wavelength)
        
    
    @staticmethod
    def beamWaistAandR(w0, R, wavelength = 1064e-9):
        
        ZR = np.pi*w0**2/wavelength
        q = (1/R-1j/ZR)**(-1)
        
        return beamq(q, wavelength)
    

    @staticmethod
    def beamWidthAandR(w, R, wavelength = 1064e-9):
        
        Z = R/(1+(R*wavelength/np.pi/w**2)**2)
        ZR = np.sqrt(Z*(R-Z))
        q = Z+1j*ZR
        
        return beamq(q, wavelength)
        
    
    @staticmethod
    def transformValue(qvalin, M = np.matrix ('1,0;0,1')):
        
        return (M.item(0,0)*qvalin+M.item(0,1))/(M.item(1,0)*qvalin+M.item(1,1))
    
        
        
    # data access methods

    def set_q(self, qvalue):
        
        if qvalue.imag < 0:
            raise Exception ("imaginary part of q parameter must be positive")
        
        self.q = qvalue
        return self

    

    def  set_wavelength(self, newwavelength):
        
        if newwavelength <= 0:
            raise Exception ("wavelength must be positive")

        self.wavelength = newwavelength
        return self
    


    def duplicate(self):
        
        # -- beamq.duplicate --
        #    
        #    Make a copy of a beamq object with the same properties as the original
        #    Example:
        #    beamcopy = beam1.duplicate();

        return beamq(self.q, self.wavelength)



    # dependent properties
    @property
    def waistSize(self):

        return np.sqrt((self.q.imag)*self.wavelength/np.pi)


    @property
    def rayleighRange(self):

        w0 = self.waistSize

        return np.pi*w0**2/self.wavelength


    @property
    def divergenceAngle(self):

        w0 = self.waistSize
        zR = self.rayleighRange

        return w0/zR


    @property
    def waistZ(self):

        return self.q.real


    @property
    def beamWidth(self):

        z = self.waistZ
        zR = self.rayleighRange
        w0 = self.waistSize

        return w0*np.sqrt(1+(z/zR)**2)


    @property
    def radiusOfCurvature(self):

        z = self.waistZ
        zR = self.rayleighRange

        if z != 0:
            return z*(1+(zR/z)**2)

        else:
            return np.inf



    # methods for making useful calculations

    def overlap(self, beam1, beam2):
    
        # -- beamq.overlap --
        #
        #    Find the overlap fraction of 2 beams (assumes axial symmetry).
        

        q1 = beam1.q
        q2 = beam2.q

        w1 = beam1.waistSize
        w2 = beam2.waistSize
        self.wavelength = beam1.wavelength

        if self.wavelength != beam2.wavelength:
            raise Exception ("Cannot overlap beams of different wavelength.")

        fraction = (2*np.pi/self.wavelength*w1*w2*1/abs(q2.conjugate()-q1))**2
        # square for 2D modematching
        return fraction



    def transform (self, M = np.matrix ('1,0;0,1')):

        # -- beamq.transform --
        #  
        #    Creates a new beamq object after being transformed by an ABCD matrix.
        #    Example:
        #    newbeam = oldbeam.transform(M)
        #    This transforms the oldbeam object and placed the new object into
        #    newbeam, using the ABCD matrix M.

        qin = self.q
        qout = self.transformValue(qin,M)

        beamout = self.duplicate()
        beamout.set_q(qout)

        return beamout


    # plotting

    def plotBeamWidth (self, qarray, zdomain, *args):

        # -- beamq.plotBeamWidth --
        #
        #    Given an array of beamq objects, this function will plot the beamwidth.
        
        ploth = plt.plot(zdomain, [q.get_beamWidth(q) for q in qarray], *args)
        plt.plot(zdomain, [-q.get_beamWidth(q) for q in qarray], *args)

        plt.show()

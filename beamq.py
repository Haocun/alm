import numpy as np
import matplotlib.pyplot as plt

class beamq(object):
    
    """
    -- beamq --
    
        The beamq class is used for calculating the properties of a 
        gaussian beam. It stores the complex beam q parameter used to 
        chatacterize a gaussian beam. By setting the 'q' and 'lambda' 
        properties of a  beamq object, it can return various properties
        of the beam.

        Constructor Methods:
            Note: The default value of lambda is 1064nm.
            beamq(q,lambda) - returns a beamq object with the defined q
                value for wavelength lambda (in meters).
            beamq.beamWaistAndZ(w0,Z,lambda) - returns a beamq object
                with a waist of w0 (in meters) at position Z (in meters)
                with wavelength lambda (in meters).
            beamq.beamWaistAndR(w0,R,lambda) - returns a beamq object
                with a waist of w0 (in meters) and a radius of R (in meters)
                at Z=0 with wavelength lambda (in meters). 
            beamq.beamWidthAndR(w,R,lambda) - returns a beamq object
                with a beam width of w (in meters) at Z=0 and a radius of 
                R (in meters) Z=0 with wavelength lambda (in meters).

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
    
    def __init__ (self, qvalue, wavelength = 1064e-9):  #???
        
        self.q = qvalue
        self.wavelength = wavelength
        self.waistSize = 0.
        self.waistZ = 0.
        self.divergenceAngle = 0.
        self.radiusOfCurvature = 0.
        self.beamWidth = 0.
        self.rayleighRange = 0.
    

    @staticmethod
    def beamWaistAandZ(w0, Z, wavelength = 1064e-9):
        
        ZR = np.pi*self.w0**2/self.wavelength
        q = self.Z+1j*self.ZR
        
        return beamq(q, wavelength)
        
    
    @staticmethod
    def beamWaistAandR(w0, R, wavelength = 1064e-9):
        
        ZR = np.pi*self.w0**2/self.wavelength
        q = (1/self.R-1j/self.ZR)**(-1)
        
        return beamq(q, wavelength)
    

    @staticmethod
    def beamWidthAandR(w, R, wavelength = 1064e-9):
        
        Z = self.R/(1+(self.R*self.wavelength/np.pi/self.w**2)**2)
        ZR = np.sqrt(self.Z*(self.R-self.Z))
        q = self.Z+1j*self.ZR
        
        return beamq(q, wavelength)
        
    
    @staticmethod
    def transformValue(qvalin, M=np.matrix ('1,0;0,1')):
        
        qvalout = (M.item(0,0)*self.qvalin+M.item(0,1))/(M.item(1,0)*self.qvalin+M.item(1,1))
    
        return qvalout
        
        
    # data access methods

    def set_q (self, qvalue):
        
        if qvalue.imag < 0:
            raise Exception ("imaginary part of q parameter must be positive")
        
        self.q = qvalue
        return self
            
    

    def  set_wavelength (self, newwavelength):
        
        if newwavelength <= 0:
            raise Exception ("wavelength must be positive")

        self.wavelength = newwavelength
        return self
    


    def duplicate (self, qold):
        
        '''-- beamq.duplicate --
        Make a copy of a beamq object with the same properties 
        as the original
        Example:
        beamcopy = beam1.duplicate;
        '''
        self = qold
        return self



    # methods for dependent properties
    def get_waistSize (self, qin):   # qin is an object

        self.wavelength = qin.wavelength
        self.waistSize = np.sqrt((qin.q.imag)*self.wavelength/np.pi)

        return self



    def get_rayleighRange (self, qin): # not sure
        # w0 = qin.waistSize
        w0 = qin.get_waistSize(qin)
        self.wavelength = qin.wavelength

        self.rayleighRange = np.pi*w0**2/self.wavelength

        return self

    # ???why dont use imag part of q directly??? if so



    def get_divergenceAngle (self, qin):
        w0 = qin.get_waistSize(qin)
        zR = qin.get_rayleighRange(qin)

        divergenceAngle = self.w0/self.zR

        return self



    def get_waistZ (self, qin):

        self.waistZ = qin.q.real

        return self



    def get_beamWidth (self, qin):

        z = qin.get_waistZ(qin)
        zR = qin.get_rayleighRange(qin)
        w0 = qin.get_waistSize(qin)

        self.beamWidth = w0*np.sqrt(1+(z/zR)**2)

        return self



    def get_radiusOfCurvature (self, qin):

        z = qin.get_waistZ(qin)
        zR = qin.get_rayleighRange(qin)

        if z != 0:
            self.radiusOfCurvature = z*(1+(zR/z)**2)

        else:
            self.radiusOfCurvature = np.inf

        return self



    # methods for making useful calculations

    def overlap (self, beam1, beam2):
    
        # -- beamq.overlap --
        # Find the overlap fraction of 2 beams (assumes axial symmetry).

        q1 = beam1.q
        q2 = beam2.q

        w1 = beam1.get_waistZ(beam1)
        w2 = beam2.get_waistZ(beam2)

        self.wavelength = beam1.wavelength

        if self.wavelength != beam2.wavelength:
            raise Exception ("Cannot overlap beams of different wavelength.")

        fraction = (2*np.pi/self.wavelength*w1*w2*1/abs(q2.conjugate()-q1))**2
        # square for 2D modematching
        return self



    def transform (self, beamin, M = np.matrix ('1,0;0,1')):

        # -- beamq.transform --
        # Creates a new beamq object after being transformed by an ABCD matrix.
        # Example:
        # newbeam = oldbeam.transform(oldbeam, M)
        # This transforms the oldbeam object and placed the new object into
        # newbeam, using the ABCD matrix M.

        qin = beamin.q

        qout = beamin.transformValue(qin, M)

        beamout = beamin.duplicate(beamin)
        beamout.q = qout

        return self 


    # plotting

    def plotBeamWidth (self, qarray, zdomain, *args):

        # -- beamq.plotBeamWidth --
        # Given an array of beamq objects, this function will plot 
        # the beamwidth.
        
        ploth = plt.plot(zdomain, [q.get_beamWidth(q) for q in qarray], *args)
        plt.plot(zdomain, [-q.get_beamWidth(q) for q in qarray], *args)

        plt.show()

        plothandle = ploth

        return self

   

   

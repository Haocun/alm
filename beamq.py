import numpy as np
import matplotlib.pyplot as plt

class beamq:
    
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
    
    def __init__ (self, q, wavelength = 1064e-9):
        
        self.q = q
        self.wavelength = wavelength
        self.waistSize = 0.
        self.waistZ = 0.
        self.divergenceAngle = 0.
        self.radiusOfCurvature = 0.
        self.beamWidth = 0.
        self.rayleighRange = 0.
    


    def beamWaistAandZ (self, w0, Z, wavelength = 1064e-9):
        
        self.w0 = w0
        self.Z = Z
        self.wavelength  = wavelength
        
        self.ZR = np.pi*self.w0**2/self.wavelength
        self.q = self.Z+1j*self.ZR
        
        return self
        
    

    def beamWaistAandR (self, w0, R, wavelength = 1064e-9):
        
        self.w0 = w0
        self.R = R
        self.wavelength = wavelength
        
        self.ZR = np.pi*self.w0**2/self.wavelength
        self.q = (1/self.R-1j/self.ZR)**(-1)
        
        return self
    

        
    def beamWidthAandR (self, w, R, wavelength = 1064e-9):
        
        self.w = w
        self.R = R
        self.wavelength = wavelength
        
        self.Z = self.R/(1+(self.R*self.wavelength/np.pi/self.w**2)**2)
        self.ZR = np.sqrt(self.Z*(self.R-self.Z))
        self.q = self.Z+1j*self.ZR
        
        return self
        
    

    def transformValue (self, qvalin, M=np.matrix ('1,0;0,1')):
        
        self.qvalin = qvalin
        self.qvalout = (M.item(0,0)*self.qvalin+M.item(0,1))/(M.item(1,0)*self.qvalin+M.item(1,1))
    
        return self.qvalout
        
    

    # constructor and data access methods
    
    def beamq (self, qvalue = 0, wavelength = 0): 
        
        if qvalue != 0:
            self.q = qvalue
            if wavelength != 0:
                self.wavelength = wavelength    
        return self 
        
    
    def set_q (self, qvalue):
        
        if qvalue.imag < 0:
            raise Exception ("imaginary part of q parameter must be positive")
        
        else:
            self.qvalue = qvalue
            self.q = self.qvalue
            return self
            
    

    def  set_wavelength (self, newwavelength):
        
        if newwavelength.imag <= 0:
            raise Exception ("wavelength must be positive")
        
        else:
            self.newwavelength = newwavelength
            self.q = self.newwavelength
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



    # methods for properties
    def get_waistSize (self, qin):   # qin is an object

        self.wavelength = qin.wavelength
        self.waistSize = np.sqrt((qin.q.imag)*self.wavelength/np.pi)

        return self.waistSize



    def get_rayleighRange (self, qin): # not sure
        # self.w0 = qin.waistSize
        self.w0 = qin.get_waistSize(qin)
        self.wavelength = qin.wavelength

        self.rayleighRange = np.pi*self.w0**2/self.wavelength

        return self.rayleighRange

    # ???why dont use imag part of q directly??? if so



    def get_divergenceAngle (self, qin):
        self.w0 = qin.get_waistSize(qin)
        self.zR = qin.get_rayleighRange(qin)

        self.divergenceAngle = self.w0/self.zR

        return self.divergenceAngle



    def get_waistZ (self, qin):

        self.waistZ = qin.q.real

        return self.waistZ



    def get_beamWidth (self, qin):

        self.z = qin.get_waistZ(qin)
        self.zR = qin.get_rayleighRange(qin)
        self.w0 = qin.get_waistSize(qin)

        self.beamWidth = self.w0*np.sqrt(1+(self.z/self.zR)**2)

        return self.beamWidth



    def get_radiusOfCurvature (self, qin):

        self.z = qin.get_waistZ(qin)
        self.zR = qin.get_rayleighRange(qin)

        if z != 0:
            self.radiusOfCurvature = self.z*(1+(self.zR/self.z)**2)

        else:
            self.radiusOfCurvature = np.inf

        return self.radiusOfCurvature



    # methods for making useful calculations

    def overlap (self, beam1, beam2):
    
        # -- beamq.overlap --
        # Find the overlap fraction of 2 beams (assumes axial symmetry).

        self.q1 = beam1.q
        self.q2 = beam2.q

        self.w1 = beam1.get_waistZ(beam1)
        self.w2 = beam2.get_waistZ(beam2)

        self.wavelength = beam1.wavelength

        if self.wavelength != beam2.wavelength:
            raise Exception ("Cannot overlap beams of different wavelength.")

        else:
            return (2*np.pi/self.wavelength*self.w1*self.w2*1/abs(self.q2.conjugate()-self.q1))**2
            # square for 2D modematching



    def transform (self, beamin, M = np.matrix ('1,0;0,1')):

        # -- beamq.transform --
        # Creates a new beamq object after being transformed by an ABCD matrix.
        # Example:
        # newbeam = oldbeam.transform(oldbeam, M)
        # This transforms the oldbeam object and placed the new object into
        # newbeam, using the ABCD matrix M.

        self.qin = beamin.q
        self.M = M

        self.qout = beamin.transformValue (self.qin, self.M)

        self.beamout = beamin.duplicate(beamin)
        self.beamout.q = self.qout

        return self 


    # plotting

    def plotBeamWidth (self, qarray, zdomain, *args):

        # -- beamq.plotBeamWidth --
        # Given an array of beamq objects, this function will plot 
        # the beamwidth.

        self.zdomain = zdomain
        
        self.ploth = plt.plot(self.zdomain, [q.get_beamWidth(q) for q in qarray], *args)
        plt.plot(self.zdomain, [-q.get_beamWidth(q) for q in qarray], *args)

        plt.show()

        self.plothandle = self.ploth

   

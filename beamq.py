import numpy as np

class beamq:
	
	'''
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
	'''
	
	def __init__ (self, q, wavelength = 1064e-9):
		
		self.q = q
		self.wavelength = wavelength
		self.waistSize = 0
		self.waistZ = 0
		self.divergenceAngle = 0
		self.radiusOfCurvature = 0
		self.beamWidth = 0
		self.rayleighRange = 0
	


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
		
	

	def transfromValue (self, qvalin, M=np.matrix ('1,0;0,1')):
		
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

import ode
from ode_graphics import CGraphics



#ode turple ()
#OpenGL list []

class PObject(object):
    def __init__(self, x, y, z, R, red, green, blue, mass):
        #shown in the class and its heritance 
        self.m_x = x
        self.m_y = y
        self.m_z = z
        self.m_R = R
        self.m_red = red
        self.m_green = green
        self.m_blue = blue
        self.m_mass = mass
        self.m_visible = True
        self.m_isQSet = False 	#is quaternion set
        self.m_local_Rot = ()	#local frame R
        self.m_local_Pos = ()	#local frame p
        self.m_q = ()			#local? global? format?
        self.m_body_ID = None
        self.m_geom = None
        self.m_world_ID = None
        self.m_space_ID = None
        self.m_cgraphics = None #ctor??
        self.m_tag = 0
        self.m_ID = 0

    def calcRotMatrix(axis, angle):
        """
        Return the row-major 3x3 rotation matrix defining a rotation around axis
        by angle.
        """
        cosTheta = math.cos(angle)
        sinTheta = math.sin(angle)
        t = 1.0 - cosTheta
        return (
                t * axis[0]**2 + cosTheta,
                t * axis[0] * axis[1] - sinTheta * axis[2],
                t * axis[0] * axis[2] + sinTheta * axis[1],
                t * axis[0] * axis[1] + sinTheta * axis[2],
                t * axis[1]**2 + cosTheta,
                t * axis[1] * axis[2] - sinTheta * axis[0],
                t * axis[0] * axis[2] - sinTheta * axis[1],
                t * axis[1] * axis[2] + sinTheta * axis[0],
                t * axis[2]**2 + cosTheta)
                
    # internal (inhertance) function
    def initPosBody(self):
        self.m_body_ID.setPosition((self.m_x, self.m_y, self.m_z))
        if ( self.m_isQSet == True): 
            self.m_body_ID.setQuaternion(self.m_q) 
        else:
            self.m_body_ID.setRotation(self.m_R)
            
    def initPosGeom(self):
        self.m_geom.setPosition((self.m_x, self.m_y, self.m_z))
        if (self.m_isQSet == True):
            self.m_geom.setQuaternion(self.m_q)  
    
    # public function

    def setRotation(self, x_axis, y_axis, z_axis, ang):
        #Must be called before init()
        self.m_q = (x_axis, y_axis, z_axis, ang) #??
        self.m_isQSet = True
        
    def setBodyPosition(self, xyz, local= False):
        if( local == False): 
            self.m_body_ID.setPosition(xyz)
        else:
            self.m_local_Pos[0] = xyz[0]
            self.m_local_Pos[1] = xyz[1]
            self.m_local_Pos[2] = xyz[2]
        
    def setBodyRotation(self, x_axis, y_axis, z_axis, ang, local = False):
        if (local == False):
            self.m_q = (x_axis, y_axis, z_axis, ang) #??
            self.m_body_ID.setQuaternion(self.m_q)
        else:
            self.m_local_Rot =  self.calcRotMatrix((x_axis, y_axis, z_axis), ang) #??
    
    def setBodyRotation_2(self, rot):
        self.m_body_ID.setRotation(rot)
    
    def getBodyPosition(self, local = False):
        if (local == True):
            x = self.m_local_Pos[0]
            y = self.m_local_Pos[1]
            z = self.m_local_Pos[2]
            
        r = self.m_body_ID.getPosition()
        x = r[0]
        y = r[1]
        z = r[2]
            
        return x, y, z
	
    def getBodyDirection(self, x, y, z):
        pass

    def getBodyRotation(self, local = False):
        if (local == True):
            r = (0, 0, 0, 0,
                 0, 0, 0, 0,
                 0, 0, 0, 0)
                 
            for k in range(9):
                r[k] = self.m_local_Rot[k]
                return r
        else:
            rr = self.m_body_ID.getRotation()
            return rr
    
    def setVisibility(self, v):
        self.m_visible = v
    
    def setColor(self, r, g, b):
        self.m_red = r
        self.m_green = g
        self.m_blue = b
    
    def getColor(self):
        return self.m_red, self.m_green, self.m_blue
        
    def getVisibility(self):
        return self.m_visible
        
    def setMass(self, mass):
        self.m_mass = mass
        
    #virtual method (common interface)
    #look for the python configuration for more details
    def init(self):
        pass
    
    def glinit(self):
        pass
    
    def draw(self):
        self.m_cgraphics.setColor(self.m_red, self.m_green, self.m_blue, 1)
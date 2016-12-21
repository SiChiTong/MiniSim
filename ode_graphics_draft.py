# -*- coding: utf-8 -*-
"""
Created on Sun Dec 18 10:07:10 2016

@author: don
"""
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4 import QtOpenGL






import ode
import math

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *


#serve as a common base utility class be called by Physics Objects (onDraw()) in ODE
class Geometry:
    @classmethod
    def sign(self, x):
        """Returns 1.0 if x is positive, -1.0 if x is negative or zero"""
        if x > 0.0: return 1.0
        else: return 1.0
    
    @classmethod
    def len3(self, v):
        """Returns the length of 3-vector v."""
        return math.sqrt(v[0]**2 + v[1]**2 + v[2]**2)
    
    @classmethod    
    def neg3(self, v):
        """Returns the negation of 3-vector v."""
        return (-v[0], -v[1], -v[2])
    
    @classmethod
    def add3(self, a, b):
        """Returns the sum of 3-vectors a and b."""
        return (a[0] + b[0], a[1] + b[1], a[2] + b[2])
    
    @classmethod    
    def sub3(self, a, b):
        """Returns the difference between 3-vectors a and b."""
        return (a[0] - b[0], a[1] - b[1], a[2] - b[2])

    @classmethod        
    def mul3(self, v, s):
        """Returns 3-vector v multiplied by scalar s."""
        return (v[0] * s, v[1] * s, v[2] * s)

    @classmethod        
    def div3(self, v, s):
        """Returns 3-vector v divided by scalar s."""
        return (v[0] / s, v[1] / s, v[2] / s)

    @classmethod        
    def dist3(self, a, b):
        """Returns the distance between point 3-vectors a and b."""
        return self.len3(self.sub3(a, b))

    @classmethod        
    def norm3(self, v):
        """Returns the unit length 3-vector parallel to 3-vector v."""
        l = self.len3(v)
        if (l > 0.0): return (v[0] / l, v[1] / l, v[2] / l)
        else: return (0.0, 0.0, 0.0)

    @classmethod        
    def dot3(self, a, b):
        """Returns the dot product of 3-vectors a and b."""
        return (a[0] * b[0] + a[1] * b[1] + a[2] * b[2])

    @classmethod    
    def cross(self, a, b):
        """Returns the cross prodcut of 3-vectors a and b"""
        return (a[1] * b[2] - a[2] * b[1], 
                a[2] * b[0] - a[0] * b[2],
                a[0] * b[1] - a[1] * b[0])

    @classmethod                
    def project3(self, v, d):
        """Returns projection of 3-vector v onto unit 3 vector"""
        return self.mul3(v, self.dot3(self.norm3(v), d))

    @classmethod
    def acosdot3(self, a, b):
        """Returns the angle between unit 3-vectors a and b."""
        x = self.dot3(a, b)
        if x < -1.0: return math.pi
        elif x > 1.0: return 0.0
        else: return math.acos(x)

    @classmethod    
    def rotate3(self, m, v):
        """Returns the rotation of 3-vector v by 3*3 (row major) matrix m."""
        return (v[0] * m[0] + v[1] * m[1] + v[2] * m[2],
                v[0] * m[3] + v[1] * m[4] + v[2] * m[5],
                v[0] * m[6] + v[1] * m[7] + v[2] * m[8])

    @classmethod                
    def invert3x3(self, m):
        """Returns the inversion (transpose) 3x3 rotation matrix"""
        return (m[0], m[3], m[6], 
                m[1], m[4], m[7],
                m[2], m[5], m[8])

    @classmethod    
    def zaxis(self, m):
        """Return the z-axis vector forom 3x3 (row major) rotation martix."""
        return (m[2], m[5], m[8])

    @classmethod        
    def calcRotMatrix(self, axis, angle):
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

    @classmethod
    def makeOpenGLMatrix(self, r, p):
        """
        Returns an OpenGL compatible (column-major, 4x4 homogeneous) transformation
        matrix from ODE compatible(row-major, 3x3) rotation matrix r and position vector p
        """
        return (r[0], r[3], r[6], 0.0,
                r[1], r[4], r[7], 0.0,
                r[2], r[5], r[8], 0.0,
                p[0], p[1], p[2], 1.0) #OPENGL: column major

    @classmethod                
    def getBodyRelVec(self, b, v):
	"""
	Returns the 3-vector v transformed into the local coordinate system of ODE
	body b.
	"""
	return self.rotate3(self.invert3x3(b.getRotation()), v)
                
    def __init__(self):
        pass
  
class CGraphics:
    """light vector. LIGHTZ is implicitly 1"""    
    LIGHTX = 1.0
    LIGHTY = 0.4
    
    """ground and sky """
    GROUND_R = 0.5
    GROUND_G = 0.5
    GROUND_B = 0.3
    
    """ground texture scale (1/size)"""
    GROUND_SCALE = 1.0  
    """offset of ground texture"""
    GROUND_OFSX = 0.5   
    GROUND_OFSY = 0.5
    SKY_SCALE = 1.0
    SKY_HEIGHT = 1.0
    CAPPED_CYLINDER_QUALITY = 3
    
    light_ambient = [0, 0, 0, 0]
    light_diffuse = [0, 0, 0, 0]
    light_specular = [0, 0, 0, 0]
    """ctor"""
    """
     @param owner: QGLWidget based Object which would use the utility to draw the physic
    """
    def __init__(self, owner= None):
        self.m_owner = owner


        self.m_view_xyz = [0.8317, -0.9817, 0.8000] #view point prop.
        self.m_view_hpr = [121.0000, -27.5000, 0.0000]
        self.setViewpoint(self.m_view_xyz, self.m_view_hpr)        
        #self.m_sphere_quality = 0

        self.m_renderDepth = 100
        self.m_graphicDisabled = False
        
        
        self.m_tex_ids = [] #Registered texture id
        self.m_frustum_right = 0
        self.m_frustum_bottom = 0
        self.m_frustum_vnear = 0
        self.m_width = 0
        self.m_height = 0        
        
    """Internal Function"""
    
    def _drawBox(self, sides):
        if self.m_graphicDisabled == True: return
        lx = sides[0] * 0.5
        ly = sides[1] * 0.5
        lz = sides[2] * 0.5
        
        #sides
        glBegin(GL_TRIANGLE_STRIP)
        glNormal3f(-1, 0, 0)
        glVertex3f(-lx, -ly, -lz)
        glVertex3f(-lx, -ly, lz)
        glVertex3f(-lx, ly, -lz)
        glVertex3f(-lx, ly, lz)

        glNormal3f(0, 1, 0)        
        glVertex3f(lx, ly, -lz)
        glVertex3f(lx, ly, lz)

        glNormal3f(1, 0, 0)
        glVertex3f(lx, -ly, -lz)
        glVertex3f(lx, -ly, lz)

        glNormal3f(0, -1, 0)
        glVertex3f(-lx, -ly, -lz)
        glVertex3f(-lx, -ly, lz)
        glEnd()
        
        #top face
        glBegin(GL_TRIANGLE_FAN)
        glNormal3f(0, 0, 1)
        glVertex3f(-lx, -ly, lz)
        glVertex3f(lx, -ly, lz)
        glVertex3f(lx, ly, lz)
        glVertex3f(-lx, ly, lz)
        glEnd()
        
        #bottom face
        glBegin(GL_TRIANGLE_FAN)
        glNormal(0, 0, -1)
        glVertex3f(-lx, -ly, -lz)
        glVertex3f(-lx, ly, -lz)
        glVertex3f(lx, ly, -lz)
        glVertex3f(lx, -ly, -lz)
        glEnd()
        
        
    
    def _drawPatch(self, p1, p2, p3, level):
        #A Mmmmmust to be implemented for importing STL
        pass
    
    def _drawSphere(self):
        #A Mmmmmust to be implemented with _drawPatch
        pass
    
    def _drawCapsule(self, l, r):
        if self.m_graphicDisabled == True: return
        
        #number of sides to the cylinder (divisible by 4)
        n = self.CAPPED_CYLINDER_QUALITY * 4
        
        l = l * 0.5
        a = math.pi * 2.0 / n
        sa = math.sin(a)
        ca = math.cos(a)
        
        #draw cylinder body
        ny = 1          #normal vector = (0, ny, mz)
        nz = 0
        glBegin(GL_TRIANGLE_STRIP)
        for i in range(n):
            glNormal3d(ny, nz, 0)
            glVertex3d(ny * r, nz * r, 1)
            glNormal3d(ny, nz, 0)
            glVertex3d(ny * r, nz * r, -1)
            #rotate ny, nz
            tmp = ca * ny - sa * nz
            nz = sa * ny + ca * nz
            ny = tmp
        glEnd()
        
        #draw first cylinder cap
        start_nx = 0
        start_ny = 1
        for j in range ( n / 4):
            start_nx2 = ca * start_nx + sa * start_ny
            start_ny2 = -sa * start_nx + ca * start_ny
            # get n = start_n and n2 = start_n2
            nx = start_nx
            ny = start_ny
            nz = 0
            
            nx2 = start_nx2
            ny2 = start_ny2
            nz2 = 0
            glBegin(GL_TRIANGLE_STRIP)
            for i in range(n):
                glNormal3d(ny2, nz2, nx2)
                glVertex3d(ny2 * r, nz2 * r, l + nx2 * r)
                glNormal3d(ny, nz, nx)
                glVertex3d(ny * r, nz * r, l + nx * r)
                
                #rotate n, n2
                tmp = ca * ny - sa * nz
                nz = sa * ny + ca * nz
                ny = tmp
                tmp = ca * ny2 - sa * nz2
                nz2 = sa * ny2 + ca * nz2
                ny2 = tmp
            glEnd()
            start_nx = start_nx2
            start_ny = start_ny2
        
        #draw second cylinder cap
        start_nx = 0
        start_ny = 1
        for j in range ( n / 4):
            start_nx2 = ca * start_nx - sa * start_ny
            start_ny2 = sa * start_nx + ca * start_ny
            # get n = start_n and n2 = start_n2
            nx = start_nx
            ny = start_ny
            nz = 0
            
            nx2 = start_nx2
            ny2 = start_ny2
            nz2 = 0
            glBegin(GL_TRIANGLE_STRIP)
            for i in range(n):
                glNormal3d(ny, nz, nx)
                glVertex3d(ny * r, nz * r, -l + nx * r)
                glNormal3d(ny2, nz2, nx2)
                glVertex3d(ny2 * r, nz2 * r, -l + nx2 * r)
                
                #rotate n, n2
                tmp = ca * ny - sa * nz
                nz = sa * ny + ca * nz
                ny = tmp
                tmp = ca * ny2 - sa * nz2
                nz2 = sa * ny2 + ca * nz2
                ny2 = tmp
            glEnd()
            start_nx = start_nx2
            start_ny = start_ny2
            

    def _drawCylinder(self, l, r, zoffset):
        if self.m_graphicDisabled == True: return
        CAPSULE_SLICES = 16
        CAPSULE_STACKS = 12
        
        cylHalfHeight = l / 2.0

        #draw the cylinder body
        glBegin(GL_TRIANGLE_STRIP)
        for i in range(0, CAPSULE_SLICES +1):
            a = float(i) * math.pi * 2.0 / float(CAPSULE_SLICES)
            sa = math.sin(a)
            ca = math.cos(a)
            glNormal3f(ca, sa, 0)
            glVertex3f(r * ca, r * sa, cylHalfHeight)
            glVertex3f(r * ca, r * sa, -cylHalfHeight)
        glEnd()
        glTranslated(0, 0, cylHalfHeight)
        glutSolidSphere(r, CAPSULE_SLICES, CAPSULE_STACKS)
        glTranslated(0, 0, -2.0 * cylHalfHeight)
        glutSolidSphere(r, CAPSULE_SLICES, CAPSULE_STACKS)            



        
    def _drawCylinder_TopTextured(self, l, r, zoffset, tex_id, robot = False):
        pass
    
    def _wrapCameraAngles(self):
        for i in range(3):
            while self.m_view_hpr[i] > 180:
                self.m_view_hpr[i] = self.m_view_hpr[i] - 360
            while self.m_view_hpr[i] < -180:
                self.m_view_hpr[i] = self.m_view_hpr[i] - 360
    
    def _setCamera(self, x, y, z, h, p, r):
        if (self.m_graphicDisabled == True): return
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glRotatef(90, 0, 0, 1)
        glRotatef(90, 0, 0, 1)
        glRotatef( r, 1, 0, 0)
        glRotatef( p, 0, 1, 0)
        glRotatef(-h, 0, 0, 1)
        glTranslatef(-x, -y, -z)
    
    
    """Public Function"""
    def disableGraphics(self):
        self.m_graphicDisabled = True
    
    def enableGraphics(self):
        self.m_graphicDisabled = False
        
    def isGraphicsEnabled(self):
        return not(self.m_graphicDisabled)
    
   # def loadTexture(self, img):
   #     if (self.m_graphicDisabled == True):
   #         return -1
   #     glEnable(GL_TEXTURE_2D)
   #     glBindTexture(GL_TEXTURE_2D, glGenTextures(1))
   #    
   #     id = self.m_owner.bindTexture(img)
   #     
   #     self.m_tex_ids.append(id)
   #     return len(self.m_tex_ids)-1
    
   # def loadTextureSkyBox(self, img):
   #     if (self.m_graphicDisabled == True):
   #         return -1
   #     glEnable(GL_TEXTURE_2D)
   #     glBindTexture(GL_TEXTURE_2D, glGenTextures(1))
   #     glTexEnvi(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)
   #     glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
   #     glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
   #     glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
   #     glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        
    
    def setViewpoint(self, xyz, hpr):
        if xyz != []:
            self.m_view_xyz[0] = xyz[0]
            self.m_view_xyz[1] = xyz[1]
            self.m_view_xyz[2] = xyz[2]
        if hpr != []:
            self.m_view_hpr[0] = hpr[0]
            self.m_view_hpr[1] = hpr[1]
            self.m_view_hpr[2] = hpr[2]
            self._wrapCameraAngles()
    
    def getViewpoint(self):
        if (self.m_graphicDisabled == True):
            return
        return self.m_view_xyz, self.m_view_hpr
        
    def getFrustum(self):
        return self.m_frustum_right, self.m_frustum_bottom, self.m_frustum_vnear
    
    def getWidth(self):
        return self.m_width
        
    def getHeight(self):
        return self.m_height
        
    def renderDepth(self):
        return self.m_renderDepth
        
    def setRenderDepth(self, depth):
        self.m_renderDepth = depth
    
    def setViewpoint_2(self, x, y, z, h, p, r):
        self.m_view_xyz[0] = x
        self.m_view_xyz[1] = y
        self.m_view_xyz[2] = z
        self.m_view_hpr[0] = h
        self.m_view_hpr[1] = p
        self.m_view_hpr[2] = r
        self._wrapCameraAngles()
    
    def cameraMotion(self, mode, deltax, deltay):
        if (self.m_graphicDisabled == True): return
        side = 0.01 * deltax
        if mode == 4:
            fwd = 0.01 * deltay
        else:
            fwd = 0.0
        s = math.sin(self.m_view_hpr[0] * math.pi / 180.0)
        c = math.cos(self.m_view_hpr[0] * math.pi / 180.0)
        
        if (mode == 1):
            self.m_view_hpr[0] = self.m_view_hpr[0] + deltax * 0.5
            self.m_view_hpr[1] = self.m_view_hpr[1] + deltay * 0.5
        else:
            self.m_view_xyz[0] = self.m_view_xyz[0] - s * side + c * fwd
            self.m_view_xyz[1] = self.m_view_xyz[1] + c * side + s * fwd
            if (mode == 2 or mode == 5):
                self.m_view_xyz[2] = self.m_view_xyz[2] + 0.01 * deltay
        self._wrapCameraAngles()
    
    def rotxy(self, x, y, a):
        ca = math.cos(a)
        sa = math.sin(a)
        xx = x * ca - y * sa
        yy = x * sa + y * ca
        return xx, yy        
        
    def lookAt(self, x, y, z):
        rx = x - self.m_view_xyz[0]
        ry = y - self.m_view_xyz[1]
        rz = z - self.m_view_xyz[2]
        rr = math.sqrt(rx*rx + ry*ry + rz*rz)
        if (rr == 0): return
        r = 0
        p = math.asin(rz/rr) * 180.0 / math.pi
        h = math.atan2(ry, rx) * 180.0 / math.pi
        self.m_view_hpr[0] = h
        self.m_view_hpr[1] = p
        self.m_view_hpr[2] = r
    
    def getCameraForward(self):
        h = self.m_view_hpr[0] * math.pi / 180.0
        p = self.m_view_hpr[1] * math.pi / 180.0
        r = self.m_view_hpr[2] * math.pi / 180.0
        x = -1
        y = 0
        z = 0
        y, z = self.rotxy(y, z, r)
        z, x = self.rotxy(z, x, -p)
        x, y = self.rotxy(x, y, h)
        return x, y, z
    
    def getCameraRight(self, x, y, z):
        h = self.m_view_hpr[0] * math.pi / 180.0
        p = self.m_view_hpr[1] * math.pi / 180.0
        r = self.m_view_hpr[2] * math.pi / 180.0
        x = 0
        y = -1
        z = 0
        y, z = self.rotxy(y, z, r)
        z, x = self.rotxy(z, x, -p)
        x, y = self.rotxy(x, y, h)
        return x, y, z
    
    def zoomCamera(self, dz):
        xx, yy, zz = self.getCameraForward()
        self.m_view_xyz[0] = self.m_view_xyz[0] + xx * dz
        self.m_view_xyz[1] = self.m_view_xyz[1] + yy * dz
        self.m_view_xyz[2] = self.m_view_xyz[2] + zz * dz
    
    def driftCamera(self, d):
        xx, yy, zz = self.getCameraForward()
        self.m_view_xyz[0] = self.m_view_xyz[0] + xx * d
        self.m_view_xyz[1] = self.m_view_xyz[1] + yy * d
        self.m_view_xyz[2] = self.m_view_xyz[2] + zz * d        
        
    def setColor(self, r, g, b, alpha):
        if (self.m_graphicDisabled == True): return
        
        
        self.light_ambient[0] = r * 0.3
        self.light_ambient[1] = g * 0.3
        self.light_ambient[2] = b * 0.3
        self.light_ambient[3] = alpha
        self.light_diffuse[0] = r * 0.7
        self.light_diffuse[1] = g * 0.7
        self.light_diffuse[2] = b * 0.7
        self.light_diffuse[3] = alpha
        self.light_specular[0] = r * 0.2
        self.light_specular[1] = g * 0.2
        self.light_specular[2] = b * 0.2
        self.light_specular[3] = alpha
        glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, self.light_ambient)
        glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, self.light_diffuse)
        glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, self.light_specular)
        glMaterialf(GL_FRONT_AND_BACK, GL_SHININESS, 5.0)
        
    
    #def setSphereQuality(self, q):
    #    pass
    
    def setShadow(self, state):
        pass
    
    def useTexture(self, tex_id):
        if (self.m_graphicDisabled == True): return
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, self.m_tex_ids[tex_id])
    
    def noTexture(self):
        if (self.m_graphicDisabled == True): return
        glDisable(GL_TEXTURE_2D)
    
    def setTransform(self, pos, R):
        if (self.m_graphicDisabled == True): return
        matrix = [0, 0, 0, 0, 
                  0, 0, 0, 0, 
                  0, 0, 0, 0,
                  0, 0, 0, 0]
        matrix[0] = R[0]
        matrix[1] = R[3]
        matrix[2] = R[6]
        matrix[3] = 0
        matrix[4] = R[1]
        matrix[5] = R[4]
        matrix[6] = R[7]
        matrix[7] = 0
        matrix[8] = R[2]
        matrix[9] = R[5]
        matrix[10] = R[8]
        matrix[11] = 0
        matrix[12] = pos[0]
        matrix[13] = pos[1]
        matrix[14] = pos[2]
        matrix[15] = 1
        
        glPushMatrix()
        glMultMatrixf(matrix)
    
    
    #Utility Function
    def initScene(self, width, height, rc, gc, bc, fog = False, fogr = 0.6, fogg = 0.6,
                  fogb = 0.6, fogdensity = 0.6):
        if (self.m_graphicDisabled == True): return
        self.m_width = width
        self.m_height = height
        
        #setup stuff
        glutInit([])
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glDisable(GL_TEXTURE_2D)
        glDisable(GL_TEXTURE_GEN_S)
        glDisable(GL_TEXTURE_GEN_T)
        glShadeModel(GL_FLAT)
        glEnable(GL_DEPTH_TEST)
        glDepthFunc(GL_LESS)
        glEnable(GL_CULL_FACE)
        glCullFace(GL_BACK)
        glFrontFace(GL_CCW)
        
        #setup viewport
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        VNEAR = 0.1
        VFAR = self.m_renderDepth
        VFAR = 1000000000000000000000000000
        K = 1 #view scale, 1 = +/- 45 degrees
        self.m_frustum_vnear = VNEAR
        if ( width > height or width == height):
            k2 = float(height) / float(width)
            self.m_frustum_right = VNEAR * K 
            self.m_frustum_bottom = VNEAR * K * k2 
        else:
            k2 = float(width) / float(height)
            self.m_frustum_right = VNEAR * K * k2
            self.m_frustum_bottom = VNEAR * K
            
        glFrustum(-self.m_frustum_right, self.m_frustum_right, -self.m_frustum_bottom,
                  self.m_frustum_bottom, VNEAR, VFAR)
        
        #setup lights It makes a difference whether this is done in the
        #GL_PROJECTION matrix mode(lights are scene relative) or the
        #GL_MODELVIEW matrix mode(lights are camera relative, bad!!)
        self.light_ambient = [0.5, 0.5, 0.5, 1.0]
        self.light_diffuse = [1.0, 1.0, 1.0, 1.0]
        self.light_specular = [1.0, 1.0, 1.0, 1.0]
        glLightfv(GL_LIGHT0, GL_AMBIENT, self.light_ambient)
        glLightfv(GL_LIGHT0, GL_DIFFUSE, self.light_diffuse)
        glLightfv(GL_LIGHT0, GL_SPECULAR, self.light_specular)
        glColor3f(1.0, 1.0, 1.0)
        
        #clear the window
        glClearColor(rc, gc, bc, 1)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        view2_xyz = [0, 0, 0]
        view2_hpr = [0, 0, 0]

        #cache the camera position        
        view2_xyz[0] = self.m_view_xyz[0]
        view2_xyz[1] = self.m_view_xyz[1]
        view2_xyz[2] = self.m_view_xyz[2]
        view2_hpr[0] = self.m_view_hpr[0]
        view2_hpr[1] = self.m_view_hpr[1]
        view2_hpr[2] = self.m_view_hpr[2]
        
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        self._setCamera(view2_xyz[0], view2_xyz[1], view2_xyz[2], view2_hpr[0], view2_hpr[1], view2_hpr[2])
        
        light_position = [self.LIGHTX, self.LIGHTY, 1.0, 0.0]
        glLightfv(GL_LIGHT0, GL_POSITION, light_position)
        
        if fog:
            fogColor = [fogr, fogg, fogb, 1]
            glFogi(GL_FOG_MODE, GL_EXP2) #set the Fog mode to GL_EXP2
            glFogf(GL_FOG_START, 5)
            glFogf(GL_FOG_END, 10)
            glFogfv(GL_FOG_COLOR, fogColor)
            glFogf(GL_FOG_DENSITY, fogdensity)
    
    def finalizeScene(self):
        pass
    
    #???
    def resetState(self):
        if self.m_graphicDisabled == True: return
        glEnable(GL_LIGHTING)
        glDisable(GL_TEXTURE_2D)
        glShadeModel(GL_FLAT)
        glEnable(GL_DEPTH_TEST)
        glDepthFunc(GL_LESS)
        glColor3f(1, 1, 1)
        self.setColor(1, 1, 1, 1)
    
    def drawSkybox(self, t1, t2, t3, t4, t5, t6):
        if (self.m_graphicDisabled == True): return
        #Store the current matrix
        glPushMatrix()

        glLoadIdentity()
        glRotatef(90, 0, 0, 1)
        glRotatef(90, 0, 1, 0)
        glRotatef(view_hpr[2], 1, 0, 0)
        glRotatef(view_hpr[1], 0, 1, 0)
        glRotatef(view_hpr[0], 0, 0, 1)
        glScalef(self.m_renderDepth, self.m_renderDepth, self.m_renderDepth)
        
        #Enable/Disable features
        glPushAttrib(GL_ENABLE_BIT)
        glEnable(GL_TEXTURE_2D)
        glShadeModel(GL_FLAT)
        glDisable(GL_LIGHTING)
        glDisable(GL_LIGHT0)
        
        #Just in case we set all vertices to white
        glColor4f(1, 1, 1, 1)
        r = 1.005   #to overcome borders problem
        
        #neg_x/right
        glBindTexture(GL_TEXTURE_2D, self.m_tex_ids[t1])
        glBegin(GL_QUADS)
        glTexCoord2f(0, 0)
        glVertex3f(-0.5, -0.5 * r, -0.5 * r)
        glTexCoord2f(1, 0)
        glVertex3f(-0.5, 0.5 * r, -0.5 * r)
        glTexCoord2f(1, 1)
        glVertex3f(-0.5, 0.5 * r, 0.5 * r)
        glTexCoord2f(0, 1)
        glVertex3f(-0.5, -0.5 * r, 0.5 * r)
        glEnd()
        
        #pos_y/front
        glBindTexture(GL_TEXTURE_2D, self.m_tex_ids[t4])
        glBegin(GL_QUADS)
        glTexCoord2f(0, 0)
        glVertex3f(-0.5 * r, 0.5, -0.5 * r)
        glTexCoord2f(1, 0)
        glVertex3f(0.5 * r, 0.5, -0.5 * r)
        glTexCoord2f(1, 1)
        glVertex3f(0.5 * r, 0.5, 0.5 * r)
        glTexCoord2f(0, 1)
        glVertex3f(-0.5 * r, 0.5, -0.5 * r)
        glEnd()
        
        #pos_x/left
        glBindTexture(GL_TEXTURE_2D, self.m_tex_ids[t2])
        glBegin(GL_QUADS)
        glTexCoord2f(0, 0)
        glVertex3f(0.5, 0.5 * r, -0.5 * r)
        glTexCoord2f(1, 0)
        glVertex3f(0.5, -0.5 * r, -0.5 * r)
        glTexCoord2f(1, 1)
        glVertex3f(0.5, -0.5 * r, 0.5 * r)
        glTexCoord2f(0, 1)
        glVertex3f(0.5, 0.5 * r, 0.5 * r)
        glEnd()
        
        #neg_y/back
        glBindTexture(GL_TEXTURE_2D, self.m_tex_ids[t3])
        glBegin(GL_QUADS)
        glTexCoord2f(0, 0)
        glVertex3f(0.5 * r, -0.5, -0.5 * r)
        glTexCoord2f(1, 0)
        glVertex3f(-0.5 * r, -0.5, -0.5 * r)
        glTexCoord2f(1, 1)
        glVertex3f(-0.5 * r, -0.5, 0.5 * r)
        glTexCoord2f(0, 1)
        glVertex3f(0.5 * r, -0.5, 0.5 * r)
        glEnd()        

        #neg_z/down
        glBindTexture(GL_TEXTURE_2D, self.m_tex_ids[t5])
        glBegin(GL_QUADS)
        glTexCoord2f(0, 0)
        glVertex3f(-0.5 * r, -0.5 * r, -0.5)
        glTexCoord2f(1, 0)
        glVertex3f(-0.5 * r, 0.5 * r, -0.5)
        glTexCoord2f(1, 1)
        glVertex3f(0.5 * r, 0.5 * r, -0.5)
        glTexCoord2f(0, 1)
        glVertex3f(0.5 * r, -0.5 * r, -0.5)
        glEnd()
        
        #pos_z/up
        glBindTexture(GL_TEXTURE_2D, self.m_tex_ids[t6])
        glBegin(GL_QUADS)
        glTexCoord2f(0, 0)
        glVertex3f(-0.5 * r, -0.5 * r, 0.5)
        glTexCoord2f(1, 0)
        glVertex3f(-0.5 * r, 0.5 * r, 0.5)
        glTexCoord2f(1, 1)
        glVertex3f(0.5 * r, 0.5 * r, 0.5)
        glTexCoord2f(0, 1)
        glVertex3f(0.5 * r, -0.5 * r, 0.5)
        glEnd()
        
        #Restore enable bits and matrix
        glPopAttrib()
        glPopMatrix()
        
    def drawSky(self):
        if self.m_graphicDisabled == True: return
        SSIZE = 1000.0
        offset = 0.0
        
        x = SSIZE * self.SKY_SCALE
        z = self.m_view_xyz[2] + self.SKY_HEIGHT
        
        glBegin(GL_QUADS)
        glNormal3f(0, 0, -1)
        glTexCoord2f(-x + offset, -x + offset)
        glVertex3f(-SSIZE + self.m_view_xyz[0], -SSIZE + self.m_view_xyz[1], z)
        glTexCoord2f(-x + offset, x + offset)
        glVertex3f(-SSIZE + self.m_view_xyz[0], SSIZE + self.m_view_xyz[1], z)
        glTexCoord2f(x + offset, x + offset)
        glVertex3f(SSIZE + self.m_view_xyz[0], SSIZE + self.m_view_xyz[1], z)
        glTexCoord2f(x + offset, -x + offset)
        glVertex3f(SSIZE + self.m_view_xyz[0], -SSIZE + self.m_view_xyz[1], z)
        glEnd()
    
        glDepthFunc(GL_LESS)
        glDepthRange(0, 1)
        
        resetState()
        
    def drawGround(self):
        if (self.m_graphicDisabled == True): return
        glDisable(GL_LIGHTING)
        glShadeModel(GL_FLAT)
        glEnable(GL_DEPTH_TEST)
        glDepthFunc(GL_LESS)
        
        gsize = 100.0
        offset = 0.0
        
        glBegin(GL_QUADS)
        glNormal3f(0, 0, 1)
        glTexCoord2f( -gsize * self.GROUND_SCALE + self.GROUND_OFSX,
                      -gsize * self.GROUND_SCALE + self.GROUND_OFSY)
        glVertex3f(-gsize, -gsize, offset)
        glTexCoord2f( gsize * self.GROUND_SCALE + self.GROUND_OFSX,
                     -gsize * self.GROUND_SCALE + self.GROUND_OFSY)
        glVertex3f(gsize, -gsize, offset)
        glTexCoord2f( gsize * self.GROUND_SCALE + self.GROUND_OFSX,
                      gsize * self.GROUND_SCALE + self.GROUND_OFSY)
        glVertex3f(gsize, gsize, offset)
        glTexCoord2f( -gsize * self.GROUND_SCALE + self.GROUND_OFSX,
                       gsize * self.GROUND_SCALE + self.GROUND_OFSY)
        glVertex3f(-gsize, gsize, offset)
        glEnd()
        
        self.resetState()
        
    
    def drawBox(self, pos, R, sides):
        if (self.m_graphicDisabled == True): return
        glShadeModel(GL_FLAT)
        self.setTransform(pos, R)
        self._drawBox(sides)
        glPopMatrix()
    
    def drawSphere(self, pos, R, radius):
        pass
    
    def drawCylinder(self, pos, R, length, radius):
        if (self.m_graphicDisabled == True): return
        glShadeModel(GL_SMOOTH)
        self.setTransform(pos, R)
        self._drawCylinder(length, radius, 0)
        glPopMatrix()
    
    def drawCylinder_TopTextured(pos, R, length, radius, tex_id, robot = False):
        pass
    
    def drawCapsule(self, pos, R, length, radius):
        if self.m_graphicDisabled == True: return
        glShadeModel(GL_SMOOTH)
        self.setTransform(pos, R)
        self._drawCapsule(length, radius)
        glPopMatrix()
    
    def drawLine(self, pos1, pos2):
        if (self.m_graphicDisabled == True): return
        glDisable(GL_LIGHTING)
        glLineWidth(2)
        glShadeModel(GL_FLAT)
        glBegin(GL_LINE)
        glVertex3f(pos1[0], pos1[1], pos1[2])
        glVertex3f(pos2[0], pos2[1], pos2[2])
        glEnd()
        
    def drawCircle(self, x0, y0, z0, r):
        if self.m_graphicDisabled == True: return
        n = 24  #number of sides to the cylinder (divisible by 4)
        
        a = math.pi * 2.0 / n
        sa = math.sin(a)
        ca = math.cos(a)
        
        #draw top cap
        glShadeModel(GL_FLAT)
        ny = 1      #normal vector = (0, ny, nz)
        nz = 0
        glBegin(GL_TRIANGLE_FAN)
        glNormal3d(0, 0, 1)
        for i in range(3):
            glNormal3d(0, 0, 1)
            glVertex3d(ny * r + x0, nz * r + y0, z0)
            #rotate ny, nz
            tmp = ca * ny - sa * nz
            nz = sa * ny + ca * nz
            ny = tmp
        glEnd()
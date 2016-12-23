# -*- coding: utf-8 -*-
"""
Created on Mon Dec 19 21:36:12 2016

@author: don
"""



from pcylinder import PCylinder
from pworld import PWorld
from ode_graphics import Geometry, CGraphics
import ode
import math,time

#########################################################
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
#############################################################

class Robot:
    # (Ragdoll) rotation directions are named by the third (z-axis) row of the 3x3 matrix,
    #           because ODE capsules are oriented along the z-axis
    rightRot = (0.0, 0.0, -1.0, 0.0, 1.0, 0.0, 1.0, 0.0, 0.0)
    leftRot = (0.0, 0.0, 1.0, 0.0, 1.0, 0.0, -1.0, 0.0, 0.0)
    upRot = (1.0, 0.0, 0.0, 0.0, 0.0, -1.0, 0.0, 1.0, 0.0)
    downRot = (1.0, 0.0, 0.0, 0.0, 0.0, -1.0, 0.0, 1.0, 0.0)
    bkwdRot = (1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0)

    # axes used to determine constrained joint rotations
    rightAxis = (1.0, 0.0, 0.0)
    leftAxis = (-1.0, 0.0, 0.0)
    upAxis = (0.0, 1.0, 0.0)
    downAxis = (0.0, -1.0, 0.0)
    bkwdAxis = (0.0, 0.0, 1.0)
    fwdAxis = (0.0, 0.0, -1.0)

    UPPER_ARM_LEN = 0.30
    FORE_ARM_LEN = 0.25
    HAND_LEN = 0.13 # wrist to mid-fingers only
    FOOT_LEN = 0.18 # ankles to base of ball of foot only
    HEEL_LEN = 0.05

    BROW_H = 1.68
    MOUTH_H = 1.53
    NECK_H = 1.50
    SHOULDER_H = 1.37
    CHEST_H = 1.35
    HIP_H = 0.86
    KNEE_H = 0.48
    ANKLE_H = 0.08

    SHOULDER_W = 0.41
    CHEST_W = 0.36 # actually wider, but we want narrower than shoulders (esp. with large radius)
    LEG_W = 0.28 # between middles of upper legs
    PELVIS_W = 0.25 # actually wider, but we want smaller than hip width

    R_SHOULDER_POS = (-SHOULDER_W * 0.5, SHOULDER_H, 0.0)
    L_SHOULDER_POS = (SHOULDER_W * 0.5, SHOULDER_H, 0.0)

    R_ELBOW_POS = Geometry.sub3(R_SHOULDER_POS, (UPPER_ARM_LEN, 0.0, 0.0))
    L_ELBOW_POS = Geometry.add3(L_SHOULDER_POS, (UPPER_ARM_LEN, 0.0, 0.0))
    R_WRIST_POS = Geometry.sub3(R_ELBOW_POS, (FORE_ARM_LEN, 0.0, 0.0))
    L_WRIST_POS = Geometry.add3(L_ELBOW_POS, (FORE_ARM_LEN, 0.0, 0.0))
    R_FINGERS_POS = Geometry.sub3(R_WRIST_POS, (HAND_LEN, 0.0, 0.0))
    L_FINGERS_POS = Geometry.add3(L_WRIST_POS, (HAND_LEN, 0.0, 0.0))

    R_HIP_POS = (-LEG_W * 0.5, HIP_H, 0.0)
    L_HIP_POS = (LEG_W * 0.5, HIP_H, 0.0)
    R_KNEE_POS = (-LEG_W * 0.5, KNEE_H, 0.0)
    L_KNEE_POS = (LEG_W * 0.5, KNEE_H, 0.0)
    R_ANKLE_POS = (-LEG_W * 0.5, ANKLE_H, 0.0)
    L_ANKLE_POS = (LEG_W * 0.5, ANKLE_H, 0.0)
    R_HEEL_POS = Geometry.sub3(R_ANKLE_POS, (0.0, 0.0, HEEL_LEN))
    L_HEEL_POS = Geometry.sub3(L_ANKLE_POS, (0.0, 0.0, HEEL_LEN))
    R_TOES_POS = Geometry.add3(R_ANKLE_POS, (0.0, 0.0, FOOT_LEN))
    L_TOES_POS = Geometry.add3(L_ANKLE_POS, (0.0, 0.0, FOOT_LEN))






    def __init__(self, world, mass, offset = (0.0, 0.0, 0.0)):

        self.m_pworld = world
        self.m_mass = mass
        self.m_bodies = []      # Vector to store all of the robot parts(model)
        self.m_geoms = []       # Vector to store all of the robot geoms(collision, rendering)
        self.m_joints = []
        
        self.m_totalMass = mass
        
        self.m_offset = offset
        
        
        #initialization with all the parts
        self.m_chest = self._addBody((-self.CHEST_W * 0.5, self.CHEST_H, 0.0), 
                                    (self.CHEST_W * 0.5, self.CHEST_H, 0.0), 
                                    0.13)
                                    
        self.m_belly = self._addBody((0.0, self.CHEST_H - 0.1, 0.0),
                                    (0.0, self.HIP_H + 0.1, 0.0),
                                    0.12)
        self.m_midSpine = self._addFixedJoint(self.m_chest, self.m_belly)
       
        self.m_pelvis = self._addBody((-self.PELVIS_W * 0.5, self.HIP_H, 0.0),
                                   (self.PELVIS_W * 0.5, self.HIP_H, 0.0),
                                   0.125)
        self.m_lowSpine = self._addFixedJoint(self.m_belly, self.m_pelvis)
        
        self.m_head = self._addBody((0.0, self.BROW_H, 0.0), 
                                 (0.0, self.MOUTH_H, 0.0), 
                                 0.11)
        self.m_neck = self._addBallJoint(self.m_chest, 
                                      self.m_head,
                                      (0.0, self.NECK_H, 0.0), 
                                      (0.0, -1.0, 0.0), 
                                      (0.0, 0.0, 1.0), 
                                      math.pi * 0.25,
			                      math.pi * 0.25, 
                                      80.0, 
                                      40.0)
        
        self.m_rightUpperLeg = self._addBody(self.R_HIP_POS, 
                                           self.R_KNEE_POS, 
                                           0.11)
        self.m_rightHip = self._addUniversalJoint(self.m_pelvis, 
                                                self.m_rightUpperLeg,
                                                self.R_HIP_POS, 
                                                self.bkwdAxis, 
                                                self.rightAxis, 
                                                -0.1 * math.pi, 
                                                0.3 * math.pi, 
                                                -0.15 * math.pi,
                                                0.75 * math.pi)

        self.m_leftUpperLeg = self._addBody(self.L_HIP_POS, 
                                          self.L_KNEE_POS, 
                                          0.11)
        self.m_leftHip = self._addUniversalJoint(self.m_pelvis, 
                                               self.m_leftUpperLeg,
                                               self.L_HIP_POS, 
                                               self.fwdAxis, 
                                               self.rightAxis, 
                                               -0.1 * math.pi, 
                                               0.3 * math.pi, 
                                               -0.15 * math.pi,
                                               0.75 * math.pi)
                                               
        self.m_rightLowerLeg = self._addBody(self.R_KNEE_POS, 
                                           self.R_ANKLE_POS, 
                                           0.09)
        self.m_rightKnee = self._addHingeJoint(self.m_rightUpperLeg,
                                             self.m_rightLowerLeg, 
                                             self.R_KNEE_POS, 
                                             self.leftAxis, 
                                             0.0, 
                                             math.pi * 0.75)
        self.m_leftLowerLeg = self._addBody(self.L_KNEE_POS, 
                                         self.L_ANKLE_POS, 
                                         0.09)
        self.m_leftKnee = self._addHingeJoint(self.m_leftUpperLeg,
                                            self.m_leftLowerLeg, 
                                            self.L_KNEE_POS, 
                                            self.leftAxis, 
                                            0.0, 
                                            math.pi * 0.75)
                                            
        self.m_rightFoot = self._addBody(self.R_HEEL_POS, 
                                       self.R_TOES_POS, 
                                       0.09)
        self.m_rightAnkle = self._addHingeJoint(self.m_rightLowerLeg,
                                              self.m_rightFoot, 
                                              self.R_ANKLE_POS, 
                                              self.rightAxis, 
                                              -0.1 * math.pi, 
                                              0.05 * math.pi)
                                              
        self.m_leftFoot = self._addBody(self.L_HEEL_POS, 
                                      self.L_TOES_POS, 
                                      0.09)
        self.m_leftAnkle = self._addHingeJoint(self.m_leftLowerLeg,
                                             self.m_leftFoot, 
                                             self.L_ANKLE_POS, 
                                             self.rightAxis, 
                                             -0.1 * math.pi, 
                                             0.05 * math.pi)
                                             
        self.m_rightUpperArm = self._addBody(self.R_SHOULDER_POS, 
                                           self.R_ELBOW_POS, 
                                           0.08)
        self.m_rightShoulder = self._addBallJoint(self.m_chest, 
                                                self.m_rightUpperArm,
                                                self.R_SHOULDER_POS, 
                                                Geometry.norm3((-1.0, -1.0, 4.0)), 
                                                (0.0, 0.0, 1.0), 
                                                math.pi * 0.5,
                                                math.pi * 0.25, 
                                                150.0, 
                                                100.0)
                                                
        self.m_leftUpperArm = self._addBody(self.L_SHOULDER_POS, 
                                         self.L_ELBOW_POS, 
                                         0.08)
        self.m_leftShoulder = self._addBallJoint(self.m_chest, 
                                              self.m_leftUpperArm,
                                              self.L_SHOULDER_POS, 
                                              Geometry.norm3((1.0, -1.0, 4.0)), 
                                              (0.0, 0.0, 1.0), 
                                              math.pi * 0.5,
                                              math.pi * 0.25, 
                                              150.0, 
                                              100.0)

        self.m_rightForeArm = self._addBody(self.R_ELBOW_POS, 
                                          self.R_WRIST_POS, 
                                          0.075)
        self.m_rightElbow = self._addHingeJoint(self.m_rightUpperArm,
                                              self.m_rightForeArm, 
                                              self.R_ELBOW_POS, 
                                              self.downAxis, 
                                              0.0, 
                                              0.6 * math.pi)
                                              
        self.m_leftForeArm = self._addBody(self.L_ELBOW_POS, 
                                         self.L_WRIST_POS, 
                                         0.075)
        self.m_leftElbow = self._addHingeJoint(self.m_leftUpperArm,
                                             self.m_leftForeArm, 
                                             self.L_ELBOW_POS, 
                                             self.upAxis, 
                                             0.0, 
                                             0.6 * math.pi)
        

        self.m_rightHand = self._addBody(self.R_WRIST_POS, 
                                       self.R_FINGERS_POS, 
                                       0.075)
        self.m_rightWrist = self._addHingeJoint(self.m_rightForeArm,
                                              self.m_rightHand, 
                                              self.R_WRIST_POS, 
                                              self.fwdAxis, 
                                              -0.1 * math.pi, 
                                              0.2 * math.pi)
                                              
        self.m_leftHand = self._addBody(self.L_WRIST_POS, 
                                     self.L_FINGERS_POS, 
                                     0.075)
        self.m_leftWrist = self._addHingeJoint(self.m_leftForeArm,
                                            self.m_leftHand, 
                                            self.L_WRIST_POS, 
                                            self.bkwdAxis, 
                                            -0.1 * math.pi, 
                                            0.2 * math.pi)
        print "chest positon"
        print self.m_chest.m_body_ID.getPosition()

    def _addBody(self, p1, p2, radius):
        """
        Adds a capsule body between joint positions p1 and p2 and with given
        radius to the ragdoll.
        """
        #p1 = Geometry.add3(p1, self.m_offset)
        #p2 = Geometry.add3(p2, self.m_offset)

        # define body rotation automatically from body axis
        za = Geometry.norm3(Geometry.sub3(p2, p1))
        
        if (math.fabs(Geometry.dot3(za, (1.0, 0.0, 0.0))) < 0.7): 
            xa = (1.0, 0.0, 0.0)
        else: 
            xa = (0.0, 1.0, 0.0)
            
        ya = Geometry.cross(za, xa)
        xa = Geometry.norm3(Geometry.cross(ya, za))
        ya = Geometry.cross(za, xa)
        rot = (xa[0], ya[0], za[0], xa[1], ya[1], za[1], xa[2], ya[2], za[2])

        tmp = Geometry.add3(Geometry.mul3(Geometry.add3(p1, p2), 0.5), self.m_offset)

        # cylinder length not including endcaps, make capsules overlap by half
        #   radius at joints
        cyllen = Geometry.dist3(p1, p2) - radius

        body = PCylinder(tmp[0], tmp[1], tmp[2], rot, radius, cyllen, 10, 1, 0, 0)
        #after all using  init() to add all the parts the pworld
        #Notice: Make sure the pworld is instanced
        self.m_pworld.addObject(body)
        body.init()
        #body.init() #ToDo: to be called in PWorld                        
        #ToDo
        """
    dJointAttach (joint,rob->chassis->body,cyl->body);
    const dReal *a = dBodyGetPosition (cyl->body);
    dJointSetHingeAxis (joint,cos(ang),sin(ang),0);
    dJointSetHingeAnchor (joint,a[0],a[1],a[2]);

    motor = dJointCreateAMotor(rob->w->world,0);
    dJointAttach(motor,rob->chassis->body,cyl->body);
    dJointSetAMotorNumAxes(motor,1);
    dJointSetAMotorAxis(motor,0,1,cos(ang),sin(ang),0);
    dJointSetAMotorParam(motor,dParamFMax,rob->cfg->robotSettings.Wheel_Motor_FMax);
    speed = 0;
    
        """



        

        body.setBodyPosition(tmp)
        body.setBodyRotation_2(rot)     #global

        self.m_bodies.append(body.m_body_ID)
        self.m_geoms.append(body.m_geom)
		
        self.m_mass += body.m_body_ID.getMass().mass
        #print self.m_mass
        #print body.m_body_ID.getMass()

        
        return body
        
        
    def _addFixedJoint(self, body1, body2):
        joint = ode.FixedJoint(self.m_pworld.m_world)
        joint.attach(body1.m_body_ID, body2.m_body_ID)
        joint.setFixed()

        joint.style = "fixed"
        self.m_joints.append(joint)

        return joint
        
    def _addHingeJoint(self, body1, body2, anchor, axis, loStop = -ode.Infinity,
                      hiStop = ode.Infinity):
                          
        anchor = Geometry.add3(anchor, self.m_offset)

        joint = ode.HingeJoint(self.m_pworld.m_world)
        joint.attach(body1.m_body_ID, body2.m_body_ID)
        joint.setAnchor(anchor)
        joint.setAxis(axis)
        joint.setParam(ode.ParamLoStop, loStop)
        joint.setParam(ode.ParamHiStop, hiStop)
        
        joint.style = "hinge"
        self.m_joints.append(joint)
        
        return joint
        
    def _addUniversalJoint(self, body1, body2, anchor, axis1, axis2,
                          loStop1 = -ode.Infinity, hiStop1 = ode.Infinity,
                          loStop2 = -ode.Infinity, hiStop2 = ode.Infinity):
                              
        anchor = Geometry.add3(anchor, self.m_offset)
        
        joint = ode.UniversalJoint(self.m_pworld.m_world)
        joint.attach(body1.m_body_ID, body2.m_body_ID)
        joint.setAnchor(anchor)
        joint.setAxis1(axis1)
        joint.setAxis2(axis2)
        joint.setParam(ode.ParamLoStop, loStop1)
        joint.setParam(ode.ParamHiStop, hiStop1)
        joint.setParam(ode.ParamLoStop2, loStop2)
        joint.setParam(ode.ParamHiStop2, hiStop2)
        
        joint.style = "univ"
        self.m_joints.append(joint)
        
        return joint
        
    def _addBallJoint(self, body1, body2, anchor, baseAxis, baseTwistUp,
                     flexLimit = math.pi, twistLimit = math.pi, flexForce = 0.0, 
                     twistForce = 0.0):
                         
        anchor = Geometry.add3(anchor, self.m_offset)
        
        # create the joint
        joint = ode.BallJoint(self.m_pworld.m_world)
        joint.attach(body1.m_body_ID, body2.m_body_ID)
        joint.setAnchor(anchor)
        
        # store the base orientation of the joint in the local coordinate system
        #   of the primary body (because baseAxis and baseTwistUp may not be
        #   orthogonal, the nearest vector to baseTwistUp but orthogonal to
        #   baseAxis is calculated and stored with the joint)
        joint.baseAxis = Geometry.getBodyRelVec(body1.m_body_ID, baseAxis)
        tempTwistUp = Geometry.getBodyRelVec(body1.m_body_ID, baseTwistUp)
        baseSide = Geometry.norm3(Geometry.cross(tempTwistUp, joint.baseAxis))
        joint.baseTwistUp = Geometry.norm3(Geometry.cross(joint.baseAxis, baseSide))

        # store the base twist up vector (original version) in the local
        #   coordinate system of the secondary body
        joint.baseTwistUp2 = Geometry.getBodyRelVec(body2.m_body_ID, baseTwistUp)

        # store joint rotation limits and resistive force factors
        joint.flexLimit = flexLimit
        joint.twistLimit = twistLimit
        joint.flexForce = flexForce
        joint.twistForce = twistForce

        joint.style = "ball"
        self.m_joints.append(joint)

        return joint

        
    
    
    
    
    #public function
    
    def step(self):
        pass
    
    def drawLabel(self):
        pass
    
   #def setSpeed(self, i, speed):
   #     pass
    
   #def getSpeed(self, i):
   #     pass
    
   #def resetSpeeds(self):
   #     pass
    
    def resetRobot(self):
        pass
    
    def getXY(self):
        pass
        #return self.x, self.y
        
    def getDir(self):
        pass
        #return self.dir
        
    def setXY(self, x, y):
        pass
    
    def setDir(self, ang):
        pass
    
    def getID(self):
        pass
    
    #def getBall(self):
        #pass






from KINEMATICS import KINEMATICS
import HELIOS
import math

_LINEMANAGER__constant_degree = math.pi/180 

class LINEMANAGER(KINEMATICS):

    def __init__(self, m, K0, Eex2, Eex3, targetCharge2, targetCharge3, MagneticFieldB, axes,c='b'):

        #print targetMass, targetCharge 
        KINEMATICS.__init__(self,m=m, K0=K0, Eex2=Eex2, Eex3=Eex3)
        
        self.LineObj2 = axes.plot([0],[0],c=c)
        self.LineObj3 = axes.plot([0],[0],c=c)
        self.targetCharge2 = targetCharge2
        self.targetCharge3 = targetCharge3
        self.MagneticFieldB = MagneticFieldB

    def SetLineWithTheta(self, thetalab2):
        tr2, tr3 = self.GenerateXYData(thetalab2)    
        self.LineObj2[0].set_data(tr2[0],tr2[1])
        self.LineObj3[0].set_data(tr3[0],tr3[1])
    
    def GenerateXYData(self,thetalab2):
        self.calculate(thetalab2*__constant_degree,0)
        tr2 = HELIOS.trajectory(v=self.V2,
                thetalab=self.thetalab2*__constant_degree, 
                charge=self.targetCharge2, 
                mass=self.m[2],
                B=self.MagneticFieldB)

        tr3 = HELIOS.trajectory(v=self.V3,
                thetalab=self.thetalab3*__constant_degree, 
                charge=self.targetCharge3, 
                mass=self.m[3],
                B=self.MagneticFieldB)
         
        return tr2, tr3

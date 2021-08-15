
## Servo Angle Control


class SPAS:

    # Constants
    MAX_ANGLE = 15          # Maximum Delfection Angle
    MAX_DELTA_ANGLE = 1     # Maximum Rate of change of Deflection Angle

    def __init__(self):
        self.prevAngle = 0

    def maxAngle(self):      
    #Caps the maximum angle
        if self.newAngle > SPAS.MAX_ANGLE:
            self.newAngle = SPAS.MAX_ANGLE

        elif self.newAngle < -1 * SPAS.MAX_ANGLE:
            self.newAngle = -1 * SPAS.MAX_ANGLE

    def stepAngle(self):
    # Set increments of servo angle
        if (self.newAngle - self.prevAngle) > 0:
            self.newAngle = self.prevAngle + SPAS.MAX_DELTA_ANGLE
        if (self.newAngle - self.prevAngle) < 0:
            self.newAngle = self.prevAngle - SPAS.MAX_DELTA_ANGLE
        else:
            self.newAngle = self.newAngle

    def getServoAngle(self, newAngle):
        ## newAngle is "output" from PIDController
        newAngle = self.maxAngle(newAngle)  
        newAngle = self.stepAngle(newAngle)

        self.prevAngle = self.newAngle
        return self.newAngle


## Notes on the Step Increments calculations       
# If angle is positive, greater than 0
# If new angle is positive, and the difference is positive, 
# add MaxDeltaAngle to previous (output) angle
# If new angle is positive, and the difference is negative,
# subtract MaxDeltaAngle from previouis (output) angle 
# If angle is negative, less than 0
# If new angle is negative, and the difference is positive,
# add MaxDeltaAngle to previous (output) angle
## Means old angle is more negative than new angle
# If new angle is negative, and the difference is negative,
# subtract MaxDeltaAngle to previous (output) angle
## Means old angle is larger than new angle
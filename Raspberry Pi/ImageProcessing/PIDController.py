class PIDController(object):

    # Constants
    MAX_ANGLE = 20
    TIMESTEP = 1/30

    # Constructor
    def __init__(self,KP,KI,KD,target):
        self.kp = KP
        self.ki = KI
        self.kd = KD
        self.setTarget(target)
        self.error = 0
        self.last_error = 0
        self.integral_error = 0
        self.derivative_error = 0
        self.output = 0

    # Sets the Target for the Controller along the axis
    def setTarget(self, target):
        self.setpoint = target
    
    # Determines the error for the Set Point, and calculates the Angle in which the plate will respond by
    def compute(self,pos):

        # Calculate the current error of the ball position
        self.error = self.setpoint - pos

        # Calculate the P, I, D Components
        self.integral_error += self.error * PIDController.TIMESTEP
        self.derivative_error = (self.error - self.last_error) / PIDController.TIMESTEP
        self.last_error = self.error

        # Determines the appropriate output angle based on the current error
        self.output = (self.kp*self.error) + (self.ki*self.integral_error) + (self.kd*self.derivative_error)

        # Caps the maximum angle
        if self.output > PIDController.MAX_ANGLE:
            self.output = PIDController.MAX_ANGLE
        elif self.output < -1 * PIDController.MAX_ANGLE:
            self.output = -1 * PIDController.MAX_ANGLE

        # Return the angle
        return self.output
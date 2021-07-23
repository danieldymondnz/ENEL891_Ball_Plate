class PIDController:

    # Constants
    MAX_ANGLE = 20          # Maximum Delfection Angle
    MAX_DELTA_ANGLE = 40    # Maximum Rate of change of Deflection Angle
    TIMESTEP = 1/30         # Equals 1/FPS
    MAX_UI = 9.5            # Integrator anti-windup limiter
    DEADZONE = 0.005        # Acceptable Error around the target position

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

    # Computes the Error of the Ball with Dead Zone
    def calculateError(self, pos):

        # Calculate the current error of the ball position
        calculatedError = self.setpoint - pos

        # If ball is considered within the deadzone, set error to zero
        if abs(calculatedError) <= PIDController.DEADZONE:
            calculatedError = 0

        return calculatedError

    # Determines the error for the Set Point, and calculates the Angle in which the plate will respond by
    def compute(self,pos):

        # Calculate the current error of the ball position
        self.error = self.calculateError(pos)

        # If there is no error, then the controller doesn't need to run
        # Return 0
        if self.error == 0:
            self.output = 0

        # Otherwise, use the controller to calculate the PID and set the angle.
        else:
            # Calculate the P, I, D Components
            self.integral_error += self.error * PIDController.TIMESTEP
            self.derivative_error = (self.error - self.last_error) / PIDController.TIMESTEP
            self.last_error = self.error
            
            # Anti-Windup for the Integrator
            if self.integral_error > PIDController.MAX_UI:
                self.integral_error = PIDController.MAX_UI
            
            # Determines the appropriate output angle based on the current error
            self.output = (self.kp*self.error) + (self.ki*self.integral_error) + (self.kd*self.derivative_error)

            # Caps the maximum angle
            if self.output > PIDController.MAX_ANGLE:
                self.output = PIDController.MAX_ANGLE
            elif self.output < -1 * PIDController.MAX_ANGLE:
                self.output = -1 * PIDController.MAX_ANGLE

            # Check the change in angle
            # TODO Check this!
                        # Set increments of servo angle
            """ if (P_aX - prevPlate_X) > increment :
                P_aX = prevPlate_X + increment
            elif (P_aX - prevPlate_X) > increment :
                P_aX = prevPlate_X - increment
  
            if (P_aY - prevPlate_Y) > increment :
                P_aY = prevPlate_Y + increment
            elif (P_aY - prevPlate_Y) > increment :
                P_aY = prevPlate_Y - increment """

        # Return the angle
        return self.output
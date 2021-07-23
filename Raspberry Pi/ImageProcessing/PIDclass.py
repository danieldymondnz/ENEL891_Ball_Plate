

class PIDCalc(object):

    def __init__(self,KP,KI,KD,target):
        self.kp = KP
        self.ki = KI
        self.kd = KD
        self.setpoint = target
        self.error = 0
        self.last_error = 0
        self.integral_error = 0
        self.derivative_error = 0
        self.output = 0
    
    def compute(self,pos):
        self.error = self.setpoint - pos
        self.integral_error += self.error * timestep
        self.derivative_error = (self.error - self.last_error) / timestep
        self.last_error = self.error

        self.output = (self.kp*self.error) + (self.ki*self.integral_error) + (self.kd*self.derivative_error)

        if self.output >= Max_angle:
            self.output = max_angle
        if self.output <= 
        return self.output
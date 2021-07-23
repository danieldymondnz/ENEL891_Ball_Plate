from PIDController import PIDController as PID

# Test-set of Coordinates
# xPoints = [0.30, 0.28, 0.25, 0.21, 0.19, 0.16, 0.13, 0.09, 0.07, 0.05, 0.03, 0.01, 0.008, 0.0049, 0.00]
xPoints = [0.30, 0.20, 0.05, -0.18]
nXPoints = len(xPoints)
n = 0

# Initial Values for angles
P_aX = 0 # plate angle X initial value
S_angleX = 90  # initial angle of servos
prevPlate_X = 0

# PID Specifications
Kp = 2.768
Ki = 1.08
Kd = 1.771

# Aim for the Setpoint in the Center of the Plate
setpoint = [0,0]

# PID Controllers for the Servos
xAxis = PID(Kp, Ki, Kd, setpoint[0])

# Loop
while n < nXPoints:

    # Grab Coordinate
    BP_x = xPoints[n]
    n = n + 1

    # Send position data to the PID Controllers and determine the desired Plate Angles
    P_aX = xAxis.compute(BP_x)

    # Convert output from plate angle to servo angle
    S_angleX = P_aX

    # Debug
    print(" === Position {} === ".format(n))
    print("Ball position: {}".format(BP_x))
    print("Plate Angle X: {}".format(P_aX))
    print("Servo angle X : {}".format(S_angleX))
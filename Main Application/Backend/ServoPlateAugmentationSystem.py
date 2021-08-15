
class ServoPlateAugmentationSystem(object):

    def plateAugmentation(rawAngle):
        
        newAngle = rawAngle
        return newAngle


        # Caps the maximum angle
        if newOutput > PID.MAX_ANGLE:
            newOutput = PID.MAX_ANGLE
        elif newOutput < -1 * PID.MAX_ANGLE:
            newOutput = -1 * PID.MAX_ANGLE

        # Check the change in angle
        # TODO Check this!
        # Set increments of servo angle
        if abs(newOutput - self.output) > PID.MAX_DELTA_ANGLE:
            newOutput = (newOutput / abs(newOutput)) * PID.MAX_DELTA_ANGLE
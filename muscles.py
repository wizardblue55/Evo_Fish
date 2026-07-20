class Muscle:
    def __init__(self, name, jointName, gear=2.0, ctrlRange=(-1, 1)):
        self.name = name
        self.jointName = jointName
        self.gear = gear
        self.ctrlRange = ctrlRange

    def toXml(self, indent=0):
        pad = "  " * indent
        return (
            f'{pad}<motor name="{self.name}" joint="{self.jointName}" '
            f'gear="{self.gear:.4f}" ctrlrange="{self.ctrlRange[0]} {self.ctrlRange[1]}"/>'
        )


def buildFishMuscles(jointNames, genome, ctrlRange=(-1, 1)):

    return [
        Muscle(name=f"{jointName}Motor", jointName=jointName, gear=genome.muscleGear, ctrlRange=ctrlRange)
        for jointName in jointNames
    ]


def muscleListToXml(muscles, indent=0):
    pad = "  " * indent
    lines = [f"{pad}<actuator>"]
    for muscle in muscles:
        lines.append(muscle.toXml(indent + 1))
    lines.append(f"{pad}</actuator>")
    return "\n".join(lines)
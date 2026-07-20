class Bone:

    def __init__(
        self,
        name,
        pos,
        geomSize,
        geomType="capsule",
        geomEuler="0 90 0",
        jointName=None,
        jointType="hinge",
        jointAxis="0 0 1",
        jointRange="-45 45",
        jointDamping=0.5,
        isFreeJoint=False,
        rgba=None,
    ):
        self.name = name
        self.pos = pos
        self.geomSize = geomSize
        self.geomType = geomType
        self.geomEuler = geomEuler
        self.jointName = jointName if jointName else f"{name}Joint"
        self.jointType = jointType  # None => rigidly welded, no joint emitted
        self.jointAxis = jointAxis
        self.jointRange = jointRange
        self.jointDamping = jointDamping
        self.isFreeJoint = isFreeJoint
        self.rgba = rgba
        self.children = []

    def addChild(self, bone):
        self.children.append(bone)
        return bone

    def hasJoint(self):
        return self.isFreeJoint or self.jointType is not None

    def _jointXml(self):
        if self.isFreeJoint:
            return f'<joint name="{self.jointName}" type="free"/>'
        if self.jointType is None:
            return None
        return (
            f'<joint name="{self.jointName}" type="{self.jointType}" '
            f'axis="{self.jointAxis}" range="{self.jointRange}" '
            f'damping="{self.jointDamping}"/>'
        )

    def _geomXml(self):
        rgbaAttr = f' rgba="{self.rgba}"' if self.rgba else ""
        return (
            f'<geom name="{self.name}Geom" type="{self.geomType}" '
            f'size="{self.geomSize}" euler="{self.geomEuler}"{rgbaAttr}/>'
        )

    def toXml(self, indent=0):
        pad = "  " * indent
        childPad = "  " * (indent + 1)

        lines = [f'{pad}<body name="{self.name}" pos="{self.pos}">']
        jointXml = self._jointXml()
        if jointXml is not None:
            lines.append(f"{childPad}{jointXml}")
        lines.append(f"{childPad}{self._geomXml()}")
        for child in self.children:
            lines.append(child.toXml(indent + 1))
        lines.append(f"{pad}</body>")

        return "\n".join(lines)

    def allJointNames(self):
        
        names = []
        if self.hasJoint() and not self.isFreeJoint:
            names.append(self.jointName)
        for child in self.children:
            names.extend(child.allJointNames())
        return names


def buildFishSkeleton(genome):
    
    head = Bone(
        name="head",
        pos="0 0 0.5",
        geomSize=f"{0.06 * genome.mouthSize:.4f} 0.08",
        isFreeJoint=True,
        jointName="root",
        rgba="0.3 0.5 0.8 1",
    )

    baseSegmentLength = 0.18
    baseSegmentWidth = 0.06

    currentParent = head
    for i in range(genome.numTailSegments):
        segmentScale = genome.tailSegmentScale * (genome.tailTaper ** i)
        length = baseSegmentLength * segmentScale
        width = baseSegmentWidth * segmentScale

        tailBone = Bone(
            name=f"tail{i + 1}",
            pos=f"{length:.4f} 0 0",
            geomSize=f"{width:.4f} {length * 0.8:.4f}",
            jointDamping=genome.muscleDamping,
            rgba="0.3 0.5 0.8 1",
        )
        currentParent.addChild(tailBone)
        currentParent = tailBone

    finTip = Bone(
        name="finTip",
        pos="0.1 0 0",
        geomSize=f"{0.06 * genome.finSize:.4f} 0.001 {0.06 * genome.finSize:.4f}",
        geomType="box",
        geomEuler="0 0 0",
        jointDamping=genome.muscleDamping,
        rgba="0.8 0.6 0.2 1",
    )
    currentParent.addChild(finTip)

    if genome.hasPectoralFins:
        for side, ySign in [("Left", 1), ("Right", -1)]:
            finBone = Bone(
                name=f"pectoralFin{side}",
                pos=f"0.05 {0.05 * ySign:.4f} 0",
                geomSize="0.02 0.04",
                geomType="capsule",
                geomEuler=f"{90 * ySign} 0 0",
                jointAxis="1 0 0",
                jointRange=f"-{genome.pectoralFinAngle:.2f} {genome.pectoralFinAngle:.2f}",
                jointDamping=genome.muscleDamping,
                rgba="0.6 0.7 0.9 1",
            )
            head.addChild(finBone)

    for i in range(genome.numEyes):
        ySign = 1 if i % 2 == 0 else -1
        eyeBone = Bone(
            name=f"eye{i + 1}",
            pos=f"0.05 {0.03 * ySign:.4f} 0.02",
            geomSize="0.015",
            geomType="sphere",
            geomEuler="0 0 0",
            jointType=None,
            rgba="0.1 0.1 0.1 1",
        )
        head.addChild(eyeBone)

    return head
import random
from dataclasses import dataclass, field, replace                                      
                                        
MAX_TAIL_SEGMENTS = 5
MAX_EYES = 2


@dataclass
class Genome:
                                                         
    numTailSegments: int = 10                                
    hasPectoralFins: bool = True
    numEyes: int = 4                               

                                                                        
    tailSegmentScale: float = 1.0                                         
    tailTaper: float = 0.85                                                      
    finSize: float = 1.0                                                   
    pectoralFinAngle: float = 30.0                                         
    mouthSize: float = 1.0                                                 

                                                          
    muscleGear: float = 2.0                                      
    muscleDamping: float = 0.5

                                                                            
    eyeFov: float = 60.0                       
    eyeRange: float = 3.0                                                

                                                                               
    dietBias: float = 0.0                                                           
    metabolismRate: float = 1.0                                  
    reproduceThreshold: float = 100.0                                          
    maxSpeedMultiplier: float = 1.0

    def maskedJointCount(self):

        return self.numTailSegments


def randomGenome():
    return Genome(
        numTailSegments=random.randint(1, MAX_TAIL_SEGMENTS),
        hasPectoralFins=random.random() < 0.7,
        numEyes=random.randint(0, MAX_EYES),
        tailSegmentScale=random.uniform(0.6, 1.4),
        tailTaper=random.uniform(0.7, 0.95),
        finSize=random.uniform(0.6, 1.6),
        pectoralFinAngle=random.uniform(0.0, 60.0),
        mouthSize=random.uniform(0.7, 1.5),
        muscleGear=random.uniform(1.0, 4.0),
        muscleDamping=random.uniform(0.2, 1.0),
        eyeFov=random.uniform(30.0, 120.0),
        eyeRange=random.uniform(1.5, 6.0),
        dietBias=random.uniform(-1.0, 1.0),
        metabolismRate=random.uniform(0.7, 1.3),
        reproduceThreshold=random.uniform(70.0, 140.0),
        maxSpeedMultiplier=random.uniform(0.7, 1.3),
    )


def mutateGenome(genome, mutationRate=0.15, mutationStrength=0.2):

    child = replace(genome)                

                                                       
    if random.random() < mutationRate:
        child.numTailSegments = max(1, min(MAX_TAIL_SEGMENTS, child.numTailSegments + random.choice([-1, 1])))
    if random.random() < mutationRate:
        child.hasPectoralFins = not child.hasPectoralFins
    if random.random() < mutationRate:
        child.numEyes = max(0, min(MAX_EYES, child.numEyes + random.choice([-1, 1])))

                                                                                   
    continuousFields = [
        "tailSegmentScale", "tailTaper", "finSize", "pectoralFinAngle", "mouthSize",
        "muscleGear", "muscleDamping", "eyeFov", "eyeRange",
        "dietBias", "metabolismRate", "reproduceThreshold", "maxSpeedMultiplier",
    ]
    for fieldName in continuousFields:
        if random.random() < mutationRate:
            currentValue = getattr(child, fieldName)
            noise = random.gauss(0, mutationStrength) * abs(currentValue if currentValue != 0 else 1.0)
            setattr(child, fieldName, currentValue + noise)

    child.dietBias = max(-1.0, min(1.0, child.dietBias))
    return child


def crossoverGenomes(parentA, parentB):

    childFields = {}
    for fieldName in parentA.__dataclass_fields__:
        chosenParent = parentA if random.random() < 0.5 else parentB
        childFields[fieldName] = getattr(chosenParent, fieldName)

    return Genome(**childFields)
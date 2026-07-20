from bone import buildFishSkeleton
from dinoDNA import randomGenome
from muscles import buildFishMuscles, muscleListToXml


def buildFishModelXml(genome=None):
    if genome is None:
        genome = randomGenome()

    skeleton = buildFishSkeleton(genome)
    muscles = buildFishMuscles(skeleton.allJointNames(), genome)

    modelXml = f"""<mujoco model="simpleFish">
  <option timestep="0.01" density="1000" viscosity="0.001" integrator="RK4">
    <flag contact="disable"/>
  </option>

  <default>
    <joint type="hinge" damping="0.5" limited="true" range="-45 45"/>
    <geom type="capsule" fluidshape="ellipsoid" rgba="0.3 0.5 0.8 1"/>
  </default>

  <worldbody>
    <light diffuse="0.8 0.8 0.8" pos="0 0 3" dir="0 0 -1"/>
{skeleton.toXml(indent=2)}
  </worldbody>

{muscleListToXml(muscles, indent=1)}
</mujoco>
"""
    return modelXml


if __name__ == "__main__":
    xml = buildFishModelXml()
    print(xml)

    with open("fish.xml", "w") as f:
        f.write(xml)
    print("\nWrote fish.xml")
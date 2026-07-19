from myosuite.utils import gym

envName = "myoElbowPose1D6MRandom-v0"

print(f"Creating environment: {envName}")
env = gym.make(envName)
env.reset()

print("Environment created successfully. Running random actions...")

numSteps = 200
for step in range(numSteps):
    action = env.action_space.sample()
    obs, reward, terminated, truncated, info = env.step(action)
    env.mj_render()

    if terminated or truncated:
        env.reset()

env.close()
print("Test complete — if a window appeared and moved, the install is good.")
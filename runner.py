import time


class Runner:

    def __init__(self, env, policy=None, render=True, realTime=True):
        self.env = env
        self.policy = policy  # callable(obs) -> action; None = random actions
        self.render = render
        self.realTime = realTime

    def chooseAction(self, obs):
        if self.policy is not None:
            return self.policy(obs)
        return self.env.action_space.sample()

    def runEpisode(self, maxSteps=None):
        """Runs one episode to completion (or until maxSteps/window-close)
        and returns (totalReward, stepsTaken)."""
        obs, info = self.env.reset()
        totalReward = 0.0
        step = 0

        while True:
            action = self.chooseAction(obs)
            obs, reward, terminated, truncated, info = self.env.step(action)
            totalReward += reward
            step += 1

            if self.render:
                self.env.render()
                if not self.env.renderer.isRunning():
                    break
                if self.realTime:
                    time.sleep(self.env.model.opt.timestep)

            if terminated or truncated:
                break
            if maxSteps is not None and step >= maxSteps:
                break

        return totalReward, step

    def runForever(self):
        """Runs episodes back-to-back until the render window is closed
        (or Ctrl+C in a headless run). Prints a summary after each one."""
        try:
            while True:
                totalReward, steps = self.runEpisode()
                print(f"Episode finished: reward={totalReward:.3f}, steps={steps}")
                if self.render and not self.env.renderer.isRunning():
                    break
        except KeyboardInterrupt:
            pass
        finally:
            self.env.close()
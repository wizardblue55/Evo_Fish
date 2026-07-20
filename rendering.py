import mujoco
import mujoco.viewer

class Renderer:

    def __init__(self, model, data):
        self.model = model
        self.data = data
        self.viewer = None

    def open(self):
        if self.viewer is None:
            self.viewer = mujoco.viewer.launch_passive(self.model, self.data)
        return self.viewer

    def sync(self):
        if self.viewer is None:
            self.open()
        self.viewer.sync()

    def isRunning(self):
        return self.viewer is not None and self.viewer.is_running()

    def close(self):
        if self.viewer is not None:
            self.viewer.close()
            self.viewer = None
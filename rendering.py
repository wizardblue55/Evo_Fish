import pyvista as pv

# Load a built-in mesh or pass the path to your own .obj/.stl file
mesh = pv.read("my_model.obj") 

# Add a basic shape if you don't have a file
# mesh = pv.Sphere()

# Initialize the plotter and render the object
plotter = pv.Plotter()
plotter.add_mesh(mesh, color="blue", show_edges=True)
plotter.show()
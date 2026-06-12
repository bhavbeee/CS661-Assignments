import vtk
import argparse
import sys

# Build the color transfer function using the values given in the assignment
def get_color_transfer_function():
    ctf = vtk.vtkColorTransferFunction()
    #  Data Value    R     G     B
    ctf.AddRGBPoint(-4931.54, 0.0, 1.0, 1.0)
    ctf.AddRGBPoint(-2508.95, 0.0, 0.0, 1.0)
    ctf.AddRGBPoint(-1873.9,  0.0, 0.0, 0.5)
    ctf.AddRGBPoint(-1027.16, 1.0, 0.0, 0.0)
    ctf.AddRGBPoint(-298.031, 1.0, 0.4, 0.0)
    ctf.AddRGBPoint( 2594.97, 1.0, 1.0, 0.0)
    return ctf

# Build the opacity (piecewise) transfer function using the values given in the assignment
def get_opacity_transfer_function():
    otf = vtk.vtkPiecewiseFunction()
    #  Data Value   Opacity
    otf.AddPoint(-4931.54, 1.0)
    otf.AddPoint(  101.815, 0.002)
    otf.AddPoint( 2594.97,  0.0)
    return otf

# Create the bounding box outline actor using vtkOutlineFilter
def get_outline_actor(image_data):
    outline_filter = vtk.vtkOutlineFilter()
    outline_filter.SetInputData(image_data)

    outline_mapper = vtk.vtkPolyDataMapper()
    outline_mapper.SetInputConnection(outline_filter.GetOutputPort())

    outline_actor = vtk.vtkActor()
    outline_actor.SetMapper(outline_mapper)
    return outline_actor

def render_volume(input_file, use_phong):
    # Load the 3D dataset from disk
    print(f"Reading data from {input_file}...")
    reader = vtk.vtkXMLImageDataReader()
    reader.SetFileName(input_file)
    reader.Update()
    image_data = reader.GetOutput()

    if image_data.GetNumberOfPoints() == 0:
        print(f"Error: No data loaded from '{input_file}'. Check the file path.")
        sys.exit(1)

    print(f"Volume loaded: dimensions = {image_data.GetDimensions()}, "
          f"points = {image_data.GetNumberOfPoints()}")

    # Set up the color and opacity transfer functions
    color_tf = get_color_transfer_function()
    opacity_tf = get_opacity_transfer_function()

    # Configure the volume property with the transfer functions
    vol_prop = vtk.vtkVolumeProperty()
    vol_prop.SetColor(color_tf)
    vol_prop.SetScalarOpacity(opacity_tf)

    # Optionally enable Phong shading with the assignment-specified coefficients
    if use_phong:
        vol_prop.ShadeOn()
        vol_prop.SetAmbient(0.5)
        vol_prop.SetDiffuse(0.5)
        vol_prop.SetSpecular(0.5)
        print("Phong shading: ENABLED (ambient=0.5, diffuse=0.5, specular=0.5)")
    else:
        vol_prop.ShadeOff()
        print("Phong shading: DISABLED")

    # Hook up the mapper to the data
    vol_mapper = vtk.vtkSmartVolumeMapper()
    vol_mapper.SetInputData(image_data)

    # Create the volume actor with the mapper and property
    volume = vtk.vtkVolume()
    volume.SetMapper(vol_mapper)
    volume.SetProperty(vol_prop)

    # Set up the renderer and add the volume + bounding box outline
    renderer = vtk.vtkRenderer()
    renderer.SetBackground(0.1, 0.1, 0.1)
    renderer.AddVolume(volume)
    renderer.AddActor(get_outline_actor(image_data))

    # Create a 1000x1000 render window as required
    render_window = vtk.vtkRenderWindow()
    render_window.SetSize(1000, 1000)
    render_window.AddRenderer(renderer)
    render_window.SetWindowName("CS661 Assignment 1 - Volume Rendering")

    # Start the interactive window
    interactor = vtk.vtkRenderWindowInteractor()
    interactor.SetRenderWindow(render_window)
    interactor.Initialize()
    render_window.Render()
    interactor.Start()

def main():
    parser = argparse.ArgumentParser(description="CS661 Assignment 1 Part 2 - Volume Rendering")
    parser.add_argument("--input", type=str, required=True, help="Path to 3D VTK image data file (.vti)")
    parser.add_argument("--phong", action="store_true", help="Enable Phong shading (off by default)")
    args = parser.parse_args()

    print(f"Input file : {args.input}")
    print(f"Phong shading requested: {args.phong}")

    render_volume(args.input, use_phong=args.phong)

if __name__ == "__main__":
    main()

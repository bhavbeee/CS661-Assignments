import vtk
import argparse
import os

# Function to extract the 2D contour lines manually without using vtkContourFilter
def extract_isocontour(input_file, isovalue, output_file):
    print(f"Reading data from {input_file}...")
    
    # load the vti dataset
    reader = vtk.vtkXMLImageDataReader()
    reader.SetFileName(input_file)
    reader.Update()
    image_data = reader.GetOutput()

    # grab grid properties we need for math
    dims = image_data.GetDimensions()
    origin = image_data.GetOrigin()
    spacing = image_data.GetSpacing()
    
    # pull the pressure data
    scalars = image_data.GetPointData().GetArray('Pressure')
    if not scalars:
        raise ValueError("Couldn't find the Pressure array in the dataset.")

    # set up VTK objects to hold our new contour lines
    points = vtk.vtkPoints()
    lines = vtk.vtkCellArray()
    
    # array to hold the isovalues so we can color it in ParaView later
    scalar_values = vtk.vtkFloatArray()
    scalar_values.SetName("Pressure")

    print(f"Extracting contour for isovalue: {isovalue}...")

    # loop through every single cell in the 2D grid
    # dims[0] is x-axis, dims[1] is y-axis
    for row in range(dims[1] - 1):
        for col in range(dims[0] - 1):
            
            # calculate 1D indices for the four corners of the current cell
            idx00 = row * dims[0] + col      # bottom-left
            idx10 = idx00 + 1                # bottom-right
            idx11 = idx10 + dims[0]          # top-right
            idx01 = idx00 + dims[0]          # top-left

            # get the actual pressure values at these corners
            s00 = scalars.GetTuple1(idx00)
            s10 = scalars.GetTuple1(idx10)
            s11 = scalars.GetTuple1(idx11)
            s01 = scalars.GetTuple1(idx01)

            intersections = []

            # The assignment strictly requires checking edges counterclockwise 
            # and we MUST start from the bottom edge.
            
            # 1. Bottom edge (moving left to right)
            if (s00 < isovalue) != (s10 < isovalue):
                # find exact intersection using linear interpolation
                t = (isovalue - s00) / (s10 - s00) if (s10 != s00) else 0.0
                x = origin[0] + (col + t) * spacing[0]
                y = origin[1] + row * spacing[1]
                intersections.append((x, y))

            # 2. Right edge (moving bottom to top)
            if (s10 < isovalue) != (s11 < isovalue):
                t = (isovalue - s10) / (s11 - s10) if (s11 != s10) else 0.0
                x = origin[0] + (col + 1) * spacing[0]
                y = origin[1] + (row + t) * spacing[1]
                intersections.append((x, y))

            # 3. Top edge (moving right to left)
            if (s11 < isovalue) != (s01 < isovalue):
                t = (isovalue - s11) / (s01 - s11) if (s01 != s11) else 0.0
                x = origin[0] + (col + 1 - t) * spacing[0]
                y = origin[1] + (row + 1) * spacing[1]
                intersections.append((x, y))

            # 4. Left edge (moving top to bottom)
            if (s01 < isovalue) != (s00 < isovalue):
                t = (isovalue - s01) / (s00 - s01) if (s00 != s01) else 0.0
                x = origin[0] + col * spacing[0]
                y = origin[1] + (row + 1 - t) * spacing[1]
                intersections.append((x, y))

            # As per assignment notes, we don't need to handle ambiguities (asymptotic decider).
            # We only process cells that have exactly 2 intersections.
            if len(intersections) == 2:
                # add the two points
                point0_id = points.InsertNextPoint(intersections[0][0], intersections[0][1], 0.0)
                point1_id = points.InsertNextPoint(intersections[1][0], intersections[1][1], 0.0)
                
                # assign the isovalue to both points
                scalar_values.InsertNextValue(isovalue)
                scalar_values.InsertNextValue(isovalue)
                
                # create a line segment connecting them
                lines.InsertNextCell(2)
                lines.InsertCellPoint(point0_id)
                lines.InsertCellPoint(point1_id)

    # bundle everything into a polydata object
    polydata = vtk.vtkPolyData()
    polydata.SetPoints(points)
    polydata.SetLines(lines)
    polydata.GetPointData().SetScalars(scalar_values)

    # write it out to disk
    writer = vtk.vtkXMLPolyDataWriter()
    writer.SetFileName(output_file)
    writer.SetInputData(polydata)
    writer.Write()
    print(f"Done! Contour saved to {output_file}")

def main():
    # handle command line inputs
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=str, required=True, help="Input VTI file")
    parser.add_argument("--isovalue", type=float, required=True, help="Isovalue (-1438 to 630)")
    parser.add_argument("--output", type=str, required=True, help="Output VTP file")
    args = parser.parse_args()

    # assignment says possible range is -1438 to 630
    if not (-1438 <= args.isovalue <= 630):
        print(f"Warning: Isovalue {args.isovalue} is outside the dataset range (-1438, 630).")

    if not os.path.exists(args.input):
        raise FileNotFoundError(f"Cannot find input file: {args.input}")

    extract_isocontour(args.input, args.isovalue, args.output)

if __name__ == "__main__":
    main()
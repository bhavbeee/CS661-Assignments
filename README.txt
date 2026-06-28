CS661 Assignment 1
Isocontour and Volume Visualization

Group Number: 8
Group Members: Anushka Rajora, Raparthi Bhavishitha, Aditi

Files Included
1. extract_isocontour.py
2. volume_render.py
3. README.txt


Requirements
The scripts were developed and tested using:
* Python 3.12.3
* VTK 9.6.2
* ParaView (for visualization of output files)

Install the required VTK package using:

pip install vtk

PART 1: 2D Isocontour Extraction
---------------------------------------------------------
Description
The script extract_isocontour.py extracts 2D isocontours manually from a VTK image dataset without using vtkContourFilter or any existing VTK contour extraction filter.
The implementation follows the assignment requirements:
* Manual contour extraction
* Counterclockwise edge traversal strictly starting from the bottom edge (bottom -> right -> top -> left).
* Linear interpolation used for exact intersection computation.
* Ambiguous cells are ignored (only processes cells with exactly two intersections).
* Output generated as VTK PolyData (.vtp)


Input Dataset
Isabel_2D.vti


Run Command
python extract_isocontour.py --input "<path_to_Isabel_2D.vti>" --isovalue <value> --output <output_file.vtp>


Example

python extract_isocontour.py --input "Data/Isabel_2D.vti" --isovalue -500 --output contour.vtp

Parameters

--input
Path to the input .vti file

--isovalue
Isovalue used for contour extraction
(Expected range: -1438 to 630)

--output
Path/name of output .vtp file

Output

The script generates a VTK PolyData (.vtp) file containing the extracted contour lines.

The output can be visualized using ParaView.

PART 2: Volume Rendering
---------------------------------------------------------
Description
The script volume_render.py performs volume rendering using vtkSmartVolumeMapper and applies the transfer functions specified in the assignment.
Implemented Features:
* vtkSmartVolumeMapper
* Color transfer function
* Opacity transfer function
* vtkOutlineFilter
* Optional Phong shading toggle
* 1000x1000 render window


Input Dataset
Isabel_3D.vti


Run WITHOUT Phong Shading
python volume_render.py --input "<path_to_Isabel_3D.vti>"


Example
python volume_render.py --input "Data/Isabel_3D.vti"


Run WITH Phong Shading
python volume_render.py --input "<path_to_Isabel_3D.vti>" --phong


Example
python volume_render.py --input "Data/Isabel_3D.vti" --phong


Parameters
--input : Path to the input .vti file
--phong : Optional flag to enable Phong shading

Phong Shading Parameters
Ambient coefficient: 0.5
Diffuse coefficient: 0.5
Specular coefficient: 0.5


Visualization
Running the script opens an interactive VTK render window displaying the rendered hurricane dataset.

---------------------------------------------------------
TESTING & SUBMISSION
---------------------------------------------------------
The scripts were tested by:
* Running both scripts with the provided datasets
* Verifying successful generation of the .vtp contour output
* Visualizing contour output in ParaView
* Testing volume rendering with and without Phong shading enabled

The final submission zip file is named:
8_Assignment1.zip

The zip file contains only:

extract_isocontour.py
volume_render.py
README.txt




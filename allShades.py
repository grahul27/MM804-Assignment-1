import vtk

## Read the model with VtkOBJREADER and import the model
reader = vtk.vtkOBJReader()
reader.SetFileName("Handle.obj")

# Function to rotate along different axis
def rotateObject(obj,x,y,z):
    obj.RotateX(x)
    obj.RotateY(y)
    obj.RotateZ(z)
    return obj

# to add light to the objects
def setupObjectLighting():
    light = vtk.vtkLight ()
    light.SetLightTypeToSceneLight()
    light.SetAmbientColor(1, 1, 1)
    light.SetDiffuseColor(1, 1, 1)
    light.SetSpecularColor(1, 1, 1)
    light.SetPosition(-100, 100, 25)
    light.SetFocalPoint(0,0,0)
    light.SetIntensity(0.8)
    return light

# Setup the common properties for the object
def setObjectProperty(property):
    
    property.ShadingOn()
    property.SetColor(0, 1, 0)
    property.SetDiffuse(0.8) 
    property.SetAmbient(0.3) 
    property.SetSpecular(1.0) 
    property.SetSpecularPower(100.0)


# creating a port function 
def CreateViewPort(reader,writeFileName,x_rotate=-90,y_rotate=0,z_rotate=0):
    
    # normal vector
    normals = vtk.vtkPolyDataNormals()
    normals.SetInputConnection(reader.GetOutputPort())

    #  mapper
    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputConnection(normals.GetOutputPort())
    
    # creating multiple actors for various views - wireframe, Gouraud, Flat, Phong
    wireframe_actor = vtk.vtkActor()
    flat_actor = vtk.vtkActor()
    gouraud_actor = vtk.vtkActor()
    phong_actor = vtk.vtkActor()

    #For Wireframe
    mapper.SetInputConnection(reader.GetOutputPort())
    wireframe_actor.SetMapper(mapper)
    wireframe_actor = rotateObject(wireframe_actor,x_rotate,y_rotate,z_rotate)
    wireframe_actor.GetProperty().SetRepresentationToWireframe()

    # For Flat shading
    flat_actor.SetMapper(mapper)

    flat_properties = flat_actor.GetProperty()
    flat_properties.SetInterpolationToFlat() # Set shading to Flat
    setObjectProperty(flat_properties)

    flat_actor = rotateObject(flat_actor,x_rotate,y_rotate,z_rotate)
    # Setup the lights for last 3 models

    light = setupObjectLighting()
    gouraud_actor.SetMapper(mapper)
    gouraud_properties = gouraud_actor.GetProperty()
    gouraud_properties.SetInterpolationToGouraud() # Set shading to Gouraud
    setObjectProperty(gouraud_properties)
    gouraud_actor = rotateObject(gouraud_actor,x_rotate,y_rotate,z_rotate)


    phong_actor.SetMapper(mapper)
    phong_properties = phong_actor.GetProperty()
    phong_properties.SetInterpolationToPhong() # Set shading to Phong
    setObjectProperty(phong_properties)
    phong_actor = rotateObject(phong_actor,x_rotate,y_rotate,z_rotate)


    render_wireframe = vtk.vtkRenderer()
    render_flat = vtk.vtkRenderer()
    render_gouraud = vtk.vtkRenderer()
    render_phong = vtk.vtkRenderer()

    # Setup the view port in a window frame
    # xmin, ymin, xmax, ymax
    render_phong.SetViewport(0.5, 0, 1.0, 0.5)
    render_wireframe.SetViewport(0, 0.5, 0.5, 1)
    render_flat.SetViewport(0.5, 0.5, 1.0, 1.0)
    render_gouraud.SetViewport(0, 0, 0.5, 0.5) 
    render_wireframe.AddActor(wireframe_actor)
    render_flat.AddActor(flat_actor)
    render_gouraud.AddActor(gouraud_actor)
    render_phong.AddActor(phong_actor)

    render_flat.AddLight(light)

    renderWindow = vtk.vtkRenderWindow()
    renderWindow.SetSize(700, 600)
    renderWindow.AddRenderer(render_wireframe)
    renderWindow.AddRenderer(render_flat)
    renderWindow.AddRenderer(render_gouraud)
    renderWindow.AddRenderer(render_phong)
    renderWindow.Render()

    # Save the output as image
    to_image = vtk.vtkWindowToImageFilter()
    to_image.SetInput(renderWindow)
    to_image.Update()
    # creating image into a output file
    jwriter = vtk.vtkJPEGWriter()    
    jwriter.SetInputData(to_image.GetOutput())
    jwriter.SetFileName(writeFileName)
    jwriter.Write()

CreateViewPort(x_rotate=-90,y_rotate=0,z_rotate=0,reader=reader,writeFileName='output.png')

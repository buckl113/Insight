# Insight
This is a library compiled from multiple Jupyterhub image analysis projects. 
These projects include a camera program, an image alignment program, a point selection program, and a paint program.
## INSTRUCTIONS:
download or copy & paste "Insight.py"

In Jupyter Notebooks:

cell [1] 

    !pip3 install mpld3 --- AFTER RUNNING ONCE, DON'T RUN AGAIN OR CLONE

cell [2] 

    # only needs to be run after kernel has restarted
    import Insight
    
cell [3] 

    # in order to run alignment, type this (and insert 1 or 2 url strings to change the images)
    Insight.alignment()
    
cell [4] 
    
    # in order to run points, type this (and insert a url string, point color, and/or point radius to change from default)
    Insight.points()

cell [5]

    # after running points and selecting points, to see the point coordinates, run this
    Insight.point_coords(xcoords,ycoords)

cell [6]

    # in order to run paint, run this (and insert a filename string to change the background image)
    Insight.paint()
    
cell [7]
    
    # after running paint and snapping a photo of your drawings, run this to view your drawings
    Insight.image_plot(image)
    
cell [8]     
    
    # in order to run camera, run this
    Insight.camera()
    
cell [9]

    # after running camera and snapping a photo , run this to view your picture
    Insight.image_plot(image)

# Insight
This is a library compiled from multiple Jupyterhub image analysis projects. 
These projects include a camera program, an image alignment program, a point selection program, and a paint program.
## camera
This allows the user to access their camera via javascript.
The user can snap a photo by clicking on the "Snap Photo" button, and the photo is displayed on an x-y plot.
## alignment
This program allows the user to input the url of two different photos.
The program uses python to allow the user to change the horizontal or vertical alignments of the photos, fade one photo into the other, change the size of each photo, and rotate the photos.
## points
This allows the user to input the url of a photo to use as a background, input point color, and input point radius.
Using both python and javascript, this program allows the user to select and drag points on the background picture, which is displayed on an x-y plot.
The program then allows the user to view the x and y coordinates of each point.
## paint
This allows the user to input the file name of a photo to use as a canvas.
This program uses javascript code to allow the user to draw on the canvas, change the color and size of their pen, erase their previous drawings, or snap a photo.
Once the "Snap Photo" button is selected, the program uses python to give the drawings a white canvas, displaying them on a x-y plot and then as a photo.

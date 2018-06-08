from PIL import Image
import matplotlib.pylab as plt
import matplotlib.image as img
from IPython.display import HTML

import base64
import io

def camera():

    main_text = """
    <video id="video" width="640" height="480" autoplay></video>
    <button id="snap">Snap Photo</button>
    <canvas id="canvas" width="640" height="480"></canvas>

    <script>
    // Grab elements, create settings, etc.
    var video = document.getElementById('video');

    // Get access to the camera!
    if(navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
        // Not adding `{ audio: true }` since we only want video now
        navigator.mediaDevices.getUserMedia({ video: true }).then(function(stream) {
            video.src = window.URL.createObjectURL(stream);
            video.play();
        });
    }
    // Elements for taking the snapshot
    var canvas = document.getElementById('canvas');
    var context = canvas.getContext('2d');
    var video = document.getElementById('video');

    // Trigger photo take
    document.getElementById("snap").addEventListener("click", function() {
        //TODO Get rid of hard coded image sizes. 
        context.drawImage(video, 0, 0, 640, 480);
        var myCanvas = document.getElementById('canvas');
        var image = myCanvas.toDataURL("image/png");

        IPython.notebook.kernel.execute("image = '" + image + "'")
        //TODO Convert Image to im 
    });

    var today= new Date()
    </script>

    """
    return HTML(main_text)
    
def image_plot(image):
    # After snapping a photo in either camera or paint, input the variable name "image" to this function
    
    # Plots the image on an x-y plane
    im = Image.open(io.BytesIO(base64.b64decode(image.split(',')[1])))
    plt.imshow(im)
    return im
    
def alignment(url1 = 'http://res.cloudinary.com/miles-extranet-dev/image/upload/ar_16:9,c_fill,w_1000,g_face,q_50/Michigan/migration_photos/G21696/G21696-msubeaumonttower01.jpg',url2 = 'http://msutoday.msu.edu/_/img/assets/2013/beaumont-spring-1.jpg'):
    # The user can input the url of up to 2 pictures. There are 2 default pictures.
    
    # Here are some libraries you will need to use
    import scipy.misc as misc
    from urllib.request import urlopen
    from scipy.misc import imread, imsave
    from skimage import transform
    import matplotlib.pylab as plt
    import sympy as sp
    sp.init_printing()
    import numpy as np
    from ipywidgets import interact
    import math
    
    # Open the two input urls
    with urlopen(url1) as file1:
        im1 = imread(file1, mode='RGB')
    file1.close()
    with urlopen(url2) as file2:
        im2 = imread(file2, mode='RGB')
    file2.close()
    im = im1
    
    def affine_image(Rotation=0,Size=1,x=0,y=0, Fade=1):
        # This function allows users to shift images horizontally and vertically, 
        # change the image size, rotate images, and fade one image into the other
        theta = -Rotation/180  * math.pi
        dx = x*im.shape[1]
        dy = y*im.shape[0]
        S = np.matrix([[1/Size,0,0], [0,1/Size,0], [0,0,1]])
        T2 = np.matrix([[1,0,im.shape[1]/2], [0,1,im.shape[0]/2], [0,0,1]])
        T1 = np.matrix([[1,0,-im.shape[1]/2-dx], [0,1,-im.shape[0]/2-dy], [0,0,1]])
        R = np.matrix([[math.cos(theta),-math.sin(theta),0],[math.sin(theta), math.cos(theta),0],[0,0,1]])
        img = transform.warp(im, T2*S*R*T1);
        # The function displays both the images overlapped on one x-y plane
        plt.imshow(im2);
        plt.imshow(img, alpha=Fade);
        plt.show();
    # Use sliders to translate images, change image size, rotate images, or fade images into each other.
    interact(affine_image,Rotation=(-180,180),Size=(0.001,5), x=(-1.0,1.0), y=(-1,1,0.1),Fade=(0.0,1.0)); ##TODO: Modify this line of code

def points(im = 'http://msutoday.msu.edu/_/img/assets/2013/beaumont-spring-1.jpg', point_color='black',point_radius=2):
    # The user can input a url of an image (there is a default image), a point color (default is black), and point radius (default is 2).
    
    # Here are some libraries you will need to use.
    import scipy.misc as misc
    from urllib.request import urlopen
    from scipy.misc import imread, imsave
    import matplotlib.pyplot as plt
    import matplotlib.image as img
    import sys
    sys.path.append('./packages')
    import mpld3
    from mpld3 import plugins
    mpld3.enable_notebook()
    
    # This checks is the input point radius is a valid number. If not, it sets the point radius to 2.
    try:
        point_radius=float(point_radius)
    except ValueError:
        point_radius=2

    # Plots the image in the notebook
    def plot(imgname):
        fig, ax = plt.subplots()
        im = img.imread(imgname)
        plt.imshow(im, origin='lower')
        return fig

    # Function called in the notebook
    def pickpoints(fig='', radius=4, color="white", x = 'x', y = 'y'):
        if not fig:
            fig = plt.gcf()
        plugins.connect(fig, Annotate(radius, color, x, y)) # color='htmlcolorname', radius=int
        plugins.connect(fig, plugins.MousePosition())

    # Main class that contains Javascript code to create and drag circles  
    class Annotate(plugins.PluginBase):
        """A plugin that creates points in a figure by clicking the mouse"""

        JAVASCRIPT = r"""
        mpld3.register_plugin("annotate", Annotate);
        Annotate.prototype = Object.create(mpld3.Plugin.prototype);
        Annotate.prototype.constructor = Annotate;
        Annotate.prototype.requiredProps = [];
        Annotate.prototype.defaultProps = {radius: 4, color: "white", x: 'x', y: 'y'};
        function Annotate(fig, props){
            mpld3.Plugin.call(this, fig, props);
        };

        Annotate.prototype.draw = function(){

            /// NECESSARY STARTUP VARIABLES ///

            var fig = this.fig;
            var ax = fig.axes;
            var dataset = [];
            var svg = d3.select(".mpld3-figure");   // existing svg element
            var radius = this.props.radius;
            var color = this.props.color;
            var x = this.props.x;
            var y = this.props.y;
            var ax = fig.axes[0];


            /// INDEXES HTML DOC TO PULL VALUES FOR x,y CALIBRATION ///
            var xcal = this.parent.axes[0].position[0];
            var ycal = this.parent.axes[0].position[1];
            console.log('x calibration: ' + xcal);
            console.log('y calibration: ' + ycal);

            var xcommand = x+" = []";
            IPython.notebook.kernel.execute(xcommand);
            var ycommand = y+" = []";
            IPython.notebook.kernel.execute(ycommand);


            ////////// CREATE POINT COMPONENT //////////

            var update_coords = function() {

                return function() {
                    var pos = d3.mouse(this),
                        xpos = ax.x.invert(pos[0]),
                        ypos = ax.y.invert(pos[1]);

                    var newpoint = {
                        cx: pos[0] + xcal,
                        cy: pos[1] + ycal,
                        r: radius,
                        fill: color
                    };
                    dataset.push(newpoint);

                    var circles = svg.selectAll("circle")
                        .data(dataset)
                        .enter()
                        .append("circle")
                        .attr(newpoint)
                        .call(drag);

                    var xcommand = x+".append("+xpos+")";
                    IPython.notebook.kernel.execute(xcommand);
                    console.log(xcommand);
                    var ycommand = y+".append("+ypos+")";
                    IPython.notebook.kernel.execute(ycommand);
                    console.log(ycommand);

                };
            }();
            ax.baseaxes
                .on("mousedown", update_coords);



            ////////// DRAG POINT COMPONENT //////////

            var drag = d3.behavior.drag()
                .on("dragstart", dragstarted)
                .on("drag", dragged)
                .on("dragend", dragended);

            function dragstarted(d) {
                 d3.event.sourceEvent.stopPropagation();
                 d3.select(this).classed("dragging", true);
            }

            function dragged(d) {
                 d3.select(this).attr("cx", d3.event.x)
                                .attr("cy", d3.event.y);             
            }

            function dragended(d, i) {
                 d3.event.sourceEvent.stopPropagation();
                 d3.select(this).classed("dragging", false);
                 var calib_cx = d3.select(this)[0][0].cx.animVal.value - xcal;
                 var calib_cy = d3.select(this)[0][0].cy.animVal.value - ycal;
                 var xcommand = x+"["+i+"] = "+ax.x.invert(calib_cx);
                 var ycommand = y+"["+i+"] = "+ax.y.invert(calib_cy);
                 IPython.notebook.kernel.execute(xcommand);
                 IPython.notebook.kernel.execute(ycommand);
                 console.log(xcommand);
                 console.log(ycommand);
            }


        };"""

        def __init__(self, radius=4, color="white", x ='x', y ='y'):
            self.dict_ = {"type": "annotate",
                          "radius": radius,
                          "color": color,
                          "x": x,
                          "y": y};
    
    # Opens and displays the image
    if type(im) == str:
        with urlopen(im) as file:
            im2 = imread(file, mode='RGB')
        im = im2
    fig = plt.figure(figsize=(9,6))
    plt.imshow(im)
    
    # Runs the pickpoints function to allow the user to pick points on the image
    pickpoints(color=point_color, radius=point_radius, x='xcoords', y='ycoords')
    
def point_coords(xcoords,ycoords):
    # After selecting points using the points function, 
    # input the variables named "xcoords" and "ycoords" into this function to display the x and y coordinates of the points.
    
    def cleanformat(var):
        # Formats x and y lists into shorter decimals, so they're not too lengthy
        varlist = []
        if type(var) == float:
            varlist = '{:05.2f}'.format(var)
        else:
            for i in range(len(var)):
                varlist.append('{:05.2f}'.format(var[i]))
        return varlist
    
    # Prints the cleanly formatted x and y coordinates
    print('x', cleanformat(xcoords))
    print('y', cleanformat(ycoords))

def paint(filename='chameleon.jpg'):
    #The user can input an image file name (There is a default image file)
    
    # Here are some necessary imports
    import matplotlib.pyplot as plt
    from IPython.display import HTML
    import base64
    from urllib.request import urlopen
    from scipy.misc import imread, imsave
    
    # Opens, reads and encodes the input image
    image = open(filename, 'rb')
    image_read = image.read()
    image_64_encode = base64.encodestring(image_read)
    
    main_txt = """
       <h1>Canvas test</h1>
       <h4>Screenshot</h4>
       <button id="snap">Snap Photo</button>
       <h4>Utilities</h4>
       <button id="eraser">Eraser</button>
       <button id="pen">Pen</button>
       <h4>Adjust pen size</h4>
       <button id="default">Default</button>
       <button id="small">Small</button>
       <button id="medium">Medium</button>
       <button id="large">Large</button>
       <h4>Adjust pen color</h4>
       <button id="black">Black</button>
       <button id="white">White</button>
       <button id="red">Red</button>
       <button id="orange">Orange</button>
       <button id="yellow">Yellow</button>
       <button id="green">Green</button>
       <button id="blue">Blue</button>
       <button id="purple">Purple</button>
       <div id="canvasDiv" style="position:relative; width:900px; height:500px">
       <!-- It's bad practice (to me) to put your CSS here.  I'd recommend the use of a CSS file! -->
          <canvas id="canvasSignature" style="border:2px solid #000000; z-index: 2;position:absolute;left:0px;top:0px;" width="900px" height="500px"></canvas>
          <canvas id="backgroundSignature" style="border:2px solid #000000; z-index: 1;position:absolute;left:0px;top:0px;" width="900px" height="500px"></canvas>
       </div>

       <script type="text/javascript" src="https://ajax.googleapis.com/ajax/libs/jquery/1.7.1/jquery.min.js"></script>
       <script type="text/javascript">
          var bacground = \""""+filename+"""\";
          $(document).ready(function () {
             initialize(bacground);
          });

          //default settings for pen
          var sigColor = 'Black';
          var sigSize = 5;
          var erase = false;



          // works out the X, Y position of the click inside the canvas from the X, Y position on the page
          function getPosition(mouseEvent, sigCanvas) {
             var x, y;
             if (mouseEvent.pageX != undefined && mouseEvent.pageY != undefined) {
                var rect = sigCanvas.getBoundingClientRect();
                x = mouseEvent.clientX - rect.left;
                y = mouseEvent.clientY - rect.top;

             } //else {
               // x = mouseEvent.clientX;// + document.body.scrollLeft + document.documentElement.scrollLeft;
               // y = mouseEvent.clientY;// + document.body.scrollTop + document.documentElement.scrollTop;
             //}
             //return { X: x - sigCanvas.offsetLeft, Y: y - sigCanvas.offsetTop };
             return {X: x, Y: y};
          }


          function initialize(bacground) {
             // get references to the canvas element as well as the 2D drawing context
             // Two canvases are initialized:
             // sigCanvas = canvasSignature = image drawn by user
             // backgroundCanvas = backgroundSignature = background image to draw over
             var sigCanvas = document.getElementById("canvasSignature");
             var backgroundCanvas = document.getElementById("backgroundSignature");
             var context = sigCanvas.getContext("2d");
             var contexted = backgroundCanvas.getContext("2d");

             //context.strokeStyle = 'Blue';
             //context.lineWidth = 5;

             //draws certain image onto canvas
             makeBase(bacground);

             function makeBase(bacground)
             {
               base_image = new Image();
               base_image.src = bacground;
               base_image.onload = function(){
                 //draw image over the background canvas
                 contexted.drawImage(base_image, 0, 0, 900, 500);
               }
             } 



             // This will be defined on a TOUCH device such as iPad or Android, etc.
             var is_touch_device = 'ontouchstart' in document.documentElement;

             if (is_touch_device) {
                // create a drawer which tracks touch movements
                var drawer = {
                   isDrawing: false,
                   touchstart: function (coors) {
                      context.beginPath();
                      context.moveTo(coors.x, coors.y);
                      this.isDrawing = true;
                   },
                   touchmove: function (coors) {
                      if (this.isDrawing) {
                         context.lineTo(coors.x, coors.y);
                         context.stroke();
                      }
                   },
                   touchend: function (coors) {
                      if (this.isDrawing) {
                         this.touchmove(coors);
                         this.isDrawing = false;
                      }
                   }
                };

                // create a function to pass touch events and coordinates to drawer
                function draw(event, sigColor, sigSize) {

                   // get the touch coordinates.  Using the first touch in case of multi-touch
                   var coors = {
                      x: event.targetTouches[0].pageX,
                      y: event.targetTouches[0].pageY
                   };

                   // Now we need to get the offset of the canvas location
                   var obj = sigCanvas;

                   if (obj.offsetParent) {
                      // Every time we find a new object, we add its offsetLeft and offsetTop to curleft and curtop.
                      do {
                         coors.x -= obj.offsetLeft;
                         coors.y -= obj.offsetTop;
                      }
                      // The while loop can be "while (obj = obj.offsetParent)" only, which does return null
                      // when null is passed back, but that creates a warning in some editors (i.e. VS2010).
                      while ((obj = obj.offsetParent) != null);
                   }

                   // pass the coordinates to the appropriate handler
                   drawer[event.type](coors);
                }


                // attach the touchstart, touchmove, touchend event listeners.
                sigCanvas.addEventListener('touchstart', draw, false);
                sigCanvas.addEventListener('touchmove', draw, false);
                sigCanvas.addEventListener('touchend', draw, false);

                // prevent elastic scrolling
                sigCanvas.addEventListener('touchmove', function (event) {
                   event.preventDefault();
                }, false); 
             }
             else {

                // start drawing when the mousedown event fires, and attach handlers to
                // draw a line to wherever the mouse moves to
                $("#canvasSignature").mousedown(function (mouseEvent) {
                   var position = getPosition(mouseEvent, sigCanvas);

                   context.moveTo(position.X, position.Y);
                   context.beginPath();

                   // attach event handlers
                   $(this).mousemove(function (mouseEvent) {
                      drawLine(mouseEvent, sigCanvas, context, sigColor, sigSize);
                   }).mouseup(function (mouseEvent) {
                      finishDrawing(mouseEvent, sigCanvas, context, sigColor, sigSize);
                   }).mouseout(function (mouseEvent) {
                      finishDrawing(mouseEvent, sigCanvas, context, sigColor, sigSize);
                   });
                });

             }
          }


          // draws a line to the x and y coordinates of the mouse event inside
          // the specified element using the specified context
          function drawLine(mouseEvent, sigCanvas, context, sigColor, sigSize) {

             var position = getPosition(mouseEvent, sigCanvas);
             context.lineTo(position.X, position.Y);
             context.strokeStyle = sigColor;
             context.lineWidth = sigSize;
             if (erase == true){
                 context.globalCompositeOperation="destination-out";
             }
             else{
                 context.globalCompositeOperation="source-over";
             }
             context.stroke();
          }

          // draws a line from the last coordiantes in the path to the finishing
          // coordinates and unbind any event handlers which need to be preceded
          // by the mouse down event
          function finishDrawing(mouseEvent, sigCanvas, context, sigColor, sigSize) {
             // draw the line to the finishing coordinates
             drawLine(mouseEvent, sigCanvas, context, sigColor, sigSize);

             context.closePath();

             // unbind any events which could draw
             $(sigCanvas).unbind("mousemove")
                         .unbind("mouseup")
                         .unbind("mouseout");
          }

    document.getElementById("default").addEventListener("click", function() {
         sigSize = 5;
    });

    document.getElementById("small").addEventListener("click", function() {
         sigSize = 2;
    });

    document.getElementById("medium").addEventListener("click", function() {
         sigSize = 10;
    });

    document.getElementById("large").addEventListener("click", function() {
         sigSize = 20;
    });

    document.getElementById("black").addEventListener("click", function() {
         sigColor = 'Black';
    });

    document.getElementById("white").addEventListener("click", function() {
         sigColor = 'White';
    });

    document.getElementById("red").addEventListener("click", function() {
         sigColor = 'Red';
    });

    document.getElementById("orange").addEventListener("click", function() {
         sigColor = 'Orange';
    });

    document.getElementById("yellow").addEventListener("click", function() {
        sigColor = 'Yellow';
    });

    document.getElementById("green").addEventListener("click", function() {
         sigColor = 'Green';
    });

    document.getElementById("blue").addEventListener("click", function() {
         sigColor = 'Blue';
    });

    document.getElementById("purple").addEventListener("click", function() {
         sigColor = 'Purple';
    });

    document.getElementById("purple").addEventListener("click", function() {
         sigColor = 'Purple';
    });

    document.getElementById("eraser").addEventListener("click", function() {
         erase = true;
         //sigColor = '#ffffff';
    });
    document.getElementById("pen").addEventListener("click", function() {
         erase = false;
    });



    // Trigger photo take
    document.getElementById("snap").addEventListener("click", function() {
        //context.drawImage(video, 0, 0, 320, 240);
        var myCanvas = document.getElementById('canvasSignature');
        var image = myCanvas.toDataURL("image/png");
        IPython.notebook.kernel.execute("print('testing')")
        IPython.notebook.kernel.execute("image = '" + image + "'")

    });

       </script>

    """
    return HTML(main_txt)

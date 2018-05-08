#!/usr/bin/env python

from gimpfu import * 

def normal_map(img, layer, strength) :
    ''' Converts a layer to gray scale, without modifying his type (RGB or RGBA).
    Note that this implementation is very inefficient, since it do not make use 
    of tiles or pixel regions. 
    
    Parameters:
    img : image The current image.
    layer : layer The layer of the image that is selected.
    '''
    # Indicates that the process has started.
    gimp.progress_init("Discolouring " + layer.name + "...")

    # Set up an undo group, so the operation will be undone in one step.
    pdb.gimp_image_undo_group_start(img)

    grayscale = pdb.gimp_layer_copy(layer, TRUE)
    grayscale.name = "grayscale"
    pdb.gimp_image_add_layer(img, grayscale, -1)

    # Iterate over all the pixels and convert them to gray.
    for x in range(grayscale.width):
        # Update the progress bar.
        gimp.progress_update(float(x) / float(grayscale.width))

        for y in range(grayscale.height):
            # Get the pixel and verify that is an RGB value.
            pixel = grayscale.get_pixel(x,y)
        
            if(len(pixel) >= 3):
                # Calculate his gray tone.
                sum = pixel[0] + pixel[1] + pixel[2]
                gray = int(sum/3)
            
                # Create a new tuple representing the new color.
                newColor = (gray,gray,gray) + pixel[3:]
                grayscale.set_pixel(x,y, newColor)

    grayscale.update(0, 0, grayscale.width, grayscale.height)
    
     # End progress.
    pdb.gimp_progress_end()

    # Indicates that the process has started.
    gimp.progress_init("Creating Normal map of " + layer.name + "...")

    normal = pdb.gimp_layer_copy(grayscale, TRUE)
    normal.name = "normal map"
    pdb.gimp_image_add_layer(img, normal, -1)

    #strength = 0.5

    pdb.gimp_layer_resize (grayscale,grayscale.width+2,grayscale.height+2,1,1)

    for x in range (0,normal.width):
        gimp.progress_update(float(x) / float(normal.width))
        
        for y in range (0,normal.height):

            xLeft = grayscale.get_pixel(x,y+1)
            xRight = grayscale.get_pixel(x+2,y+1)
            yUp = grayscale.get_pixel(x+1,y)
            yDown = grayscale.get_pixel(x+1,y+2)
            xDelta = ((xLeft[0]*strength-xRight[0]*strength)+255)*0.5
            yDelta = ((yUp[0]*strength-yDown[0]*strength)+255)*0.5
            newColor = [int(xDelta),int(yDelta),255,255]
            normal.set_pixel(x,y,newColor)
    
    # Update the layer.
    normal.update(0, 0, normal.width, normal.height)
    normal.name = "old normal map"
    grayscale.name = "normal map"
    pdb.gimp_image_merge_down(img, normal, EXPAND_AS_NECESSARY)
    

    # Close the undo group.
    pdb.gimp_image_undo_group_end(img)
    
    # End progress.
    pdb.gimp_progress_end()

register(
    "python_fu_normal_map",
    "Normal map",
    "Converts a layer to gray scale and makes normal map",
    "Aleksandra Ujfalusi, Aleksandra Haska, Milica Lazor",
    "Aleksandra Ujfalusi, Aleksandra Haska, Milica Lazor",
    "2018",
    "<Image>/Test/Normal map",
    "RGB, RGB*",
    [
        (PF_SLIDER, "strength", "Strength", 0.5, (0,1, 0.05))
    ],
    [],
    normal_map)

main()

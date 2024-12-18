## Using BigVolumeViewer

By selecting a **B** checkbox in the Sources panel, you can view the 3D dataset in the BigVolumeViewer (BVV) window.  
<img width="400" alt="image" src="./tutorial_images/bvv/sources_buttons_bvv.png">  

BVV navigation controls (rotation, zoom, etc) are [the same as in BigDataViewer](./explore_a_project.html#browsing).  

It supports two rendering modes: Maximum Intensity projection and Volumetric (transclucent/alpha blending), see an example below.  
You can toggle between them using keyboard shortcut **`O`** (letter, not a number).  

<img width="800" alt="comparison of rendering modes, left=max, right=volumetric" src="./tutorial_images/bvv/bvv_render_style.png">

You can synchronize the dataset view (and timepoint) with the BigDataViewer window view using shortcut **`D`**.  

Compared with 3DViewer volume rendering using a fixed resolution, BVV works directly with the raw data. It loads corresponding multi-resolution data levels depending on the current view.  

For the 3D volume rendering substantially more data is required to be loaded and processed, therefore for a smoother experience in displaying remote dataset it is recommended to use high-speed network connections.   
As with all 3D applications, a better GPU card with large amount of GPU memory is recommended. You can adjust the amount of dedicated GPU memory and tweak quality/performance using BVV setting command explained below. 

### Adjusting color(LUT), brightness and opacity

As with BigDataViewer, you can configure the appearance of each source in BVV using shortcut **`S`** (also in the Cards Panel, activated by a shortcut **`P`**).    
The square on the left shows a color that is used to display the volume.  
You can change it using left click. Or you can apply Fiji installed LUT using right-click.  
<img width="500" alt="LUT selection example" src="./tutorial_images/bvv/bvv_lut_selection.gif">   
The top slider maps minimum and maximum shade of selected source color (or min and max of LUT) to the selected data range (like a standard Fiji's "brightness" dialog).  
Upon loading a source to BVV, its contrast and range will be taken from the current BDV source settings.  
There are additional source display setting, which you can expand by clicking on "three triangles" bar:  
<img width="490" alt="expand settings" src="./tutorial_images/bvv/bvv_expand_brightness.gif">  
The second slider from the top (marked as **γ**) adjusts non-linear color/LUT mapping by introducing gamma correction (a power-law). Overall color/LUT adjustments can be illustrated using an example below.  
<img width="490" alt="expand settings" src="./tutorial_images/bvv/bvv_lutrange.gif">  
Here we have a box volume, where intensities are increasing from 0 to 255, left-to-right slices. Intensity values are colored using ImageJ's periodic "3-3-2" LUT shown in the color bar. Changing min max range values of the top slider maps the range of LUT application with respect to the data (voxel values) range. Changing gamma slider introduces non-linear mapping. 




### BigVolumeViewer settings

To change BVV settings, right click on the BigDataViewer window and select "Configure BigVolumeViewer Rendering".  
Short parameters description (and [a bit longer](https://forum.image.sc/t/bigvolumeviewer-tech-demo/12104), if interested) :  

- **Render width and height** - the true quality of 3D rendering performed by GPU and stretched to the current window size. Increasing them makes better picture at the expense of higher computational load;
- **Dither window size** and **number of dither samples**. Interpolating nearby pixels (withing the window) instead of sampling the volume. Increasing these values will speed up rendering at the expense of quality;
- **GPU cache tile size** size of the 3D blocks (in pixels) that are loaded to GPU;
- **GPU cache size (in MB)** limits the storage of the data in GPU memory. Increasing this parameter speeds up data display (should be less than your available GPU memory).
- **Camera distance**, **Clip distance far/near** parameters define [viewing frustum](https://en.wikipedia.org/wiki/Viewing_frustum) of the perspective virtual camera. See a picture below to get an idea. "Camera distance" should be always larger than "clip distance near". If you want to get "BDV slice" view, you can set "clip distance near" to zero.   
<img width="600" alt="camera frustum illustration" src="./tutorial_images/bvv/bvv_frustum.png">

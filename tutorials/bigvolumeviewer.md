## Using BigVolumeViewer

By selecting a **B** checkbox in the Sources panel, you can view the 3D dataset in the BigVolumeViewer (BVV) window.  
<img width="400" alt="image" src="./tutorial_images/sources_buttons.png">  

BVV navigation controls (rotation, zoom, etc) are [the same as in BigDataViewer](./explore_a_project.html#browsing).  

It supports two rendering modes: Maximum Intensity projection and Volumetric (transclucent/alpha blending), see an example below.  
You can toggle between them using keyboard shortcut <kbd>O</kbd> (letter, not a number).  

<img width="800" alt="comparison of rendering modes, left=max, right=volumetric" src="./tutorial_images/bvv/bvv_render_style.png">

You can synchronize the dataset view (and timepoint) with the BigDataViewer window view using shortcut <kbd>D</kbd>.  

Compared with 3DViewer volume rendering using a fixed resolution, BVV works directly with the raw data. It loads corresponding multi-resolution data levels depending on the current view.  

For the 3D volume rendering substantially more data is required to be loaded and processed, therefore for a smoother experience in displaying remote dataset it is recommended to use high-speed network connections.   
As with all 3D applications, a better GPU card with large amount of GPU memory is recommended. You can adjust the amount of dedicated GPU memory and tweak quality/performance using BVV setting command explained below. 

### Adjusting brightness, contrast and opacity

As with BigDataViewer, you can configure the appearance of each source in BVV using shortcut <kbd>S</kbd> (also in the Cards Panel, activated by a shortcut <kbd>P</kbd>).   
Upon loading a source to BVV, its contrast and range will be taken from the current BDV source settings.   
The square on the left shows a color that is used to display the volume.  
You can change it using left click. Or you can apply Fiji installed LUT using right-click.  
<img alt="LUT selection example" src="./tutorial_images/bvv/bvv_lut_selection.gif">   




### BigVolumeViewer settings

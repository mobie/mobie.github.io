## Using BigVolumeViewer

By selecting a **B** checkbox in the Sources panel, you can view the 3D dataset in the BigVolumeViewer (BVV) window.  
<img width="400" alt="image" src="./tutorial_images/sources_buttons.png">  

BVV navigation controls (rotation, zoom, etc) are [the same as in BigDataViewer](./explore_a_project.html#browsing).  

It supports two rendering modes: Maximum Intensity projection and Volumetric (transclucent/alpha blending), see an example below.  
You can toggle between them using keyboard shortcut **`O`** (letter, not a number).  

<img width="800" alt="image" src="./tutorial_images/bvv/bvv_render_style.png">

You can synchronize the dataset view (and timepoint) with the BigDataViewer window view using shortcut **`D`**.  

Compared with 3DViewer volume rendering using a fixed resolution, BVV works directly with the raw data. It loads corresponding multi-resolution data levels depending on the current view.  

For the 3D volume rendering substantially more data is required to be loaded and processed, therefore for a smoother experience in displaying remote dataset it is recommended to use high-speed network connections.   
As with all 3D applications, a better GPU card with large amount of GPU memory is recommended. You can adjust the amount of dedicated GPU memory and tweak quality/performance using BVV setting command explained below. 

### Adjusting brightness, contrast and opacity

#### BigVolumeViewer settings

# More Features

- Transformations
-

## Screenshots

To take a screenshot of the MoBIE viewer, right click inside it and select **Take Screenshot**.

This will open the following menu:

<img width="400" alt="image" src="./tutorial_images/screenshot_ui.png">

- **Sampling** - Sampling of screenshot (uses same units as viewer, see the viewer scalebar).
- **Show RGB Image** - create an RGB image of the viewer.
- **Show Multi-Channel Image** - create a multi-channel image, where each image shown in the viewer becomes
a separate channel.

The screenshots produced will be opened as normal ImageJ images that you can save / analyse however
you want.

As an example, take this setup from the Platyneris project:

<img width="600" alt="image" src="./tutorial_images/screenshot-mobie.png">

Here the raw EM data is shown, as well as 2 images showing the expression pattern of
two genes (in green and pink).

Taking a screenshot with **Show RGB Image** checked gives:

<img width="400" alt="image" src="./tutorial_images/screenshot_rgb.png">

and with **Show Multi-Channel Image** checked, gives a multi-channel image with the
following 3 channels:

raw | ache | allcr1
---|---|---
<img width="300" alt="image" src="./tutorial_images/screenshot_channel_1.png">  |  <img width="300" alt="image" src="./tutorial_images/screenshot_channel_2.png"> | <img width="300" alt="image" src="./tutorial_images/screenshot_channel_3.png">

## Show Raw images

You can also export the raw data shown in MoBIE at various resolution levels.
To do so, right click in the MoBIE viewer and select **Show Raw Image(s)**

This will open a window like below for each image shown:

<img width="250" alt="image" src="./tutorial_images/show_raw.png">

Here you can select which resolution level to export. In this dropdown, the pixel dimensions
of every resolution level are shown. For example, in the above image the selected resolution level
is an image of 27499 x 25916 x 11416 pixels.

Make sure you select a resolution level that your computer can handle! For example,
if your working on a laptop without much memory then you should select a lower resolution level with
an image of smaller total size.

All exported images will be opened as normal imageJ images that you can save / analyse however
you want.

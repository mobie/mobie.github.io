# Views and locations

## Locations

The viewer (BigDataViewer) places all images within the same physical coordinate system.
The current coordinates of your mouse are displayed in the top right corner of the window.

### Saving a location / orientation

To save your current location and orientation, you can right click in the viewer and select
**Log Current View**

<img width="600" alt="image" src="./tutorial_images/logLocation.png">

This will print a series of values to the **Log window** like so:
```
# Current view
To restore the view, any of below lines can be pasted into the 'location' text field.
To share views with other people we recommend 'normalizedAffine'.
{"position":[147.8058920398392,127.96038933601736,142.7000000000002],"timepoint":0}
{"affineTransform":[2.4773774193548403,0.0,0.0,-62.17097938709691,0.0,2.4773774193548403,0.0,-48.00617911290328,0.0,0.0,2.4773774193548403,-353.52175774193614],"timepoint":0}
{"normalizedAffine":[0.004074633913412566,0.0,0.0,-0.6022549003077251,0.0,0.004074633913412566,0.0,-0.521391741962012,0.0,0.0,0.004074633913412566,-0.5814502594439739],"timepoint":0}
{"normalVector":[0.0,0.0,1.0],"timepoint":0}
```

- **position** Location (x, y, z) in physical coordinates e.g. for the
Platybrowser dataset, this is in micrometer
- **affineTransform** Orientation of the viewer - the 12 comma separated values
here, are the affine transformation of this current view
- **normalizedAffine** Orientation of the viewer, normalised to window size.
- **normalVector** The normal vector to the plane you are currently viewing.

### Moving to a location / orientation

To move to a position, you simply copy one of these printed lines into the **location** field and click **move**.

- **position** Using the (x, y, z) position will move your viewer to that
location, but not change its current orientation
- **affineTransform**  Using this affine transform, will move your viewer to
that location, and change the orientation to match. **Note:**
This is dependent on the size of your viewer window i.e. if your window is not
the same size as when you saved the location, the result will be different.
- **normalizedAffine** Using the 12 normalised values, will move your viewer to
that location, and change the orientation to match. It is normalised to the
size of your viewer window, and so should give very similar results independent
of your current window size.
- **normalVector** Using this vector, will change the orientation of your viewer
to a plane with a normal parallel to this. It will not change the position of
the viewer, only its orientation.

In general, we recommend using **position** (if you don't care about
orientation), or **normalizedAffine** (if you do).

## Views

Views are a way to save the current setup of your viewer, so anyone can browse
to it quickly and easily. Selecting a view will take you to the exact location
and orientation saved, with the same images added to the viewer, and the same
tables, plots and colour scheme.

To access a view, simply select it's name from the MoBIE dropdown menus and
select 'view'.  Only a subset of views are shown in this dropdown by default.
If the project contains more, you can view them by right clicking
in the mobie viewer and selecting **Load Additional Views**, and then Load from
**Project**.

<img width="600" alt="image" src="./tutorial_images/loadAdditionalViews.png">

You can also load your own views from the file system. To create your own
views, see the **Creating your own views** tutorial [here](./creating_your_own_views.md).

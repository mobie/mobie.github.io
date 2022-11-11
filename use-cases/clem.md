# Correlative light and electron microscopy

A correlative light and electron microscopy (**CLEM**) project combines imaging data from both modalities to benefit from the dynamic and specific localization of labeled entities (Fluorescence Microscopy, **FM**) and the high  resolution
structural and contextual information (Electron Microscopy, **EM**).

## Data & project set-up

The data for this project comes from two different experiments (one using _S. cerevisiae_, one using a HeLa cell line) that are available as different [datasets](../specs/template_dataset.md).
It contains 2D FM images to target features of interest and EM data in both 2D (overview maps) and 3D (reconstructed electron tomographic volumes at different resolutions).

The original data in various formats (`MRC`, `TIF`, etc.) was converted to the MoBIE data format using the [MoBIE python library](https://github.com/mobie/mobie-utils-python).
Initial registrations were imported using the metadata from [SerialEM]() and [ec-CLEM]() software and the refined using MoBIE's transformation functionality.

## Exploring the project

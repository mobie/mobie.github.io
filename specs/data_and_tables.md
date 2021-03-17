# MoBIE image data, metadata and table specification

## Image data

Image data is stored in a multi-dimensionl, chunked data format.
MoBIE primarily supports the [n5](https://github.com/saalfeldlab/n5) data format, using the [bdv n5 format](https://github.com/bigdataviewer/bigdataviewer-core/blob/master/BDV%20N5%20format.md) to represent timepoints and multi-scale image pyramids.
In addition, MoBIE supports [HDF5](), again using the [bdv hdf5 format](TODO link); however this format can only be read locally and **does not** support remote access from an object store.
There is also experimental support for the emerging [ome ngff](https://ngff.openmicroscopy.org/latest/).

## Table data

MoBIE supports two kinds of tables:

The label id `0` is reseved for background and should not be listed in the table.

## Metadata

### Source Metadata

Specification for an entry in `sources.json`
- `storage`:
    - `remote`:
    - `local`:
- `type`:
- `menuItem`:
- `tableFolder`:
- `view`:

```json
{
}
```

### View Metadata

**displayGroups:**

- `imageDisplayGroup`
    - `color`
    - `contrastLimits`
    - `name`
    - `sources`
    - `timepoint`
- `maskDisplayGroup`
    - TODO how is this different from image?
- `segmentationDisplayGroup`
    - `alpha`
    - `color` (incl. multi-color LUTs such as "Glasbey")
    - `colorByColumn`
    - `selectedLabelIds`
    - `showSelectedSegmentsIn3d`
    - `name`
    - `sources`
    - `tables` (currently only additional tables, to be added to the default table)
    - `timepoint`

```json
```

**transformGroups:**

- `affine`
    - `name`
    - `parameters`
    - `sources`
    - `timepoint`
- `autoGrid`
    - `name`
    - `sources`
    - `timepoint`

```json
```

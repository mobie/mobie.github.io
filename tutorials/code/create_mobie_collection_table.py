import os
import pandas as pd


def normalize_mobie_table_entry_dict(entries, use_abs_path=False, table_filepath=None):

    def _normalize_uri(uri):
        if use_abs_path:
            uri = os.path.abspath(uri)
        else:
            assert table_filepath is not None
            uri = os.path.relpath(uri, os.path.split(table_filepath)[0])
        return uri

    def _normalize_affine(affine):
        return ','.join([str(x) for x in affine])

    def _normalize_exclusive(exclusive):
        if type(exclusive) is not str:
            return 'true' if exclusive else 'false'
        return exclusive

    def _normalize_contrast_limits(contrast_limits):
        return ','.join(f'{x:.1f}' if isinstance(x, int) or x == int(x) else str(x) for x in contrast_limits)

    # Let's make sure everything is a list!
    for k, v in entries.items():
        assert type(v) == list, 'Entries have to be given as as list even if only one element is added!'

    # First pass to determine the number of entries or check that the length of the arrays matches the given entry count
    entry_count = max([len(v) for _, v in entries.items()])

    for k, v in entries.items():

        assert len(v) == entry_count or len(v) == 1, 'The number of elements in an entry must match the entry count or be of len = 1'
        if len(v) == 1:
            entries[k] = v * entry_count

    # Now we can make sure that everything is properly readable by MoBIE
    for k, v in entries.items():

        for idx, item in enumerate(v):
            if k == 'uri':
                v[idx] = _normalize_uri(item)
            elif k == 'name':
                pass
            elif k == 'type':
                pass
            elif k == 'view':
                pass
            elif k == 'group':
                pass
            elif k == 'affine':
                v[idx] = _normalize_affine(item)
            elif k == 'blend':
                pass
            elif k == 'exclusive':
                v[idx] = _normalize_exclusive(item)
            elif k == 'contrast_limits':
                v[idx] = _normalize_contrast_limits(item)
            else:
                pass

        entries[k] = v

    return entries


# Inputs are automatically obtained from microscope project metadata
map_filepaths = ['path/to/image1.tif', 'path/to/image2.tif']
affine_transforms = [[1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0], [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0]]  # Scaling is done from image meta data and not from here!
names = ['Image1', 'Image1']
contrast_limits = [[10, 230], [50, 255]]
view_name = 'View1'
group_name = 'Group1'

# Set up a dictionary that contains all entries
entries=dict(
    uri=map_filepaths,
    type=['intensities'],
    view=[view_name],
    group=[group_name],
    affine=affine_transforms,
    name=names,
    blend=['alpha'],
    exclusive=[True],
    contrast_limits=contrast_limits
)

# Translate the dictionary entries into a MoBIE-readable format, e.g. concatenating the affine transform to a single string
entries = normalize_mobie_table_entry_dict(entries, use_abs_path=True)

# Where to save the resulting table
table_filepath = 'test_mobie_table.tsv'

# Create the table
new_table_data = pd.DataFrame(entries)
new_table_data.to_csv(table_filepath, index=False, sep='\t')

# # Append the table (Use this instead of the above if you need to add to an existing table)
# table_data = pd.DataFrame()
# if os.path.exists(table_filepath):
#     table_data = pd.read_csv(table_filepath, sep='\t')
# new_table_data = pd.concat([table_data, pd.DataFrame(entries)], ignore_index=True, sort=False)
# new_table_data = new_table_data.fillna('')
# new_table_data.to_csv(table_filepath, index=False, sep='\t')



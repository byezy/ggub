from os.path import join


def morph_filename(filename, out_path="", prefix="", suffix="", replacements=[(".", "_")], ext=""):
    morphed = filename
    for find, replace in replacements:
        morphed = morphed.replace(find, replace)
    return join(out_path, prefix + morphed + suffix + ext)


# v = gd['vectors'].copy()
# # v.drop('vector', axis=1, inplace=True)
# v.rename(columns={'fullpath': 'in_vector'}, inplace=True)
# v['out_raster'] = v['filename'].apply(lambda x: join(out_folder, f'{x}.tif'))
# gui.pretty_df(v)


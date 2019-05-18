from os.path import join

v = gd['vectors'].copy()
# v.drop('vector', axis=1, inplace=True)
v.rename(columns={'fullpath': 'in_vector'}, inplace=True)
v['out_raster'] = v['filename'].apply(lambda x: join(out_folder, f'{x}.tif'))
gui.pretty_df(v)


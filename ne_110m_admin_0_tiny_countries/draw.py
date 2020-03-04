import geopandas as gpd 

shapefile = './ne_110m_admin_0_tiny_countries.shp'

f = gpd.read_file(shapefile)[['ADMIN', 'ADM0_A3', 'geometry']]
f.columns = ['country', 'country_code', 'geometry']

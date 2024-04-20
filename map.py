import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
import model


def create_map(data):

    berlin_neighbourhoods_df = gpd.read_file("./DataSet/neighbourhoods.geojson")
    berlin_neighbourhoods_df = berlin_neighbourhoods_df[~berlin_neighbourhoods_df['neighbourhood_group'].isnull()]

    plz_shape_df = gpd.read_file('./DataSet/plz-5stellig.shp.zip', dtype={'plz': str})
    plz_shape_df = plz_shape_df[(10789 <= plz_shape_df["plz"].astype(int)) & (plz_shape_df["plz"].astype(int) <= 12307)]
    plz_region_df = pd.read_csv(
        './DataSet/zuordnung_plz_ort.csv', 
        sep=',', 
        dtype={'plz': str}
    )

    plz_region_df.drop('osm_id', axis=1, inplace=True)
    plz_region_df = plz_region_df[(10789 <= plz_region_df["plz"].astype(int)) & (plz_region_df["plz"].astype(int) <= 12307)]
    berlin_df = pd.merge(
        left=plz_shape_df, 
        right=plz_region_df, 
        on='plz',
        how='inner'
    )

    berlin_df.drop(['note'], axis=1, inplace=True)

    probabilities = model.get_percentage(data)

    cmap = plt.colormaps.get_cmap("coolwarm")
    min_prob=min(probabilities.values())
    max_prob=max(probabilities.values())
    norm = Normalize(vmin=min_prob,vmax=max_prob)
    fig, ax = plt.subplots()
    ax.tick_params(left=False, bottom=False)
    ax.set_xticklabels([]) 
    ax.set_yticklabels([])
    berlin_df.plot(ax=ax, alpha=0.2)

    for _, row in berlin_neighbourhoods_df.iterrows():
        neighborhood_name = row['neighbourhood_group']  
        neighborhood_polygon = row['geometry']  

        probability = probabilities.get(neighborhood_name, 0.5)  # Default to 0.5 if no probability is specified

        color = cmap(norm(probability))
        
        berlin_neighbourhoods_df[berlin_neighbourhoods_df['neighbourhood_group'] == neighborhood_name].plot(
            ax=ax,
            color=color,
            edgecolor='black'
        )

    sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
    sm.set_array([])  # Required for matplotlib 3.1 and later
    cbar = plt.colorbar(sm, ax=ax, label='Probability')

    ax.set(title='Accident Probability by District', aspect=1.3)

    plt.savefig("./Images/Map.jpg")
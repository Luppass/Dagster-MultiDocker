from dagster import AssetSelection, define_asset_job
from ..partitions import monthly_partition, weekly_partition

# si fuese un asset creado con @asset, pondremos
# aqf_asset_selection = AssetSelection.keys("aqf_load_data_ticker")

# los notebooks como no son assets, van en grupos
aqf_asset_selection = AssetSelection.groups("Notebooks")


notebook_job = define_asset_job(
    name="notebook_job",
    selection=aqf_asset_selection
)
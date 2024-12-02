from dagster import file_relative_path, asset, AssetIn, MetadataValue
from dagstermill import define_dagstermill_asset
import pandas as pd
import ssl
ssl._create_default_https_context = ssl._create_unverified_context ## Error certs con Pandas al hacer un request con HTTPS


dagstermill_notebook = define_dagstermill_asset(
    name = "dagstermill_notebook",
    notebook_path = file_relative_path(__file__,"../notebooks/hola.ipynb"),
    group_name = "Notebooks",
    io_manager_key="output_notebook_io_manager",
    ins={"test": AssetIn("asset_test")},
)


test2 = define_dagstermill_asset(
    name = "test2",
    notebook_path = file_relative_path(__file__,"../notebooks/hola2.ipynb"),
    group_name = "Notebooks",
    io_manager_key="output_notebook_io_manager",
)

@asset(group_name="Notebooks")
def asset_test():
    return pd.read_csv(
        "https://archive.ics.uci.edu/ml/machine-learning-databases/iris/iris.data",
        names=[
            "Sepal length (cm)",
            "Sepal width (cm)",
            "Petal length (cm)",
            "Petal width (cm)",
            "Species",
        ],
    )
    
    

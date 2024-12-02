from dagster import FilesystemIOManager, graph, op, schedule, Definitions
from dagster_docker import docker_executor # type: ignore
from dagstermill import ConfigurableLocalOutputNotebookIOManager
import importlib
import assets.assets_notebook

# Recargar el módulo en tiempo de ejecución
importlib.reload(assets.assets_notebook)

# Vuelve a obtener los assets actualizados
from assets.assets_notebook import asset_test, dagstermill_notebook, test2


@op
def hello():
    return 1

@op
def goodbye(foo):
    if foo != 1:
        raise Exception("Bad io manager")
    return foo * 2

@graph
def my_graph():
    goodbye(hello())


my_job = my_graph.to_job(name="my_job")

my_step_isolated_job = my_graph.to_job(
    name="my_step_isolated_job",
    executor_def=docker_executor,
    resource_defs={"io_manager": FilesystemIOManager(base_dir="/tmp/io_manager_storage")},
)


@schedule(cron_schedule="* * * * *", job=my_job, execution_timezone="US/Central")
def my_schedule(_context):
    return {}


defs = Definitions(
    assets=[asset_test, dagstermill_notebook, test2],  # Assets definidos en assets.assets_notebook
    jobs=[my_job, my_step_isolated_job],  # Jobs definidos
    schedules=[my_schedule],  # Schedule definido
    resources={
        "io_manager": FilesystemIOManager(base_dir="/tmp/io_manager_storage"), 
        "output_notebook_io_manager": ConfigurableLocalOutputNotebookIOManager(base_dir="/opt/dagster/app/notebooks-output")
    },
)
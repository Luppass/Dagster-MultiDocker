from dagster import IOManager, io_manager, OutputContext, InputContext
import os
import json


## No está en uso -> ¿Desarrollo?
class NotebookIOManager(IOManager):
    def __init__(self, base_dir):
        self.base_dir = base_dir

    def _get_path(self, context):
        # Genera el nombre del archivo con la extensión .ipynb
        return os.path.join(
            self.base_dir, f"{context.step_key}_{context.name}.ipynb"
        )

    def handle_output(self, context: OutputContext, obj):
        # Guarda el objeto (notebook) en el archivo con extensión .ipynb
        path = self._get_path(context)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(obj, f)

    def load_input(self, context: InputContext):
        # Carga el objeto (notebook) desde el archivo con extensión .ipynb
        path = self._get_path(context.upstream_output)
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

@io_manager
def notebook_io_manager(init_context):
    base_dir = "/opt/dagster/notebook-outputs"
    return NotebookIOManager(base_dir=base_dir)
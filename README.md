# Dagster-MultiDocker  
Implementación de **Dagster** con **Docker Compose**.

## Introducción  
Este repositorio contiene una configuración básica para desplegar **Dagster** utilizando Docker Compose. Permite una gestión modular de las definiciones y facilita la escalabilidad de los componentes del sistema.

---

## Gestión de Definiciones en Dagster  

### Problema Detectado (27/11/2024)  
Se ha identificado un problema con la recarga de definiciones en el servidor web de Dagster:  
- **Síntoma**: Al realizar cambios en los objetos (por ejemplo, añadir nuevos *assets* o modificar *jobs*), dichos cambios no se reflejan correctamente dando lugar a fallos de "keys" al intentar materializar dichos activos.  
- **Solución Temporal**: Es necesario reiniciar completamente el contenedor que actúa como repositorio de código.

### Solución Paso a Paso  
Ejecuta los siguientes comandos para reiniciar y reconstruir el contenedor afectado:  

```bash
docker-compose stop dagster_user_code && docker-compose rm -f dagster_user_code && docker-compose build --no-cache dagster_user_code && docker-compose up -d dagster_user_code


import os
from dagster import ConfigurableIOManager, MetadataValue, InputContext, OutputContext
import nbformat

class MyNotebookIOManager(ConfigurableIOManager):
    base_dir: str

    def handle_output(self, context: OutputContext, obj):
        if obj is None:
            return

        # Usar el nombre del output y añadir el prefijo "output-"
        output_name = context.name
        notebook_path = os.path.join(self.base_dir, f"output-{output_name}.ipynb")

        # Guardar el notebook usando nbformat
        with open(notebook_path, "w", encoding="utf-8") as f:
            nbformat.write(obj, f)

        context.add_output_metadata(
            {"notebook_path": MetadataValue.notebook(notebook_path)}
        )

    def load_input(self, context: InputContext):
        # Aquí también se debe reflejar el mismo patrón de nombre
        output_name = context.upstream_output.name
        notebook_path = os.path.join(self.base_dir, f"output-{output_name}.ipynb")

        with open(notebook_path, "r", encoding="utf-8") as f:
            return nbformat.read(f, as_version=4)

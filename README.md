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
from dagster import ConfigurableIOManager, MetadataValue, IInputContext, IOutputContext

class MyNotebookIOManager(ConfigurableIOManager):
    """IO Manager personalizado para notebooks.
    
    Este IO Manager asume:
    - Que se reciben objetos "notebook" (por ejemplo, archivos .ipynb) como output.
    - Que se pueden cargar esos objetos desde un directorio base.
    - Que se registra metadata en el contexto de salida.
    """
    
    base_dir: str  # Directorio base configurable vía recursos.

    def handle_output(self, context: IOutputContext, obj):
        # Validar que obj es el notebook o la información necesaria
        # para persistirlo en el sistema de ficheros.
        #
        # Suponiendo que `obj` es un contenido binario o un dict representando el notebook:
        if obj is None:
            # No hay nada que guardar
            return
        
        # Definir ruta de destino. Por ejemplo, usando el nombre del output.
        # La convención la puedes adaptar según tu caso.
        output_name = context.name
        notebook_path = os.path.join(self.base_dir, f"{output_name}.ipynb")

        # Guardar el notebook en el sistema de ficheros
        # Si `obj` es un dict con el contenido JSON del notebook:
        # import json
        # with open(notebook_path, "w", encoding="utf-8") as f:
        #     json.dump(obj, f)
        
        # Si `obj` es un string o binario con el contenido del notebook:
        with open(notebook_path, "wb") as f:
            f.write(obj)

        # Registrar la metadata con la ruta al notebook
        context.add_output_metadata({
            "notebook_path": MetadataValue.notebook(notebook_path),
        })

    def load_input(self, context: IInputContext):
        # Para cargar el notebook, asumimos un patrón similar al de handle_output
        # y que el upstream output tiene un nombre conocido o podemos derivar la ruta.
        # Si `context.upstream_output` está disponible, podemos obtener el nombre del output.
        output_name = context.upstream_output.name
        notebook_path = os.path.join(self.base_dir, f"{output_name}.ipynb")

        # Cargar el contenido del notebook
        # Dependiendo del formato en el que se guardó:
        # with open(notebook_path, "r", encoding="utf-8") as f:
        #     return json.load(f)
        
        with open(notebook_path, "rb") as f:
            notebook_content = f.read()
        
        return notebook_content

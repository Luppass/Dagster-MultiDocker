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

def create_notebook_asset(notebook_name, input_path, output_path):
    @asset(name=notebook_name)
    def notebook_asset(context):
        logger.info(f"Ejecutando notebook: {notebook_name}")
        try:
            pm.execute_notebook(input_path, output_path)
            logger.info(f"Notebook ejecutado exitosamente: {notebook_name}")
            
            # Añadimos metadatos para mostrar el notebook en la UI de Dagster
            context.add_output_metadata({"notebook": MetadataValue.notebook(output_path)})
        except Exception as e:
            logger.error(f"Error al ejecutar el notebook {notebook_name}: {e}")
            raise e
    return notebook_asset

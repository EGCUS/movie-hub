# Política de gestión de commits
*Normativa para la creación y gestión de commits.*
*Fecha de elaboración*: 31/10/2025

## Propósito
Este documento tiene el objetivo de establecer una serie de normas para la gestión de los commits en el proyecto, a fin de registrar de una forma más clara y eficiente los cambios que se van haciendo sobre el código.

## Estructura de mensajes de commit
Los mensajes de commit deben tener la siguiente forma: `<tipo>: <nombre>`
El nombre debe describir brevemente lo que se ha hecho en el commit.

## Tipos de commits
Distinguimos 4 tipos de commits en este proyecto:
- feat: un commit que añade una nueva característica o funcionalidad.
- docs: commits que se añaden o modifican la documentación del proyecto.
- fix: commits para arreglos de bugs.
- test: commits dedicados a la implementación de pruebas.

## Reglas relativas a los commits

### Atomicidad
Los commits deben ser atómicos, es decir, solo deben realizar los cambios que se describan en la issue asociada al commit, nada más. Puede ocurrir que una issue incluya varias actividades, dependiendo del tamaño de estas.

### Ramas
Cada commit debe pertenecer a una rama con un propósito claro; es totalmente posible realizar varios commits en una rama antes de fusionarla con develop. Una vez finalice la preparación de los flujos de trabajo y las fases previas al desarrollo, queda **prohibido** hacer cambios directamente sobre develop y mucho menos sobre main.

### Revisión
El autor del commit es responsable de verificar antes de subir los cambios, que su código no introduce errores ni conflictos, y que pase correctamente las pruebas, salvo que haya algún error identificado en ellas, o bien se deban ampliar para cubrir el nuevo código, lo cual debería hacerse en una rama distinta.

## Workflow
Existe un workflow en el proyecto, `.github/workflows/feature-branch.yml` que entre otras cosas se encarga de validar los commits, por lo que cualquier commit que no siga el formato indicado anteriormente no será aceptado por el flujo de trabajo.

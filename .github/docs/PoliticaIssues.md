# Política de gestión de issues
*Normativa para la creación y control de issues.*
*Fecha de elaboración*: 31/10/2025

## Propósito
Este documento tiene el objetivo de establecer una serie de normas para la creación y seguimiento de las issues en el proyecto, a fin de controlar las tareas del proyecto y organizar el trabajo de forma clara.

## Formato
Las issues o tareas se van a gestionar desde **zenhub**. A la hora de crear una issue hay que tener en cuenta lo siguiente:
- Se le debe añadir un nombre lo más corto posible que resuma el propósito de la issue.
- Es recomendable añadir una descripción si el nombre no aclara el objetivo de la issue.
- Se le debe asignar una etiqueta dependiendo del tipo de issue (feature, fix, test, docs o epic).
- Se debe asignar la issue a una de las milestones, dependiendo de a qué entregable corresponda.
- En caso de que la tarea tenga relación con un work item, se debe añadir a su épica correspondiente, si es que el work item dispone de una.

## Épicas
Las épicas son un tipo de issue que agrupa otras issues más pequeñas relacionadas. Normalmente, cada épica se asocia a uno o varios work items. El trabajo necesario para cada work item se divide en sub-issues que detallan tareas más específicas.

## Flujo de trabajo
En zenhub hay 4 pipelines o columnas entre las que se deben ir moviendo las issues dependiendo de su estado. El desarrollador asignado a cada issue es responsable de irla moviendo de una columna a otra según vaya progresando. Estas son las columnas:
- New issues: aquí estarán las issues recién creadas, cuando no tengan a nadie asignado.
- To Do: aquí se moverán las nuevas issues una vez tengan a alguien asignado, pero aún no se haya empezado a trabajar en ellas. Aquí un mismo desarrollador puede tener varias issues simultáneamente.
- In Progress: una vez que se empiece a trabajar sobre una issue, debe ir en esta pipeline. Aquí es recomendable que un mismo desarrollador tenga **una sola issue** y no coloque otra issue en esta pipeline hasta que haya pasado la anterior a Done.
- Done: cuando una issue se termine y se fusione la rama correspondiente con develop, la issue asociada se moverá a esta pipeline.

La columna closed se usará para tareas erróneas o repetidas, a modo de papelera, pero no tendrá influencia alguna sobre el flujo de trabajo.

## Buenas prácticas

- Se recomienda que el estado de las issues se mantenga actualizado, si un miembro del equipo no pudiera cambiar la tarea de columna al poco tiempo de haber avanzado con ella, otro compañero puede cambiarla de columna por él, aunque es preferible que cada uno se responsabilice de sus propias issues.
- Aunque una tarea no se corresponda con un work item, si es de gran tamaño, se puede convertir perfectamente en una épica y dividirla en subtareas.
- La columna closed **solo** debe usarse para tareas desechables, añadiendo un comentario de por qué esa issue está ahí. En ningún caso se puede usar para tareas que se hayan finalizado pero influyan en el desarrollo.

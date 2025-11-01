# Política de gestión de ramas

*Normativa para la creación, gestión y seguimiento de las ramas.*
*Fecha de elaboración*: 31/10/2025

## Propósito

Este documento tiene el objetivo de establecer una serie de normas para la gestión de las ramas en el proyecto, con el objetivo de separar el trabajo de cada desarrollador de forma clara y así evitar conflictos en el código.

## Estructura de ramas del proyecto

El proyecto cuenta con 2 ramas principales:
- **main**: es la rama principal del proyecto, en ella solo se subirá el código cuando esté en condiciones de hacer una **release**, el resto del tiempo permanecerá sin cambios.
-  **develop**: esta es la rama de producción, a ella se subirán todos los cambios que se vayan introduciendo mediante las ramas más pequeñas que se explican posteriormente. Cuando el código esté listo para lanzar una release, se fusionará esta rama con main.

Por otra parte, cada desarrollador creará ramas a partir de main para trabajar. Esas ramas estarán destinadas a un solo cambio. Cuando estas ramas ya no sean necesarias, deben borrarse del repositorio, así como del entorno local de cada desarrollador; de este modo se evita que se acumulen.

## Tipos de ramas

Hay 4 tipos de ramas estrechamente relacionadas con los tipos de commits:
- feature: una rama dedicada a añadir una nueva característica o funcionalidad.
- docs: ramas en las que se añade o modifica la documentación del proyecto.
- fix: ramas para arreglos de bugs.
- test: ramas dedicadas a la implementación de pruebas.

## Reglas relativas a las ramas

### Nombres
Las ramas deben seguir esta estructura en sus nombres: `<tipo>/<nombre-con-guiones>`
Es **importante** que las ramas sigan esta estructura, ya que de lo contrario puede que algunos flujos de trabajo no funcionen correctamente.
En cuanto a los nombres, se recomienda que no sean demasiado largos, y si el nombre está formado por varias palabras, se deben **usar guiones** para separarlas, nunca espacios.

### Eliminación
Como ya se ha mencionado, las ramas que no se vayan a utilizar más deben ser eliminadas. Para este propósito se ha definido un flujo de trabajo `.github/workflows/feature-branch` que, entre otras funciones, borra las ramas una vez se hace commit en ellas. Por esto es importante asegurarse de que los commits no producen errores ni conflictos en el código.

### Atomicidad
De igual modo que los commits deben ser atómicos, las ramas igual, no se deben realizar cambios que estén fuera de lo descrito en la issue para la que se haya creado la rama.

### Revisión
Antes de fusionar una rama, es importante asegurarse de que el código del entorno local está actualizado y que los cambios de la rama no produzcan conflictos en el código.

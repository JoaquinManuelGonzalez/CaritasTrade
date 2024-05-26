## Título:
Listar intercambios
## Narrativa:
- Como Usuario
- Quiero visualizar mi listado de intercambios
- Para gestionar los intercambios pendientes.
## Reglas de Negocio
- N/A
## Criterios de aceptación:
- **Escenario 1: Listar Intercambios exitoso**
    + **Dado** que se pudo recuperar la información de los intercambios existentes en el sistema para mis publicaciones.
    + **Cuando** se ingrese a la interfaz de manejo de solicitudes de intercambio. 
    + **Entonces** el sistema despliega en pantalla un listado de los intercambios registrados, acompañado de opciones para ver las publicaciones ofrecidas, las solicitadas y los usuarios que enviaron las solicitudes junto a botones para aceptar o rechazar cada solicitud de intercambio.

- **Escenario 2: Listado Vacío**
    + **Dado** que no se pudo recuperar la información de que exista alguna solicitud de intercambio en el sistema.
    + **Cuando** se ingrese a la interfaz de manejo de solicitudes de intercambio. 
    + **Entonces** el sistema muestra en pantalla el mensaje "Usted no tiene solicitudes de intercambio pendientes". 
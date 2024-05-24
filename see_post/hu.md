## Título:
Enviar solicitud de intercambio

## Narrativa:
- Como usuario registrado
- Quiero enviar solicitudes de intercambios
- Para realizar intercambios de bienes con otros usuarios

## Reglas de Negocio
- reputacion mayor igual a 3 estrellas
- Intercambios activos menores a 5

## Criterios de aceptación:
- **Escenario 1: Enviar solicitud de intercambio exitosa**
    + **Dado** un usuario registrado con un reputacion de 5 estrellas que tiene 1 intercambio activo y no envio solicitud para la publicación actual
    + **Cuando** se selecciona la opcion "Solicitar intercambio" para el producto "pancitos" y se confirma la operacion
    + **Entonces** el sistema envia al usuario que posteo el producto una solicitud de intercambio e informa en pantalla el mensaje "Solicitud de intercambio enviada con exito"  
- **Escenario 2: Enviar solicitud de intercambio fallido por reputacion baja**
    + **Dado** un usuario registrado con un reputacion de 1 estrella que tiene 1 intercambio activo y no envio solicitud para la publicación actual
    + **Cuando** se selecciona la opcion "Solicitar intercambio" para el producto "pancitos" y se confirma la operacion
    + **Entonces** el sistema informa en pantalla el mensaje "La reputacion actual es menor a 3 estrellas"  
- **Escenario 3: Enviar solicitud de intercambio fallido por intercambios maximos alcanzados**
    + **Dado** un usuario registrado con un reputacion de 5 estrella que tiene 5 intercambios activos y no envio solicitud para la publicación actual
    + **Cuando** se selecciona la opcion "Solicitar intercambio" para el producto "pancitos" y se confirma la operacion
    + **Entonces** el sistema informa en pantalla el mensaje "La cantidad de intercambios activos alcanzo el maximo"  
- **Escenario 4: Enviar solicitud de intercambio fallido por solicitud ya enviada**
    + **Dado** un usuario registrado con un reputacion de 1 estrella que tiene 5 intercambios activos y envio solicitud para la publicación actual
    + **Cuando** se selecciona la opcion "Solicitar intercambio" para el producto "pancitos" y se confirma la operacion
    + **Entonces** el sistema informa en pantalla el mensaje "Ya se envio una solicitud de intercambio para la publicación"  
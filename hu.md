## Título:
*Registrar intercambio*

## Narrativa:
- Como ayudante
- Quiero registrar un intercambio 
- Para mantener un registro de todas las transacciones y actividades relacionadas con el intercambio.

## Reglas de Negocio
- Se deben cargar 1 CáritasCoins si la transaccion va correctamente, o sacar 1 CaritasCoin si es que tiene más de 1 y no se produce correctamente.
- 
## Criterios de aceptación:
- **Escenario 1: Registro exitoso**
    + **Dado** dos afiliados de caritas, "Francisco Percara" que trae una mochila, con codigo válido ab5jxb6f y "Joaquin Gonzalez" que trae una goma, con codigo valido b5jxb6fa 
    + **Cuando** ingresa los codigos ab5jxb6f y b5jxb6fa, presiona "Terminar", y confirma la operación
    + **Entonces** el sistema registra el intercambio, se muestra un mensaje en pantalla "Se ha registrado el intercambio de forma exitosa", da de baja la publicación, se suman una CáritasCoins a la cuentas de los involucrados **Y** se habilita la calificacion entre las partes.

- **Escenario 2: Registro fallido por que falta un afiliado**
    + **Dado** un afiliado de Caritas "Tomas Bruschi" con codigo valido 5jxb6fab, que tenia una transacción con "Felipe Massera" que tenia 1 CáritasCoins, 
    + **Cuando** ingresa el codigo 5jxb6fab, presiona "Terminar", y confirma la operación
    + **Entonces** se muestra un mensaje en pantalla "Se ha penalizado al usuario Felipe Massera" y el sistema resta a la cuenta de "Felipe Massera" una CáritasCoins dejandola en 0.

- **Escenario 3: Registro fallido por codigo erroneo**
    + **Dado** dos afiliados de caritas, "Francisco Percara" que trae una mochila, con codigo erroneo ab5jxb6f y "Joaquin Gonzalez" que trae una goma, con codigo erroneo b5jxb6fa  
    + **Cuando** ingresa los codigos jxb6fab5 y xb6fab5j, presiona "Terminar", y confirma la operación
    + **Entonces** el sistema informa en pantalla "Alguno o ambos de los codigos son invalidos".

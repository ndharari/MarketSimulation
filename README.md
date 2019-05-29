# Market Simulation

## Introducción

En el siguiente trabajo se presenta una modelización de mercado basada en agentes en Python. Mediante un modelo simple se muestra que las cantidades relativas de compradores y vendedores son importantes a la hora de definir el precio de equilibrio de mercado. El objetivo de este trabajo es mostrar que frente a una  proporción mayor de vendedores el precio de equilibrio es menor, cuando se encuentran cantidades similares de compradores-vendedores el resultado es un valor intermedio y cuando abundan relativamente los compradores el precio de equilibrio es mayor.
La intención final del trabajo es presentar estas tres situaciones y lograr una representación del los equilibrios obtenidos gráficamente.

## El Modelo

Se propone un mercado con cantidades fijas ​de firmas y consumidores. Ambos operan de forma independiente por lo que no hay posibilidad de cartelización o acuerdos en la oferta o en la demanda. Estos tienen un valor de reserva individual que determina cuál es el máximo (mínimo) valor por el cual están dispuestos a comprar (vender) el bien a lo largo de los turnos. Además, cada uno de los agentes tiene un "precio esperado" para cada uno de los periodos que representa cuanto *cree* que es el precio actual del bien. Este valor se actualiza período a período y funciona como el mecanismo de ajuste del modelo. 

Al comenzar cada ronda, los compradores se dirigen hacia los vendedores de manera aleatoria. Ambas partes proceden a mostrar sus precios esperados en un "sobre cerrado". Si el precio que "propone" el vendedor es menor que el propuesto por el comprador se efectúa la compra. Caso contrario, no ocurre intercambio. Conforme avanzan los turnos se puede apreciar que se tiende a un precio de equilibrio.

Una explicación más minuciosa sobre los parámetros del modelo y el mecanismo de ajuste  se puede encontrar haciendo click [aquí.](https://www.overleaf.com/read/vdmyrpszhbcx "Simulación de Mercado en Python")


## Known problems / Future improvements

- Need to figure out what happens if Nº sellers > Nº buyers
- Differences in market compositions should be seen.
- Better the adjust mechanism.
- End game at market equilibrium, not at set number of turns
- Add some Graphical interface to analyze results
(graph showing convergence)

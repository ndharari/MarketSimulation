# Market Simulation

### El Modelo

Sea un mercado con cantidad fija de firmas y consumidores. No hay posibilidad de cartelización en la oferta ni en la demanda.
Los consumidores pueden comprar hasta 1 bien por ronda, de igual forma para los vendedores.
Tanto consumidores como vendedores tienen un valor de reserva $r$ que determina cual es el máximo (mínimo) valor dispuestos a vender por un bien. 
En cada período el mercado ordena de forma aleatoria a los compradores y estos se dirigen hacia el vendedor. Ambas partes "muestran" en sobre cerrado el precio por el que piensan intercambiar el bien. Si el precio del vendedor es menor que el del consumidor, el bien se intercambia al precio propuesto por el vendedor.


A su vez, consumidores y vendedores tienen un precio esperado $P^e$. Si en el periodo anterior se realizó un intercambio, el precio esperado será aquel del intercambio efectuado. En caso de que no se haya hecho, $P^e$ será el menor (mayor) entre el precio de reserva y el promedio entre el último precio "visto".

### Compradores



### Vendedores


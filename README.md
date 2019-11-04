# Market Simulation

###  Introducción

A continuación se presenta una modelización de mercado basada en agentes en Python. Mediante un modelo simple de doble subasta con ajuste secuencial se mostrará que las cantidades relativas de $m$ compradores y $n$ vendedores son importantes a la hora de definir el precio de equilibrio de mercado. Se encontrará que mientras el conjunto de costos  sea menor en su totalidad al de precios de reserva (asegurando que todos los compradores puedan, *a priori* consumir el bien - y viceversa) el precio de equilibrio estará cercano al precio máximo (o mínimo) que está dispuesto a pagar el $|n-m|$ -último individuo, ordenados por sus disposiciones de mayor a menor (en caso de haber más vendedores que compradores, se presenta el caso contrario)  En las oportunidades donde las cantidades son idénticas, el precio de equilibrio es intermedio.
La intención final del trabajo es presentar estas tres situaciones y lograr una representación del los equilibrios obtenidos gráficamente.

###  El Modelo

Se propone un mercado donde un conjunto fijo de $A$ agentes heterogéneos, entre ellos vendedores $S$ y consumidores $B$ con $A = {s_1, s_2,... s_n; b_1, b_2, ... b_m}$ deciden en cada periodo $t \in {1, 2, ...T}$ si intercambiar o no una única unidad de un bien homogéneo. Ambos grupos operan de forma atomizada e independiente por lo que no hay posibilidad de cartelización o acuerdos tanto en la oferta como en la demanda. No se consideran funciones de producción, ganancias,  ni riqueza: periodo a periodo los vendedores tendrán bienes a su disposición para vender y consumidores dinero para intercambiar por ellos. Se asume que cada individuo tiene una utilidad de reserva $U$ medida en términos monetarios que representa -en el caso del vendedor $s_i$- el costo mínimo $c_i$ por el que está dispuesto a desprenderse del bien en cuestión, mientras que en el caso del comprador $b_j$ el precio máximo idiosincrático $r_j$ dispuesto a pagar por el mismo.

Al inicio de cada ronda de mercado, los jugadores forman pares de forma aleatoria hasta agotar el numero de compradores o vendedores. En el caso en el que los conjuntos no tengan el mismo tamaño, $n \neq m$, habrá $|n-m|$ individuos que quedarán automáticamente fuera de las negociaciones. De esto se infiere fácilmente que para un determinado periodo no puede ocurrir que simultáneamente individuos de ambos conjuntos queden sin pareja.  

Una vez de a pares, cada vendedor $s_i$ propone un precio de venta $p_{s_i, t}$ de acuerdo a cuanto consideran que podrían vender su producto en el turno $t$. Los compradores observan este precio y lo comparan con su propio precio esperado $p_{b_j, t}$. De cumplirse la siguiente condición

$$
\text{Condición de intercambio en  $t$ entre  $s_i$ y $b_j$} \\
p_{s_i, t}\leq p_{b_j, t}
$$

los agentes realizarán el intercambio a precio $p=p_{s_i, t}$. Es importante notar que la condición de intercambio en $t$ es estáticamente independiente de las utilidades $U$ (costos, precios de reserva) generales de los agentes. Es decir, una vez definidos ambos precios esperados - cuyas mecánicas de ajuste se explicarán en el siguiente apartado - como los consumidores no reevalúan sus expectativas hasta el siguiente periodo, si $b_j$ se encuentra frente a un precio tal que $ r_j > p_{s_i, t} > p_{b_j, t} $ no comprará el bien aún cuando su precio es menor que el que estaría dispuesto a pagar. Esto es porque cree que estaría siendo engañado y que es posible conseguir el bien por un precio menor. 

Una vez que todos los pares decidieron si realizar o no la transacción, ambas partes se separan y todos los agentes que participaron en el mercado en $t$ - agrupados o no - reevalúan sus expectativas de precios para el siguiente periodo y deciden si continuarán participando en el mismo. El juego continúa hasta que terminen los turnos o hasta que no reste un número positivo de vendedores o consumidores. 

Una explicación más minuciosa sobre los parámetros del modelo y el mecanismo de ajuste  se puede encontrar haciendo click [aquí.](https://www.overleaf.com/read/vdmyrpszhbcx "Simulación de Mercado en Python")

## Known problems / Future improvements

- Known bug: sometimes sellers and buyers get 

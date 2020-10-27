# Ajuste dinámico de precios en un modelo basado en agentes en Python

## Nicolás David Harari

El siguiente es el repositorio del código utilizado para la simulación de mi tesina de grado para la Lic. de Economía en la Universidad de Buenos Aires. El texto completo se puede encontrar [aquí](https://github.com/ndharari/MarketSimulation/tree/master/Tesis) en formato `.pdf` o en el [siguiente link](https://ndharari.github.io/MarketSimulation/) como página web. 

###  Resumen

Los modelos tradicionales de equilibrio walrasiano presentan una elegante caracterización de los valores de equilibrio que puede tomar una economía dado las características de los agentes ---en este caso las firmas y los consumidores. Sin embargo, un número creciente de autores plantean que no logran explicitar de forma convincente el mecanismo por el cual los precios llegan a aquellos equilibrios (Arthur, 2015; A. Kirman, 2006; A. P. Kirman & Vriend, 2001). Ellos plantean la posibilidad de obtener resultados superadores a los obtenidos mediante las técnicas de modelización tradicional utilizando el paradigma de la economía computacional y técnicas de teoría de la complejidad (Albin y Foley 1992; Arthur 2015; Gode y Sunder 1993; Hommes 2013; Kirman y Vriend 2001; Vriend 1995; Wilhite 2001)

En el siguiente trabajo se considera un modelo simple de mercado donde una población de de <img src="https://render.githubusercontent.com/render/math?math=n"> vendedores y <img src="https://render.githubusercontent.com/render/math?math=m"> compradores heterogéneos deciden si intercambiar o no una única unidad de un bien homogéneo.  El precio de intercambio se actualiza periodo a periodo, conforme los agentes renuevan sus precios esperados para cada periodo. Los resultados presentados al final del trabajo fueron obtenidos utilizando el lenguaje de programación `python` cuyo código es de elaboración personal y se encuentra en este repositorio.

De esta forma se logra replicar el resultado esperado por los modelos de mercado tradicionales: las cantidades relativas de compradores y vendedores cumplen un rol fundamental a la hora de definir el precio de equilibrio emergente. A través de las simulaciones, se encuentra que mientras que todos los agentes en <img src="https://render.githubusercontent.com/render/math?math=t_0"> puedan obtener beneficios de intercambio el precio de equilibrio final suele estar cercano al precio máximo (o mínimo) que está dispuesto a pagar el <img src="https://render.githubusercontent.com/render/math?math=|n-m|"> -avo individuo, ordenados por sus disposiciones de mayor a menor (en caso de haber más vendedores que compradores, se presenta el caso contrario). En las oportunidades donde las cantidades son idénticas, el precio de equilibrio tiende a ser intermedio.


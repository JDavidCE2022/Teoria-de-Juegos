# TALLER 1 - TEORÍA DE JUEGOS

# Importamos 'itertools' que es un modulo de python que ofrece funciones para realizar productos
# cartesianos entre otras funciones.
import itertools

# Definimos una lista que contiene las posibles acciones que pueden realizar las 5 ciudades:
#"R", "C" e "I".
conjunto_de_acciones = ["R","C","I"]

# Con la función 'product' del modulo 'itertools' creamos una lista con el producto cartesiano de
# la lista 'conjunto_de_acciones' por si misma 5 veces, pues, son 5 ciudades y cada una tiene el mismo
# conjunto de acciones. Se establece el orden de este producto como Aa*Ab*Ac*Ad*Ae.
conjunto_de_acciones_conjuntas = list(itertools.product(conjunto_de_acciones, repeat=5))

# Definimos una función 'pagos' que recibe como parametros una lista que representa una determinada
# configuración de acciones de los jugadores (un elemento de 'conjunto_de_acciones_conjuntas') y
# un número 'nd' (abrevación de "número decisión") que determina si calcula el pago para cada jugador
# en ese vector de acciones en especifico o solamente de un solo jugador en particular. Dicho esto, 
# esta función retornará alguno de estos 2 calculos anteriormente mencionados.
def pagos(vector_de_acciones, nd):

    # Si 'nd' es 5, indica que queremos que retorne una lista con los pagos de cada jugador en base
    # a 'vector_de_acciones'.
    if nd == 5:

        # Definimos una lista llena de ceros de tamaño 5 llamada 'vector_de_pagos'. Esta es la que
        # retornaremos.
        vector_de_pagos = [0]*5

        # Realizamos un ciclo con variable de iteración 'j' que tomará valores de 0 a 4 donde
        # cada valor se referirá a una ciudad en especifica. Es decir:
        #     0 : a
        #     1 : b
        #     2 : c
        #     3 : d
        #     4 : e
        for j in range(5):

            # Se determina el valor en cada posición de 'vector_de_pagos' dependiendo del valor de
            # 'vector_de_acciones' en dicha posición. Pues, cada uso del suelo tiene una forma
            # diferente de calcularle su valor.

            # Si el uso que la ciudad 'j' a su suelo es "R" entonces su valor será el número de
            # municipios contiguos que designarón su zona al comercio menos el número de municipios
            # contiguos que designaron su zona a la industria. Se usa 'max' y 'min' en estos calculos
            # para evitar errores relacionados con referencias a elementos fuera de la lista y para
            # tratar el "Impacto ambiental alto" y el "Impacto ambiental marginal".
            if vector_de_acciones[j] == "R":
                vector_de_pagos[j] = (int(vector_de_acciones[max(0,j-1)] == "C") 
                                   + int(vector_de_acciones[min(4,j+1)] == "C")
                                   - int(vector_de_acciones[max(0,j-1)] == "I")
                                   - int(vector_de_acciones[min(4,j+1)] == "I")
                                  )

            # Si la ciudad 'j' destina su suelo para ser usado como comercio ("C"), entonces su valor
            # será igual al número de zonas residenciales contiguas.
            elif vector_de_acciones[j] == "C":
                vector_de_pagos[j] = (int(vector_de_acciones[max(0,j-1)] == "R") 
               + int(vector_de_acciones[min(4,j+1)] == "R"))

            # Si "I" es elegido como el uso del suelo para la ciudad 'j', entonces este sueldo valdrá
            # un valor equivalente a la cantidad de zonas residenciales del area metropolitana mas el número
            # de municipios contiguos destinados a la industria menos el impacto ambiental que es igual
            # al maximo entre 0 y el minimo del número de municipios industriales o 4, 
            # este mínimo decrementado en 1.
            else:
                vector_de_pagos[j] = (vector_de_acciones.count("R")
                                      + int(vector_de_acciones[max(0,j-1)] == "I" and max(0,j-1) != j)
                                      + int(vector_de_acciones[min(4,j+1)] == "I" and min(4,j+1) != j)
                                      - max(min(4,vector_de_acciones.count("I")) - 1, 0)
                                     )

        # Retornamos 'vector_de_pagos' y salimos de la función.
        return vector_de_pagos

    # Si 'nd' no es 5, indica que queremos que retorne unicamente el pago del jugador 'nd' en base
    # a 'vector_de_acciones'. La forma de calcular el pago es analoga al anterior bloque condicional.
    else:
        if vector_de_acciones[nd] == "R":
          return (int(vector_de_acciones[max(0,nd-1)] == "C") 
                             + int(vector_de_acciones[min(4,nd+1)] == "C")
                             - int(vector_de_acciones[max(0,nd-1)] == "I")
                             - int(vector_de_acciones[min(4,nd+1)] == "I")
                            )
        elif vector_de_acciones[nd] == "C":
          return (int(vector_de_acciones[max(0,nd-1)] == "R") 
         + int(vector_de_acciones[min(4,nd+1)] == "R"))
        else:
          return (vector_de_acciones.count("R")
                                + int(vector_de_acciones[max(0,nd-1)] == "I" and max(0,nd-1) != nd)
                                + int(vector_de_acciones[min(4,nd+1)] == "I" and min(4,nd+1) != nd)
                                - max(min(4,vector_de_acciones.count("I")) - 1, 0)
                               )

# Definimos una función 'esENEP' que recibirá como parametro una lista 'vector_de_acciones' que es 
# un elemento de 'conjunto_de_acciones_conjuntas'. Esta función retornará un valor booleano
# que será 'True' si la configuración de acciones ingresadas es un ENEP o 'False' en caso contrario.
# Tambien retornará, junto con el valor booleano, un número entero que representará la suma total
# de los valores de todos los municipios para el perfil 'vector_de_acciones'.
def esENEP(vector_de_acciones):

    # Calculamos el vector de pagos para todas las ciudades en base de 'vector_de_acciones'.
    vector_de_pagos = pagos(vector_de_acciones,5)

    # Iteramos con 'i' desde 0 hasta 4, osea, sobre todas las ciudades.
    for i in range(5):

        # Iteramos sobre todas las acciones de 'i' que sean diferentes a la acción que este
        # tiene en 'vector_de_acciones'. Usamos un filtro con 'filter' para este proposito.
        for j in filter(lambda e : e != vector_de_acciones[i], conjunto_de_acciones):

            # Creamos 'vector_de_acciones_alt' que es una copia de 'vector_de_acciones'.
            vector_de_acciones_alt = vector_de_acciones[:]
            
            # En la copia, reemplazamos la acción original destinada para 'i' por la acción
            # 'j' que recordemos que es diferente a este acción original. Esto deja fijo
            # las acciones de los otros jugadores.
            vector_de_acciones_alt[i] = j

            # Si el pago de la ciudad 'i' en la configuración vector_de_acciones es menor que
            # el pago de la ciudad 'i' en al configuración vector_de_acciones_alt, entonces
            # 'i' tiene incentivos a desviarse, por lo que 'vector_de_acciones' no es un ENEP
            # y se retorna 'False' junto con la suma total del valor de todas las ciudades.
            # Esto rompería inmediatamente los ciclos y terminaría la función (pues, ya se
            # habría demostrado que no es ENEP).
            if vector_de_pagos[i] < pagos(vector_de_acciones_alt, i):
                return False, sum(vector_de_pagos)

    # Si se completa los ciclos anteriores, es porque ninguna ciudad tuvo incentivos a desviarse.
    # Por lo tanto, retornamos 'True' junto con la suma total del valor de la metrópolis.
    return True, sum(vector_de_pagos)

# Definimos una variable llamada 'maximo_pago' que guardará el maximo pago conjunto que la metropolis
# puede alcanzar. En un principio lo inicializamos en -15 debido a que esta es una cota inferior en
# el valor maximo, pues, se hayó multiplicando -3 (la maxima penalidad por el impacto ambiental) por 5
# (el número de ciudades), esto ignorando ganancia alguna.
maximo_pago = -15

# Inicializamos en 0 la variable 'numeros_de_ENEPs', esta llevará registro del número de ENEPs que
# encontremos.
numeros_de_ENEPs = 0

# Declaramos la lista 'ENEPs' que guardará los indices de las configuraciones pertenecientes a
# 'conjunto_de_acciones_conjuntas' que sean ENEPs. Osea, que guardará enteros entre 0 y 243 - 1 = 242.
ENEPs = []

# Declaramos un iterador 'it' que guardará registro temporal de indice en cada iteración del ciclo.
# Esta variable es la que guardaremos en 'ENEPs' y comenzará en 0.
it = 0

# Iteramos sobre cada elemento de 'conjunto_de_acciones_conjuntas', es decir, sobre cada perfil de acción
# conjunta posible. Cada elemento iterado será registrado temporalmente por 'vector_de_acciones'.
for vector_de_acciones in conjunto_de_acciones_conjuntas:

    # Declaramos dos variables locales, 'es' y 'valor_conjunto' que guardaran respectivamente la respuesta
    # a la pregunta de que si 'vector_de_acciones' es un ENEP y un entero que es la suma total del valor
    # de la metropolis. Estos resultados serán retornados por la función previamente definida 'esENEP' que
    # recibe como parametro 'vector_de_acciones' del ciclo convertido a lista (pues, el modulo 'itertools'
    # los guarda como tuplas no inmutables).
    es, valor_conjunto = esENEP(list(vector_de_acciones))

    # Si 'es' es verdadera, esto quiere decir que 'vector_de_acciones' es un ENEP y por lo tanto aumentamos
    # en una unidad 'numeros_de_ENEPs', añadimos 'it' (el indice de esta configuración en 
    # 'conjunto_de_acciones_conjuntas') a 'ENEPs' y actualizamos 'maximo_pago' a 'valor_conjunto'
    # en caso de que este ultimo sea mayor al 'maximo_pago' registrado, sino, 'maximo_pago' queda igual.
    if es == True:
        numeros_de_ENEPs += 1
        ENEPs.append(it)
        maximo_pago = max(maximo_pago, valor_conjunto)

    # En caso contrario, entonces no hacemos ninguna actualización a las variables relacionadas con los ENEPs
    # pero si a 'maximo_pago'.
    else:
        maximo_pago = max(maximo_pago, valor_conjunto)

    # Incrementamos 'i' en una unidad.
    it += 1

# Creamos una lista llamada 'conf_maximas' que cumpla una función similar a 'ENEPs': Guardar los indices
# de las configuraciones que retornen un maximo valor conjunto.
conf_maximas = []

# De nuevo creamos un iterador 'it' inicializado en 0 para llevar registro de los indices.
it = 0

# Nuevamente iteramos sobre todos los elementos de 'conjunto_de_acciones_conjuntas'.
for vector_de_acciones in conjunto_de_acciones_conjuntas:

    # Calculamos el valor conjunto del actual 'vector_de_acciones'.
    _, valor_conjunto = esENEP(list(vector_de_acciones))

    # Si el valor conjunto del actual 'vector_de_acciones' es igual al maximo pago conjunto global, 
    # entonces guardamos su indice en 'conf_maximas'.
    if valor_conjunto == maximo_pago:
        conf_maximas.append(it)

    # Le sumamos 1 a 'it'.
    it += 1

# Imprimimos los resultados.

# Imprimimos el titulo del codigo.
print("TEORIA DE JUEGOS - POT\n")

# Imprimimos el maximo valor conjunto de la metropolis.
print(f"El maximo valor conjunto de la tierra es {maximo_pago}.\n")

# Imprimiremos las acciones conjuntas que corresponden al valor maximo iterando sobre 'conf_maximas'.
print("Las acciones conjuntas que maximizan el pago conjunto son: ")
for accion in conf_maximas:
    print(f"{conjunto_de_acciones_conjuntas[accion]}")

# Imprimimos las acciones de 'conf_maximas' que se encuentren en 'ENEPs', para observar las acciones
# conjuntas "optimas" que son ENEPs.
print("\nDe las cuales las unicas que son ENEPs son: ")
for accion in conf_maximas:
    if accion in ENEPs:
        print(f"{conjunto_de_acciones_conjuntas[accion]}")

# Imprimimos el número de ENEPs del juego junto con las acciones conjuntas que son ENEPs. Esto iterando
# sobre 'ENEPs'.
print(f"\nEl numero de ENEPs que contiene este juego es {numeros_de_ENEPs}. Y son los siguientes: ")
for accion in ENEPs:
    print(f"{conjunto_de_acciones_conjuntas[accion]}")

# Imprimimos mensaje de aclaración sobre el orden de las configuraciones.
print("Donde la correspondencia es (a, b, c, d, e).")
"""Este modulo define la clase LocalSearch.

LocalSearch representa un algoritmo de busqueda local general.

Las subclases que se encuentran en este modulo son:

* HillClimbing: algoritmo de ascension de colinas. Se mueve al sucesor con
mejor valor objetivo. Ya viene implementado.

* HillClimbingReset: algoritmo de ascension de colinas de reinicio aleatorio.
No viene implementado, se debe completar.

* Tabu: algoritmo de busqueda tabu.
No viene implementado, se debe completar.
"""


from __future__ import annotations
from time import time
from problem import OptProblem, TSP
import math



class LocalSearch:
    """Clase que representa un algoritmo de busqueda local general."""

    def __init__(self) -> None:
        """Construye una instancia de la clase."""
        self.niters = 0  # Numero de iteraciones totales
        self.time = 0  # Tiempo de ejecucion
        self.tour = []  # Solucion, inicialmente vacia
        self.value = None  # Valor objetivo de la solucion

    def solve(self, problem: OptProblem):
        """Resuelve un problema de optimizacion."""
        self.tour = problem.init
        self.value = problem.obj_val(problem.init)


class HillClimbing(LocalSearch):
    """Clase que representa un algoritmo de ascension de colinas.

    En cada iteracion se mueve al estado sucesor con mejor valor objetivo.
    El criterio de parada es alcanzar un optimo local.
    """

    def solve(self, problem: OptProblem):
        """Resuelve un problema de optimizacion con ascension de colinas.

        Argumentos:
        ==========
        problem: OptProblem
            un problema de optimizacion
        """
        # Inicio del reloj
        start = time()

        # Arrancamos del estado inicial
        actual = problem.init
        value = problem.obj_val(problem.init)

        while True:

            # Buscamos la acción que genera el sucesor con mayor valor objetivo
            act, succ_val = problem.max_action(actual)

            # Retornar si estamos en un maximo local:
            # el valor objetivo del sucesor es menor o igual al del estado actual
            if succ_val <= value:

                self.tour = actual
                self.value = value
                end = time()
                self.time = end-start
                return

            # Sino, nos movemos al sucesor
            actual = problem.result(actual, act)
            value = succ_val
            self.niters += 1


class HillClimbingReset(LocalSearch):

    """Algoritmo de ascension de colinas con reinicio aleatorio."""


    """Clase que representa un algoritmo de ascension de colinas.

    En cada iteracion se mueve al estado sucesor con mejor valor objetivo.
    El criterio de parada es alcanzar un optimo local.
    """
    def estimate_max_restarts(self, problem: TSP, base: float = 0.30) -> int:
        """Determina un número adecuado de reinicios basado en el tamaño del problema TSP.

        Argumentos:
        ==========
        problem: TSP
            Instancia del problema del viajante. Debe contener:
            - Un atributo G con el grafo del problema
            - Método number_of_nodes() en G para obtener el número de ciudades
            - Opcionalmente un atributo init con el tour inicial
        base: float
            Factor de escala para ajustar el número de reinicios (default=0.30)

        Retorno:
        =======
        int: 
            Número estimado de reinicios aleatorios recomendados

        Excepciones:
        ===========
        ValueError:
            - Si el problema no tiene la estructura esperada de TSP
            - Si el tour inicial no coincide con el número de ciudades
        """
        if not hasattr(problem, 'G') or not hasattr(problem.G, 'number_of_nodes'):
            raise ValueError("El problema no tiene la estructura de TSP esperada")
        
        n = problem.G.number_of_nodes()
        
        if not hasattr(problem, 'init'):
            # Si no tiene init, usamos el número de nodos directamente
            state_space_size = math.factorial(n - 1)
        else:
            # Si tiene init, verificamos su longitud
            if len(problem.init) != n + 1:  # +1 por el 0 inicial/final
                raise ValueError("El tour inicial no coincide con el número de ciudades")
            state_space_size = math.factorial(n - 1)
        
        return int(base * math.log(state_space_size))
    def solve(self, problem: TSP, max_restarts=10):
        """Resuelve un problema de optimizacion con ascension de colinas.

        Argumentos:
        ==========
        problem: OptProblem
            un problema de optimizacion
        """
        # Inicializamos reinicios y la cantidad que queremos
        max_restarts = self.estimate_max_restarts(problem)
        restarts = 0
        best_value = -float("inf") 
        best_solution = None
        # Inicio del reloj
        start = time()

        while restarts <= max_restarts:
            if restarts == 0:
                actual_state = problem.init
            else:
                actual_state = problem.random_reset()

        # Arrancamos del estado inicial
        
            value = problem.obj_val(actual_state)

            while True:

                # Buscamos la acción que genera el sucesor con mayor valor objetivo
                act, succ_val = problem.max_action(actual_state)

                # Retornar si estamos en un maximo local:
                # el valor objetivo del sucesor es menor o igual al del estado actual


                if succ_val <= value:
                    break

                # Sino, nos movemos al sucesor
                actual_state = problem.result(actual_state, act)
                value = succ_val
                self.niters += 1

            if value > best_value:
                best_value = value
                best_solution = actual_state
            
            restarts += 1
        

        end = time()
        self.value = best_value
        self.tour = best_solution
        self.time = end-start



class Tabu(LocalSearch):
    """Algoritmo de busqueda tabu."""
    def solve(self, problem: TSP, max_stops = 10):
        stops = 0
        actual_state = problem.init
        best_state = actual_state
        best_value = problem.obj_val(actual_state)
        tabu = []
        tabu_len = 7
        start = time()


        while stops <= max_stops:

            act, succ_val = problem.max_action(actual_state,tabu)

            # Moverse al sucesor
            next_state = problem.result(actual_state, act)

            # Registrar iteración
            self.niters += 1

            # Ver si encontramos una mejor solución global
            if succ_val > best_value:
                best_value = succ_val
                best_state = next_state
                stops = 0  # reseteamos porque mejoramos
            else:
                stops += 1  # no mejoramos, contamos estancamiento

            # Agregamos acción a la lista tabú
            tabu.append(act)
            
            if len(tabu) > tabu_len:
                tabu.pop(0)
                
            actual_state = next_state  # avanzamos

        end = time()
        self.tour = best_state
        self.value = best_value
        self.time = end - start
              



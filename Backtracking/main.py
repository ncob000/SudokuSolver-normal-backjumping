import copy
import os
from itertools import product, permutations


class KillerSudokuSolver:
    """
    Solucionador de Sudoku Killer utilizando técnicas de propagación 
    de restricciones y backtracking.

    Este solver aplica restricciones de Sudoku tradicional y restricciones adicionales
    para sudoku killer (celdas con sumas objetivo específicas).

    Atributos:
    ---------
    grid : list[list[str]]
        Matriz 9x9 que define el identificador de jaula para cada celda del tablero.
        Cada celda pertenece a una jaula identificada por un código único (C1, C2, etc.).
        
    cages : dict
        Diccionario donde las claves son los identificadores de jaula y los valores son
        las sumas objetivo de dichas jaulas.
        
    verbose : bool
        Si es True, activa salida detallada
        
    board : list[list[int]]
        Representación interna del tablero con los valores actuales de las celdas.
        
    domains : dict
        Diccionario que asocia a cada celda los valores posibles (dominio) que puede
        tomar según las restricciones aplicadas.

    Metodos:
    --------
    __init__(grid, cages, verbose=False):
        Inicializa la cuadrícula, las jaulas, y define los valores iniciales del tablero.

    initializeDomains():
        Calcula los dominios iniciales para cada celda basandose en las restricciones.

    getCageCells(cage_id):
        Encuentra las celdas asociadas a una jaula especifica.

    eliminateValues():
        Aplica propagación de restricciones para reducir los valores posibles en cada celda.

    genValidCombinations(cells, target_sum, domains):
        Genera combinaciones de valores válidas para celdas de jaulas no asignadas.

    solver():
        Método principal que utiliza backtracking y propagación de restricciones
        para resolver el tablero.
    """
    def __init__(self, grid, cages, verbose=False):
        """
        Inicializa la clase killerSudokuSolver

        Parametors
        ----------
        grid : list[list[str]]
            Matriz 9x9 con identificadores de jaula para cada celda.
        cages : dict
            Diccionario con las sumas objetivo de las jaulas.
        verbose : bool, opcional
            salida detallada
        """
        self.grid = grid
        self.cages = cages
        self.verbose = verbose
        self.board = [[0 for _ in range(9)] for _ in range(9)]
        self.domains = self.initializeDomains()

    def initializeDomains(self):
        """
        Inicialisa los dominios para cada celda teniendo en cuenta las restricciones

        Return
        ------
        domains : dict
            Diccionario que contiene los posibles valores para cada celda.
            Las claves son coordenadas (fila, columna) y los valores son listas
            con los números posibles en esa celda.
        """
        domains = {}
        if self.verbose:
            print("\nInicializando dominios para cada celda...")

        # Recorrer cada celda del tablero
        for row in range(9):
            for col in range(9):
                # Caso donde la celda tiene un valor predefinido (por seguridad en algun tipo de tablero)
                if self.grid[row][col] != "0" and not self.grid[row][col].startswith("."):
                    domains[(row, col)] = [int(self.grid[row][col][0])]
                else:
                    # La celda puede tomar cualquier valor del dominio
                    domains[(row, col)] = list(range(1, 10))
                    if self.verbose:
                        print(f"Celda ({row}, {col}) tiene dominio completo: {domains[(row, col)]}")
        if self.verbose:
            print("Dominios inicializados.\n")
        
        return domains

    def getCageCells(self, cage_id):
        """
        Encuentra todas las celdas que pertenecen a una jaula específica del tablero.

        Parametros
        ----------
        cage_id : str
            identificador de jaula, ej: (C1, C2, ..., Cn)

        Return
        ------
        cage_cells : list
            Lista de coordenadas de las celdas que pertenecen a la jaula especificada.
        """
        if self.verbose:
            print(f"Buscando celdas para la jaula: {cage_id}...")

        # Lista que recorre todas las celdas del tablero 9x9 e identifica a las celdas
        # que pertenecen a la jaula `cage_id` 
        cage_cells = [
            (row, col)
            for row in range(9)
            for col in range(9)
            if self.grid[row][col].endswith(cage_id)
        ]

        if self.verbose:
            print(f"Se encontraron {len(cage_cells)} celdas para la jaula: {cage_id}.\n")

        return cage_cells

    def eliminateValues(self):
        """
        Realice la propagación de restricciones "constraint propagation" eliminando valores imposibles
        en base a las restricciones especificas del sudoku killer.

        Fuentes utilizadas:
            - "https://info.bb-ai.net/student_projects/project_reports/Henry-Davies-Killer-Sudoku.pdf"
            - "https://medium.com/my-udacity-ai-nanodegree-notes/solving-sudoku-think-constraint-satisfaction-problem-75763f0742c9"

        Return
        ------
        bool
            True si la propagacion fue exitosa, False si se encuentra alguna contradiccion
        """
        changed = True # sirve para seguir iterando mientras haya cambios
        while changed:
            changed = False

            # Reestricciones de fila columna y caja (conjunto de celdas 3x3 del tablero)
            for constraint_type in ["row", "col", "box"]:
                if self.verbose:
                    print(f"Procesando restricciones para: {constraint_type}")

                # Conjunto de celdas segun el tipod de restriccion
                if constraint_type == "row":
                    constraints = [[(i, col) for col in range(9)] for i in range(9)]

                elif constraint_type == "col":
                    constraints = [[(row, i) for row in range(9)] for i in range(9)]

                else:  # box
                    constraints = [
                        [
                            (3 * (box // 3) + r, 3 * (box % 3) + c)
                            for r in range(3)
                            for c in range(3)
                        ]
                        for box in range(9)
                    ]
                    
                    
                # Plicar restricciones dentro de cada conjunto
                for cells in constraints:
                    # Obtener los valores actuales de estas celdas
                    values = [self.board[row][col] for row, col in cells]

                    # Elimina los valores que ya se estan usando en este conjunto de restricciones
                    used_values = set(v for v in values if v != 0)

                    for row, col in cells:
                        if self.board[row][col] == 0: # si la celda no tiene valor asignado
                            old_domain = self.domains[(row, col)].copy()
                            # Reducir el dominio eliminando valores ya utilizados
                            self.domains[(row, col)] = [
                                val
                                for val in self.domains[(row, col)]
                                if val not in used_values
                            ]
                            if self.verbose and self.domains[(row, col)] != old_domain:
                                print(
                                    f"Dominio de la celda ({row}, {col}) reducido: {old_domain} -> {self.domains[(row, col)]}"
                                )
                            # caso donde queda un unico valor dentro del dominio
                            if len(self.domains[(row, col)]) == 1:
                                self.board[row][col] = self.domains[(row, col)][0]
                                changed = True
                                if self.verbose:
                                    print(
                                        f"Tomando valor {self.board[row][col]} en la celda ({row}, {col})"
                                    )

                            # Caso donde no quedan valores en el dominio (contradiccion)
                            if len(self.domains[(row, col)]) == 0:
                                return False

            # ------------------------------------------------------------------------------------
            # Restricciones de las jaulas
            for cage_id, target_sum in self.cages.items():

                if self.verbose:
                    print(
                        f"\nProcesando restricciones para la jaula: {cage_id} con suma objetivo: {target_sum}"
                    )

                cage_cells = self.getCageCells(cage_id)
                cage_values = [self.board[row][col] for row, col in cage_cells]

                # Filtrar el valores o valores asignados
                unassigned_cells = [
                    cell for cell in cage_cells if self.board[cell[0]][cell[1]] == 0
                ]

                # Si todas las celdas dentro de una jaula ya tienen valores asignados se verifica
                # que se cumpla la suma objetivo de a jaula
                if len(unassigned_cells) == 0 and sum(cage_values) != target_sum:
                    return False

                # Podar los dominios para las celdas de la jaula
                if unassigned_cells:
                    # Encontrar las combinaciones válidas para celdas no asignadas
                    current_sum = sum(cage_values)
                    remaining_sum = target_sum - current_sum

                    # Generar posibles combinaciones
                    valid_combinations = self.genValidCombinations(
                        unassigned_cells,
                        remaining_sum,
                        [self.domains[cell] for cell in unassigned_cells],
                    )

                    # Contradiccion
                    if not valid_combinations:
                        return False

                    # Actualizar (reducir) dominio basandose en las combinaciones asignadas
                    for cell in unassigned_cells:
                        possible_values = set(
                            val for combo in valid_combinations for val in combo
                        )
                        new_domain = [
                            val for val in self.domains[cell] if val in possible_values
                        ]

                        
                        if not new_domain:
                            return False

                        if len(new_domain) < len(self.domains[cell]):
                            self.domains[cell] = new_domain
                            changed = True
                            if self.verbose:
                                print(
                                    f"Reducción del dominio para la celda {cell} a {new_domain}"
                                )

                            # Si solo queda un valor, se asigna a la celda
                            if len(new_domain) == 1:
                                row, col = cell
                                self.board[row][col] = new_domain[0]
                                changed = True
                                if self.verbose:
                                    print(
                                        f"Tomando valor {self.board[row][col]} en la celda ({row}, {col})"
                                    )

        return True

    def genValidCombinations(self, cells, target_sum, domains):
        """
        Generar las combinaciones de valores validas para celdas de las jaulas no asignadas.

        Parametros
        ----------
        cells : list
            celdas sin asignar de la jaula
        target_sum :  int
            Suma objetivo de la jaula
        domains : list
            Lista de listas, donde cada sublista representa los posibles valores de cada celda.


        Return
        ------
        valod_combinations : list
            lista de Combinaciones validas
        """
        valid_combinations = [] # lista para amacenar combinaciones validas

        if self.verbose:
            print(
                f"Generando combinaciones válidas para las celdas {cells} con suma objetivo {target_sum}..."
            )

        # producto cartesiano de los valores posibles de cada celda
        for combo in product(*domains):
            if (
                len(set(combo)) == len(combo)  # Todos los valores unicos
                and sum(combo) == target_sum   # Suma valida
            ):
                valid_combinations.append(combo)

        if self.verbose:
            print(f"{len(valid_combinations)} combinaciones válidas encontradas.")

        return valid_combinations

    def solver(self):
        """
        Metodo principal que usa "backtracking" con "constraits propagation" para resolver
        El tablero de sudoku killer

        Returns
        -------
        board : list
            tablero resulto resspresentado como una lista de listas
        None :
            cuando no se encontro solucion

        """
        if self.verbose:
            print("Iniciando la propagación de restricciones...")

        # constraint propagation inicial
        if not self.eliminateValues():
            return None

        # Revisar si el tablero esta completamente resulto
        if all(all(cell != 0 for cell in row) for row in self.board):
            if self.verbose:
                print("El tablero está completamente resuelto.")
            return self.board

        # heuristica MRV (minimum remaining value)
        # Encontrar la celda con el dominio mas pequeno
        min_domain_cell = min(
            (
                (row, col)
                for row in range(9)
                for col in range(9)
                if self.board[row][col] == 0
            ),
            # Definimos una funcion anonima que toma como argumento a las cordenadas de una celda del
            # tablero y recupera el dominio de la celda en un diccionario
            key=lambda cell: len(self.domains[cell]),
        )

        row, col = min_domain_cell

        # Intentar todos los valores posibles para la celda actual
        for value in self.domains[(row, col)]:
            # Crear una copia del estado actual para realizar backtraking
            board_copy = copy.deepcopy(self.board)
            domains_copy = copy.deepcopy(self.domains)

            # Asignamos el valor temporalmente a la celda
            self.board[row][col] = value

            # Resolucion recursiva con propagacion de restricciones.
            if self.eliminateValues():
                solution = self.solver()
                if solution:
                    return solution

            # Backtrack
            self.board = board_copy
            self.domains = domains_copy

            if self.verbose:
                print(
                    f"Apicando backtracking desde celda ({row}, {col}) con el valor {value}"
                )

        return None


# --------------------------------------------------------------------------------------------


def readKillerSudoku(file_path, verbose=False):
    """
    Funcion que lee e interpreta un tablero de sudoku killer.
    El formato de los tableros almacenados en los archivos .txt estan inspirado por
    el formato utilizado en el siguiente proyecto:
    "https://github.com/omelkonian/ai-collection/tree/master/Killer%20Sudoku/killer_sudokus"    


    Parametros
    ----------
    file_path : str
        Path del tablero.txt
    verbose : bool
        activar salida detallada

    Return
    ------
    Grid : tuple
        tupla que representa la cuadricula del tablero
    cage : tuple
        tupla que representa las jaulas del tablero

    """

    with open(file_path, "r") as file:
        lines = file.readlines()

    # Leer la cuadricula (primeras 9 lineas)
    grid = [line.strip().split() for line in lines[:9]]
    if verbose:
        print("Tablero cargado:\n")
        for row in grid:
            # Extraer solo los números, omitiendo el prefijo '.C'
            # Con el cual se formatea correctamnete el tablero
            row_numbers = [cell[2:] for cell in row]  # .C1 -> 1
            print("\t".join(row_numbers))

    # Leer las sumas objetivos de cada jaula
    cages = {}
    for line in lines[10:]:
        cage_id, sum_value = line.strip().split(":")
        cages[cage_id.strip()] = int(sum_value.strip())

    if verbose:
        print("\nDatos de jaulas del tablero cargado:\n")
        for cage_id, sum_value in cages.items():
            print(f"cage ID:{cage_id}\tsum value:{sum_value}")

    return grid, cages


def printSudokuGrid(board):
    """
    Imprime el tablero de sudoku con separadores para cada caja (3x3)

    Parametros
    ----------
    board : list
        tablero 9x9 de sudoku killer
    """

    for i, row in enumerate(board):
        # Print row
        row_str = []
        for j, num in enumerate(row):
            row_str.append(str(num))

            # Anadir espaciado cada tres columnas
            if (j + 1) % 3 == 0 and j < 8:
                row_str.append("  ")

        print(" ".join(row_str))

        # Anadir espaciado despues de cada fila
        if (i + 1) % 3 == 0 and i < 8:
            print()


def solveKillerSudoku(file_path, verbose=False):
    """
    En esta funcion se llaman las funciones necesarias para resolver el sudoku

    Parametros
    ----------
    file_path : str
        Path del tablero a resolver
    verbose : bool
        activar salida detallada

    Return
    ------
    solution : list or None
        Tablero resulto o None si no hay solucion
    """

    grid, cages = readKillerSudoku(file_path, verbose)

    solver = KillerSudokuSolver(grid, cages, verbose)
    solution = solver.solver()

    if solution:
        print("\nSudoku resuelto:")
        # if verbose:
        printSudokuGrid(solution)
        return solution
    else:
        print("\nNo se encontro ninguna solucion!!.")
        return None


if __name__ == "__main__":
    try:
        current_dir = os.path.dirname(__file__)  # Carpeta actual
        board_name = "KL5DRCOP.txt"  # Nombre del tablero
        file_path = os.path.join(current_dir, board_name)  # Ruta al archivo
        verbose = False
        
        if not os.path.exists(file_path):
            raise FileNotFoundError(
                f"El archivo '{board_name}' no se encontró en {current_dir}."
            )

        board_code = board_name.removesuffix(".txt")
        print(f"\nLeyendo tablero desde: {file_path}...")
        print(f"Resolviendo Sudoku Killer con código {board_code}\n")
        solveKillerSudoku(file_path, verbose)

    except FileNotFoundError as e:
        print(f"Error: {e}")

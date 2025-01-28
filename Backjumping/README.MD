# Sudoku solver
solucionador de un tablero se sudoku nivel imposible de <https://www.sudokumania.com.ar> utilizando principalmente algoritmo de backjumping.

Los tableros estan almacenados en el directorio `\boards` del proyecto y tienen el siguiente
formato:

```txt
9,0,2,0,0,0,0,4,0
0,0,1,9,0,5,0,6,0
0,0,0,0,0,0,0,0,0
0,7,9,0,6,0,3,2,0
2,4,0,0,0,0,0,0,0
0,0,0,0,0,0,0,5,0
0,0,0,0,0,0,0,0,0
7,0,0,0,0,3,5,0,0
0,0,3,2,5,0,0,0,0
```

Donde el 0 representa celdas vacias.

## Verbose

para activar el verbose, especificar el parametro `--verbose` en la linea de comandos, en caso de no hacerlo el programa no imprimira informacion adicional.

```shell
python main.py --verbose
```

Adicionalmente se pueden especicar los parametros:

- `--verbose-level` Nivel de detalle del verbose, desde 1 hasta 3, **_default 1_**.
- `--iteration-level` Numero de iteraciones por cada impresion del verbose, **_default 10_**.
- `--boardcode` Nombre del tablero a ser probado, **_default DG9TFMNR.txt_**.
- `--help`

Ejemplo de uso:

```shell
python main.py --verbose --verbose-level 2 --iteration-level 1 --boardcode DG9USZLF.txt
```

O sin la impresion del verbose y con los valores default:

```shell
python main.py
```

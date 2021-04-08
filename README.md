## LHSP

Genera archivos .cub visualizables con el programa GaussView o
cualquier otro capaz de leer archivos .cub provenientes de Gaussian.
Corresponden a los campos escalares del potencial de la hiperblandura
local así como de sus dos componentes. No son los mismos archivos que
genera el código LHS, de hecho LHSP está en investigación pues se basa
en el cálculo del potencial electrostático molecular. Por cada sistema
molecular, se requiere como alimentación de 5 archivos .log del
sistema con N, N+1, N+2, N-1, N-2 electrones y los archivos .fchk con
N, N+p y N-q electrones, donde p y q son el grado de degeneración en
orbitales de frontera LUMO y HOMO, respectivamente. Al igual que con
los códigos Dualdescriptor y DDP, todos esos sistemas deben poseer la
misma geometría molecular que la del sistema con N electrones.
Utilizable solo en servidores con sistema operativo Linux y siempre
tenga instalados y operativos los programas Gaussian y sus
complementarios cubegen y cubman.

## Requerimientos

Requiere servidor con los software cubegen y cubeman de Gaussian.

## Installation

Copia la carpeta LHSP en tu cuenta del servidor. 
```
$ scp LHSP.tar user@server:/home/user/
```
Descomprime el archivo
```
$ tar -xvf  LHSP.tar
```
También puedes crear un alias en $ .bashrc. Utiliza un editor de texto 
```
$ vi ~.bashrc
```
Y agrega esta ultima linea: 
```
alias lhsp='python /home/user/LHPS/lhsp.py'
```

## Ejecución
Debes crear un archivo N+p.cub, los 5 archivos .log y tener los 3 archivos .fchk (proyecto Gaussian), luego ejecutar el programa mediante el comando python

Version Linea de Comandos:
```
$ python /home/user/LHSP/lhsp.py
```
o simplemente usado el alias lhsp:
```
$ lhsp
```

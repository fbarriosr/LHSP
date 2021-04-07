## LHSP

Genera archivos .cub visualizables con el programa GaussView o cualquier otro capaz de leer archivos .cub provenientes de Gaussian. Corresponden a los campos escalares del potencial de la hiperblandura local así como de sus dos componentes. No son los mismos archivos que genera el código LHS, de hecho LHSP está en investigación pues se basa en el cálculo del potencial electrostático molecular. Por cada sistema molecular, requiere como alimentación de al menos cinco archivos .log correspondientes al sistema con N, N+1, N+2, N-1, N-2. Si el grado de degeneración en orbitales de frontera LUMO y HOMO es superior a 2, también requiere como alimentación de los archivos .fchk correspondientes al sistema con N+p y N-q electrones, siendo p>2 y q>2.
Utilizable solo en servidores con sistema operativo Linux y siempre tenga instalados y operativos
los programas Gaussian y sus complementarios cubegen y cubman.

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

## LHSP

Es un proyecto "UNIX" para automatizar las rutinas del software Gaussian. Debido a que este presenta una sintaxis compleja para los usuarios no habituados a la programación, lo cual lleva a errores y a perdida de tiempo en entender cómo utilizar el programa.

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

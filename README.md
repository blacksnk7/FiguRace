<h1 align="center">FiguRace</h1>

<div align="center">

</div>

---

<p align="center"> Juego de cartas desarrollado en python para explayar nuestros conocimientos aprendidos en las clases.  
    <br> 
</p>

## Tabla de contenidos

- [Sobre](#about)
- [Inicializar el juego](#getting_started)
- [Construido usando](#built_using)
- [Autores](#authors)

## Sobre <a name = "about"></a>

Este proyecto es un juego totalmente funcional, desarrollado por cuatro estudiantes, para demostrar nuestros aprendizajes en el lenguaje python. La estructura e ideas bases fueron ya dadas por la catedra y tuvimos que programar el esquema dado.

### Prerequisitos

Abrir una terminal de comandos, desplazarse al path actual de figurace y, sobre el equipo o en un ambiente virtual con python mayor a 3.10 instalado, ejecutar el siguiente comando:

```
pip install -r requirements.txt
```

También se pueden instalar las librerías independientemente con los siguientes comandos:

```
pip install PySimpleGUI==4.60.0
pip install pygame==2.1.2
pip install googletrans==4.0.0rc1
pip install pandas==1.4.2
pip install matplotlib==3.5.2
pip install uuid==1.30
pip install notebook==6.4.12
```

Luego se debera desplazar a la carpeta src\data\jupyter_notebooks y ejecutar movies.ipynb, spotify.ipynb y volcanoes.ipynb; los csv quedaran guardados en files_csv.

## Iniciar el juego <a name = "getting_started"></a>

Para poder inicializar el juego primero se deben descargar las librerías detalladas en los prerequisitos (o en el archivo requirements) y ejecutar los tres jupyter notebooks para conseguir los csv deseados en caso de que se no estén o se eliminen. Luego solo se debe ejecutar el archivo figurace.py desde su ubicación.

### Estructura de repositorio

Visión general de la estructura de directorios.

├── README.md <br>
├── figurace.py <br>
├── src <br>
│ ├── common <br>
│ ├── data <br>
│ │ ├── files_csv <br>
│ │ ├── files_csv_to_load <br>
│ │ ├── files_json <br>
│ │ ├── img <br>
│ │ ├── jupyter_notebooks <br>
│ │ ├── music <br>
│ ├── windows

## Construido usando <a name = "built_using"></a>

- [Base de datos de Spotify](https://www.kaggle.com/datasets/muhmores/spotify-top-100-songs-of-20152019) - Dataset
- [Base de datos de volcanos](https://public.opendatasoft.com/explore/dataset/significant-volcanic-eruption-database/table/) - Dataset
- [Base de datos de películas](https://www.kaggle.com/datasets/disham993/9000-movies-dataset) - Dataset
- [Music used from] https://www.FesliyanStudios.com - Musica
- [PySimpleGUI](https://pysimplegui.readthedocs.io/en/latest/) - Python GUI
- [PyGame](https://github.com/pygame/pygame/) - PyGame

## Autores <a name = "authors"></a>

- [@Fabrizio Torrico](https://github.com/Torr1co) - Estudiante
- [@Antonio Glorioso](https://github.com/Ationno) - Estudiante
- [@Austin Myles](https://github.com/Austin-Myles) - Estudiante
- [@Sebastián Ferro](https://github.com/blacksnk7) - Estudiante

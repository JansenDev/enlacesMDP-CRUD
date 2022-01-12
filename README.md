# Applicacion por consola en Python-CRUD

La aplicación permite almacenar enlaces a páginas web bajo una o más
etiquetas y recuperar dichos enlaces en orden cronológico de creación, de
manera paginada al proporcionar una o más etiquetas. Cada enlace
almacenado contará con un título, un URL, un conjunto de etiquetas y una
fecha de creación.
La aplicación es, en esencia, similar a servicios como Raindrop ó Pinboard.

#EJEMPLOS DE USO EN LA LÍNEA DE COMANDOS

## Agregar un enlace

```bash
mdplinks "https://www.mdp.com.pe" --tags empresa,programacion,software --title "Página web de MDP"
```

## Recuperar enlaces
```bash
mdplinks --tags empresa
```

## Editar un enlace
```bash
mdplinks "https://www.mdp.com.pe" --tags empresa,programacion,software --title "Página web de MDP"
```

### Salida:

```bash
* Página web de MDP
URL: https://www.mdp.com.pe
Etiquetas: empresa, programación, software
Fecha y hora de creación: lunes 3 de enero de 2021 18:00:00 -05:00
```

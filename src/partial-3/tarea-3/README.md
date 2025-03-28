# Tarea 3: Detección de Triángulos y Almacenamiento en Base de Datos

| Criterio | Descripción | Puntos |
|----------|-------------|--------|
| Detección de triángulos | Identificamos correcta de triángulos equiláteros, isósceles y escalenos usando OpenCV. | 3 pts |
| Interfaz gráfica (Tkinter) | Diseño funcional y fácil de usar para cargar imágenes y visualizar resultados. | 2 pts |
| Almacenamiento en MySQL | Registro correcto de los conteos en la base de datos a traves de Shell Script. | 2 pts |
| Integracion Shell Script | Comunicacion efectiva entre Python y Shell Script para la inserción de datos. | 2 pts |
| Código limpio y documentado | Código organizado, modular y con comentarios explicativos | 1 pts |

## Process Overview

This project involves detecting triangles in an image, saving the results to a database and integrating Python with a Shell Script for data insertion. Below is a detailed guide to execute the process:

### Start the Database

Ensure the MariaDB service is running:

```sh
sudo service mariadb start
```

### Set Up the Database

Create the database, user, and table if they do not already exist:

```sh
sudo mysql -e "CREATE DATABASE IF NOT EXISTS triangulos; CREATE USER IF NOT EXISTS 'Developer'@'localhost' IDENTIFIED BY 'uth1234'; GRANT ALL PRIVILEGES ON triangulos.* TO 'Developer'@'localhost'; FLUSH PRIVILEGES;"

mysql -u Developer -puth1234 triangulos -e "CREATE TABLE IF NOT EXISTS detecciones (id INT AUTO_INCREMENT PRIMARY KEY, tipo VARCHAR(20) NOT NULL, num_lados INT NOT NULL, perimetro DOUBLE NOT NULL, fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP);"
```

### Run the Detection Script

Execute the Python script to detect triangles in the selected image:

```sh
python deteccion_formas.py
```

This script uses OpenCV to identify triangles (equilateral, isosceles, or scalene) and calculates their properties such as the number of sides and perimeter.

### Save Results to the Database

The `guardar_triangulo.sh` script is used to save the detection results into the `detecciones` table in the database. No need to run this file, this is included automatically in the Python script.

Ensure the script has executable permissions:

```sh

chmod +x guardar_triangulo.sh
```

### Verify the Data

To confirm that the data has been saved correctly, query the database:

```sh
mysql -u Developer -puth1234 triangulos -e "SELECT * FROM detecciones;"
```

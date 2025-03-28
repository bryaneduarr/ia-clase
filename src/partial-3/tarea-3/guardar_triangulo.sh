#!/bin/bash

# Datos de conexión
DB_USER="Developer"
DB_PASS="uth1234"
DB_NAME="triangulos"
DB_HOST="localhost"  # Changed from 'mysql' to 'localhost'

# Parámetros
TIPO_TRIANGULO=$1
NUM_LADOS=$2
PERIMETRO=$3

# Insertar en la base de datos
mysql -h $DB_HOST -u $DB_USER -p$DB_PASS $DB_NAME -e "INSERT INTO detecciones (tipo, num_lados, perimetro, fecha) VALUES ('$TIPO_TRIANGULO', $NUM_LADOS, $PERIMETRO, NOW());"

echo "Registro insertado: $TIPO_TRIANGULO  - Lados: $NUM_LADOS - Perímetro: $PERIMETRO"

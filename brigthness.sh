#!/usr/bin/env sh

delta=5    # cambio en porcentaje por paso (más pequeño = más suave)
min=5      # mínimo permitido en %
max=100    # máximo permitido en %

# Obtener el valor actual en %
current=$(brightnessctl get)
total=$(brightnessctl max)
percent=$(( 100 * current / total ))

# Calcular el nuevo valor
if [ "$1" = "-u" ]; then
    new=$((percent + delta))
elif [ "$1" = "-d" ]; then
    new=$((percent - delta))
else
    echo "¿Subir o bajar el brillo? Usa -u para subir o -d para bajar."
    exit 1
fi

# Limitar al rango permitido
if [ $new -lt $min ]; then
    new=$min
elif [ $new -gt $max ]; then
    new=$max
fi

# Aplicar directamente el porcentaje calculado
brightnessctl set "${new}%"

#!/bin/bash

# Comando para crear el tópico en Kafka
kafka-topics.sh --create --topic crypto_price --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1 --if-not-exists

# Mantener Kafka corriendo después de la creación del tópico
exec "$@"

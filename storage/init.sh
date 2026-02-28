#!/bin/bash
echo "Starting PostgreSQL..."
docker-compose up -d
echo "Waiting for DB..."
sleep 5
echo "Database ready!"

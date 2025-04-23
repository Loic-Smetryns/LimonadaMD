#!/bin/bash

if [ -d "temp_update" ]; then
    rm -r "temp_update"
    echo "Suppression du dossier temp_update."
fi

echo "Création du dossier temp_update"
mkdir "temp_update"

source limonada/env/bin/activate
python limonada/manage.py migrate
deactivate

cd temp_update

python -m venv env
source env/bin/activate
pip install sqlite3-to-mysql

echo "Entrez l'IP de la base de donnée (par défaut 127.0.0.1) : "
read input
ip=${input:-"127.0.0.1"}

echo "Entrez le port de la base de donnée (par défaut 3306) : "
read input
port=${input:-"3306"}

echo "Entrez le nom d'utilisateur SQL (par défaut root) : "
read input
user=${input:-"root"}

echo "Entrez le mot de passe SQL (par défaut password) : "
read input
password=${input:-"password"}

echo "Entrez le nom de la base de donnée (par défaut limonada_db) : "
read input
name=${input:-"limonada_db"}

mysql -u $user -p$password -e "DROP DATABASE IF EXISTS $name;"
mysql -u $user -p$password -e "CREATE DATABASE IF NOT EXISTS $name;"

sqlite3mysql -f ../limonada/db.sqlite3 -d $name -u $user -h $ip -P $port --mysql-password $password

cd ../

if [ -d "temp_update" ]; then
    rm -r "temp_update"
    echo "Suppression du dossier temp_update."
fi
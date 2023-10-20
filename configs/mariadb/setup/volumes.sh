#!/bin/bash

echo -e "\033[1;34m\t●\033[0m Criando diretório de dados: ./${DB_DATA}"
mkdir -p ~/${APP_NAME}/${DB_DATA} && chown -R ${DB_OS_UID}:${DB_OS_GID} ~/${APP_NAME}/${DB_DATA}

echo -e "\033[1;34m\t●\033[0m Criando diretório de logs: ./${DB_LOG}"
mkdir -p ~/${APP_NAME}/${DB_LOG} && chown -R ${DB_OS_UID}:${DB_OS_GID} ~/${APP_NAME}/${DB_LOG}
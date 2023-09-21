#!/bin/bash

vermelho="\e[31m"
verde="\e[32m"
amarelo="\e[33m"
azul="\e[34m"
roxo="\e[38;2;128;0;128m"
reset="\e[0m"

echo -e "${amarelo}|================================================|${reset}"
echo -e "${amarelo}|${reset}        ${roxo}Seja bem-vindo ao Ulek'Checkuser${reset}        ${amarelo}|${reset}"
echo -e "${amarelo}|================================================|${reset}"
echo -e "${amarelo}|${reset}${roxo}Aplicativos Suportados:${reset}                         ${amarelo}|${reset}"
echo -e "${amarelo}|================================================|${reset}"
echo -e "${amarelo}|${reset}${azul}DTunnel${reset}                                         ${amarelo}|${reset}"
echo -e "${amarelo}|${reset}${azul}DTunnel Mod${reset}                                     ${amarelo}|${reset}"
echo -e "${amarelo}|${reset}${azul}Conecta4G${reset}                                       ${amarelo}|${reset}"
echo -e "${amarelo}|${reset}${azul}GLTunnel Mod${reset}                                    ${amarelo}|${reset}"
echo -e "${amarelo}|${reset}${azul}AnyVpn Mod (em testes)${reset}                          ${amarelo}|${reset}"
echo -e "${amarelo}|================================================|${reset}"

echo -e "${amarelo}==>${reset}${azul}Instalar:${reset} ${amarelo}1${reset}"
echo -e "${amarelo}==>${reset}${azul}Desinstalar:${reset} ${amarelo}2${reset}"
echo -e "${amarelo}==>${reset}${azul}Cancelar:${reset} ${amarelo}0${reset}"

read escolha

if [ "$escolha" -eq 1 ]; then
    sudo apt update && sudo apt upgrade && sudo apt install python3 python3-pip && pip install sqlite3 hypercorn colorlog fastapi pydantic
    echo "installed" > checkuserUlekInfo.txt

    git clone https://github.com/UlekBR/UlekCheckUser.git
    echo 'alias UlekCheckUser="nohup python3 /root/UlekCheckUser/menu.py"' >> ~/.bashrc

    echo -e "${roxo}Para iniciar, acesse o menu digitando 'UlekCheckUser' (sem aspas)."
elif [ "$escolha" -eq 2 ]; then
    rm checkuserUlekInfo.txt
    rm -rf UlekCheckUser
elif [ "$escolha" -eq 0 ]; then
    exit 0
else
    echo "Opção inválida. Por favor, digite 1 para instalar, 2 para desinstalar ou 0 para cancelar."
fi

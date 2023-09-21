#!/bin/bash

vermelho="\e[31m"
verde="\e[32m"
amarelo="\e[33m"
azul="\e[34m"
roxo="\e[38;2;128;0;128m"
reset="\e[0m"

echo -e "${amarelo}|================================================|${reset}"
echo -e "${amarelo}|${reset}        ${roxo}Seja bem-vindo ao 'Checkuser${reset}        ${amarelo}|${reset}"
echo -e "${amarelo}|================================================|${reset}"
echo -e "${amarelo}|${reset}${roxo}Aplicativos Suportados:${reset}                         ${amarelo}|${reset}"
echo -e "${amarelo}|================================================|${reset}"
echo -e "${amarelo}|${reset}${azul}DTUNNEL${reset}                                         ${amarelo}|${reset}"
echo -e "${amarelo}|${reset}${azul}DTUNNEL MOD${reset}                                     ${amarelo}|${reset}"
echo -e "${amarelo}|${reset}${azul}CONECTA4G${reset}                                       ${amarelo}|${reset}"
echo -e "${amarelo}|${reset}${azul}GLTUNNEL MOD${reset}                                    ${amarelo}|${reset}"
echo -e "${amarelo}|${reset}${azul}ANYVPN MOD (em testes)${reset}                          ${amarelo}|${reset}"
echo -e "${amarelo}|================================================|${reset}"

echo -e "${amarelo}==>${reset}${azul}Instalar:${reset} ${amarelo}1${reset}"
echo -e "${amarelo}==>${reset}${azul}Desinstalar:${reset} ${amarelo}2${reset}"
echo -e "${amarelo}==>${reset}${azul}Cancelar:${reset} ${amarelo}0${reset}"

read escolha

if [ "$escolha" -eq 1 ]; then
    sudo apt update && sudo apt upgrade && sudo apt install python3 python3-pip && pip install sqlite3 hypercorn colorlog fastapi pydantic
    echo "installed" > TurboCheckInfo.txt

    git clone https://github.com/PhoenixxZ2023/CheckUserTURBO.git
    echo 'alias UlekCheckUser="nohup python3 /root/CheckUserTURBO/menu.py"' >> ~/.bashrc

    echo -e "${roxo}Para iniciar, acesse o menu digitando 'TurboCheck' (sem aspas)."
elif [ "$escolha" -eq 2 ]; then
    rm TurboCheck.txt
    rm -rf TurboCheck
elif [ "$escolha" -eq 0 ]; then
    exit 0
else
    echo "Opção inválida. Por favor, digite 1 para instalar, 2 para desinstalar ou 0 para cancelar."
fi

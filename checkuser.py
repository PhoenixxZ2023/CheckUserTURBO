import asyncio
from datetime import datetime
import os
from fastapi import FastAPI, HTTPException, Request
import sqlite3
import argparse
import hypercorn.asyncio
from hypercorn import Config
import logging
import colorlog

app = FastAPI()


def runCommand(action: str):
    try:
        command = f'{action}'
        result = os.popen(command).readlines()
        final = result[0].strip()
        return final
    except Exception as e:
        return None


def user_usuario(username: str):
    if runCommand(f'grep -wc {username} /etc/passwd') == "1":
        return username
    else:
        return "Not exist"


def user_conectados(username: str):
    return runCommand(f'ps -u {username} | grep sshd | wc -l')


def user_limite(username: str):
    try:
        if os.path.isfile('/root/usuarios.db'):
            with open('/root/usuarios.db', 'r') as f:
                for line in f:
                    parts = line.strip().split()
                    if len(parts) == 2 and parts[0] == username:
                        return parts[1]
    except Exception as e:
        pass

    try:
        connection = sqlite3.connect('/etc/DTunnelManager/db.sqlite3')
        cursor = connection.cursor()
        cursor.execute("SELECT connection_limit FROM users WHERE username = ?", (username,))
        result = cursor.fetchone()
        if result:
            return f"{result[0]}"
        else:
            return "000"
    except Exception as e:
        return str(e)


def user_data(username: str):
    return runCommand(f"date -d \"$(chage -l {username} | grep -i co | awk -F : '{{print $2}}')\" '+%d/%m/%Y'")


def user_dias_restantes(username: str):
    return runCommand(
        f'echo $((($(date -d "$(chage -l {username} | grep -i co | awk -F : \'{{print $2}}\')" "+%s") - $(date -d $(date "+%Y-%m-%d") "+%s")) / 86400))')


def format_date_for_anymod(date_string):
    date = datetime.strptime(date_string, "%d/%m/%Y")
    formatted_date = date.strftime("%Y-%m-%d-")
    return formatted_date






# Configuração do log com colorlog
handler = colorlog.StreamHandler()
handler.setFormatter(colorlog.ColoredFormatter(
    "%(log_color)s%(levelname)s [%(name)s]: %(message)s",
    log_colors={
        'DEBUG': 'cyan',
        'INFO': 'green',
        'WARNING': 'yellow',
        'ERROR': 'red',
        'CRITICAL': 'bold_red',
    }
))
logger = colorlog.getLogger()
logger.addHandler(handler)
logger.setLevel(logging.INFO)



@app.post('/checkUser', response_model=dict)
async def c4g(result: dict, request: Request):
    global username, client_ip
    try:
        username = result['user']
        client_ip = request.client.host

        user_info = {
            "username": username,
            "count_connection": user_conectados(username),
            "expiration_date": user_data(username),
            "expiration_days": user_dias_restantes(username),
            "limiter_user": user_limite(username)
        }
        logger.info(
            f"Usando o CheckUser: [Conecta4g] | Solicitação bem-sucedida para o usuário ({username}) | IP da Requisição: {client_ip}")
        return user_info

    except Exception as e:
        logger.error(
            f"Usando o CheckUser: [Conecta4g] | Solicitação Mal-sucedida para o usuário ({username}) | IP da Requisição: {client_ip}")
        raise HTTPException(status_code=500, detail=str(e))


# Repita o mesmo padrão para as outras duas rotas (/gl/check e /anymod)

@app.get('/gl/check/{username}', response_model=dict)
async def gl(username: str, request: Request):
    global client_ip
    try:
        client_ip = request.client.host
        user_info = {
            "username": username,
            "count_connection": user_conectados(username),
            "expiration_date": user_data(username),
            "expiration_days": user_dias_restantes(username),
            "limit_connection": user_limite(username)
        }
        logger.info(
            f"Usando o CheckUser: [GlTunnel] | Solicitação bem-sucedida para o usuário ({username}) | IP da Requisição: {client_ip}")
        return user_info

    except Exception as e:
        logger.error(
            f"Usando o CheckUser: [GlTunnel] | Solicitação mal-sucedida para o usuário ({username}) | IP da Requisição: {client_ip}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post('/anymod', response_model=dict)
async def anymod(username: str, deviceid: str):
    try:
        user = user_usuario(username)
        online = user_conectados(user)
        limite = user_limite(user)
        device = "false" if online > limite else deviceid
        is_active = "false" if online > limite else "true"
        response = {
            "USER_ID": username,
            "DEVICE": device,
            "is_active": is_active,
            "expiration_date": format_date_for_anymod(user_data(user)),
            "expiry": f"{user_dias_restantes(user)} dias.",
            "uuid": "null"
        }
        logger.info(
            f"Usando o CheckUser: [AnyVPN] | Solicitação bem-sucedida para o usuário ({username}) | IP da Requisição: {client_ip}")
        return response

    except Exception as e:
        logger.error(
            f"Usando o CheckUser: [AnyVPN] | Solicitação mal-sucedida para o usuário ({username}) | IP da Requisição: {client_ip}")
        raise HTTPException(status_code=500, detail=str(e))


def parse_args():
    parser = argparse.ArgumentParser(description="Meu aplicativo com Hypercorn")
    parser.add_argument('--port', type=int, default=5000, help="Porta para executar o aplicativo")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    porta = args.port
    hypercorn_config = Config()
    hypercorn_config.bind = [f"0.0.0.0:{porta}"]
    hypercorn_config.use_reloader = True  # Para desenvolvimento, pode ser removido em produção


    async def run():
        await hypercorn.asyncio.serve(app, hypercorn_config)


    # Executar o loop de eventos assíncrono
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())

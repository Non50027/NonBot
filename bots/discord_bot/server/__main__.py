import subprocess

if __name__=="__main__":
    subprocess.Popen(
        [
            "uvicorn",
            "bots.discord_bot.server.request:app",
            "--host",
            # "0.0.0.0",
            "61.63.220.46",
            "--port", 
            "7615", 
            "--reload",
            "--ssl-keyfile=D:\\DiscordBot\\NonBot\\non.com.tw.key",
            "--ssl-certfile=D:\\DiscordBot\\NonBot\\non.com.tw.pem"
        ],
        shell= False
    )
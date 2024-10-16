& .\\.venv\\Scripts\\Activate.ps1


function Start-NewProcess {
    param(
        [string]$process_name,
        [string]$command
    )
    # 獲取當前工作目錄
    $current_directory = Get-Location

    Start-Process -NoNewWindow -PassThru -FilePath "wt" -ArgumentList "-w 0 new-tab -p `"PowerShell`" --title `"$process_name`" -- pwsh -Command `"cd $current_directory && & .\\.venv\\Scripts\\Activate.ps1 && $command && cmd /c exit`""
    Start-Sleep -Seconds 2
}

function Stop-ProcessById {
    param([int]$process_id)
    Stop-Process -Id $process_id -Force
}
function stop-BotProcess {
    param(
        [string]$bot_command  # Bot 的具體命令或路徑
    )

    # 使用 WMI 查找具體運行 bot 的進程
    $process = Get-WmiObject Win32_Process | Where-Object {
        $_.CommandLine -like "*$bot_command*" -and $_.CommandLine -like "*python*" 
    }
    
    if ($process) {
        foreach ($p in $process) {
            # Write-Host "Found process: ID = $($p.ProcessId)"
            # Write-Host "Name = $($p.Name)"
            Write-Host "Command Line = $($p.CommandLine)"
            Stop-Process -Id $p.ProcessId -Force
            Write-Host "stop: $($p.Name)"
        }
    } else {
        Write-Host "No processes found matching command: $bot_command"
    }
}

# 執行 Django 的遷移並啟動後端
Start-NewProcess -process_name "Django" -command "cd .\\backend && python .\\manage.py makemigrations && python .\\manage.py migrate && python .\\manage.py runserver 0.0.0.0:8615"

# 啟動 Discord Bot
# Start-NewProcess -process_name "Discord Bot" -command "python .\\bots\\discord_bot"
Start-NewProcess -process_name "Bot" -command "python .\\bot"

# 啟動前端
Start-NewProcess -process_name "Vue3" -command "cd .\\frontend && yarn dev --host --port 5615"

# 啟動 Uvicorn
# Start-NewProcess -process_name "Uvicorn" -command "python .\\bots\\discord_bot\\server"

# 啟動 Twitch Bot
# Start-NewProcess -process_name "Twitch Bot" -command "python .\\bots\\twitch_bot"

# 控制界面，讓你能啟動、重啟或停止每個進程
while ($true) {
    
    $command = Read-Host "輸入指令 (-title, stopAll, exit)"
    
    switch ($command) {
        # "dc_server" {
        #     stop-BotProcess  -bot_command "python .\\bots\\discord_bot\\server"
        #     Start-NewProcess -process_name "Uvicorn" -command "python .\\bots\\discord_bot\\server"
        # }
        "twitch" {
            stop-BotProcess  -bot_command "python .\\bots\\twitch_bot"
            Start-NewProcess -process_name "Twitch Bot" -command "python .\\bots\\twitch_bot"
        }
        "discord" {
            # stop-BotProcess  -bot_command "python .\\bots\\discord_bot"
            # Start-NewProcess -process_name "Discord Bot" -command "python .\\bots\\discord_bot"
            stop-BotProcess  -bot_command "python .\\bot"
            Start-NewProcess -process_name "Bot" -command "python .\\bot"
        }
        "stopAll" {
            # 停止 Twitch bot
            stop-BotProcess  -bot_command "python .\\bots\\twitch_bot"
            
            # 停止 Discord bot
            stop-BotProcess  -bot_command "python .\\bots\\discord_bot"
            
            break
        }
        "exit" {
            break
        }
        default {
            Write-Host "無效的指令"
        }
    }
}

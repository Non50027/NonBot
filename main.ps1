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


# 啟動前端
Start-NewProcess -process_name "Vue3" -command "cd .\\frontend && npm run dev --host --port"

# 啟動 fastAPI+ bot
Start-NewProcess -process_name "Bot" -command "python .\\bot"


# 控制界面，讓你能啟動、重啟或停止每個進程
while ($true) {
    
    $command = Read-Host "輸入指令 (bot, exit)"
    
    switch ($command) {
        "bot" {
            stop-BotProcess  -bot_command "python .\\bot"
            Start-NewProcess -process_name "Bot" -command "python .\\bot"
        }
        "exit" {
            break
        }
        default {
            Write-Host "無效的指令"
        }
    }
}

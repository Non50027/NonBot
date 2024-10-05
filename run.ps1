# 啟動虛擬環境
& .\\.venv\\Scripts\\Activate.ps1

switch ($args[0]) {
    # 預設行為
    "" {
        # 執行 Django 的遷移並啟動後端
        python .\\backend\\manage.py makemigrations $args[1]
        python .\\backend\\manage.py migrate $args[1]
        Start-Process -NoNewWindow -FilePath "cmd" -ArgumentList "/c python .\\backend\\manage.py runserver 0.0.0.0:8615" 
        Start-Sleep -Seconds 3
        
        # 啟動前端
        Push-Location .\frontend
        Start-Process -NoNewWindow -FilePath "cmd" -ArgumentList "/c yarn dev --host --port 5615" 
        Pop-Location
        Start-Sleep -Seconds 4
        
        # 啟動 twitch_bot
        Start-Process -NoNewWindow -FilePath "cmd" -ArgumentList "/c python .\\bots\\twitch_bot\\run.py" 
        Start-Sleep -Seconds 5

        # 啟動 discord_bot
        # Start-Process -NoNewWindow -FilePath "cmd" -ArgumentList "/c python .\\bots\\discord_bot\\run.py" 
        python .\\bots\\discord_bot\\run.py

    }
    # 生成 freezefile.txt
    "-f" {
        pip freeze > freezefile.txt
    }
    # 安裝 freezefile.txt 中的包
    "-i" {
        pip install -r freezefile.txt
    }
    # 遷移資料庫
    "-m" {
        python .\\backend\\manage.py makemigrations $args[1]
        python .\\backend\\manage.py migrate $args[1]
    }
    default {
        Write-Host "未知的參數: $args[0]"
    }
}

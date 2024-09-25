# 啟動虛擬環境
& .\\.venv\\Scripts\\Activate.ps1

switch ($args[0]) {
    # 預設行為
    "" {
        # 啟動 discord_bot
        Push-Location .\backend\discord_bot
        Start-Process -NoNewWindow -FilePath "cmd" -ArgumentList "/c python runBot.py" 
        Pop-Location
        
        # 啟動 twitch_bot
        Push-Location .\backend\twitch_bot
        Start-Process -NoNewWindow -FilePath "cmd" -ArgumentList "/c python runBot.py" 
        Pop-Location
        Pop-Location
        
        # 啟動前端
        Push-Location .\frontend
        Start-Process -NoNewWindow -FilePath "cmd" -ArgumentList "/c yarn dev --host --port 5615" 
        Pop-Location
        
        # 執行 Django 的遷移並啟動後端
        python .\\backend\\manage.py makemigrations $args[1]
        python .\\backend\\manage.py migrate $args[1]
        python .\\backend\\manage.py runserver 0.0.0.0:8615
        # Push-Location .\backend
        # Start-Process -NoNewWindow -FilePath "cmd" -ArgumentList "/c python manage.py runserver 0.0.0.0:8615" 
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

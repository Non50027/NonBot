#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import asyncio
import tracemalloc, warnings
# import subprocess  # 用來啟動 Django 伺服器

# from discord_bot.botMain import startBot

def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "無法導入Django"
        ) from exc
        
    execute_from_command_line(sys.argv)
    
    # 將 RuntimeWarning 轉換為 error
    warnings.simplefilter('error', RuntimeWarning)
    
    # 啟動記憶體分配跟蹤
    tracemalloc.start()



if __name__ == '__main__':
    main()

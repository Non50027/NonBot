
def restart_task(func):
    try:
        if func.is_running():
            func.stop()
        func.start()
    except Exception as e:
        print('live task start error', e)
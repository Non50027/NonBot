import os

# 更新 .env 中的值
def update_env_variable(key, new_value):
    # 讀取現有的 .env 檔案內容
    
    file_path= os.path.join(os.path.dirname(__file__).split('\\bot')[0], '.env')
    with open(file_path, "r") as file:
        lines = file.readlines()
        
    # 準備寫入的內容
    updated_lines = []
    found = False

    for line in lines:
        # 去掉空白及換行
        stripped_line = line.strip()
        # 如果這一行是我們要更新的變數
        if stripped_line.startswith(f"{key}="):
            # 更新該變數的值
            updated_lines.append(f"{key}={new_value}\n")
            found = True
        else:
            # 保留其他的變數
            updated_lines.append(line)

    # 如果變數不存在，則新增一行
    if not found:
        updated_lines.append(f"{key}={new_value}\n")
        
    # 將更新後的內容寫回 .env 檔案
    with open(file_path, "w") as file:
        file.writelines(updated_lines)
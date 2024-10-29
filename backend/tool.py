import os, requests
from django.conf import settings

# 讀取 .env
def load_env(file_path):
    with open(file_path) as f:
        for line in f:
            if line.startswith('#') or '=' not in line:
                continue
            key, value = line.strip().split('=', 1)
            os.environ[key] = value

# 將樹狀目錄下的檔案包含路徑輸出為 List
def file_dir_list(url, select):
    ''''
    將樹狀目錄下的檔案包含路徑輸出為 List
    url (str): 根目錄
    select (tuple(str)): 指定你要的檔案 EX : '.py'
    l= []
    for root, dirs, files in os.walk(url):
        if not root.endswith(('.git', '__pycache__')) # 過濾指定目錄
            for file in files:
                if file.endswith(select):  # 指定需要的檔案
                    l.append(os.path.join(root, file))
    return l
    '''
    return [os.path.join(root, file) for root, dirs, files in os.walk(url) if not root.endswith(('.git', '__pycache__', 'events')) for file in files if file.endswith(select) and not file.startswith('_')]

# 全進制轉換器
def convert_base(num: str, from_base: int, to_base: int):
    '''
    全進制轉換器
    num (str): 要轉換的數字
    from_base (int): 原進制 預設為 10
    to_base (int): 目標進制 預設為 16
    '''
    if num == '0':
        return "0"
    
    # 將原始進制數字轉為十進制
    if from_base!= 10:
        num = int(num, from_base)
    else:
        num= int(num)

    # 將十進制轉換為目標進制
    temp = [chr(i) for i in range(48, 58)] + [chr(i) for i in range(65, 91)]
    number = ""
    while num > 0:
        i = num % to_base
        number = temp[i] + number
        num = num // to_base
    return number

# 更新 .env 中的值
def update_env_variable(key, new_value):
    # 讀取現有的 .env 檔案內容
    file_path= os.path.join(settings.BASE_DIR.parent, '.env')
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


import os
import json

def get_image_files(directory):
    # 圖片格式
    image_extensions = ('.png', '.jpg', '.jpeg', '.gif')
    # 圖片列表
    image_files = []
    
    # 遞歸遍歷目錄
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.startswith("_"): continue
            if not file.lower().endswith(image_extensions): continue
            # 構建文件 URI
            file_path = os.path.join(root, file)
            file_uri = f"file:///{file_path.replace('\\', '/')}"
            image_files.append(file_uri)
    
    return image_files

def update_settings(settings_path, images_directory):
    # 讀取當前的 settings.json
    with open(settings_path, 'r', encoding='utf-8') as f:
        settings = json.load(f)
    
    # 獲取圖片列表
    images = get_image_files(images_directory)
    
    # 更新 settings
    if "background.fullscreen" not in settings:
        settings["background.fullscreen"] = {}
    
    settings["background.fullscreen"]["images"] = images
    
    # 保存更新後的 settings.json
    with open(settings_path, 'w', encoding='utf-8') as f:
        json.dump(settings, f, indent=4, ensure_ascii=False)

# 使用示例
settings_path = r"C:\Users\user\AppData\Roaming\Cursor\User\settings.json"
images_directory = r"N:\SubBonus"  # 你的圖片目錄

update_settings(settings_path, images_directory)
print(123)
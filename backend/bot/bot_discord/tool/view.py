import discord, os
from .serve import get_file_dir_list

class SelectFileView(discord.ui.View):
    def __init__(self, *, timeout: float | None = 180, function_name):
        super().__init__(timeout=timeout)
        self.function_name= function_name
        
    # 動態創建檔案選單
    @discord.ui.select(
        placeholder="選擇檔案",
        options=[discord.SelectOption(
            label=_.split('\\')[-1][:-3], 
            value='.'.join(['discord_bot']+ _.split('discord_bot\\')[-1].split('\\'))[:-3]
        ) for _ in get_file_dir_list(os.path.dirname(os.path.dirname(__file__)))]
    )
    async def select_callback(self, interaction: discord.Interaction, select: discord.ui.Select):
        # 當使用者選擇了檔案，這裡會被觸發
        chosen_value = select.values[0]
        chosen_label = next(option.label for option in select.options if option.value == chosen_value)  # 根據 value 找對應的 label
        try:
            await self.function_name(chosen_value)
            await interaction.response.send_message(f"載入 {chosen_label} ... OK", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"失敗: {e}", ephemeral=True)

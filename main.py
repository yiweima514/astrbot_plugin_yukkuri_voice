import os
import subprocess
from astrbot.api.star import Context, Star, register
from astrbot.api.event.filter import on_decorating_result
from astrbot.core.platform.astr_message_event import AstrMessageEvent
from astrbot.core.message.components import Record, Plain
from deep_translator import GoogleTranslator

@register("yukkuri_voice", "Claude", "将回复转换为真正的本地油库里(AquesTalk带完美音调)语音", "1.0.0")
class YukkuriVoice(Star):
    def __init__(self, context: Context):
        super().__init__(context)
        self.translator = GoogleTranslator(source='auto', target='ja')

        # 获取当前插件目录
        self.plugin_dir = os.path.dirname(os.path.abspath(__file__))
        self.exe_path = os.path.join(self.plugin_dir, "YukkuriWrapper.exe")
        self.temp_wav_path = os.path.join(self.plugin_dir, "output.wav")

    def generate_wav(self, text: str) -> bool:
        if not os.path.exists(self.exe_path):
            print("[Yukkuri Plugin] 找不到 YukkuriWrapper.exe 外挂程序！")
            return False

        try:
            # 1. 中文翻译成日文
            ja_text = self.translator.translate(text)
            if not ja_text:
                return False

            # 2. 调用外挂程序生成语音
            # YukkuriWrapper.exe <text> <output.wav>
            # 它在后台会调用 32位的 AqKanji2Koe.dll 进行断句、注音调
            # 然后传给 32位的 AquesTalk32.dll 生成完美的音频
            result = subprocess.run(
                [self.exe_path, ja_text, self.temp_wav_path],
                cwd=self.plugin_dir,
                capture_output=True,
                text=True,
                creationflags=subprocess.CREATE_NO_WINDOW # 隐藏黑框
            )

            if result.returncode == 0 and "SUCCESS" in result.stdout:
                return True
            else:
                print(f"[Yukkuri Plugin] 外挂执行失败: {result.stdout} {result.stderr}")
                return False

        except Exception as e:
            print(f"[Yukkuri Plugin] 生成失败: {e}")
            return False

    @on_decorating_result()
    async def make_yukkuri(self, event: AstrMessageEvent):
        result = event.get_result()
        if not result or not result.chain:
            return

        new_chain = []
        for comp in result.chain:
            if isinstance(comp, Plain) and len(comp.text.strip()) > 0:
                original_text = comp.text.strip()
                new_chain.append(comp) # 保留文字

                # 生成语音并追加 Record
                if self.generate_wav(original_text):
                    new_chain.append(Record(file=self.temp_wav_path))
            else:
                new_chain.append(comp)

        result.chain = new_chain

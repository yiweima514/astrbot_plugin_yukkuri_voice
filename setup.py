import os
import glob
import subprocess

def find_csc():
    # 查找 Windows 系统自带的 C# 编译器
    pattern = r"C:\Windows\Microsoft.NET\Framework\v*\csc.exe"
    matches = glob.glob(pattern)
    if matches:
        return sorted(matches)[-1]
    return None

def main():
    print("--- Yukkuri Voice Plugin 安装脚本 ---")

    # 1. 检查必要文件
    required_paths = [
        "AqKanji2Koe.dll",
        "AquesTalk32.dll",
        "aq_dic",
        "YukkuriWrapper.cs"
    ]

    missing = [p for p in required_paths if not os.path.exists(p)]
    if missing:
        print("❌ 错误: 缺少以下必须的文件或文件夹:")
        for m in missing:
            print(f"  - {m}")
        print("\n请确保您已经将 AQUEST 相关的 32位 DLL 和字典文件夹放置于本目录下。")
        if os.path.exists("AquesTalk.dll") and "AquesTalk32.dll" in missing:
            print("💡 提示: 发现 'AquesTalk.dll'。请将其重命名为 'AquesTalk32.dll'。")
        return

    # 2. 查找编译器
    csc_path = find_csc()
    if not csc_path:
        print("❌ 错误: 找不到 csc.exe 编译器。您的系统似乎没有安装 .NET Framework。")
        return

    print(f"✅ 找到 C# 编译器: {csc_path}")

    # 3. 编译外挂程序
    print("⚙️ 正在编译 YukkuriWrapper.cs 为 32 位程序...")
    cmd = [csc_path, "/nologo", "/platform:x86", "/out:YukkuriWrapper.exe", "YukkuriWrapper.cs"]

    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode == 0:
        print("✅ 成功: YukkuriWrapper.exe 编译完成！现在您可以启动 AstrBot 了。")
    else:
        print("❌ 错误: 编译失败。")
        print(result.stdout)

if __name__ == "__main__":
    main()
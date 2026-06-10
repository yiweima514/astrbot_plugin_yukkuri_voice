using System;
using System.IO;
using System.Runtime.InteropServices;
using System.Text;

namespace Yukkuri
{
    class Program
    {
        [DllImport("AqKanji2Koe.dll", CallingConvention = CallingConvention.StdCall)]
        public static extern IntPtr AqKanji2Koe_Create(string pathDic, ref int pErr);

        [DllImport("AqKanji2Koe.dll", CallingConvention = CallingConvention.StdCall)]
        public static extern void AqKanji2Koe_Release(IntPtr handle);

        [DllImport("AqKanji2Koe.dll", CallingConvention = CallingConvention.StdCall)]
        public static extern int AqKanji2Koe_Convert_utf8(IntPtr handle, byte[] kanji, byte[] koe, int sizeKoe);

        [DllImport("AquesTalk32.dll", CallingConvention = CallingConvention.StdCall)]
        public static extern IntPtr AquesTalk_Synthe_Utf8(byte[] koe, int iSpeed, ref int pSize);

        [DllImport("AquesTalk32.dll", CallingConvention = CallingConvention.StdCall)]
        public static extern void AquesTalk_FreeWave(IntPtr wav);

        static void Main(string[] args)
        {
            if (args.Length < 2)
            {
                Console.WriteLine("Usage: YukkuriWrapper.exe <text> <output.wav>");
                return;
            }

            string text = args[0];
            string outFile = args[1];
            string baseDir = AppDomain.CurrentDomain.BaseDirectory;

            int err = 0;
            string dicPath = Path.Combine(baseDir, "aq_dic");
            IntPtr handle = AqKanji2Koe_Create(dicPath, ref err);
            if (handle == IntPtr.Zero)
            {
                Console.WriteLine("AqKanji2Koe_Create failed: " + err);
                return;
            }

            byte[] inBytes = Encoding.UTF8.GetBytes(text + "\0");
            byte[] outBytes = new byte[8192];

            int res = AqKanji2Koe_Convert_utf8(handle, inBytes, outBytes, outBytes.Length);
            if (res != 0)
            {
                Console.WriteLine("AqKanji2Koe_Convert_utf8 failed: " + res);
                AqKanji2Koe_Release(handle);
                return;
            }

            AqKanji2Koe_Release(handle);

            int size = 0;
            IntPtr wavPtr = AquesTalk_Synthe_Utf8(outBytes, 100, ref size);
            if (wavPtr == IntPtr.Zero)
            {
                Console.WriteLine("AquesTalk_Synthe_Utf8 failed");
                return;
            }

            byte[] wavData = new byte[size];
            Marshal.Copy(wavPtr, wavData, 0, size);
            File.WriteAllBytes(outFile, wavData);

            AquesTalk_FreeWave(wavPtr);
            Console.WriteLine("SUCCESS");
        }
    }
}

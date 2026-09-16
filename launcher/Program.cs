using System;
using System.Diagnostics;
using System.IO;
using System.Reflection;
using System.Windows.Forms;

[assembly: AssemblyTitle("FOMC Dashboard")]
[assembly: AssemblyProduct("FOMC Dashboard XAU/USD")]
[assembly: AssemblyDescription("Bulletin FOMC 2020-2026 - analisa emas XAU/USD")]
[assembly: AssemblyVersion("1.0.0.0")]
[assembly: AssemblyFileVersion("1.0.0.0")]

static class Program
{
    const string ResourceName = "fomc-dashboard.html";

    [STAThread]
    static void Main()
    {
        try
        {
            string appDir = Path.Combine(
                Environment.GetFolderPath(Environment.SpecialFolder.LocalApplicationData),
                "FOMC Dashboard");
            Directory.CreateDirectory(appDir);

            // Dashboard dibawa di dalam exe dan ditulis ulang setiap kali dibuka,
            // jadi versi yang tampil selalu sama dengan exe ini.
            string htmlPath = Path.Combine(appDir, ResourceName);
            using (Stream src = Assembly.GetExecutingAssembly().GetManifestResourceStream(ResourceName))
            using (FileStream dst = File.Create(htmlPath))
            {
                src.CopyTo(dst);
            }

            string url = new Uri(htmlPath).AbsoluteUri;
            string edge = FindEdge();
            if (edge != null)
            {
                // Mode aplikasi: jendela sendiri tanpa address bar. Profil terpisah
                // menyimpan API key Twelve Data dan pengaturan antar sesi.
                string profile = Path.Combine(appDir, "edge-profile");
                string args = "--app=\"" + url + "\""
                    + " --user-data-dir=\"" + profile + "\""
                    + " --window-size=1400,900"
                    + " --no-first-run --no-default-browser-check";
                Process.Start(new ProcessStartInfo(edge, args) { UseShellExecute = false });
            }
            else
            {
                Process.Start(new ProcessStartInfo(url) { UseShellExecute = true });
            }
        }
        catch (Exception ex)
        {
            MessageBox.Show("FOMC Dashboard gagal dibuka:\n\n" + ex.Message,
                "FOMC Dashboard", MessageBoxButtons.OK, MessageBoxIcon.Error);
        }
    }

    static string FindEdge()
    {
        string[] candidates =
        {
            Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.ProgramFilesX86), @"Microsoft\Edge\Application\msedge.exe"),
            Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.ProgramFiles), @"Microsoft\Edge\Application\msedge.exe"),
            Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.LocalApplicationData), @"Microsoft\Edge\Application\msedge.exe"),
        };
        foreach (string c in candidates)
        {
            if (File.Exists(c)) return c;
        }
        return null;
    }
}

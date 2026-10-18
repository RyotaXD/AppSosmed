import flet as ft
import os

def main(page: ft.Page):
    page.title = "AppSosmed"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 30
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.scroll = ft.ScrollMode.ADAPTIVE

    # Komponen UI Dasar
    judul = ft.Text("Menu Downloader", size=22, weight=ft.FontWeight.BOLD, color=ft.colors.CYAN)
    url_input = ft.TextField(
        label="Tempel Link / URL Disini", 
        border_color=ft.colors.MAGENTA,
        width=320,
        border_radius=10
    )
    
    status_text = ft.Text("Status: Siap digunakan", color=ft.colors.YELLOW)
    progress_ring = ft.ProgressRing(visible=False, color=ft.colors.CYAN)

    def download_clicked(e):
        if not url_input.value:
            status_text.value = "❌ URL tidak boleh kosong!"
            status_text.color = ft.colors.RED
            page.update()
            return

        status_text.value = "⏳ Sedang memproses data"
        status_text.color = ft.colors.CYAN
        progress_ring.visible = True
        page.update()

        try:
            # LAZY IMPORT: Modul dipanggil di sini agar Android tidak blank saat loading awal
            import yt_dlp
            import requests
            from rich.console import Console

            console = Console()
            console.log(f"Mencoba mengakses: {url_input.value}")

            # Validasi URL sederhana menggunakan requests
            headers = {'User-Agent': 'Mozilla/5.0'}
            res = requests.head(url_input.value, headers=headers, allow_redirects=True, timeout=5)
            if res.status_code >= 400:
                console.log("URL mungkin tidak valid atau diblokir.")

            # Menyiapkan folder penyimpanan di Android
            save_path = "/storage/emulated/0/Download/AppSosmed"
            if not os.path.exists(save_path):
                os.makedirs(save_path, exist_ok=True)

            ydl_opts = {
                'format': 'bestvideo+bestaudio/best',
                'merge_output_format': 'mp4',
                'outtmpl': f'{save_path}/%(title)s_%(id)s.%(ext)s',
                'quiet': True,
                'no_warnings': True,
            }

            status_text.value = "⏳ Sedang mengunduh video..."
            page.update()

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url_input.value])

            status_text.value = "✅ Sukses! Cek folder Download/AppSosmed"
            status_text.color = ft.colors.GREEN
            url_input.value = ""

        except Exception as ex:
            status_text.value = f"❌ Gagal: Terjadi kesalahan saat download"
            status_text.color = ft.colors.RED
        finally:
            progress_ring.visible = False
            page.update()

    tombol = ft.ElevatedButton(
        "DOWNLOAD", 
        on_click=download_clicked,
        bgcolor=ft.colors.CYAN,
        color=ft.colors.BLACK,
        width=320,
        height=50,
    )

    page.add(
        judul,
        ft.Divider(height=20, color=ft.colors.TRANSPARENT),
        url_input,
        tombol,
        ft.Divider(height=15, color=ft.colors.TRANSPARENT),
        progress_ring,
        status_text
    )

ft.app(target=main)

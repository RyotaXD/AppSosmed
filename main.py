import flet as ft
import yt_dlp
import os

def main(page: ft.Page):
    page.title = "AppSosmed"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 30
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # Fungsi otomatis meminta izin penyimpanan saat aplikasi dibuka (Khusus Android)
    def request_permissions():
        try:
            import permission_handler as ph
            # Meminta izin akses storage/manage external storage
            ph.Permission.STORAGE.request()
            ph.Permission.MANAGE_EXTERNAL_STORAGE.request()
        except Exception:
            pass

    # Jalankan permintaan izin saat halaman dimuat
    page.on_load = lambda _: request_permissions()

    # Komponen Teks
    judul = ft.Text("Menu Downloader", size=22, weight=ft.FontWeight.BOLD, color=ft.colors.CYAN)
    subtitle = ft.Text("YouTube | Facebook | Instagram | TikTok", size=12, color=ft.colors.WHITE70)
    
    # Input URL dan Dropdown
    url_input = ft.TextField(
        label="Tempel Link / URL Disini", 
        hint_text="https://...",
        border_color=ft.colors.MAGENTA,
        width=320,
        border_radius=10
    )
    
    platform_dropdown = ft.Dropdown(
        label="Pilih Platform",
        width=320,
        border_color=ft.colors.MAGENTA,
        border_radius=10,
        options=[
            ft.dropdown.Option("YouTube"),
            ft.dropdown.Option("Facebook"),
            ft.dropdown.Option("Instagram"),
            ft.dropdown.Option("TikTok")
        ]
    )
    
    status_text = ft.Text("Status: Siap mendownload", color=ft.colors.YELLOW)
    progress_ring = ft.ProgressRing(visible=False, color=ft.colors.CYAN)

    def download_clicked(e):
        if not url_input.value or not platform_dropdown.value:
            status_text.value = "❌ URL dan Platform harus diisi!"
            status_text.color = ft.colors.RED
            page.update()
            return

        status_text.value = "⏳ Mengunduh..."
        status_text.color = ft.colors.CYAN
        progress_ring.visible = True
        page.update()

        try:
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

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url_input.value])

            status_text.value = "✅ Berhasil! Cek folder Download/AppSosmed"
            status_text.color = ft.colors.GREEN
            url_input.value = ""
        except Exception as ex:
            status_text.value = f"❌ Gagal mendownload"
            status_text.color = ft.colors.RED
        finally:
            progress_ring.visible = False
            page.update()

    tombol = ft.ElevatedButton(
        "DOWNLOAD SEKARANG", 
        on_click=download_clicked,
        bgcolor=ft.colors.CYAN,
        color=ft.colors.BLACK,
        width=320,
        height=50,
    )

    page.add(
        judul,
        subtitle,
        ft.Divider(height=20, color=ft.colors.TRANSPARENT),
        platform_dropdown,
        url_input,
        tombol,
        ft.Divider(height=15, color=ft.colors.TRANSPARENT),
        progress_ring,
        status_text
    )

ft.app(main)

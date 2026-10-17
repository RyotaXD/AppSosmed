import flet as ft
import yt_dlp
import os

def main(page: ft.Page):
    # Pengaturan dasar halaman aplikasi
    page.title = "RyotaXD Downloader"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 30
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # Komponen Teks
    judul = ft.Text("RYOTAXD DOWNLOADER", size=26, weight=ft.FontWeight.BOLD, color=ft.colors.MAGENTA)
    subtitle = ft.Text("YouTube | Facebook | Instagram | TikTok", size=12, color=ft.colors.WHITE70)
    
    # Input URL dan Dropdown
    url_input = ft.TextField(
        label="Tempel Link / URL Disini", 
        hint_text="https://...",
        border_color=ft.colors.CYAN,
        width=320,
        border_radius=10
    )
    
    platform_dropdown = ft.Dropdown(
        label="Pilih Platform",
        width=320,
        border_color=ft.colors.CYAN,
        border_radius=10,
        options=[
            ft.dropdown.Option("YouTube"),
            ft.dropdown.Option("Facebook"),
            ft.dropdown.Option("Instagram"),
            ft.dropdown.Option("TikTok")
        ]
    )
    
    # Status dan Loading
    status_text = ft.Text("Status: Standby...", color=ft.colors.YELLOW)
    progress_ring = ft.ProgressRing(visible=False, color=ft.colors.MAGENTA)

    # Fungsi Eksekusi Download
    def download_clicked(e):
        if not url_input.value:
            status_text.value = "❌ Masukkan URL terlebih dahulu!"
            status_text.color = ft.colors.RED
            page.update()
            return
        if not platform_dropdown.value:
            status_text.value = "❌ Pilih platform!"
            status_text.color = ft.colors.RED
            page.update()
            return

        status_text.value = f"⏳ Mengunduh dari {platform_dropdown.value}..."
        status_text.color = ft.colors.CYAN
        progress_ring.visible = True
        
        # Matikan tombol sementara agar tidak diklik dua kali
        url_input.disabled = True
        platform_dropdown.disabled = True
        tombol.disabled = True
        page.update()

        try:
            # Path penyimpanan khusus Android
            save_path = "/storage/emulated/0/Download/RyotaXD"
            if not os.path.exists(save_path):
                os.makedirs(save_path)

            ydl_opts = {
                'format': 'bestvideo+bestaudio/best',
                'merge_output_format': 'mp4',
                'outtmpl': f'{save_path}/%(title)s_%(id)s.%(ext)s',
                'quiet': True,
                'no_warnings': True,
            }

            # Menjalankan yt-dlp
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url_input.value])

            status_text.value = f"✅ Berhasil! Cek folder Download/RyotaXD"
            status_text.color = ft.colors.GREEN
            url_input.value = "" # Kosongkan input setelah sukses
            
        except Exception as ex:
            status_text.value = f"❌ Gagal: Link private/tidak valid"
            status_text.color = ft.colors.RED
        finally:
            progress_ring.visible = False
            url_input.disabled = False
            platform_dropdown.disabled = False
            tombol.disabled = False
            page.update()

    # Tombol Download
    tombol = ft.ElevatedButton(
        "DOWNLOAD SEKARANG", 
        on_click=download_clicked,
        bgcolor=ft.colors.MAGENTA,
        color=ft.colors.WHITE,
        width=320,
        height=55,
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10))
    )

    # Menyusun semua komponen ke layar aplikasi
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

# Eksekusi Flet untuk mode aplikasi murni (APK)
ft.app(target=main)

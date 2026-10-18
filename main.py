import flet as ft
import os

def main(page: ft.Page):
    page.title = "AppSosmed Downloader"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 30
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.scroll = ft.ScrollMode.ADAPTIVE

    # UI Komponen
    judul = ft.Text("APPSOSMED DOWNLOADER", size=22, weight=ft.FontWeight.BOLD, color=ft.colors.CYAN)
    subtitle = ft.Text("Versi Ultimate | Support Bulk URL", size=12, color=ft.colors.WHITE70)
    
    platform_dropdown = ft.Dropdown(
        label="Pilih Platform Target",
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

    url_input = ft.TextField(
        label="Tempel Link (Banyak link? Pisahkan dgn spasi/enter)", 
        multiline=True,
        min_lines=1,
        max_lines=4,
        border_color=ft.colors.MAGENTA,
        width=320,
        border_radius=10
    )
    
    status_text = ft.Text("Status: Siap mendownload", color=ft.colors.YELLOW, text_align=ft.TextAlign.CENTER)
    progress_bar = ft.ProgressBar(width=320, visible=False, color=ft.colors.CYAN)

    def download_clicked(e):
        if not url_input.value or not platform_dropdown.value:
            status_text.value = "❌ Platform & URL tidak boleh kosong!"
            status_text.color = ft.colors.RED
            page.update()
            return

        urls = [u.strip() for u in url_input.value.replace(",", " ").split() if u.strip()]
        if not urls: return

        status_text.value = "⏳ Menyiapkan mesin..."
        status_text.color = ft.colors.CYAN
        progress_bar.visible = True
        page.update()

        try:
            import yt_dlp
            import requests
            import urllib3
            from bs4 import BeautifulSoup
            import re
            import time

            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
            session = requests.Session()

            platform = platform_dropdown.value
            base_path = f"/storage/emulated/0/Download/AppSosmed/{platform}"
            if not os.path.exists(base_path):
                os.makedirs(base_path, exist_ok=True)

            for index, url in enumerate(urls, 1):
                status_text.value = f"⏳ Mengunduh {index} dari {len(urls)}...\n[Target: {url[:25]}...]"
                page.update()

                if platform == "TikTok":
                    user_ip, user_loc = "140.213.39.86", "ID"
                    try:
                        trace = session.get("https://ssstik.io/cdn-cgi/trace", verify=False, timeout=10).text
                        for line in trace.split("\n"):
                            if "=" in line:
                                p = line.split("=", 1)
                                if p[0] == 'ip': user_ip = p[1]
                                if p[0] == 'loc': user_loc = p[1]
                    except: pass

                    html_home = session.get("https://ssstik.io/id", verify=False, timeout=10).text
                    token_tt = "Y0FLY3E_"
                    m = re.search(r'name="tt"\s+value="([^"]+)"', html_home)
                    if m: token_tt = m.group(1)

                    dl_headers = {
                        "Host": "ssstik.io",
                        "User-Agent": "Mozilla/5.0 (Linux; Android 14; V2201 Build/UP1A.231005.007)",
                        "Accept": "*/*",
                        "X-Requested-With": "mark.via.gp",
                        "Content-Type": "application/x-www-form-urlencoded",
                        "Referer": "https://ssstik.io/id"
                    }
                    post_data = {"id": url, "locale": "id", "tt": token_tt, "debug": f"ab=1&loc={user_loc}&ip={user_ip}"}
                    
                    res = session.post("https://ssstik.io/abc?url=dl", data=post_data, headers=dl_headers, verify=False, timeout=10).text
                    soup = BeautifulSoup(res, "html.parser")
                    user_node = soup.select_one('#avatarAndTextUsual h2')
                    username = user_node.text.strip() if user_node else "TikToker"
                    
                    video_node = soup.find("a", class_=lambda x: x and "without_watermark" in x)
                    if video_node:
                        video_url = video_node.get("href")
                        filename = f"{re.sub(r'[^\w\-_\.]', '', username)}_{int(time.time())}.mp4"
                        filepath = os.path.join(base_path, filename)
                        
                        res_file = session.get(video_url, stream=True, verify=False, timeout=30)
                        with open(filepath, 'wb') as f:
                            for chunk in res_file.iter_content(chunk_size=1024*1024):
                                if chunk: f.write(chunk)
                    else:
                        continue
                else:
                    ydl_opts = {
                        'format': 'bestvideo+bestaudio/best',
                        'merge_output_format': 'mp4',
                        'outtmpl': f'{base_path}/%(title)s_%(id)s.%(ext)s',
                        'quiet': True,
                        'no_warnings': True,
                        'ignoreerrors': True
                    }
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        ydl.download([url])

            status_text.value = f"✅ PROSES SELESAI!\nCek Folder: Download/AppSosmed/{platform}"
            status_text.color = ft.colors.GREEN
            url_input.value = ""

        except Exception as ex:
            status_text.value = f"❌ Terjadi kesalahan saat memproses data."
            status_text.color = ft.colors.RED
        finally:
            progress_bar.visible = False
            page.update()

    tombol = ft.ElevatedButton(
        "M U L A I   D O W N L O A D", 
        on_click=download_clicked,
        bgcolor=ft.colors.CYAN,
        color=ft.colors.BLACK,
        width=320,
        height=50,
    )

    page.add(
        judul,
        subtitle,
        ft.Divider(height=15, color=ft.colors.TRANSPARENT),
        platform_dropdown,
        url_input,
        tombol,
        ft.Divider(height=10, color=ft.colors.TRANSPARENT),
        progress_bar,
        status_text
    )

ft.app(main)
    

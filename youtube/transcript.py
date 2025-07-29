import os

import yt_dlp


def download(url):
    ydl_opts = {
        "writeautomaticsub": True,
        "skip_download": True,
        "subtitleslangs": ["en"],
        "subtitlesformat": "srt",
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url)
        filename = ydl.prepare_filename(info_dict)
        ydl.download(url)

        subtitle_filename = filename.replace(filename.split(".")[-1], "en.srt")

        with open(subtitle_filename, "r") as f:
            content = f.read()

        # remove empty lines
        content = "\n".join(
            [
                line
                for line in content.split("\n")
                if line.strip() and not line.isdigit() and "-->" not in line
            ]
        )

        # delete file
        os.remove(subtitle_filename)

        return content

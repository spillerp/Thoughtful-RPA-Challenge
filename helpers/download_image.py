from RPA.HTTP import HTTP
import os


class ImageDownloader:
    def __init__(self, download_dir="output/"):
        self.http = HTTP()
        self.download_dir = download_dir
        if not os.path.exists(self.download_dir):
            os.makedirs(self.download_dir)

    def download_image(self, image_src, filename, format: str | None = None):
        if format is None:
            download_path = os.path.join(self.download_dir, filename)
        else:
            download_path = os.path.join(self.download_dir, filename + format)

        self.http.download(url=image_src, target_file=download_path)
        print(f"Image downloaded successfully to {download_path}")
        return download_path

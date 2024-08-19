from RPA.Excel.Files import Files
from .download_image import ImageDownloader
import logging
import re


class WriteToExcel:
    def __init__(self):
        self.output_path = 'output/news_data.xlsx'
        self.worksheet = 'data'
        self.lib = Files()
        self.image = ImageDownloader()

    def write_news_data(self, news_list, search_phrase):
        """Write news data to an Excel file."""
        self.lib.create_workbook(self.output_path, "xlsx", self.worksheet)

        try:
            headers = [
                "Title", "Description", "Author", "Picture Filename",
                "Search Phrase Count", "Words in Phrase Count", "Contains Money"
            ]
            self.lib.append_rows_to_worksheet([headers], self.worksheet)

            for news in news_list:
                index = news.get('index', 0)
                title = news.get('h2_text', '')
                description = news.get('p_text', '')
                author = news.get('author', 'Unknown')
                img_src = news.get('img_srcs', '')
                picture_filename = f"image{index}"

                if img_src:
                    self.image.download_image(img_src, picture_filename, '.jpg')

                search_phrase_words = search_phrase.lower().split()
                partial_phrase_count = 0
                if len(search_phrase_words) > 1:
                    for word in search_phrase_words:
                        word = r'\b' + re.escape(word) + r'\b'
                        partial_phrase_count += len(re.findall(word, title.lower()))
                        partial_phrase_count += len(re.findall(word, description.lower()))
                search_phrase_count = (
                    title.lower().count(search_phrase.lower()) +
                    description.lower().count(search_phrase.lower())
                )

                money_pattern = re.compile(
                    r"(\$\d+(?:,\d{3})*(?:\.\d+)?|\d+(?:\.\d+)?\s?"
                    r"(dollars|USD))"
                )
                money_in_text = bool(
                    money_pattern.search(title) or money_pattern.search(description)
                )

                row = [
                    title, description, author, picture_filename,
                    search_phrase_count, partial_phrase_count, money_in_text
                ]
                self.lib.append_rows_to_worksheet([row], self.worksheet)

            self.lib.save_workbook(self.output_path)

        except Exception as e:
            logging.info(f"Error writing data to Excel: {str(e)}")
            self.lib.close_workbook()

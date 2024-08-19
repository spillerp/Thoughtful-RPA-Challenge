from helpers import ImageDownloader, CustomSelenium, WriteToExcel
from utils import DataStorage, WorkItemManager
from locators import Locators
from robocorp.tasks import task
import logging


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

logger.info("Initiating Helpers")
selenium = CustomSelenium()
donwload = ImageDownloader()
locators = Locators()
excel = WriteToExcel()

logger.info("Initiating Utils")
data = DataStorage()
wi = WorkItemManager()

logger.info("Instatiating Web Locators")
home_search = locators.HOMEPAGE_SEARCH
search_input = locators.SEARCH_INPUT
search_btn = locators.SEARCH_BUTTON
search_results = locators.SEARCH_RESULTS
first_result = locators.FIRST_CHILD
load_more_btn = locators.LOAD_MORE_BUTTON


@task
def RetrieveInputData():
    logger.info("Retrieving Input Data")
    try:
        input_data = wi.list_variables()
        search_phrase = input_data['search_phrase']
        number_of_news = input_data['number_of_news']
        data.set_data("search_phrase", search_phrase)
        data.set_data("number_of_news", number_of_news)
    except Exception as e:
        logger.info(f"Error while retrieving input data: {str(e)}")


@task
def WebSearch():
    logger.info("Initiating Browser Search")
    try:
        search_phrase = data.get_data("search_phrase")
        selenium.set_webdriver()
        selenium.open_url("https://gothamist.com/")
        selenium.click_button(home_search)
        selenium.input_text(search_input, search_phrase, True)
        selenium.wait_for_element(first_result)
    except Exception as e:
        logger.info(f"Error in browser search: {str(e)}")


@task
def ExtractNewsData():
    logger.info("Extracting News Data")
    try:
        number_of_news = data.get_data("number_of_news")
        news_count = selenium.count_childs(search_results)
        while news_count < number_of_news:
            selenium.click_button(load_more_btn)
            news_count = selenium.count_childs(search_results)
        all_news = selenium.get_info_from_childs(search_results)
        if len(all_news) > number_of_news:
            all_news = all_news[:number_of_news]
        data.set_data("search_results", all_news)
    except Exception as e:
        logger.info(f"Error while extracting news data: {str(e)}")


@task
def FillExcel():
    logger.info("Filling Excel")
    try:
        search_phrase = data.get_data("search_phrase")
        results = data.get_data("search_results")
        excel.write_news_data(results, search_phrase)
    except Exception as e:
        logger.info(f"Error while filling excel: {str(e)}")

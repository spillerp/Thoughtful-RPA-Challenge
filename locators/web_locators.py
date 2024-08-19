class Locators:
    HOMEPAGE_SEARCH = (
        '//*[@id="__nuxt"]/div/div/main/header/div[1]/div[2]/div[2]/button'
    )
    SEARCH_INPUT = '//*[@id="search"]/input'
    SEARCH_BUTTON = '//*[@id="search"]/button'
    SEARCH_RESULTS = '//*[@id="resultList"]/div[2]'
    LOAD_MORE_BUTTON = (
        '//*[@id="resultList"]/div[2]/button'
    )
    FIRST_CHILD = '//*[@id="resultList"]/div[2]/div[1]'

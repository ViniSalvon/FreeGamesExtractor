# URLS: 
URL_MAIN = 'https://old.reddit.com/r/Freegamestuff/'

# WebDriverWait
WDW_TIMEOUT_0 = 30    # tempo de timeout em segundos
WDW_PF_0      = 1     # tempo de espera entre tentativas

# XPATHES: 
XP_TITLES      = ".//a[@data-event-action='title']"
XP_DIV_ENTRIES = "//div[@class='top-matter']"
XP_ENTRY_TIME  = ".//time[@class='']"
XP_ENTRIES     = "//div[@class='top-matter' and not(contains(., 'promoted'))]"

# QUANTAS ENTRADAS SALVAR NO JSON? Deixe None para salvar todas.
SAVE_ENTRIES = 5


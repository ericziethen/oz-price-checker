from urllib.parse import urljoin

LOCAL_SERVER_HTTP = R'http://localhost:8080'

INVALID_XPATH = 'invalid-xpath/'

TEST_PAGE_NOT_FOUND = urljoin(LOCAL_SERVER_HTTP, 'ThisDoesntExist.html')
TEST_PAGE_WITH_PRICE_20 = urljoin(LOCAL_SERVER_HTTP, 'SinglePageNoJSWithPrice20.html')
TEST_PAGE_WITH_PRICE_20_XPATH = '//price/text()'

TEST_PAGE_WITH_PRICE_100 = urljoin(LOCAL_SERVER_HTTP, 'SinglePageNoJSWithPrice100.html')

TEST_PAGE_WITH_PRICE_12_95 = urljoin(LOCAL_SERVER_HTTP, 'SinglePageNoJSWithPrice12.95.html')
TEST_PAGE_WITH_PRICE_12_95_XPATH_WHOLE = '//price-whole/text()'
TEST_PAGE_WITH_PRICE_12_95_XPATH_FRACTION = '//price-fraction/text()'

HTML_WITH_PRICE = ("""
    <!DOCTYPE html>
    <html>
        <body>
            <price class="dollar-value">20</price>
        </body>
    </html>
    """)

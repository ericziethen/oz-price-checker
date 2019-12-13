from urllib.parse import urljoin

LOCAL_SERVER_HTTP = R'http://localhost:8080'

TEST_PAGE_NOT_FOUND = urljoin(LOCAL_SERVER_HTTP, 'ThisDoesntExist.html')
TEST_PAGE_WITH_PRICE_20 = urljoin(LOCAL_SERVER_HTTP, 'SinglePageNoJSWithPrice20.html')
TEST_PAGE_WITH_PRICE_100 = urljoin(LOCAL_SERVER_HTTP, 'SinglePageNoJSWithPrice100.html')


HTML_WITH_PRICE = ("""
    <!DOCTYPE html>
    <html>
        <body>
            <price class="dollar-value">20</price>
        </body>
    </html>
    """)

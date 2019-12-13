from urllib.parse import urljoin

LOCAL_SERVER_HTTP = R'http://localhost:8080'

TEST_PAGE_NOT_FOUNT = urljoin(LOCAL_SERVER_HTTP, 'ThisDoesntExist.html')
TEST_PAGE_WITH_PRICE = urljoin(LOCAL_SERVER_HTTP, 'SinglePageNoJSWithPrice.html')


HTML_WITH_PRICE = ("""
    <!DOCTYPE html>
    <html>
        <body>
            <price class="dollar-value">20</price>
        </body>
    </html>
    """)

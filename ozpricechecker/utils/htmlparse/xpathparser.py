"""Parse HTML using Xpath."""

import lxml  # nosec
import lxml.html  # nosec
import lxml.etree  # nosec


def get_xpath_from_html(xpath, html_source):
    """Get the xpath value from the given html."""
    # logger.info(F'get_xpath_from_html Xpath: {xpath} HTML:\n">>>>>{html_source}<<<<<"')
    try:
        # pylint: disable=c-extension-no-member
        root = lxml.etree.fromstring(html_source)  # nosec
        # pylint: enable=c-extension-no-member
        result = root.xpath(xpath)
    except (lxml.etree.XPathEvalError, lxml.etree.XMLSyntaxError) as error:  # pylint: disable=c-extension-no-member
        raise ValueError(F'Xpath Error for "{xpath}" - {type({error})}: {error}')
    else:
        if result:
            return result[0]

    return None

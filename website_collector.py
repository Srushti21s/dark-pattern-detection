
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup


def collect_website(url):

    print("Opening website...")

    with sync_playwright() as p:

        browser = p.chromium.launch(headless=True)

        page = browser.new_page()

        page.goto(
            url,
            wait_until="domcontentloaded",
            timeout=30000
        )

        page.wait_for_timeout(2000)

        html = page.content()

        soup = BeautifulSoup(html, "html.parser")

        # Remove unnecessary HTML elements
        for tag in soup(["script", "style", "noscript"]):
            tag.decompose()

        # Extract webpage text
        text = soup.get_text(separator=" ", strip=True)

        # Extract buttons
        buttons = [
            b.get_text(" ", strip=True)
            for b in soup.find_all("button")
        ]

        # Extract links
        links = [
            a.get_text(" ", strip=True)
            for a in soup.find_all("a")
        ]

        browser.close()

        return {
            "text": text,
            "buttons": buttons,
            "links": links
        }


# Test the function
if __name__ == "__main__":

    result = collect_website("https://example.com")

    print("\nWEBSITE TEXT:")
    print(result["text"])

    print("\nBUTTONS:")
    print(result["buttons"])

    print("\nLINKS:")
    print(result["links"])

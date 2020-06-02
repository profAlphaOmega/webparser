from Crawler import Crawler

crawler = Crawler("https://www.nike.com")
payload = dict()
# payload.update(crawler.get_footer())
payload.update(crawler.get_navigation())
# payload.update(crawler.get_imgs())
payload.update(crawler.get_hero())
payload.update(crawler.get_favicons())
payload.update(crawler.get_anchors())
payload.update(crawler.get_logos())
payload.update(crawler.get_paragraphs())
payload.update(crawler.get_spans())
payload.update(crawler.get_htags())


print(payload)

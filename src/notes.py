# headers = {
        #     'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
        #     'Accept': 'text/html',
        #     'Cache-Control': 'no-cache',
        #     'Accept-Encoding': 'gzip, deflate, br',
        #     'Accept-Language': 'en-US,en',
        #     'Connection': 'keep-alive',
        # }

# try:
        #     self.page = requests.get(url, headers=headers, timeout=5)
        # except requests.Timeout as e:
        #     print(f"TIMEOUT: {str(e)}")




# How to filter
# On class
#   soup.find_all(class_=re.compile("site-nav__link"))
# You can compound as well (2-ways)
#   soup.find_all(class_=re.compile("site-nav__link"), href="/")
#   soup.find_all(attrs={"class":"site-nav__link"}, href="/")
# This is how you search for specific (exact) classes
#   soup.find_all("p", class_="body strikeout")

# On other non-supported attrs
#   soup.find_all(attrs={"name": "email"})

# You can also do some psuedo selector action
# soup.select("span.site-nav__link-menu-label")
# # <span class="site-nav__link-menu-label">Menu</span>
#   soup.select(".site-nav__link")
#   soup.select("#someid")
# You can pass multiple
#     soup.select("#link1,#link2")

# Searching for strings
# soup.find_all(string="Elsie")
# # [u'Elsie']
#
# soup.find_all(string=["Tillie", "Elsie", "Lacie"])
# # [u'Elsie', u'Lacie', u'Tillie']
#
# soup.find_all(string=re.compile("Dormouse"))
# [u"The Dormouse's story", u"The Dormouse's story"]
#
# def is_the_only_string_within_a_tag(s):
#     """Return True if this string is the only child of its parent tag."""
#     return (s == s.parent.string)
#
# soup.find_all(string=is_the_only_string_within_a_tag)
# # [u"The Dormouse's story", u"The Dormouse's story", u'Elsie', u'Lacie', u'Tillie', u'...']

# To find only direct children, set recursive to False
# soup.html.find_all("title", recursive=False)

# Finds an href of an anchor in the first element of ALL instance of a regex class search
#   soup.find_all(class_=re.compile("product-single__thumbnail*"))[0].find('a').attrs['href']
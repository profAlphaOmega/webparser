from urllib.parse import urlparse
from bs4 import BeautifulSoup
import requests
import re
from utils import relative_path_check, string_striper, add_header_args, dedup

from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class Crawler:
    def __init__(self, url):
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
            'Accept': 'text/html',
            'Cache-Control': 'no-cache',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en',
            'Connection': 'keep-alive',
        }

        # Chrome Headless Browsers Setup
            # https://intoli.com/blog/running-selenium-with-headless-chrome/
        options = webdriver.ChromeOptions()
        options = add_header_args(options, self.headers)
        options.add_argument('headless')
        driver = webdriver.Chrome(executable_path='/home/lupin/sites/webparser/src/chromedriver', options=options) 
        
        self.url_attrs = urlparse(url)
        driver.get(url) 
        self.soup = BeautifulSoup(driver.page_source, 'html.parser')

    @property
    def hostname(self):
        return self.url_attrs.hostname

    @property
    def scheme(self):
        return self.url_attrs.scheme

    @property
    def full_hostname(self):
        return self.scheme + '://' + self.hostname



    def get_imgs(self):
        imglist = self.soup.find_all('img')
        iconlist = self.soup.find_all("link", rel=re.compile("icon", re.IGNORECASE))
        imgslist = imglist + iconlist
        results = list()
        for img in imgslist:
            for k, path in img.attrs.items():
                if any(x in k for x in ['src', 'href']):
                    d = dict()
                    if relative_path_check(path):
                        d["path"] = f"{path}"
                    else:
                        d["path"] = f"{self.full_hostname}{path}"
                    results.append(d)
        return dict(imgs=results)

    def get_favicons(self):
        favicon = self.soup.find("link", rel="icon")
        favlink = self.soup.find_all("link", href=re.compile("favicon", re.IGNORECASE))
        favimg = self.soup.find_all("img", src=re.compile("favicon", re.IGNORECASE))
        
        favlist = [favicon] + favlink + favimg
        results = list()
        for f in favlist:
            for k, path in f.attrs.items():
                if any(x in k for x in ['src', 'href']):
                    d = dict()
                    if relative_path_check(path):
                        d["path"] = f"{path}"
                    else:
                        d["path"] = f"{self.full_hostname}{path}"
                    results.append(d)
        results = dedup(results)
        return dict(favicons=results)

    def get_logos(self):
        logoimg = self.soup.find_all("img", src=re.compile("logo", re.IGNORECASE))
        logolink = self.soup.find_all("link", href=re.compile("logo", re.IGNORECASE))
        logolist = logoimg + logolink
        results = list()
        for l in logolist:
            for k, path in l.attrs.items():
                if any(x in k for x in ['src', 'href']):
                    d = dict()
                    if relative_path_check(path):
                        d["path"] = f"{path}"
                    else:
                        d["path"] = f"{self.full_hostname}{path}"
                    results.append(d)
        return dict(logos=results)

    def get_anchors(self):
        anchors = self.soup.find_all('a')
        results = list()
        for anchor in anchors:
            # IF <img> tag in child
            for k, v in anchor.attrs.items():
                if 'href' in k:
                    d = dict()
                    d["contents"] = string_striper(anchor.text)
                    d["path"] = f"{self.full_hostname}{v}"
                    results.append(d)
        return dict(anchors=results)

    def get_htags(self):
        htags = self.soup.find_all(re.compile("h[1-6+] *", re.IGNORECASE))
        results = list()
        for h in htags:
            # Make sure there is content, some h1's are imgs
            if h.string:
                d = dict()
                d["contents"] = string_striper(h.string)
                d["name"] = h.name
                results.append(d)
        return dict(htags=results)

    def get_paragraphs(self):
        paragraphs = self.soup.find_all('p')
        results = list()
        for p in paragraphs:
            # Make sure there is content, some h1's are imgs
            if p.string:
                d = dict()
                d["contents"] = string_striper(p.string)
                d["name"] = p.name
                results.append(d)
        return dict(p=results)

    def get_spans(self):
        spans = self.soup.find_all('span')
        results = list()
        for s in spans:
            # Make sure there is content, some h1's are imgs
            if s.string:
                d = dict()
                d["contents"] = string_striper(s.string)
                d["name"] = s.name
                results.append(d)
        return dict(spans=results)



    def get_hero(self):
        hero_section_id = self.soup.find_all("section", id=re.compile("hero", re.IGNORECASE))
        hero_section_c = self.soup.find_all("section", class_=re.compile("hero", re.IGNORECASE))
        hero_sections = hero_section_c + hero_section_id
        if not hero_sections:
            div_section_id = self.soup.find_all("div", id=re.compile("hero", re.IGNORECASE))
            div_section_c = self.soup.find_all("div", class_=re.compile("hero", re.IGNORECASE))
            div_sections = div_section_c + div_section_id
            pass
        if hero_section_id:
            pass
        if hero_section_c:
            pass
        # test for divs next, have to be careful to avoid dups if sections are found
        # maybe just exit out after finding something in the section, cause chances are there will be nested divs
        return


    def find_element(self, elm):
        ''' in order due to typical structure of links
        '''
        e = dict()

        # href
        try:
            e["href"] = elm.attrs.get('href')
            if e["href"]:
                if relative_path_check(e["href"]):
                    e["href"] = f"{self.full_hostname}{e['href']}"
        except AttributeError:
            e["href"] = None
 
        if not e["href"]:
            try:
                for descendant in elm.descendants:
                    try:
                        e["href"] = descendant.attrs.get('href')
                        if e["href"]:
                            if relative_path_check(e["href"]):
                                e["href"] = f"{self.full_hostname}{e['href']}"
                            break
                    except AttributeError:
                        continue
            except AttributeError:
                pass

        # string
        try:
            e["string"] = elm.string
        except AttributeError:
            e["string"] = None

        if not e["string"]:
            try:
                for descendant in elm.descendants:
                    try:
                        if descendant.string:
                            e["string"] = string_striper(descendant.string)
                            break
                    except AttributeError:
                        continue
            except AttributeError:
                pass
        return e


    def get_navigation(self):
        ''' Only a find() and not find_all() because we don't want to construct a nav with potential duplicate links,
            if it were a mobile nav element for example.
        '''
        # TODO: try to find icons or imgs in nav links if no string is found
        results = list()
        navs = self.soup.find_all('nav')

        if navs:
            li_results = list()
            li_a_results = list()
            li_button_results = list()

            # results = list()
            ss = list()
            for nav in navs:
                li_elements = list()

                ss += nav.stripped_strings                
                # descendants
                for gc in nav.descendants:
                    try:
                        li_elements += gc.find_all('li')
                    except AttributeError:
                        continue

                if li_elements:
                    li_a_elements = list()
                    li_button_elements = list()
                    
                    for li_elm in li_elements:
                        e = self.find_element(li_elm)
                        e["context"] = li_elm.name
                        e["type"] = "link"
                        li_results.append(e)

                        # find specific types of elements only
                        li_a_elements.append(li_elm.find('a'))
                        li_button_elements.append(li_elm.find('button'))

                    if li_a_elements:
                        for li_a_element in li_a_elements:
                            e = self.find_element(li_a_element)
                            e["context"] = "a"
                            e["type"] = "link"
                            li_a_results.append(e)
                    
                    if li_button_elements:
                        for li_button_element in li_button_elements:
                            e = self.find_element(li_button_element)
                            e["context"] = "button"
                            e["type"] = "link"
                            li_button_results.append(e)
            
            li_results = dedup(li_results)
            li_a_results = dedup(li_a_results)
            li_button_results = dedup(li_button_results)

        return dict(nav=dict(a=li_a_results,buttons=li_button_results, all=li_results,ss=ss))


    def get_footer(self):
        # results = list()
        li_results = list()
        footers = self.soup.find_all('footer')
        if footers:
            for footer in footers:
                li_elements = list()
                for gc in footer.descendants:
                    try:
                        li_elements += gc.find_all('li')
                    except AttributeError:
                        continue
                    
                if li_elements:
                    li_results = list()
                    
                    for li_elm in li_elements:
                        e = self.find_element(li_elm)
                        e["context"] = li_elm.name
                        e["type"] = "link"
                        li_results.append(e)
                    li_results = dedup(li_results)
        
        return dict(footer=dict(all=li_results))
     
#!/usr/bin/env python
from __future__ import print_function

try: # Python 3
    from urllib.request import urlopen
    from urllib.parse import urlencode
except ImportError: # Python 2
    from urllib import urlopen, urlencode
import argparse
import sys
import os
from pydoc import pager
from bs4 import BeautifulSoup as Soup
from bs4.element import Tag
import requests
from bs4 import BeautifulSoup
import csv

def prompt(*args):
    old_stdout = sys.stdout
    try:
        sys.stdout = sys.stderr
        return raw_input(*args) if hasattr(__builtins__, 'raw_input') else input(*args)
    finally:
        sys.stdout = old_stdout


def parse_lyrics_page(url):
    soup = make_soup(url)
    return [div for div in soup.findAll('div')][22].text.strip()

def make_soup(url):
    return Soup(urlopen(url).read(), 'html.parser')

def splitter(n, s):
    pieces = s.split()
    return (" ".join(pieces[i:i+n]) for i in range(0, len(pieces), n))

def get_lyrics(search, url):
    results = [td for td in make_soup('http://search.azlyrics.com/search.php?' + urlencode({'q': search})).findAll('td') if td and td.find('a')][:-1]
    outp = []
    final_list = []
    song = []
    for n, td in enumerate(results):
        x = ""
        for a in td.contents[1:4]:
            if type(a) is Tag:
                x += a.text
            else:
                x += a
        if "0. 1\n2" not in x:
            song = x.strip().split("by")
            if song[0].strip().lower() == search.strip().lower():
                #print("MATCH = ** "+search+" ** "+song[0])
                if search == "wouldn’t you agree":
                    print("wouldn’t you agree")
                outp.append(x.strip())
                final_list.append([url, search, song[0], song[1]])
            
    if len(outp) > 0:
        #print('Results for "'+search+'"', end='\n\t', file=sys.stderr)
        #print('\n\t'.join(outp), file=sys.stderr)    
        #print('Results for: '+search+", length = "+str(len(outp)))
        #print(outp)
        print("FOUND = "+str(final_list))
        with open("Csongs.csv", 'a+') as f:
            fc = csv.writer(f, lineterminator='\n')
            fc.writerows(final_list)
        return

def main():
    #url = input("Enter URL\n")

    urlList = [
"https://www.outsystems.com/blog/posts/masters-front-end-universe/",
"https://www.outsystems.com/blog/small-budget-cross-platform-mobile-app-development-tools-compared.html",
"https://www.outsystems.com/blog/posts/securing-outsystems-apis-oauth2/",
"https://www.outsystems.com/blog/free-cross-platform-mobile-app-development-tools-compared.html",
"https://www.outsystems.com/blog/posts/low-code_conversations-with-myself/",
"https://www.outsystems.com/blog/cross-platform-mobile-app-development-tools-compared.html",
"https://www.outsystems.com/blog/posts/how-to-create-uber-like-address-selector/",
"https://www.outsystems.com/blog/posts/6-scaling-considerations-mobile-apps/",
"https://www.outsystems.com/blog/posts/creating-front-end-universe/",
"https://www.outsystems.com/blog/posts/building-iot-mobile-app/",
"https://www.outsystems.com/blog/posts/fun-with-feature-flags-live-mobile-apps/",
"https://www.outsystems.com/blog/posts/product-design-team-builds-product-users-love/",
"https://www.outsystems.com/blog/posts/building-blockchain-enabled-app/"
]
    for onePage in urlList:
        page = requests.get(onePage)
        #print(page.status_code)

        soup = BeautifulSoup(page.content, 'html.parser')
        full_content = soup.find_all(class_='col-xs-12 col-sm-8 col-sm-offset-2')

        #print("Title = "+soup.title.string)
        full_text = ""
        search_term = []

        for par in full_content:
            full_text += par.get_text() 

        full_text = ' '.join(full_text.split())

        dot_string_list = full_text.split(".")

        for i in dot_string_list:
            for piece in splitter(3, i):
                    search_term.insert(len(search_term), piece)

        for term in search_term:
            if len(term.split()) >= 3:
                get_lyrics(term, onePage)

if __name__ == '__main__':
    sys.exit(main())

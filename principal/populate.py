from django.http.response import HttpResponseRedirect, HttpResponse
from principal.models import ReleasesDiscogs, ReleasesBeatport, ReleasesJuno, AllReleases
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
import requests
from bs4 import BeautifulSoup
import concurrent.futures
from datetime import datetime
import re
import json
import os

ARL = "f7bf81223f117d96a012d7fd7c7b3090932438264ac5b8f82aa7d17f975560969c64b437f50d03b6b2005d026f8e76138d556874e2423c6a5c06cbd854c790e53b056317baa8c47857b2442e0763e6f7dfa143209f6b61ff60c10cc14aa22747"
DOWNLOAD_DIR = "E:/Audio/"
path = "data"
userAgent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36"
headers = {
    "User-Agent": userAgent
}
BASE_URL_DISCOGS = "https://www.discogs.com"
BASE_URL_BEATPORT = "https://www.beatport.com"
BASE_URL_JUNO = "https://www.junodownload.com"


# Funcion de acceso restringido que carga los datos en la BD
@login_required(login_url='/ingresar')
def populateDatabase(request):
    populate_releases_by_label_discogs()

    # se hace logout para obligar a login cada vez que se vaya a poblar la BD
    logout(request)
    return HttpResponseRedirect('/inicio')


def populate_releases_by_label_discogs(label_name, allServices):
    print("Loading discogs label releases...")
    if allServices != True:
        ReleasesDiscogs.objects.all().delete()

    # Scrapping section START
    url = "https://www.discogs.com/search/?q=" + \
        label_name.replace(" ", "+") + "&type=label"
    f = requests.get(url, headers=headers).content
    soup = BeautifulSoup(f, "lxml")
    label_link = BASE_URL_DISCOGS + \
        str(soup.find("a", class_="thumbnail_link")
            ["href"] + "?sort=year&sort_order=desc")
    label_page = requests.get(label_link, headers=headers).content
    label_page_soup = BeautifulSoup(label_page, "lxml")
    pagination_section = label_page_soup.find(
        "ul", class_="pagination_page_links").find_all("li", class_="hide_mobile")
    num_pages = int(pagination_section[len(
        pagination_section) - 1].text.strip())
    discogs_releases_list = []
    for i in range(0, num_pages):  # num_pages
        url_page_label = label_link + "&limit=500&page=" + str(i + 1)
        releases_in_page = requests.get(
            url_page_label, headers=headers).content
        releases_in_page_soup = BeautifulSoup(releases_in_page, "lxml")
        list_of_releases = releases_in_page_soup.find_all(
            "tr", class_="r_tr")
        releases_list = list()
        with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
            future_to_url = {executor.submit(
                discogs_iterate_releases, release, allServices): release for release in list_of_releases}
    if allServices != True:
        print("Discogs releases inserted: " +
              str(ReleasesDiscogs.objects.count()))
        print("-------------------------------------------------")


def populate_releases_by_label_beatport(label_name, allServices):
    if allServices != True:
        ReleasesBeatport.objects.all().delete()
    print("Loading beatport label releases...")
    url = "https://www.beatport.com/search/labels?q=" + \
        label_name.replace(" ", "+")
    f = requests.get(url, headers=headers).content
    soup = BeautifulSoup(f, "lxml")
    label_link = BASE_URL_BEATPORT + \
        str(soup.find("li", class_="bucket-item").find("a")
            ["href"] + "/releases")
    label_page = requests.get(label_link, headers=headers).content
    label_page_soup = BeautifulSoup(label_page, "lxml")
    pagination_section = label_page_soup.find(
        "div", class_="pag-numbers").find_all("a")

    num_pages = int(pagination_section[len(
        pagination_section) - 1].text.strip())

    for i in range(0, num_pages):  # num_pages
        url_page_label = label_link + "?page=" + str(i + 1)
        releases_in_page = requests.get(
            url_page_label, headers=headers).content
        releases_in_page_soup = BeautifulSoup(releases_in_page, "lxml")
        list_of_releases = releases_in_page_soup.find_all(
            "li", class_="bucket-item")
        releases_list = list()

        with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
            future_to_url = {executor.submit(
                beatport_iterate_releases, release, allServices): release for release in list_of_releases}
    if allServices != True:
        print("Beatport releases inserted: " +
              str(ReleasesBeatport.objects.count()))
        print("-------------------------------------------------")


def populate_releases_by_label_juno(label_name, allServices):
    print("Loading juno label releases...")
    if allServices != True:
        ReleasesJuno.objects.all().delete()

    # Scrapping section START
    url = "https://www.junodownload.com/search/?q%5Ball%5D%5B%5D=" + \
        label_name.replace(" ", "+")
    f = requests.get(url, headers=headers).content
    soup = BeautifulSoup(f, "lxml")
    label_link = BASE_URL_JUNO + "/labels/" + re.match(r"[\S]*=([\S]*)", str(soup.find_all(
        "div", class_="listing-widget")[6].find("a", class_="facet-item")["href"]))[1] + "/?items_per_page=100"
    label_link_cache_joker = BASE_URL_JUNO + "/labels/" + re.match(r"[\S]*=([\S]*)", str(soup.find_all(
        "div", class_="listing-widget")[6].find("a", class_="facet-item")["href"]))[1]
    label_page = requests.get(label_link, headers=headers).content
    label_page_soup = BeautifulSoup(label_page, "lxml")
    pagination_section = label_page_soup.find_all(
        "div", class_="dropdown-menu-right")[2].find_all("a", class_="dropdown-item")[-1].text
    num_pages = int(pagination_section)
    for i in range(0, num_pages):  # num_pages
        url_page_label = label_link_cache_joker + "/" + str(i + 1)
        releases_in_page = requests.get(
            url_page_label, headers=headers).content
        releases_in_page_soup = BeautifulSoup(releases_in_page, "lxml")
        list_of_releases = releases_in_page_soup.find_all(
            "div", class_="jd-listing-item")
        releases_list = list()

        with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
            future_to_url = {executor.submit(
                juno_iterate_releases, release, allServices): release for release in list_of_releases}

    if allServices != True:
        print("Juno releases inserted: " + str(ReleasesJuno.objects.count()))
        print("-------------------------------------------------")


def juno_iterate_releases(release, allServices):
    artist = release.find("div", class_="juno-artist").text.strip()
    cat_date = release.find(
        "div", class_="mb-lg-4").find_all("br")
    catalog_number = cat_date[0].previous_sibling
    title = release.find("a", class_="juno-title").text.strip()
    year = str(datetime.strptime(
        str(cat_date[0].next_sibling), '%d %b %y').date())
    image = str()
    image = re.findall(r"(https.*.jpg)", str(release.find(
        "img")))[0]
    if allServices == True:
        AllReleases.objects.create(artist=str(artist), catalog_number=str(
            catalog_number), title=str(title), year=str(year), image=str(image))
    else:
        ReleasesJuno.objects.create(artist=str(artist), catalog_number=str(
            catalog_number), title=str(title), year=str(year), image=str(image))


def beatport_iterate_releases(release, allServices):
    artist = ", ".join(word.strip() for word in release.find(
        "p", class_="buk-horz-release-artists").text.strip().split(","))
    # Get catalog number START
    album_url = BASE_URL_BEATPORT + str(release.find(
        "p", class_="buk-horz-release-title").find("a")["href"])
    # Get catalog number END
    title = release.find(
        "p", class_="buk-horz-release-title").find("a").text.strip()
    year = release.find(
        "p", class_="buk-horz-release-released").text.strip()
    image = str()
    image = release.find(
        "img", class_="horz-release-artwork")["data-src"]
    if allServices == True:
        AllReleases.objects.create(artist=str(artist), catalog_number=str(
            album_url), title=str(title), year=str(year), image=str(image))
    else:
        ReleasesBeatport.objects.create(artist=str(artist), catalog_number=str(
            album_url), title=str(title), year=str(year), image=str(image))


def discogs_iterate_releases(release, allServices):
    artist = release.find("td", class_="artist").text.strip()
    catalog_number = release.find(
        "td", class_="catno_first").text.strip()
    title = release.find("td", class_="title").find("a").text.strip()
    year = release.find("td", class_="year").text.strip()
    if year == None or year == "Unknown":
        year = "1970"
    try:
        image = release.find("img")["data-src"]
    except:
        image = "http://hosted.netro.ca/morplay/player/img/blankart.jpg"
    # Scrapping section END
    if allServices == True:
        AllReleases.objects.create(artist=str(artist), catalog_number=str(
            catalog_number), title=str(title), year=str(year), image=str(image))
    else:
        ReleasesDiscogs.objects.create(artist=str(artist), catalog_number=str(
            catalog_number), title=str(title), year=str(year), image=str(image))


def get_deezer_album_url(album_and_artist):
    url = "https://www.deezer.com/search/" + \
        album_and_artist.replace("(Mix)", "").replace(
            "(Extended Re-Edit)", "").replace("(Extended Mixes)", "").replace("(Extended Mix)", "").replace("Extended Mix", "").replace("Extended Remix", "").replace(" ", "%20").replace("(", "").replace(")", "").replace("&", "")
    print(url)
    f = requests.get(url, headers=headers).content
    soup = BeautifulSoup(f, "html.parser")
    res = soup.find("div", class_="hidden").find(
        "script",)
    site_json = json.loads(res.contents[0].replace(
        "window.__DZR_APP_STATE__ = ", ""))
    albumId = site_json['ALBUM']["data"][0]["ALB_ID"]
    finalUrl = "https://www.deezer.com/en/album/" + str(albumId)
    p = os.popen("deemix -b flac -p" + DOWNLOAD_DIR +
                 datetime.today().strftime("%d-%m-%Y") + " " + finalUrl, "w")
    p.write(ARL + "\n")

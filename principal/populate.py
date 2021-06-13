from django.http.response import HttpResponseRedirect, HttpResponse
from principal.models import ReleasesDiscogs, ReleasesBeatport
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
import requests
from bs4 import BeautifulSoup
import urllib.request
import concurrent.futures

path = "data"
userAgent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36"
headers = {
    "User-Agent": userAgent
}
BASE_URL_DISCOGS = "https://www.discogs.com"
BASE_URL_BEATPORT = "https://www.beatport.com"
# Funcion de acceso restringido que carga los datos en la BD


@login_required(login_url='/ingresar')
def populateDatabase(request):
    populate_labels_by_discogs()

    # se hace logout para obligar a login cada vez que se vaya a poblar la BD
    logout(request)
    return HttpResponseRedirect('/inicio')


def populate_labels_by_discogs(label_name):
    print("Loading discogs label releases...")
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
                discogs_iterate_releases, release): release for release in list_of_releases}
            for future in concurrent.futures.as_completed(future_to_url):
                try:
                    data = future.result()
                except Exception as exc:
                    print('%r generated an exception: %s' % (url, exc))
                else:
                    print("Added release")

    print("Discogs releases inserted: " + str(ReleasesDiscogs.objects.count()))
    print("-------------------------------------------------")


def populate_releases_by_label_beatport(label_name):
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
                beatport_iterate_releases, release): release for release in list_of_releases}

    print("Beatport releases inserted: " +
          str(ReleasesBeatport.objects.count()))
    print("-------------------------------------------------")


def beatport_iterate_releases(release):
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
    ReleasesBeatport.objects.create(artist=str(artist), catalog_number=str(
        album_url), title=str(title), year=str(year), image=str(image))


def discogs_iterate_releases(release):
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
    ReleasesDiscogs.objects.create(artist=str(artist), catalog_number=str(
        catalog_number), title=str(title), year=str(year), image=str(image))

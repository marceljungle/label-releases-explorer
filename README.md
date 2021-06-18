# label-releases-explorer

## Description
Get all releases of a given label name, filter its albums and download them with a single click. This is using `deemix` package to download songs from deezer, so this is basically searching the name of the album that you clicked on using Deezer web page search and then it uses the album id to download that album with the `deemix` package.

**Deemix** reddit: r/deemix/
## Steps to get it working
1. Install dependencies, it needs to be done manually for now:
    * `python -m pip install django`
    * `python -m pip install requests`
    * `python -m pip install bs4`
    * `python -m pip install deemix`
2. Insert your Deezer ARL, for that, follow this steps:
    * Go to deezer.com and log in into your account
    * Click on the lock located behind the link in the URL section
    * Click on `Cookies` and search for `deezer.com`
    * Click to expand 'Cookies' folder, and search carefully for `arl`
    * Select `arl` and double click and copy the content of the `Content` section
    * Now go to `populate.py` of this script and copy your ARL in the global variable
3. Start the script with `python manage.py runserver`, this will start the server in `localhost:8000` if you want to use other port, you can run the script with `python manage.py runserver <port>`
4. Now, you can use Discogs, Beatport and Juno to search music albums and then queue them to deemix.
5. To change your download location, go to `populate.py` and change `DOWNLOAD_DIR` global variable, by default, the script will create a subfolder inside that location with today's date.
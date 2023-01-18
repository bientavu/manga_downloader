# - Manga DownOFF -
:bangbang: This is a Work In Progress project, some stuff might break/not work properly :bangbang:

## Description
Manga DownOFF is python script to download mangas/webtoons from
online scan reader websites. It downloads the images from a page
and pack them into a ZIP file that is converted to CBZ file. It is 
a WIP project, feel free to contribute to the project
if you want. It was only a personal tool for me to download the
chapters of my favorites mangas/webtoons in order to have them 
offline and be able to read them in the metro, plane, etc...

## Steps of the script
1. With a given scan URL (for example https://www.pantheon-scan.fr/overgeared-chapitre-),
the script parse the pages looking for images.
2. It gets all the src images urls based on a class attributes you set up
3. It downloads the images inside folders created based on the number
of chapters selected in the variables.
4. Folders are zipped in .ZIP files
5. It changes the extensions of zipped files to .CBZ

## Important notes
### Images, classes, and renaming
The core of the script that makes it work or break is the urls
parsing to download the images. Depending on what website you target,
you will have to analyze how the images are working by inspecting 
the page:
- Make sure the url of the image is directly accessible by opening
it and download it.
- Check the class of the image. You'll need to find a class that is
assigned only to the images of the chapter. 95% of the time, the images
for the chapter has their own class.
- Images are downloaded then directly renamed into `001.jpg`, `002.jpg`, `003.jpg`,
`004.jpg`, `005.jpg`, etc. It allows to keep the right order for the images
because sometimes, the file names of are totally random. This leads
to a chapter that have the images in disorder.

### Downloading images: an easy way & a tricky one
The script downloads the images in a batch with a list of the URLs that 
has been retrieved (with urllib request), **this is the easy way**.
Unfortunately, some websites has a cloudflare
protection with captcha that totally blocks us from downloading the
images in a batch. It is possible to fake a browser in the request
function, but honestly, it never worked for me... I always faced 403 errors.
To overcome this issue, I put in place a selenium function that will
launch a real Chrome browser. The URLs list is pasted into a Chrome
extension that automatically downloads all the images, **this is the
tricky one**.

⚠️ Be careful, this method is actually faster but
I couldn't find an easy way to rename the files while they are being
downloaded. This means that if the filenames of the images are not
already in order, the chapter order will be messed up. Make sure that
it's in order, or find a way to improve my script ⚠️

## Inputs
To add your manga/webtoon, insert it into the INPUTS dictionary.
How it works:
```
{
    \\ With Selenium not selected
    "name_of_your_manga_1": [
        "url_of_your_manga_1",
        "target_image_class",
        "no_selenium"
    ],
    \\ With Selenium and Cloudflare selected
    "name_of_your_manga_2": [
        "url_of_your_manga_2",
        "target_image_class",
        "selenium_flaresolverr"
    ]
}
```
Examples are already in the projects.

## Variables
| Variables      |            Values            | Description                                                                  |
|----------------|:----------------------------:|------------------------------------------------------------------------------|
| SELECT_MANGA   |      name_of_your_manga      | The name of the manga/webtoon added in the INPUTS                            |
| CHAPTER_FROM   |           X (int)            | Chapter number where to start the download                                   |
| CHAPTER_TO     |           X (int)            | Chapter number where to finish the download                                  |
| CLASS_SRC_NAME |      target_image_class      | The target class associated with the images to download onlt them            |
| WORKING_DIR    |     PATH of working dir      | Full path of the working directory, will be deleted at the end of the script |
| OUTPUT_CBZ_DIR |    PATH of CBZ output dir    | Full path where the CBZ files will be stored at the end                      |
| EXTENSION_DIR  | PATH of chrome extension dir | Full path where the .crz chrome extension is located                         |
| WEBDRIVER_DIR  | PATH of chrome webdriver dir | Full path of the chrome webdriver                                            |


## Requirements
### FlareSolverr with Docker
In order to get the full list of images URLs when Cloudflare is present,
you'll need to start a docker with [FlareSolverr](https://github.com/FlareSolverr/FlareSolverr).
To do so this simple command line will do the job:

`docker run -p 8191:8191 -e LOG_LEVEL=info -e CAPTCHA_SOLVER=hcaptcha-solver ghcr.io/flaresolverr/flaresolverr:latest`

### Selenium
The [WebDriver for Chrome](https://chromedriver.chromium.org/getting-started) is mandatory.
You can follow the instruction on the website, it's easy. Just copy/paste the full path
of the executable in the `WEBDRIVER_DIR` variable.

## Reading advices
### Smartphones
- [ComicScreen - PDF, ComicReader](https://play.google.com/store/apps/details?id=com.viewer.comicscreen&hl=fr&gl=US): Best reader so far for me,
 it supports many reading options: horizontal, vertical, right to left, left to right, etc. Webtoons are fully supported with an awesome infinite horizontal scrolling.

### Desktops
- [OpenComic](https://github.com/ollm/OpenComic): It's difficult to find a reader that supports an infinite 
horizontal scrolling for webtoons on desktops. This is one is the goat. And it's on macOS, Linux & Windows.
  (For webtoons, tick the webtoon option + set the vertical margin at 0px). Enjoy !
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


The script downloads the images in a batch with a list of the URLs that 
has been retrieved (with urllib request). Unfortunately, some websites has a cloudflare
protection with captcha that totally blocks us from downloading the
images in a batch. It is possible to fake a browser in the request
function, but honestly, it never worked for me... I always faced 403 errors.
To overcome this issue, I put in place a selenium function that will
launch a real Chrome browser. The URLs list is pasted into a Chrome
extension that automatically downloads all the images.

:small_red_triangle: Be careful, this method is actually faster but
I couldn't find an easy way to rename the files while they are being
downloaded :small_red_triangle: 

## What is working
- Webtoons seems to work great
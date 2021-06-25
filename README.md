![License](https://img.shields.io/github/license/phineas-pta/kinh_nhat_tung)
![GitHub last commit](https://img.shields.io/github/last-commit/phineas-pta/kinh_nhat_tung?logo=git)
![GitHub branch checks state](https://img.shields.io/github/checks-status/phineas-pta/kinh_nhat_tung/master?logo=github)
![GitHub deployments](https://img.shields.io/github/deployments/phineas-pta/kinh_nhat_tung/github-pages?logo=jekyll&label=Github%20page)
![GitHub language count](https://img.shields.io/github/languages/count/phineas-pta/kinh_nhat_tung?logo=github)
![GitHub code size](https://img.shields.io/github/languages/code-size/phineas-pta/kinh_nhat_tung?logo=github)
![GitHub repo size](https://img.shields.io/github/repo-size/phineas-pta/kinh_nhat_tung?logo=github)
![Docker build](https://img.shields.io/docker/automated/horimiyasanxmiyamurakun/dr.doofenshmirtz?logo=docker)
![GitHub Workflow Status](https://img.shields.io/github/workflow/status/phineas-pta/kinh_nhat_tung/Publish%20Docker%20image?logo=docker)
![Docker Image Size](https://img.shields.io/docker/image-size/horimiyasanxmiyamurakun/dr.doofenshmirtz?logo=docker)

# Vietnamese Mahayana Buddhist liturgy in multiple languages

thiền môn nhật tụng Việt bằng nhiều thứ tiếng

to be used in liturgy, please ask for a Vietnamese to guide you

**DISCLAIMER: this is a work of compilation, not garanted for authenticity**

feel free to contact me if you need more detailed references

the site is online here: https://phineas-pta.github.io/kinh_nhat_tung/

many thanks to @buddhist-uni for sharing my work on [their site](https://buddhistuniversity.net/content/reference/kinh-nhat-tung_phineas-pta)

# web page formatting

| ![Screenshot showing Heart Sutra example](assets/example_heart_sutra.png) |
|:--:|
| *Screenshot showing Heart Sutra example* |

some selected sutras include Sanskrit version in Siddham script

option to show/hide languages

option to toggle dark mode

additional setup:

 - Favicon: SuttaCentral: https://raw.githubusercontent.com/suttacentral/suttacentral/master/client/img/favicon.ico
 - Google Noto Sans Siddham font: https://github.com/googlefonts/noto-fonts/blob/master/hinted/ttf/NotoSansSiddham/NotoSansSiddham-Regular.ttf, under the [SIL OFL v1.1](assets/fonts/OFL.txt)
 - AR PL (Arphic Public Licensed) UKaiHK font: https://github.com/SilentByte/fonts-arphic-ukai/blob/master/fonts-arphic-ukai/ukai.ttc, under the [Arphic public license](assets/fonts/ARPHICPL.txt)
 - Charmonman font: https://github.com/cadsondemak/Charmonman/blob/master/fonts/Charmonman-Regular.ttf, under the [SIL OFL v1.1](assets/fonts/OFL.txt)
 - Grenze Gotisch font: https://github.com/Omnibus-Type/Grenze-Gotisch/blob/master/fonts/ttf/GrenzeGotisch-ExtraBold.ttf, under the [SIL OFL v1.1](assets/fonts/OFL.txt)
 - MuseoModerno font: https://github.com/Omnibus-Type/MuseoModerno/blob/master/fonts/ttf/MuseoModerno-Regular.ttf, under the [SIL OFL v1.1](assets/fonts/OFL.txt)

*additional file*: `quotations.html`: predecessor of the site

# use locally

with Jekyll: `bundle install` to install all dependencies then `bundle exec jekyll serve --no-watch`

with Docker: `docker run -p 4000:4000 horimiyasanxmiyamurakun/dr.doofenshmirtz`

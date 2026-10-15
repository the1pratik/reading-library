from playwright.sync_api import sync_playwright
import os
u='file://'+os.path.abspath('library/index.html')
with sync_playwright() as p:
    b=p.chromium.launch();pg=b.new_page(viewport={'width':1360,'height':900})
    errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.goto(u);pg.wait_for_timeout(1800)
    pg.screenshot(path='preview.png',full_page=True)
    pg.click('.hero .cv >> nth=0');pg.wait_for_timeout(1800);pg.screenshot(path='preview_open.png')
    m=b.new_page(viewport={'width':390,'height':844});m.goto(u);m.wait_for_timeout(1500);m.screenshot(path='preview_mobile.png',full_page=True)
    print('errors',errs)

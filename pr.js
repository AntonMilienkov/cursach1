const puppeteer = require('puppeteer');
const fs = require('fs');
const { json } = require('stream/consumers');

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

const path_file = '/Users/antonmilienkov/Documents/Anton/cursach/JS_prof/profile.json';


(async () => {
  const browser = await puppeteer.launch({headless: false});
  const page = await browser.newPage();

  await page.goto('https://software-testing.ru/library/testing/general-testing/3056-testing-buttons')
  await sleep(scrape_time * 2000);
  await page.reload();
  var scrape_time, FPS, i, data_json, DrawFrames;
  scrape_time = 1;
  i = 0;
  await sleep(scrape_time * 5000);
  while (i++ < 20) {
    await console.log(i);
    await fs.truncate(path_file, 0, function() {});
    await page.tracing.start({path: path_file,
      screenshots: false,
      categories: ['devtools.timeline']
     });

    const buttonSelector = '#tpmod-left > div.moduletable_menu > div > ul > li.item6 > a > span';
    await page.waitForSelector(buttonSelector)
    page.click(buttonSelector);

    await sleep(scrape_time * 2000);
    await page.tracing.stop();

    try {
      const data = fs.readFileSync(path_file, 'utf8');
      data_json = await JSON.parse(data);
    } catch (err) {
      console.error(err);
    }

    DrawFrames = 0;
    for (args in data_json["traceEvents"]) {
      if (await args["name"] == "DrawFrame") {
        await ++DrawFrames;
      }
    }

    FPS = await DrawFrames / scrape_time;
    await console.log('FPS:', await DrawFrames / scrape_time);

  }
  await browser.close();
})();



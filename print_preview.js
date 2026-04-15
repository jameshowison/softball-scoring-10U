const puppeteer = require('puppeteer');
const path = require('path');

const BASE = path.resolve(__dirname);

const SHEETS = [
  {
    html: 'scoresheet_letter_portrait.html',
    pdf:  'preview_letter_portrait.pdf',
    format: 'Letter', landscape: false,
  },
  {
    html: 'scoresheet_letter_landscape.html',
    pdf:  'preview_letter_landscape.pdf',
    format: 'Letter', landscape: true,
  },
  {
    html: 'scoresheet_letter_2up_landscape.html',
    pdf:  'preview_letter_2up_landscape.pdf',
    format: 'Letter', landscape: true,
  },
];

(async () => {
  const browser = await puppeteer.launch({
    executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
  });

  for (const sheet of SHEETS) {
    const page = await browser.newPage();
    await page.goto(`file://${BASE}/${sheet.html}`, { waitUntil: 'networkidle0' });
    await page.pdf({
      path: `${BASE}/${sheet.pdf}`,
      format: sheet.format,
      landscape: sheet.landscape,
      printBackground: true,
      displayHeaderFooter: false,
      margin: { top: 0, bottom: 0, left: 0, right: 0 },
    });
    await page.close();
    console.log(`Generated ${sheet.pdf}`);
  }

  await browser.close();
})();

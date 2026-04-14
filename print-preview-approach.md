# Print Preview Approach

## Problem

Chrome's `--print-to-pdf` CLI flag always injects its own headers and footers (date, page title, URL, page number). There is no command-line flag that reliably suppresses them.

## Solution: Puppeteer via CDP

Use [Puppeteer](https://pptr.dev/) to drive Chrome via the DevTools Protocol (CDP), which exposes `Page.printToPDF` with a `displayHeaderFooter` option the CLI doesn't expose.

### Setup

```bash
npm install puppeteer
```

### Script

```js
const puppeteer = require('puppeteer');
(async () => {
  const browser = await puppeteer.launch({
    executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
  });
  const page = await browser.newPage();
  await page.goto(
    'file:///Users/jlh5498/Documents/softball-scoring-10U/scoresheet_letter_portrait.html',
    { waitUntil: 'networkidle0' }
  );
  await page.pdf({
    path: '/Users/jlh5498/Documents/softball-scoring-10U/print_preview.pdf',
    format: 'Letter',
    landscape: false,
    printBackground: true,   // honours CSS background colours
    displayHeaderFooter: false,
    margin: { top: 0, bottom: 0, left: 0, right: 0 }
  });
  await browser.close();
})();
```

### Run

```bash
node print_preview.js
```

## Key flags

| Option | Value | Why |
|---|---|---|
| `executablePath` | system Chrome | use the already-installed browser |
| `waitUntil: 'networkidle0'` | — | wait for all resources before printing |
| `printBackground` | `true` | preserves grey row shading from CSS |
| `displayHeaderFooter` | `false` | suppresses date/title/URL/page-number chrome adds |
| `margin` | all `0` | let the `@page { margin: 0.4in }` CSS rule control margins |

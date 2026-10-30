//Optional central browser check for the generated evaluation artifacts.
//Run with an existing Playwright-compatible host and repository preview on port 8765.
async (page) => {
  const results = [];
  const check = (name, pass, observed) => ({name, pass: Boolean(pass), observed});
  const briefs = ['repair-booking', 'cafe-menu', 'developer-tool', 'signup-component', 'operations-app', 'brand-restyle', 'settings-restructure', 'museum-visit'];
  for (const brief of briefs) {
    for (const arm of ['baseline', 'expanded']) {
      const checks = [];
      await page.goto(`http://127.0.0.1:8765/output/design-expansion/renders/${brief}/${arm}/index.html`);
      for (const width of [390, 1280]) {
        await page.setViewportSize({width, height: 900});
        const overflow = await page.evaluate(() => document.documentElement.scrollWidth > innerWidth);
        checks.push(check(`document overflow at ${width}`, !overflow, overflow));
      }
      if (brief === 'repair-booking') {
        await page.locator('button[type=submit]').click();
        checks.push(check('empty choice blocked', !(await page.locator('#confirmation').isVisible()), 'confirmation visibility'));
        await page.locator('select').selectOption({index: 1});
        await page.locator('button[type=submit]').click();
        const text = await page.locator('#confirmation').innerText();
        checks.push(check('selected session confirmed locally', text.includes('10am') && await page.locator('#confirmation').isVisible(), text));
      } else if (brief === 'cafe-menu') {
        for (const [filter, count] of [['food', 1], ['drinks', 2]]) {
          await page.locator(`[data-filter=${filter}]`).click();
          const visible = await page.locator('[data-category]:visible').count();
          checks.push(check(`${filter} filter`, visible === count, visible));
        }
        await page.locator('#reset').click();
        const visible = await page.locator('[data-category]:visible').count();
        checks.push(check('reset full menu', visible === 3, visible));
      } else if (brief === 'developer-tool') {
        await page.locator('#text').fill('One two\nthree');
        const count = await page.locator('#count').innerText();
        checks.push(check('live word count', count.trim() === '3', count));
        await page.locator('#clear').click();
        const cleared = {text: await page.locator('#text').inputValue(), count: await page.locator('#count').innerText()};
        checks.push(check('clear restores empty count', cleared.text === '' && cleared.count.trim() === '0', cleared));
      } else if (brief === 'signup-component') {
        const success = arm === 'baseline' ? '#confirmation' : '#success';
        await page.locator('#email').fill('bad');
        await page.locator('button[type=submit]').click();
        checks.push(check('invalid email blocked', !(await page.locator(success).isVisible()), 'confirmation visibility'));
        await page.locator('#email').fill('reader@example.com');
        await page.locator('button[type=submit]').click();
        const text = await page.locator(success).innerText();
        checks.push(check('valid local confirmation', await page.locator(success).isVisible() && text.includes('reader@example.com'), text));
        await page.locator(arm === 'baseline' ? '#reset' : '#edit-email').click();
        checks.push(check('return to input', await page.locator('#email').isVisible(), 'email visibility'));
      } else if (brief === 'operations-app') {
        await page.locator(arm === 'baseline' ? '[data-status=Ready]' : 'input[name=status][value=ready]').click();
        const ready = await page.locator('tbody tr:visible').count();
        checks.push(check('ready filter', ready === 2, ready));
        await page.locator('#search').fill('no-such-equipment');
        const empty = await page.locator('tbody tr:visible').count();
        checks.push(check('empty state', empty === 0 && await page.locator('#empty').isVisible(), empty));
        await page.locator('#empty-reset').click();
        const reset = {rows: await page.locator('tbody tr:visible').count(), query: await page.locator('#search').inputValue()};
        checks.push(check('empty recovery', reset.rows === 4 && reset.query === '', reset));
      } else if (brief === 'museum-visit') {
        await page.locator('button[type=submit]').click();
        checks.push(check('missing date blocked', !(await page.locator('#confirmation').isVisible()), 'confirmation visibility'));
        const dates = await page.evaluate(() => {
          const d = new Date(); d.setDate(d.getDate() + 7);
          while (d.getDay() !== 4) d.setDate(d.getDate() + 1);
          const local = value => `${value.getFullYear()}-${String(value.getMonth() + 1).padStart(2, '0')}-${String(value.getDate()).padStart(2, '0')}`;
          const thursday = local(d); d.setDate(d.getDate() + 4);
          return {thursday, monday: local(d)};
        });
        await page.locator('#visit-date').fill(dates.monday);
        await page.locator('#party-size').fill('2');
        await page.locator('button[type=submit]').click();
        checks.push(check('closed day blocked', !(await page.locator('#confirmation').isVisible()) && (await page.locator('#date-error').innerText()).length > 0, 'date error and no confirmation'));
        await page.locator('#visit-date').fill(dates.thursday);
        await page.locator('#party-size').fill('0');
        await page.locator('button[type=submit]').click();
        checks.push(check('invalid party blocked', !(await page.locator('#confirmation').isVisible()) && (await page.locator('#party-error').innerText()).length > 0, 'party error and no confirmation'));
        await page.locator('#party-size').fill('2');
        await page.locator('button[type=submit]').click();
        const text = await page.locator('#confirmation').innerText();
        checks.push(check('valid plan preserves visitor facts', await page.locator('#confirmation').isVisible() && ['2 people', 'Thursday', '11am', 'Oak Street'].every(value => text.includes(value)) && text.toLowerCase().includes('free'), text));
      } else {
        await page.evaluate(() => localStorage.clear());
        await page.reload();
        await page.locator('#email').fill('bad');
        await page.locator('[data-analytics=settings-save]').click();
        const blocked = await page.evaluate(() => localStorage.getItem('fieldnote-settings') === null);
        checks.push(check('invalid save blocked', blocked, blocked));
        await page.locator('#email').fill('reader@example.com');
        await page.locator('#zone').selectOption('America/Los_Angeles');
        await page.locator('#digest').check();
        await page.locator('[data-analytics=settings-save]').click();
        const event = await page.evaluate(() => window.lastAnalyticsEvent);
        checks.push(check('analytics retained', event === 'settings-save', event));
        await page.reload();
        const saved = {email: await page.locator('#email').inputValue(), zone: await page.locator('#zone').inputValue(), digest: await page.locator('#digest').isChecked()};
        checks.push(check('save survives reload', saved.email === 'reader@example.com' && saved.zone === 'America/Los_Angeles' && saved.digest, saved));
        checks.push(check('billing destination retained', await page.locator('#billing').count() === 1, 'billing anchor'));
      }
      results.push({brief, arm, checks, pass: checks.every(item => item.pass)});
    }
  }
  return {results, pass: results.every(item => item.pass), limitation: 'Selected browser journeys only; visual judgment and broader accessibility are separate.'};
}

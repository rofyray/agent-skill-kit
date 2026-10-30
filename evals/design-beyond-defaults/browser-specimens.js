async (page) => {
  const origin = 'http://127.0.0.1:8765';
  const output = 'output/design-revision/material-state-checks';
  const measurements = [], journeys = [], captures = [], failures = [];
  const check = (condition, label) => { if (!condition) failures.push(label); };
  const ready = async () => {
    await page.evaluate(async () => {
      await document.fonts.ready;
      await new Promise(resolve => requestAnimationFrame(() => requestAnimationFrame(resolve)));
    });
  };
  await page.goto(origin + '/skills/design-beyond-defaults/assets/material-specimens.html');
  const ids = await page.locator('.material').evaluateAll(es => es.map(e => e.id));
  check(ids.length === 12, 'twelve materials present');
  for (const width of [320, 390, 768, 780, 781, 1280, 1920]) {
    await page.setViewportSize({width, height: 900});
    await ready();
    for (const id of ids) {
      const measurement = await page.locator('#' + id).evaluate(el => ({
        sectionOverflow: el.scrollWidth > el.clientWidth,
        pageOverflow: document.documentElement.scrollWidth > innerWidth,
        panelOverflow: [...el.querySelectorAll('.sample')].some(e => e.scrollWidth > e.clientWidth),
        escapedControls: [...el.querySelectorAll('.sample select,.sample button')].filter(e => {
          const child = e.getBoundingClientRect(), parent = e.closest('.sample').getBoundingClientRect();
          return child.width && (child.left < parent.left - .5 || child.right > parent.right + .5);
        }).length
      }));
      measurements.push({id, width, ...measurement});
      check(!measurement.sectionOverflow && !measurement.pageOverflow && !measurement.panelOverflow && !measurement.escapedControls, `${id} containment at ${width}`);
    }
  }
  for (const width of [320, 1280]) {
    await page.setViewportSize({width, height: 900});
    await page.reload();
    await ready();
    for (const id of ids) {
      const section = page.locator('#' + id);
      const capture = async state => {
        await ready();
        const path = `${output}/${id}-${width}-${state}.png`;
        await section.screenshot({path});
        captures.push({id, width, state, path});
      };
      await section.locator('form select').focus();
      await page.keyboard.press('Tab');
      const focus = await section.locator('.preview-button').evaluate(el => ({
        active: document.activeElement === el, style: getComputedStyle(el).outlineStyle,
        width: parseFloat(getComputedStyle(el).outlineWidth)
      }));
      await page.keyboard.press('Enter');
      const invalid = await section.locator('form select').evaluate(el => ({
        invalid: !el.checkValidity(), described: el.getAttribute('aria-describedby'),
        marked: el.getAttribute('aria-invalid') === 'true', focused: document.activeElement === el
      }));
      const errorText = await section.locator('.error').innerText();
      const invalidStatus = await section.locator('.confirmation').textContent();
      await capture('invalid');
      await section.locator('form select').selectOption({label: 'Sunday afternoon'});
      await section.locator('form select').focus();
      await page.keyboard.press('Tab');
      await page.keyboard.press('Enter');
      const success = await section.locator('.confirmation').innerText();
      const cleared = !(await section.locator('.error').textContent()) && !(await section.locator('form select').getAttribute('aria-invalid'));
      await capture('confirmed');
      await section.locator('.filter').selectOption('blocked');
      const empty = await section.locator('.empty').isVisible();
      const emptyCount = await section.locator('.rows li:visible').count();
      await capture('empty');
      await section.locator('.reset-filter').focus();
      await page.keyboard.press('Enter');
      const reset = await section.locator('.rows li:visible').count();
      const recoveryFocus = await section.locator('.filter').evaluate(el => document.activeElement === el);
      await section.locator('.task').nth(1).focus();
      await page.keyboard.press('Space');
      const selectionCount = await section.locator('.task[aria-pressed=true]').count();
      const selected = await section.locator('.task[aria-pressed=true]').getAttribute('data-task');
      const zero = await section.locator('.task[aria-pressed=true] .task-count-value').innerText();
      await section.locator('.filter').selectOption('open');
      const open = await section.locator('.rows li:visible').count();
      const hiddenSelection = await section.locator('.selection-note').innerText();
      await section.locator('.filter').selectOption('done');
      const done = await section.locator('.rows li:visible').count();
      await section.locator('.filter').selectOption('all');
      await section.locator('form select').selectOption('');
      const staleCleared = !(await section.locator('.confirmation').textContent());
      check(focus.active && focus.style !== 'none' && focus.width >= 2, `${id} visible keyboard focus at ${width}`);
      check(invalid.invalid && invalid.marked && invalid.focused && invalid.described && errorText.length > 0 && !invalidStatus, `${id} invalid submission blocked at ${width}`);
      check(success.includes('Sunday afternoon') && success.includes('No booking was sent') && cleared && staleCleared, `${id} preview and edit recovery at ${width}`);
      check(empty && emptyCount === 0 && reset === 3 && recoveryFocus, `${id} empty filter recovery at ${width}`);
      check(selectionCount === 1 && selected === 'Prepare workbenches' && zero === '0' && open === 2 && done === 1 && hiddenSelection === 'No selected task in this view', `${id} selection and filtering at ${width}`);
      journeys.push({id, width, focus, invalid, errorText, invalidStatus, success, cleared, staleCleared, empty, emptyCount, reset, recoveryFocus, selectionCount, selected, zero, open, done, hiddenSelection});
    }
  }
  return {measurements, journeys, captures, failures};
}

// const assert = require('assert');

// describe('Google Search Function test name', () => {
//   it('can find search results 1', async () => {
//     await browser.url('https://www.google.co.in/');
//     // const prompt = await $('[id="L2AGLb"]'); // consent popup is coming for other location which needs to be accepted to proceed
//     // if(prompt.elementId)
//     //   await prompt.click();
//     // const input = await $('[name="q"]');
//     // await input.setValue('test123');
//     const title = await browser.getTitle();
//     await browser.pause(10000);
//     assert.equal(title, 'Google');
//   });

//   it('can find search results 2', async () => {
//     await browser.url('https://www.google.co.in/');
//     const prompt = await $('[id="L2AGLb"]'); // consent popup is coming for other location which needs to be accepted to proceed
//     if(prompt.elementId)
//       await prompt.click();
//     const input = await $('[name="q"]');
//     await input.setValue('test123');
//     const title = await browser.getTitle();
//     await browser.pause(10000);
//     assert.equal(title, 'Google');
//   });
// });

const assert = require('assert');

describe('Command Log Test Case Insights test_name [10 testcases]', () => {
    const n = 1; // change this to the number of test cases you want

    for (let i = 1; i <= n; i++) {
        it(`Type1- #testCase${i}`, async () => {
            await browser.url('https://www.google.co.in/');
            const title = await browser.getTitle();
            await browser.pause(10000);
            assert.equal(title, 'Google');
        });

        it(`Type2- #testCase${i}`, async () => {
            await browser.url('https://www.google.co.in/');
            const prompt = await $('[id="L2AGLb"]'); // consent popup is coming for other location which needs to be accepted to proceed
            if (prompt.elementId)
                await prompt.click();
            const input = await $('[name="q"]');
            await input.setValue('test123');
            const title = await browser.getTitle();
            await browser.pause(10000);
            assert.equal(title, 'Google');
        });
    }
});

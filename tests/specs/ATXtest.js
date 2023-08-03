describe('Test Case Insights Test', () => {
    const n = 2; // change this to the number of test cases you want
    let anyTestFailed = false;

    beforeEach(() => {
        browser.setTimeout({ 'implicit': 10000 }); // Set the implicit wait timeout to 10 seconds
    });

    afterEach(function() {
      if (this.currentTest.state === 'failed') {
        anyTestFailed = true;
      }
    });

    after(async function() {
      if (anyTestFailed) {
        await browser.execute('lambda-status=failed');
      } else {
        await browser.execute('lambda-status=passed');
      }
    });
    function delay(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }

    for (let i = 1; i <= n; i++) {
      let date = new Date();
      let timestamp = `${date.getHours()}:${date.getMinutes()}:${date.getDate()} ${date.getSeconds()}:${date.getMonth() + 1}:${date.getFullYear()}`; 

      // it(`should login to LambdaTest #testCase${i}_${timestamp}`, async () => {
      it(`should login to LambdaTest #testCase`, async () => {
        await browser.url('https://stage-accounts.lambdatestinternal.com/login');
        const emailField = await $('#email');
        await emailField.setValue('18_apr@ltqa.lambdatestautomation.com');
        // await emailField.setValue('19_apr@ltqa.lambdatestautomation.com');
        // await emailField.setValue('24_apr@ltqa.lambdatestautomation.com');
        // await emailField.setValue('27_mar@ltqa.lambdatestautomation.com');
        // await emailField.setValue('28_apr@ltqa.lambdatestautomation.com');
        await delay(2000);
        // await emailField.setValue('abc@xyz.com');
        // await passwordField.setValue('123');
        const passwordField = await $('#password');
        await passwordField.setValue('12345678');
        await delay(2000);
        const loginButton = await $('#login-button');
        await loginButton.click();
        await delay(2000);
        await browser.url('https://stage-accounts.lambdatestinternal.com/dashboard');
        const insightLink = await $("[class*='item__insights']");
        await insightLink.click();
        await delay(2000);
      });

      // it(`should perform search and open first dashboard #testCase${i}_${timestamp}`, async () => {
      it(`should perform search and open first dashboard #testCase`, async () => {
        const searchField = await $('#search');
        await searchField.setValue('Sanity');
        await delay(3000);
        const textData = await $("[class*='divide-y divide-gray-200']>:nth-child(1)");
        await delay(2000);
        await textData.click();
        await delay(2000);
      });

      it(`should logout from LT and open youtube #testCase`, async () => {
        // await browser.execute('window.scrollTo(0,document.body.scrollHeight)');
        await delay(2000);
        const accountButton = await $('#profile__dropdown__parent');
        await accountButton.click();
        const logout = await $('#app__logout');
        await logout.click();
        await delay(2000);
        await browser.url('https://www.youtube.com/');
        // await browser.execute(`smartui.takeFullPageScreenshot,{"screenshotName":"LT-ATX","smartScroll":false}`);
      });

      it(`Todo Test #testCase`, async () => {
        await browser.url("https://lambdatest.github.io/sample-todo-app/");
        
        // Click on the first 5 items
        for(let i=1; i<=5; i++) {
            const item = $(`[class="list-unstyled"]>:nth-child(${i})>input`);
            await item.click();

        }
    
        // Add n number of items and click on them
        const n = 5; // The number of items you want to add
        for(let i=1; i<=n; i++) {
            const addvalue = $('#sampletodotext');
            await addvalue.setValue(`Item ${i+5}`); // Added to existing 5 items
            const addButton = $('#addbutton');
            await addButton.click();
    
            // Click on the added item
            const newItem = $(`[class="list-unstyled"]>:nth-child(${i+5})>input`);
            await newItem.click();
        }
    });
    

    it(`Google Search #testCase`, async () => {
      await browser.url("https://www.google.com");
      const searchBox = $('[class="gLFyf"]');
      await searchBox.click();
      await searchBox.setValue('Lambdatest');
      await browser.keys("\uE007"); // "\uE007" is the Unicode value for the "Enter" key
    });
    

    it(`Demo steps #testCase`, async () => {
      await browser.url('https://www.lambdatest.com/automation-demos/');

      const username = $('#username');
      await username.setValue('lambda');
      const password = $('#password');
      await password.setValue('lambda123');
      await browser.keys("\uE007"); // "\uE007" is the Unicode value for the "Enter" key
      await delay(2000);
      const displayPage = $('#developer-name');
      // await displayPage.isDisplayed();
      await displayPage.setValue('demo@lambdatest.com');
      const random = $('[class="radio-button pb-20"]>:nth-child(5)');
      await random.click();
      const other = $('#others');
      await other.click();
      const checkbox = $('#tried-ecom');
      await checkbox.click();
      const textArea = $('#comments');
      await textArea.setValue('Hi This is LambdaTest automation Demo');
      const submit= $('[id="submit-button"]');
      await submit.click();
  });


  }
});

describe('Command Log Test Case Insights test_name-Demo Function [10 testcases]', () => {
  const n = 1; // change this to the number of test cases you want

  for (let i = 1; i <= n; i++) {
      it(`Demo steps #testCase${i}`, async () => {
          await browser.url('https://www.lambdatest.com/automation-demos/');

          for(let j = 0; j < 600; j++) {
              await browser.getTitle();
              await browser.getTitle();
          }

          const username = $('#username');
          await username.setValue('lambda');
          const password = $('#password');
          await password.setValue('lambda123');
          const loginButton = $('/html/body/div[1]/div[1]/section[2]/div/div/form/div[3]/button');
          await loginButton.click();
          const displayPage = $('#developer-name');
          await displayPage.isDisplayed();
          await displayPage.setValue('demo@lambdatest.com');
          const random = $('/html/body/div[1]/div[1]/section[2]/div/div/div[1]/p[4]/label/input');
          await random.click();
          const other = $('#others');
          await other.click();
          const checkbox = $('#tried-ecom');
          await checkbox.click();
          const textArea = $('#comments');
          await textArea.setValue('Hi This is LambdaTest automation Demo');
      });
  }
});

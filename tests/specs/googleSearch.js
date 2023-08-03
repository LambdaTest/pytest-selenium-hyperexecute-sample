// describe('Command Log Test Case Insights test_name-Google Fucntion [10 testcases]', ()=>{
//     it ('Google Search #testCase1',()=>{
//         browser.url("https://www.google.com");

//         for( var i=0; i<600; i++){
//             browser.getTitle()
//             browser.getTitle()
//         }
//         const searchBOx= $('/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input');
//         searchBOx.click();
//         const TypeLambdatest= $('/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input');
//         TypeLambdatest.setValue('Lambdatest');
//     });

//     it ('Google Search #testCase2',()=>{
//         browser.url("https://www.google.com");

//         for( var i=0; i<600; i++){
//             browser.getTitle()
//             browser.getTitle()
//         }
//         const searchBOx= $('/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input');
//         searchBOx.click();
//         const TypeLambdatest= $('/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input');
//         TypeLambdatest.setValue('Lambdatest');
//     });
// });

describe('Command Log Test Case Insights test_name-Google Function [10 testcases]', () => {
    const n = 1; // change this to the number of test cases you want

    for (let i = 1; i <= n; i++) {
        it(`Google Search #testCase${i}`, () => {
            browser.url("https://www.google.com");

            for(let j = 0; j < 600; j++) {
                browser.getTitle()
                browser.getTitle()
            }

            const searchBox = $('/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input');
            searchBox.click();
            const TypeLambdatest = $('/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input');
            TypeLambdatest.setValue('Lambdatest');
        });
    }
});

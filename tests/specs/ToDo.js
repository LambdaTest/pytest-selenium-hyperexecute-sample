// describe('SampleTest',()=>{
//     it('Sample Todo Test',()=>{
//     browser.url("https://lambdatest.github.io/sample-todo-app/");
//     const firstItem= $('body > div > div > div > ul > li:nth-child(1) > input');
//     firstItem.click();
//     const secondItem= $('body > div > div > div > ul > li:nth-child(2) > input');
//     secondItem.click();
//     const thirditem= $('body > div > div > div > ul > li:nth-child(3) > input');
//     thirditem.click();
//     const addvalue= $('#sampletodotext');
//     addvalue.setValue('Add new item');
//     const itemadded= $('#addbutton');
//     itemadded.click();
// });
// });
describe('Command Log Test Case Insights Todo-test_name [10 testcases]', () => {
    const n = 1; // change this to the number of test cases you want
    for (let i = 1; i <= n; i++) {
        it(`Sample Todo Test #testCase${i}`, () => {
            browser.url("https://lambdatest.github.io/sample-todo-app/");
            const firstItem = $('body > div > div > div > ul > li:nth-child(1) > input');
            firstItem.click();
            const secondItem = $('body > div > div > div > ul > li:nth-child(2) > input');
            secondItem.click();
            const thirditem = $('body > div > div > div > ul > li:nth-child(3) > input');
            thirditem.click();
            const addvalue = $('#sampletodotext');
            addvalue.setValue('Add new item');
            const itemadded = $('#addbutton');
            itemadded.click();
        });
    }
});

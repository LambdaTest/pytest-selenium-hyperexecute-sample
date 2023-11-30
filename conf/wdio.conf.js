const browser = (process.argv[5] || 'Chrome');
// const WdioCaptureIt = require('lambdatest-test-case-analytics').default;
let date = new Date();

// convert to IST
let istDate = new Date(date.toLocaleString('en-US', {timeZone: 'Asia/Kolkata'}));

istDate.setMinutes(istDate.getMinutes() + 15);


let year = istDate.getFullYear();
let month = ('0' + (istDate.getMonth()+1)).slice(-2); // months are zero indexed
let day = ('0' + istDate.getDate()).slice(-2);
let hours = ('0' + istDate.getHours()).slice(-2);
let minutes = ('0' + istDate.getMinutes()).slice(-2);
let seconds = ('0' + istDate.getSeconds()).slice(-2);

let timestamp = `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`;

exports.config = {
  services: [
    ['lambdatest-test-case-analytics', {}],
    // [WdioCaptureIt, {}],
    [
      "lambdatest",
      {
        tunnel: false,
        lambdatestOpts: {
          logFile: "tunnel.log"
        }
      }
    ]
  ],
  user: process.env.LT_USERNAME,
  key: process.env.LT_ACCESS_KEY,
  buildName: process.env.LT_BUILD_NAME,
  specs: ["../tests/specs/ATXtest.js"],
  exclude: [],

  capabilities: [
    {
      "LT:Options": {
      browserName: browser,
      version: 116,
      name: "TestCase Insights test",
      // build: "Test Case Insights ATX n=1, 3 testcases try5",
      // build: "Test Case Insights ATX n=2, 6 testcases try11",
      build: `TestCase_Insights_build_${timestamp}`,
      // build: "Test Case Insights ATX n=20, 60 testcases try2",
      visual: true,
      tags: ["ATX-testCaseInsights"],
      console: true,
      network: true,
      platformName: process.env.HYPEREXECUTE_PLATFORM || 'windows 10'  
      // platformName: process.env.HYPEREXECUTE_PLATFORM || 'MacOS Catalina'  
    }
    }],
  logLevel: "info",
  coloredLogs: true,
  screenshotPath: "./errorShots/",
  waitforTimeout: 100000,
  connectionRetryTimeout: 90000,
  connectionRetryCount: 1,
  path: "/wd/hub",
  hostname: "hub.lambdatest.com",
  port: 80,
  framework: "mocha",
  mochaOpts: {
    ui: "bdd",
    timeout: 12000000
  }
};

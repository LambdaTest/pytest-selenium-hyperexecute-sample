const browser = (process.argv[5] || 'Chrome');
// const WdioCaptureIt = require('lambdatest-test-case-analytics').default;
let date = new Date();
let istDate = new Date(date.toLocaleString('en-US', { timeZone: 'Asia/Kolkata' }));
let timestamp = `${istDate.getHours()}:${istDate.getMinutes()}:${istDate.getDate()} ${istDate.getSeconds()}:${istDate.getMonth() + 1}:${istDate.getFullYear()}`;
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
  specs: ["./tests/specs/ATXtest.js"],
  exclude: [],

  capabilities: [
    {
      "LT:Options": {
      browserName: browser,
      version: "latest",
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

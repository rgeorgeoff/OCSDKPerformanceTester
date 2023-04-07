import os
import time as t
import argparse

import LogcatReader
import OCHelper
from ConfigReader import *
from OCHelper import *
from LogcatReader import *

def install_app(appPath):
    # Use a breakpoint in the code line below to debug your script.
    os.system("echo Hello from the other side!")
    installAndStartApp(appPath)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="SDK perf test runner", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-p", "--pin", help="pin of logged in user")
    parser.add_argument("-t", "--timeout", help="App max time (seconds) to run before timeout. Default = 120")
    args = parser.parse_args()
    config = vars(args)

    # wake device up if asleep and wait a sec for the result
    simulateKeyPressToWakeUp()
    t.sleep(2)
    setConstantClockSpeeds()
    t.sleep(1)

    disableBothersomeFeatures(config['pin'])

    for testConfig in get_config_data():
        #skip if not testing based off config
        if not testConfig.enabled:
            continue

        print(f"## Started running test for: {testConfig.testName}")
        # clear logs
        print(f"#Clearing adb logs")
        clearLogcat()
        # install and run the game
        print(f"#Installing And Starting App: {testConfig.packageName}")
        Error = installAndStartApp(testConfig.appPath, testConfig.packageName, testConfig.activityName)
        if Error:
            continue
        #give some time for app to boot and collect some logs
        # wait until app is done? - Read a log and until it prints some string its not done
        print(f"#Waiting for app to load and run: {testConfig.packageName} - {testConfig.appRunTime} seconds")
        t.sleep(testConfig.appRunTime)
        # capture logs
        print(f"#Collecting Logs")
        logs = getVrAPILogcat().stdout
        # parse the logs
        print(f"#Parsing Logs")
        parsedLogs = parseLogs(logs)
        # print results
        print(f"Avg GPU% usage: {parsedLogs.gpuP * 100}%")
        print(f"Avg CPU% usage: {parsedLogs.cpuP * 100}%")
        print(getVrAPILogcat().stderr)
        # close and clear app
        print(f"#Closing and removing app")
        closeAndClearApp(testConfig.packageName)

    enableBothersomeFeatures(config['pin'])

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

import os
import time as t
import argparse

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

    timeoutPerAppSeconds = 120
    parser = argparse.ArgumentParser(description="SDK perf test runner", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-p", "--pin", help="pin of logged in user")
    parser.add_argument("-t", "--timeout", help="App max time (seconds) to run before timeout. Default = 120")
    args = parser.parse_args()
    config = vars(args)
    print(config)

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
        installAndStartApp(testConfig.appPath, testConfig.packageName, testConfig.activityName)
        #give some time for app to boot and collect some logs
        # wait until app is done? - Read a log and until it prints some string its not done
        print(f"#Waiting for app to load and run: {testConfig.packageName}")
        t.sleep(5)
        # capture logs
        print(f"#Collecting Logs")
        print(getVrAPILogcat().stdout)
        print(getVrAPILogcat().stderr)
        # parse the logs
        print(f"#Parcing Logs")
        #TODO
        # print results
        # TODO
        # close and clear app
        print(f"#Closing and removing app")
        closeAndClearApp(testConfig.packageName)

    enableBothersomeFeatures(config['pin'])

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

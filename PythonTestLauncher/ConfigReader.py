from bs4 import BeautifulSoup


class Test:
    def __init__(self, testName, age, packageName, activityName, appRunTime, enabled):
        self.testName = testName
        self.appPath = age
        self.packageName = packageName
        self.activityName = activityName
        self.appRunTime = appRunTime
        self.enabled = enabled == "true"


def get_config_data(fileName):
    # Reading the data inside the xml
    # file to a variable under the name
    # data
    tests = []
    with open('Configs/'+fileName, 'r') as f:
        data = f.read()

    # Passing the stored data inside
    # the beautifulsoup parser, storing
    # the returned object
    soup = BeautifulSoup(data, "xml")
    b_unique = soup.testsToRun.find_all('test')

    for i in b_unique:
        tests.append(Test(i.testName.contents[0], "../" + i.appPath.contents[0], i.packageName.contents[0],
                          i.activityName.contents[0], int(i.appRunTime.contents[0]), i.enabled.contents[0]))
    return tests

    # Extracting the data stored in a
    # specific attribute of the
    # `child` tag
    # value = b_name.get('test')
    #
    # print(value)

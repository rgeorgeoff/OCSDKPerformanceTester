## What is it
A way to sequentially test our SDKs performance and give developers an idea of what %GPU a feature will take from the system to put in their apps. This will also help ensure our SDKs remain performant and dont bloat.

## How to Run

You can run the code by running the main.py with an argument for the pin (-p). IE:   
```python3 main.py -p 1234```

The devices logged in users pin number will be needed to programatically disable services from the device that get in the way of automated testing: Guardian, Dialogs, and Auto Sleep. These are reenabled by the script after testing is done.

The device will need to be connected to Wifi for the pin to validate.

You can enable and disable apps in the PythonTestLauncher\config.xml to only run the tests you want.


## Creating a new project to test

- First copy either the base project for either BIRP or URP as a starting point into a new folder under the UnityProjects directory that describes the tech you want to test. [Ex: Avatars, Passthrough, etc.]
- Open your project and configure the Main Scene to run your test, including any settings you need to change in the project for your tech to run.
- Modify the builds Package Name in the android project build settings to be unique and descriptive of what you are testing. [Ex: com.Meta.PerfTestingPassthrough1]
- Modify the Product Name in the android project build settings to be descriptive of the test. [Ex: Passthrough1]. You can also optionally increment the version here if changes are made in the future.
- When you are ready, build the apk to the projects "Builds" folder under a file that is descriptive of the test being run in this apk. [Ex:OpenXRTestProj\UnityProjects\Passthrough\Builds\Single3DPassthroughObject1]
- Create a new test object under "testsToRun" element in the config in the \PythonTestLauncher\config.xml file. Here you can define the path to your build, the package and activity name, the appRunTime, and more. Recommended is to copy an existing one and modify to your needs.
- Run the script to see results.

## Weird results?
- You can don your headset while the tests are running to ensure your tests are running properly and your scene is set up
- Ensure you have sufficient appRunTime to get 10 seconds of scene stability from start up. So if start up and scene stability takes 11 seconds to reach, you would need a minimum of 21 seconds, and you should buffer it by another 2-3 seconds to be sure, so recommended appRunTime would be 24 (seconds).

# Ready the connected device to run a test by factory resetting the device,
# connecting to wifi and logging in a test user.
#
# testUserEmail/testUserPassword: specify the credentials of an existing Oculus test
#   user (https://developer.oculus.com/resources/test-users). This is the
#   user that will be logged into the device after it's been reset. Generally, these
#   email addresses are in the @tfbnw.net domain.
#
# testUserPin: if the device is in a logged in state, then it must be a developer
#   or test user that's logged in AND (for security purposes) this parameter must
#   specify that user's Oculus store PIN. If calling this method when the device
#   is in a non-logged in state, this parameter is ignored.
#   Note that the logged in user may be different from the test user specified above.
#
# wifiSSID/wifiPassowrd: specify valid credentials for a wifi network that is in range..
#
# deviceId: specify the device's serial number--only required if multiple headsets
#   are connected to the host machine.
import subprocess
from datetime import time


def setupDeviceForTest(
    testUserEmail,
    testUserPassword,
    testUserPin,
    wifiSSID,
    wifiPassword,
    deviceId=None,
):
    # Factory reset the device to get a clean test environment. This is a requirement
    # of the subsequent SETUP_FOR_TEST call. WIPE_DEVICE will reset the device but also
    # preserve ADB access after the subsequent reboot.
    result = __runAdbShell(
        f"content call --uri content://com.oculus.rc --method WIPE_DEVICE "
        f"--extra 'PIN:s:{testUserPin}'",
        deviceId,
    )
    if result.returncode == 0 and "Success=true" in result.stdout:
        __runAdbCommand("wait-for-disconnect", deviceId)
        __waitForDeviceBootCompleted(40, deviceId)
    else:
        print(
            f"WIPE_DEVICE call failed: returncode={result.returncode}; {result.stdout}; {result.stderr};"
        )
        return -1

    # Connect to wifi and log in the test user.
    result = __runAdbShell(
        f"content call --uri content://com.oculus.rc --method SETUP_FOR_TEST "
        f"--extra 'WIFI_SSID:s:{wifiSSID}' --extra 'WIFI_PWD:s:{wifiPassword}' --extra 'WIFI_AUTH:s:WPA' "
        f"--extra 'EMAIL:s:{testUserEmail}' --extra 'PWD:s:{testUserPassword}'",
        deviceId,
    )
    if result.returncode == 0 and "Success=true" in result.stdout:
        __runAdbCommand("wait-for-disconnect", deviceId)
        __waitForDeviceBootCompleted(40, deviceId)
        __waitForDumpSys("Horizon logged in: true", 10, deviceId)
    else:
        print(
            f"SETUP_FOR_TEST call failed: returncode={result.returncode}; {result.stdout}; {result.stderr};"
        )
        return -1


# Install the specified APK and launch the app.
def installAndStartApp(apkPath, packageName, activityName, deviceId=None):
    __runAdbCommand(f"install {apkPath}", deviceId)
    __runAdbShell(f"am start -S {packageName}/{activityName}", deviceId)


def sleepHeadset(deviceId=None):
    __runAdbShell("input keyevent POWER", deviceId)


def __runShellCommand(command):
    print(f"SHELL: {command}")
    split = command.split()
    result = subprocess.run(split, capture_output=True, text=True)
    return result


def __getDeviceArg(deviceId):
    if deviceId is None:
        return " "
    else:
        return f" -s {deviceId} "


def __runAdbShell(command, deviceId):
    return __runShellCommand("adb" + __getDeviceArg(deviceId) + "shell " + command)


def __runAdbCommand(command, deviceId):
    return __runShellCommand("adb" + __getDeviceArg(deviceId) + command)


def __waitForProperty(property, maxSeconds, deviceId):
    print(f"Waiting for {property} to turn true")
    start = time.time()
    while "1" not in __runAdbShell(f"getprop {property}", deviceId).stdout:
        if time.time() - start > maxSeconds:
            raise RuntimeError(f"timed out while waiting for {property} to turn true")
        __sleep(2)
    print(f"{property} is true")


def __waitForDeviceBootCompleted(maxSeconds, deviceId):
    __runAdbCommand("wait-for-device", deviceId)
    __waitForProperty("sys.boot_completed", maxSeconds, deviceId)
    __sleep(2)


def __waitForCommand(command, targetString, maxSeconds):
    print(f"Waiting for command '{command}' to return '{targetString}'")
    start = time.time()
    while True:
        result = __runShellCommand(command)
        # Break the loop if we find the target string in stdout or stderr.
        if (
            result.stderr.find(targetString) >= 0
            or result.stdout.find(targetString) >= 0
        ):
            break
        # Raise an exception if we don't find the target in time.
        if time.time() - start > maxSeconds:
            raise RuntimeError(
                f"timed out while waiting for command '{command}' to return '{targetString}'. \n"
                + f"STDOUT: {result.stdout} \n"
                + f"STDERR: {result.stderr} \n"
            )
        __sleep(2)
    print("Found return string: " + targetString)


def __waitForDumpSys(targetString, maxSeconds, deviceId):
    __waitForCommand(
        "adb" + __getDeviceArg(deviceId) + "shell dumpsys CompanionService",
        targetString,
        maxSeconds,
    )


def __sleep(seconds):
    print(f"SLEEP {seconds}s")
    time.sleep(seconds)


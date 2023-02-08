#if OVR_UNITY_ASSET_STORE

#if USING_XR_MANAGEMENT && (USING_XR_SDK_OCULUS || USING_XR_SDK_OPENXR)
#define USING_XR_SDK
#endif

#if UNITY_2020_1_OR_NEWER
#define REQUIRES_XR_SDK
#endif

using System.Collections;
using System.Collections.Generic;
using System.IO;
using UnityEngine;
using UnityEditor;
using Microsoft.Win32;
using System.Diagnostics;

public class MetaXRSimulatorEnabler : MonoBehaviour
{
	const string OpenXrRegKey = "HKEY_LOCAL_MACHINE\\SOFTWARE\\Khronos\\OpenXR\\1";

	private static string GetSimulatorJsonPath()
	{
		string rootPath = OVRPluginUpdater.GetEnabledUtilsPluginRootPath();
		if (!string.IsNullOrEmpty(rootPath))
		{
			return rootPath + "\\MetaXRSimulator\\SIMULATOR.json";
		}
		else
		{
			return null;
		}
	}

	private static string GetSimulatorDllPath()
	{
		string rootPath = OVRPluginUpdater.GetEnabledUtilsPluginRootPath();
		if (!string.IsNullOrEmpty(rootPath))
		{
			return rootPath + "\\MetaXRSimulator\\SIMULATOR.dll";
		}
		else
		{
			return null;
		}
	}

	private static string GetSimulatorActivateScriptPath()
	{
		string rootPath = OVRPluginUpdater.GetEnabledUtilsPluginRootPath();
		if (!string.IsNullOrEmpty(rootPath))
		{
			return rootPath + "\\MetaXRSimulator\\activate_simulator.ps1";
		}
		else
		{
			return null;
		}
	}

	private static string GetSimulatorDeactivateScriptPath()
	{
		string rootPath = OVRPluginUpdater.GetEnabledUtilsPluginRootPath();
		if (!string.IsNullOrEmpty(rootPath))
		{
			return rootPath + "\\MetaXRSimulator\\deactivate_simulator.ps1";
		}
		else
		{
			return null;
		}
	}

	private static string GetActiveOpenXrRuntimeJsonPath()
	{
		string activeRuntimeJsonPath = Registry.GetValue(OpenXrRegKey, "ActiveRuntime", string.Empty) as string;
		return activeRuntimeJsonPath;
	}

	private static string GetCurrentProjectPath()
	{
		return Directory.GetParent(Application.dataPath).FullName;
	}

	private static void RestartUnityEditor()
	{
		EditorApplication.OpenProject(GetCurrentProjectPath());
	}

	const string kActivateSimulator = "Oculus/Meta XR Simulator/Activate";
	[MenuItem(kActivateSimulator, true, 0)]
	private static bool ValidateSimulatorActivated()
	{
		string simulatorJsonPath = GetSimulatorJsonPath();
		string simulatorDllPath = GetSimulatorDllPath();
		string activeOpenXrRuntimeJson = GetActiveOpenXrRuntimeJsonPath();

		bool checkMenuItem = false;

		if (!string.IsNullOrEmpty(simulatorJsonPath) &&
			!string.IsNullOrEmpty(simulatorDllPath) &&
			File.Exists(simulatorJsonPath) &&
			File.Exists(simulatorDllPath) &&
			!string.IsNullOrEmpty(activeOpenXrRuntimeJson))
		{
			if (simulatorJsonPath == activeOpenXrRuntimeJson)
			{
				checkMenuItem = true;
			}
		}

		Menu.SetChecked(kActivateSimulator, checkMenuItem);

		return true;
	}

	[MenuItem(kActivateSimulator, false, 0)]
	private static void ActivateSimulator()
	{
		string simulatorJsonPath = GetSimulatorJsonPath();
		string simulatorDllPath = GetSimulatorDllPath();
		string activeOpenXrRuntimeJsonPath = GetActiveOpenXrRuntimeJsonPath();

		if (string.IsNullOrEmpty(simulatorJsonPath) || !File.Exists(simulatorJsonPath))
		{
			EditorUtility.DisplayDialog("Meta XR Simulator Not Found", "SIMULATOR.json is not found. Please enable OVRPlugin through Oculus/Tools/OVR Utilities Plugin/Set OVRPlugin To OpenXR", "Ok");
		}

		if (simulatorJsonPath == activeOpenXrRuntimeJsonPath)
		{
			EditorUtility.DisplayDialog("Meta XR Simulator is Activated", "Meta XR Simulator has been activated as the current OpenXR Runtime", "Ok");
			return;
		}

		bool okToContinue = EditorUtility.DisplayDialog("Meta XR Simulator", "A powershell script will be launched to set Meta XR Simulator as the Active OpenXR Runtime. You will be asked to grant Administrator priviledge through a system User Access Control Dialog. Please accept when prompted.", "Continue", "Cancel");
		if (!okToContinue)
			return;

		LaunchAndWaitPowerShellScript(GetSimulatorActivateScriptPath());

		string newActiveOpenXrRuntimeJsonPath = GetActiveOpenXrRuntimeJsonPath();
		if (newActiveOpenXrRuntimeJsonPath == simulatorJsonPath)
		{
			EditorUtility.DisplayDialog("Meta XR Simulator is Activated", "Meta XR Simulator has been set as the active OpenXR Runtime", "Ok");
			if (EditorUtility.DisplayDialog("Restart Unity",
										"Unity editor needs to be restarted after changing the activate OpenXR Runtime. Do you want to restart now?",
										"Restart",
										"Not Now"))
			{
				RestartUnityEditor();
			}
		}
		else
		{
			EditorUtility.DisplayDialog("Unable to activate Meta XR Simulator", "Unable to set Meta XR Simulator as the active OpenXR Runtime", "Ok");
		}
	}

	const string kDeactivateSimulator = "Oculus/Meta XR Simulator/Deactivate";
	[MenuItem(kDeactivateSimulator, true, 1)]
	private static bool ValidateSimulatorDeactivated()
	{
		string simulatorJsonPath = GetSimulatorJsonPath();
		string simulatorDllPath = GetSimulatorDllPath();
		string activeOpenXrRuntimeJson = GetActiveOpenXrRuntimeJsonPath();

		bool checkMenuItem = true;

		if (!string.IsNullOrEmpty(simulatorJsonPath) &&
			!string.IsNullOrEmpty(simulatorDllPath) &&
			File.Exists(simulatorJsonPath) &&
			File.Exists(simulatorDllPath) &&
			!string.IsNullOrEmpty(activeOpenXrRuntimeJson))
		{
			if (simulatorJsonPath == activeOpenXrRuntimeJson)
			{
				checkMenuItem = false;
			}
		}

		Menu.SetChecked(kDeactivateSimulator, checkMenuItem);

		return true;
	}

	[MenuItem(kDeactivateSimulator, false, 1)]
	private static void DeactivateSimulator()
	{
		string simulatorJsonPath = GetSimulatorJsonPath();
		string simulatorDllPath = GetSimulatorDllPath();
		string activeOpenXrRuntimeJsonPath = GetActiveOpenXrRuntimeJsonPath();

		if (string.IsNullOrEmpty(simulatorJsonPath) || !File.Exists(simulatorJsonPath))
		{
			EditorUtility.DisplayDialog("Meta XR Simulator Not Found", "SIMULATOR.json is not found. Please enable OVRPlugin through Oculus/Tools/OVR Utilities Plugin/Set OVRPlugin To OpenXR", "Ok");
		}

		if (simulatorJsonPath != activeOpenXrRuntimeJsonPath)
		{
			EditorUtility.DisplayDialog("Meta XR Simulator is not Activated", "Meta XR Simulator is not the current OpenXR Runtime", "Ok");
			return;
		}

		bool okToContinue = EditorUtility.DisplayDialog("Meta XR Simulator", "A powershell script will be launched to deactivate Meta XR Simulator and restore the previous Active OpenXR Runtime. You will be asked to grant Administrator priviledge through a system User Access Control Dialog. Please accept when prompted.", "Continue", "Cancel");
		if (!okToContinue)
			return;

		LaunchAndWaitPowerShellScript(GetSimulatorDeactivateScriptPath());

		string newActiveOpenXrRuntimeJsonPath = GetActiveOpenXrRuntimeJsonPath();
		if (newActiveOpenXrRuntimeJsonPath != simulatorJsonPath)
		{
			EditorUtility.DisplayDialog("Meta XR Simulator is deactivated", "Meta XR Simulator has been deactivated as the current OpenXR Runtime", "Ok");
		}

		if (newActiveOpenXrRuntimeJsonPath != activeOpenXrRuntimeJsonPath)
		{
			if (EditorUtility.DisplayDialog("Restart Unity",
										"Unity editor needs to be restarted after changing the activate OpenXR Runtime. Do you want to restart now?",
										"Restart",
										"Not Now"))
			{
				RestartUnityEditor();
			}
		}
		else
		{
			EditorUtility.DisplayDialog("Unable to deactivate Meta XR Simulator", "The active OpenXR runtime is not changed", "Ok");
		}
	}

	private static void LaunchAndWaitPowerShellScript(string ps1File)
	{
		var startInfo = new ProcessStartInfo()
		{
			FileName = "powershell.exe",
			Arguments = $"-NoProfile -ExecutionPolicy unrestricted -file \"{ps1File}\"",
			UseShellExecute = false,
			RedirectStandardOutput = true //This option means it will take anything the process outputs and put it in test.StandardOutput ie from PS's "write-Output $user"
		};
		Process psProcess = Process.Start(startInfo); //creates a powershell process with the above start options
		psProcess.WaitForExit(); //We need this because Start() simply launches the script it does not wait for it to finish or the below line would not have any data
	}
}

#endif // #if OVR_UNITY_ASSET_STORE

using System.Collections;
using System.Collections.Generic;
using DefaultNamespace;
using TMPro;
using UnityEngine;
using UnityEngine.InputSystem;
using UnityEngine.SceneManagement;
using UnityEngine.Serialization;

public class SceneNavigation : MonoBehaviour
{
    // Start is called before the first frame update
    public InputAction NextFeature;
    public InputAction PrevFeature;
    public InputAction NextFeatureIteration;
    public InputAction PreviousFeatureIteration;

    public InputAction DefaultScene;
    public InputAction PreviousSceneAndFeature;

    public InputActionMap ActionsMap;

    public SceneMap SceneMap;

    public TextMeshProUGUI BottomDisplay;

    private int featureSelection_; // feature we are looking at
    private int featureSceneSelection_; // scene version of the feature we are looking at

    private int prevFeatureSelection_; // previous scene data stored for quick go back
    private int prevFeatureSceneSelection_; // previous scene data stored for quick go back

    void Awake()
    {
        // get actions fom input map
        NextFeature = ActionsMap.FindAction("GoNextFeature");
        PrevFeature = ActionsMap.FindAction("GoPrevFeature");
        NextFeatureIteration = ActionsMap.FindAction("GoNextFeatureTest");
        PreviousFeatureIteration = ActionsMap.FindAction("GoPrevFeatureTest");
        DefaultScene = ActionsMap.FindAction("GoToDefault");
        PreviousSceneAndFeature = ActionsMap.FindAction("GoToPrevious");

        //set function calls on performed - may change to analog joysticks
        NextFeature.performed += GoNextFeature;
        PrevFeature.performed += GoPrevFeature;
        NextFeatureIteration.performed += GoPrevFeature;
        PreviousFeatureIteration.performed += GoPrevFeature;

        DefaultScene.performed += GoDefaultScene;
        PreviousSceneAndFeature.performed += GoToPreviousSceneAndFeature;

        DontDestroyOnLoad(gameObject);
    }

    private void GoToPreviousSceneAndFeature(InputAction.CallbackContext obj)
    {
        var amountPressed = obj.ReadValue<float>();
        var tempFeature = featureSelection_;
        var tempScene = featureSceneSelection_;

        featureSelection_ = prevFeatureSelection_;
        featureSceneSelection_ = prevFeatureSceneSelection_;

        prevFeatureSceneSelection_ = tempScene;
        prevFeatureSelection_ = tempFeature;

        LoadSceneAndChangeDisplay();
    }

    private void GoDefaultScene(InputAction.CallbackContext obj)
    {
        StorePrevious();
        featureSceneSelection_ = 0;
        featureSelection_ = 0;

        LoadSceneAndChangeDisplay();
    }

    private void GoPrevFeature(InputAction.CallbackContext obj)
    {
        StorePrevious();
        featureSceneSelection_ = 0;
        featureSelection_--;

        if (featureSelection_ < 0)
        {
            featureSelection_ = SceneMap.SceneMapOrganizedByFeature.Count - 1;
        }

        LoadSceneAndChangeDisplay();
    }

    // Go to scene index 0 of the next feature

    private void GoNextFeature(InputAction.CallbackContext obj)
    {
        StorePrevious();
        featureSceneSelection_ = 0;
        featureSelection_++;

        if (featureSelection_ > SceneMap.SceneMapOrganizedByFeature.Count - 1)
        {
            featureSelection_ = 0;
        }

        LoadSceneAndChangeDisplay();
    }

    private void LoadSceneAndChangeDisplay()
    {
        var sceneData = SceneMap.SceneMapOrganizedByFeature[(Feature)(featureSelection_ % SceneMap.SceneMapOrganizedByFeature.Count)][
            featureSceneSelection_];

        // load new scene
        SceneManager.LoadScene(
            sceneData.SceneName
        );

        BottomDisplay.text = $"{sceneData.FeatureBeingTested} : {sceneData.DetailsAboutThisTest}";
    }

    private void StorePrevious()
    {
        prevFeatureSelection_ = featureSelection_;
        prevFeatureSceneSelection_ = featureSceneSelection_;
    }
}

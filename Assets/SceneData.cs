namespace DefaultNamespace
{
    public class SceneData
    {
        public string SceneName; // passthrough_test_scene_1
        public Feature FeatureBeingTested; //PassThrough
        public string DetailsAboutThisTest; //"This is testing a single capsule mesh passthrough layer covering about 10% of the screen"
    }

    public enum Feature
    {
        DefaultNoFeature = 0,
        Passthrough = 1,
        AvatarSDK = 2,
    }
}
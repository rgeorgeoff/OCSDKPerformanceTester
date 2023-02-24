using System.Collections.Generic;
using UnityEngine;

namespace DefaultNamespace
{

    [CreateAssetMenu(fileName = "SceneMap", menuName = "ScriptableObjects/SceneMap", order = 1)]
    public class SceneMap : ScriptableObject
    {
        public List<SceneData> SceneDataList;


        public Dictionary<Feature, List<SceneData>> sceneMapOrganizedByFeature_;
        public Dictionary<Feature, List<SceneData>> SceneMapOrganizedByFeature
        {
            get{
                if (sceneMapOrganizedByFeature_ == null)
                {
                    BuildDictionary();
                }
                return sceneMapOrganizedByFeature_;
            }
        }

        private void BuildDictionary()
        {
            sceneMapOrganizedByFeature_ = new();
            foreach (var sceneData in SceneDataList)
            {
                if (!sceneMapOrganizedByFeature_.ContainsKey(sceneData.FeatureBeingTested))
                {
                    sceneMapOrganizedByFeature_[sceneData.FeatureBeingTested] = new List<SceneData>();
                }
                sceneMapOrganizedByFeature_[sceneData.FeatureBeingTested].Add(sceneData);
            }
        }
    }


}
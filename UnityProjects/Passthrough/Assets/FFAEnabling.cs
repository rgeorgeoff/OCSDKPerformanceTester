using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class FFAEnabling : MonoBehaviour
{
    // Start is called before the first frame update
    void Start()
    {
        OVRManager.fixedFoveatedRenderingLevel = OVRManager.FixedFoveatedRenderingLevel.Low; // it's the maximum foveation level
        OVRManager.useDynamicFixedFoveatedRendering = true;
    }

    // Update is called once per frame
    void Update()
    {

    }
}

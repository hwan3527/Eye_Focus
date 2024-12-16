using System.Collections;
using System.Collections.Generic;
using UnityEditor;
using UnityEngine;

public class BoomController : ItemController
{
   PalyerController palyerController;
    protected override void ItemGain()
    {
        base.ItemGain();
        palyerController = base.player.GetComponent<PalyerController>();
        if(palyerController.Boom <4)
        {
            palyerController.Boom++;
        }
    }
}

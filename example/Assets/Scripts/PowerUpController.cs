using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class PowerUpController : ItemController
{
    PalyerController palyerController;

    protected override void ItemGain()
    {
        base.ItemGain();
        
        palyerController = base.player.GetComponent<PalyerController>();
        if(palyerController.Damage < 3)
        {
            palyerController.Damage++;
        }
        if(palyerController.Damage >=3)
        {
            UImanager.instance.ScoreAdd(base.score);
        }
    }
}

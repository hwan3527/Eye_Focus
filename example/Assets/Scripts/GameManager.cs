using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class GameManager : MonoBehaviour
{
    public GameObject playerPrefab;
    public PalyerController palyerController;
    public Vector3 playerPos;
    public int lifeCount;

    public static GameManager instance;

    void Awake()
    {
        if(instance == null)
        {
            instance = this;
        }
        else
        {
            Destroy(gameObject);
        }
        DontDestroyOnLoad(gameObject);
    }

    // Start is called before the first frame update
    void Start()
    {
        lifeCount = 2;
        UImanager.instance.LifeCheck(lifeCount);
        CreatePlayer();
    }

    public void CreatePlayer()
    {
        if (lifeCount >= 0)
        {
            GameObject player = Instantiate(playerPrefab);
            float x = Random.Range(-9.0f, 9.0f);
            float y = -18.0f;
            playerPos = new Vector3(x,y,0);
            player.transform.position = playerPos;
            palyerController = player.GetComponent<PalyerController>();
        }
    }

    //플레이어 라이프 감소

    public void PlayerLifeRemove()
    {
        lifeCount--;
    }
    public void GameOverCheck()
    {
        if(lifeCount < 0)
        {
            UImanager.instance.GameOver();
        }
    }
}

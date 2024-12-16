using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.SceneManagement;

public class GameManager : MonoBehaviour
{
    const float ORIGIN_SPEED = 3;

    public static float globalSpeed;
    public static float score;
    public static bool isLive;
    public GameObject uiOver;

    void Awake()
    {
        isLive = true;

        if (!PlayerPrefs.HasKey("Score"))
            PlayerPrefs.SetFloat("Score", 0);
    }

    void Update()
    {
        if (!isLive)
            return;

        score += Time.deltaTime * 2;
        globalSpeed = ORIGIN_SPEED + score * 0.01f;
        
    }

    public void GameOver()
    {
        uiOver.SetActive(true);
        isLive = false;

        float highScore = PlayerPrefs.GetFloat("Score");
        PlayerPrefs.SetFloat("Score", Mathf.Max(highScore, score));
    }

    public void Restart()
    {
        SceneManager.LoadScene(0);
        score = 0;
        isLive = true;
    }
}

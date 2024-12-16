using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using UnityEngine.SceneManagement;

public class UImanager : MonoBehaviour
{
    //점수
    public Text scoreText;
    public Text highScoreText;
    public int score;
    public int highScore;
    //라이프
    public GameObject[] ui_Life;
    // 싱글턴 인스턴스 추가
    public static UImanager instance;
    
     //암막
    public Image blackOut_Curtt;
    float blackOut_Curtt_value;
    float blackOut_Curtt_speed;

    //게임오버
    public Image gameOVerImage;

    //보스 HP
    public Image hpbarFrame;
    public Image hpbar1;
    public Image hpbar2;
    public float MaxHp1;
    public float MaxHp2;
    public BossController bossController;
    public bool isBossSpwan;

    // 플레이 시간 관련
    public Text timeText; // UI에 표시할 텍스트
    private float playTime; // 게임 시작 후 흐른 시간

    private bool isGameOver; // 게임 오버 상태를 추적하는 변수


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
        score = 0;
        blackOut_Curtt_value = 1.0f;
        blackOut_Curtt_speed = 0.5f;
        highScore = PlayerPrefs.GetInt("HighScore", 0);
        isBossSpwan = false;
        playTime = 0.0f; // 게임 시간 초기화
    }

    void Update()
    {
        if(blackOut_Curtt_value > 0)
        {
            HideBlackOut_Curtt();
        }
        if(isBossSpwan)
        {
            BossHpBarCheck();
        }
        if(isBossSpwan == false)
        {
            hpbarFrame.gameObject.SetActive(false);
            hpbar1.gameObject.SetActive(false);
            hpbar2.gameObject.SetActive(false);

        if (!isGameOver)
        {
            playTime += Time.deltaTime;
            UpdateTimeUI();
        }
        }
    }

    public void HideBlackOut_Curtt()
    {
        blackOut_Curtt_value -= Time.deltaTime * blackOut_Curtt_speed;
        blackOut_Curtt.color = new Color(0.0f, 0.0f, 0.0f, blackOut_Curtt_value);
    }

    public void ScoreAdd(int _score)
    {
        score += _score;
        scoreText.text = score.ToString();
    }

    public void LifeCheck(int lifeCount)
    {
        for (int i = 0; i < ui_Life.Length; i++)
        {
            if(i + 1 <= lifeCount)
                ui_Life[i].SetActive(true);
            else
                ui_Life[i].SetActive(false);
        }
    }

    public void GameOver()
    {
        // 게임 오버 상태에서 타이머 멈추기
        isGameOver = true; // 게임 오버 상태로 변경
        gameOVerImage.gameObject.SetActive(true);
        if(score > highScore)
        {
            PlayerPrefs.SetInt("HighScore", score);
            highScore = score;
        }
        highScoreText.text = highScore.ToString();
    }

    public void ReturnTitle()
    {
        SceneManager.LoadScene("Title");

        Destroy(UImanager.instance.gameObject);
        Destroy(GameManager.instance.gameObject);
        Destroy(SoundManager.instance.gameObject);
    }

    public void BossHpBarCheck()
    {
        hpbarFrame.gameObject.SetActive(true);
        hpbar1.gameObject.SetActive(true);
        hpbar2.gameObject.SetActive(true);

        hpbar1.fillAmount = bossController.hp1 / MaxHp1;
        hpbar2.fillAmount = bossController.hp2 / MaxHp2;
    }

    // 플레이 시간 UI 업데이트 함수
    void UpdateTimeUI()
    {
        // 시간(초)을 분:초 형태로 변환
        int minutes = Mathf.FloorToInt(playTime / 60);
        int seconds = Mathf.FloorToInt(playTime % 60);
        
        // "0:00" 형태로 표시
        timeText.text = string.Format("{0:00}:{1:00}", minutes, seconds);
    }
}

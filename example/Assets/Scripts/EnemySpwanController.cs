using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class EnemySpwanController : MonoBehaviour
{
    //생성위치
    public Transform[] enemySpwans;
    //적 프리팹
    public GameObject[] enemyGameObject;
    //시간을 재는 변수
    float time;
    //적 생성 시간
    float respwanTime;
    //적 생성 숫자
    int enemyCount;
    //랜덤 숫자 변수를 저장하는 배열
    int[] randomCount;
    //웨이브  >> 추후 사용
    int wave;
    //플레이어 변수
    GameObject player;
    //보스 관련
    bool bossCreate;
    public GameObject bossGameObject;
    // Start is called before the first frame update
    void Start()
    {
        time = 0;
        respwanTime = 5.0f;
        enemyCount = 3;
        randomCount = new int[enemyCount];
        wave = 0;
        bossCreate = false;
        //player = GameObject.FindGameObjectWithTag("Player");

    }

    // Update is called once per frame
    void Update()
    {
        Timer();
        //보스생성
        if (wave >=5 && bossCreate == false)
        {
            BossCreate();
        }
    }

    void Timer()
    {
        time += Time.deltaTime;
        if (time > respwanTime)
        {
            RandomPos();
            EnemyCreate();
            wave++;
            time -= time;
        }
    }

    void RandomPos()
    {
        for (int i = 0; i < enemyCount; i++)
        {
            randomCount[i] = Random.Range(0,9);
        }
    }

    void EnemyCreate()
    {
        //if (player == null)
        //    return;

        if(GameManager.instance.lifeCount < 0)
            return;
        
        for(int i = 0; i < enemyCount; i++)
        {
            // 랜덤 적 선택
            int tmpCnt = Random.Range(0, enemyGameObject.Length);
            //생성
            GameObject tmp = GameObject.Instantiate(enemyGameObject[tmpCnt]);
            //위치
            tmp.transform.position = enemySpwans[randomCount[i]].position;
            //동일 위치를 방지하기 위한 조금의 위치 값 조정
            float tmpX = tmp.transform.position.x;
            float result = Random.Range(tmpX - 2.0f, tmpX + 2.0f);
            tmp.transform.position = new Vector3(result, tmp.transform.position.y, transform.position.z);
        }
    }

    void BossCreate()
    {
        bossCreate = true;
        GameObject tmp = GameObject.Instantiate(bossGameObject);
        int randomCount = Random.Range(0,9);
        tmp.transform.position = enemySpwans[randomCount].position;
        BossController bossController = tmp.GetComponent<BossController>();

        UImanager.instance.isBossSpwan = true;
        UImanager.instance.MaxHp1 = bossController.hp1;
        UImanager.instance.MaxHp2 = bossController.hp2;
        UImanager.instance.bossController = bossController;
    }
}

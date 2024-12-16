using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class EnemyController : MonoBehaviour
{
    public GameObject enemyBullet;
    float fireDelay;

    Animator animator;
    bool onDead;
    float time;
    GameObject player;
    PalyerController palyerController; 
    //이동관련
    Rigidbody2D rg2D;
    float moveSpeed;
    //아이템
    public GameObject[] item;

    //HP
    int hp;
    //태그 임시저장
    public string tagName;

    //점수
    int score;


    // Start is called before the first frame update
    void Start()
    {
        animator = GetComponent<Animator>();
        onDead = false;
        time = 0.0f;
        player = GameObject.FindGameObjectWithTag("Player");
        palyerController = player.GetComponent<PalyerController>();
        moveSpeed = Random.Range(2.0f, 5.0f);
        rg2D = GetComponent<Rigidbody2D>();
        fireDelay = 2.5f;
        if(gameObject.CompareTag("ItemDropEnemy"))
        {
            hp = 3;
        }
        else
        {
            hp = 1;
        }
        tagName = gameObject.tag;
        score = 10;
    }

public void FireBullet()
{
    if (player ==null)
        return;
    fireDelay +=Time.deltaTime;
    if (fireDelay > 3f)
    {
        Instantiate(enemyBullet, transform.position, Quaternion.identity);
        fireDelay -= 3f;
    }
}

    // Update is called once per frame
    void Update()
    {
        if(onDead)
            time += Time.deltaTime;
        
        if(time > 0.6f)
        {
            Destroy(gameObject);
            if(tagName == "ItemDropEnemy")
            {
                int temp = Random.Range(0, 2);
                Instantiate(item[temp], transform.position, Quaternion.identity);
            }
        }
        FireBullet();
        Move();
    }

    //적 움직임
    private void Move()
    {
        if (player == null)
        {
            return;
        }
        Vector3 distance = player.transform.position - transform.position;
        Vector3 dir = distance.normalized;
        rg2D.velocity = dir * moveSpeed;
    }

    //적 처지
    private void OnTriggerEnter2D(Collider2D collision)
    {
        if(collision.CompareTag("bullet"))
        {
           hp = hp - palyerController.Damage;
           if(hp <=0)
           {
                animator.SetInteger("State", 1);
                OnDead();
           }
        }
        if (collision.CompareTag("BlockCollider"))
        {
            OnDisapper();
        }
    }

    private void OnDead()
    {
        onDead = true;
        if(gameObject.tag !="Untagged")
        {
            UImanager.instance.ScoreAdd(score);
            SoundManager.instance.enemyDeadSound.Play();
        }
        gameObject.tag = "Untagged";
        //스코어 증가 코드 작성
    }

    private void OnDisapper()
    {
        Destroy(gameObject);
    }
}

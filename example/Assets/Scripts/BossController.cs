using System.Collections;
using UnityEngine;

public class BossController : MonoBehaviour
{
    GameObject player;
    PalyerController palyerController;
    //채력바
    public float hp1;
    public float hp2;

    Animator animator;

    bool onDead;
    bool isSpwan;
    //점수
    int score;

    float time;
    Transform spwanMovePos;
    float speed;

    //총알 위치
    public Transform LAttackPos;
    public Transform RAttackPos;
    //총알
    public GameObject bossBullet;
    //총알 딜레이
    float fireDelay;

    //애니메이션 상태 확인용
    // -1 : 대기, 이동 반복 , 0: 대기, 이동 , 1 : L공격,  2 : R공격, 3: Die
    int animNumber;

    //피격관련
    public SpriteRenderer spriteRenderer;
    Color currentColor;


    void Awake()
    {
        hp1 = 30.0f;
        hp2 = 100.0f;
    }
    // Start is called before the first frame update
    void Start()
    {
        spwanMovePos = GameObject.Find("BossSpwan").GetComponent<Transform>();

        animator = GetComponent<Animator>();

        onDead = false;
        isSpwan = true;
        score =1000;
        speed = 10;

        animNumber = 0;

        currentColor = spriteRenderer.color;
    }

    // Update is called once per frame
    void Update()
    {
        if(isSpwan)
        {
            BossSpwan();
        }
        if(onDead)
        {
            time += Time.deltaTime;
        }
        if(time > 0.6f)
        {
            Destroy(gameObject);
        }
        if(player == null && GameManager.instance.lifeCount >= 0)
        {
            PlayerFind();
        }
        FireBullet();
        AnimationSystem();
    }

    private void OnDead()
    {
        onDead = true;
        UImanager.instance.isBossSpwan = false;
        if(gameObject.tag !="Untagged")
        {
            //스코어증가
            UImanager.instance.ScoreAdd(score);
            SoundManager.instance.enemyDeadSound.Play();
        }
        gameObject.tag = "Untagged";
    }

    private void BossSpwan()
    {
        transform.position = Vector3.MoveTowards(transform.position, spwanMovePos.position, Time.deltaTime * speed);
        if(transform.position == spwanMovePos.position)
        {
            isSpwan=false;
        }
    }

     private void OnTriggerEnter2D(Collider2D collision)
    {
        if(collision.CompareTag("bullet"))
        {
            if(hp1 > 0)
            {
                hp1 = hp1 - palyerController.Damage;
            }
            else
            {
                hp2 = hp2 - palyerController.Damage;
            }
            StartCoroutine(OnDamagedEffect());
        }
        if (hp2 <= 0)
        {
            animator.SetTrigger("Die");
            OnDead();
        }    
    }

    public void PlayerFind()
    {
        player = GameObject.FindGameObjectWithTag("Player");
        palyerController = player.GetComponent<PalyerController>();
    }

    void FireBullet()
    {
        //총알 발사 애니메이션
        if(hp1 > 0 && isSpwan == false)
        {
            fireDelay += Time.deltaTime;
            //공격 딜레이가 1.0초 지나고 L공격 상태가 아니면
            if(fireDelay > 1.0f && animNumber !=1)
            {
                //L공격
                animNumber = 1;
                fireDelay -= fireDelay;
            }
        }
        if(hp1 <= 0)
        {
            fireDelay += Time.deltaTime;
            //공격 딜레이가 1.0초 지나고 R공격 상태가 아니면
            if(fireDelay > 1.0f && animNumber !=2)
            {
                //R공격
                animNumber = 2;
                fireDelay -= fireDelay;
                StartCoroutine(RAttackThreeTimes());
            }
        }
    }

    //애니메이션은 따로 관리
    void AnimationSystem()
    {
        //대기이동
        if(animNumber == 0)
        {
            StartCoroutine(Co_Idle());
        }
        if(animNumber == 1)
        {
            StartCoroutine(Co_LAttack());
        }
        if(animNumber == 2)
        {
            StartCoroutine(Co_RAttack());
        }
    }

    IEnumerator Co_Idle()
    {
        animNumber = -1;
        animator.SetTrigger("Idle");
        yield return new WaitForSeconds(0.6f);
    }

    IEnumerator Co_LAttack()
    {
        animNumber = -1;
        animator.SetTrigger("LAttack");
        yield return new WaitForSeconds(0.6f);
        animNumber = 0;
    }

    IEnumerator Co_RAttack()
    {
        animNumber = -1; // 애니메이션 중 상태로 설정
        animator.SetTrigger("RAttack");
        yield return new WaitForSeconds(0.9f);
        animNumber = 0; // 대기 상태로 전환
    }

    void LAttack()
    {
        if(player == null)
        {
            return;
        }
        Instantiate(bossBullet, LAttackPos.position, Quaternion.identity);
        fireDelay -= 1f;
    }

    void RAttack()
    {
        if(player == null)
        {
            return;
        }
        Instantiate(bossBullet, RAttackPos.position, Quaternion.identity);
        fireDelay -= 1f;
    }

    IEnumerator OnDamagedEffect()
    {
        spriteRenderer.color = Color.red;
        yield return new WaitForSeconds(0.2f);
        spriteRenderer.color = currentColor;
    }

    IEnumerator RAttackThreeTimes()
    {
        for (int i = 0; i < 3; i++) // 3회 반복
        {
            RAttack();
            yield return new WaitForSeconds(0.6f); // 각 공격 간의 지연 시간
        }
        animNumber = 0;
    }
}

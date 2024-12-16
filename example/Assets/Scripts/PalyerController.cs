using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class PalyerController : MonoBehaviour
{
    float x;
    float y;

    public Vector3 limitMax; 
    public Vector3 limitMin; 
    Vector3 temp;

    public GameObject[] prefabBullet;
    float time;
    public float speed;

    //아이템

    public int Damage;
    public int Boom;

//player 파괴 변수
    float fireDelay;
    Animator animator;
    bool onDead;

  private UDPReceiver udpReceiver; // UDPReceiver 참조

    // Start is called before the first frame update
    private void Start()
    {
      time =0;
      speed = 10.0f;
      fireDelay = 0;

      animator = GetComponent<Animator>();
      onDead = false;

      Damage = 1;
      Boom = 0;

      // UDPReceiver 컴포넌트 찾기
      udpReceiver = FindObjectOfType<UDPReceiver>();
    }

    // Update is called once per frame
    void Update()
    {
      Move();
      FireBullet();
      OnDeadCheck();
    }

    public void Move()
    {
      //float x =Input.GetAxis("Horizontal")* speed * Time.deltaTime;
      //float y =Input.GetAxis("Vertical")* speed * Time.deltaTime;

      float x = 0;
      float y = 0;  

      // UDP 데이터 기반으로 이동
      if (udpReceiver != null)
      {
        switch (udpReceiver.receivedNumber)
        {
                case 0: // 중앙 정지
                    x = 0;
                    y = 0;
                    break;
                case 1: // 왼쪽
                    x = -speed * Time.deltaTime;
                    break;
                case 2: // 오른쪽
                    x = speed * Time.deltaTime;
                    break;
                case 3: // 위
                    y = speed * Time.deltaTime;
                    break;
                case 4: // 아래
                    y = -speed * Time.deltaTime;
                    break;
        }
      }
      
      transform.Translate(new Vector3(x,y,0));

      if(transform.position.x > limitMax.x)
      {
        temp.x = limitMax.x;
        temp.y = transform.position.y;
        transform.position = temp;
      }

      if(transform.position.y > limitMax.y)
      {
        temp.y = limitMax.y;
        temp.x = transform.position.x;
        transform.position = temp;
      }

      if(transform.position.x < limitMin.x)
      {
        temp.x = limitMin.x;
        temp.y = transform.position.y;
        transform.position = temp;
      }

      if(transform.position.y < limitMin.y)
      {
        temp.y = limitMin.y;
        temp.x = transform.position.x;
        transform.position = temp;
      }
    }

    public void FireBullet()
    {
      fireDelay += Time.deltaTime;
      Debug.Log("Fire" + fireDelay);
      if (fireDelay > 0.3f)
      {
        Instantiate(prefabBullet[Damage - 1], transform.position, Quaternion.identity);
        fireDelay -= 0.3f;
      }
    }
    private void OnDrawGizmos()
    {
      Gizmos.color = Color.red;
      Gizmos.DrawLine(limitMin, new Vector2(limitMax.x, limitMin.y));
      Gizmos.DrawLine(limitMin, new Vector2(limitMin.x, limitMax.y));
      Gizmos.DrawLine(limitMax, new Vector2(limitMax.x, limitMin.y));
      Gizmos.DrawLine(limitMax, new Vector2(limitMin.x, limitMax.y));
    }
  
    private void OnTriggerEnter2D(Collider2D collision)
    {
      if (collision.CompareTag("enemyBullet"))
      {
        animator.SetInteger("State", 1);
        onDead = true;
      }
    }

    private void OnDeadCheck()
    {
      if (onDead)
      {
        if(SoundManager.instance.playerDeadSound.isPlaying == false)
        {
          SoundManager.instance.playerDeadSound.Play();
        }
        time += Time.deltaTime;
      }

      if (time > 0.6f)
      {
        Destroy(gameObject);
        GameManager.instance.PlayerLifeRemove();
        GameManager.instance.CreatePlayer();
        UImanager.instance.LifeCheck(GameManager.instance.lifeCount);
        GameManager.instance.GameOverCheck();
      }
    }
}


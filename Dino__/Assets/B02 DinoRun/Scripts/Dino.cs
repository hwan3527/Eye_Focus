using UnityEngine;
using UnityEngine.Events; // UnityEvent를 사용하기 위해 추가
using System;
using System.Net;
using System.Net.Sockets;
using System.Text;
using System.Collections;

public class Dino : MonoBehaviour
{
    public enum State { Stand, Run, Jump, Hit }
    public float highJumpPower = 14f;  // 높게 점프
    public float lowJumpPower = 11f;   // 낮게 점프
    public bool isGround;
    public UnityEvent onHit;

    private Rigidbody2D rigid;
    private Animator anim;

    private UDPReceiver udpReceiver; // UDPReceiver 참조

    void Awake()
    {
        rigid = GetComponent<Rigidbody2D>();
        anim = GetComponent<Animator>();

        // UDPReceiver 컴포넌트 찾기
        udpReceiver = FindObjectOfType<UDPReceiver>();
        if (udpReceiver == null)
        {
            Debug.LogError("UDPReceiver 스크립트를 찾을 수 없습니다.");
        }
    }

    void Update()
    {
        if (!GameManager.isLive)
            return;

        if (udpReceiver != null)
        {
            // UDPReceiver에서 수신한 값에 따라 점프 처리
            if (udpReceiver.receivedNumber == 3 && isGround) // 위쪽 감지: 높게 점프
            {
                Jump(highJumpPower);
                udpReceiver.receivedNumber = 0; // 값 초기화
            }
            else if (udpReceiver.receivedNumber == 4 && isGround) // 아래쪽 감지: 낮게 점프
            {
                Jump(lowJumpPower);
                udpReceiver.receivedNumber = 0; // 값 초기화
            }
        }
    }

    private void Jump(float jumpPower)
    {
        rigid.AddForce(Vector2.up * jumpPower, ForceMode2D.Impulse);
        ChangeAnim(State.Jump);
        Debug.Log($"Jump with power: {jumpPower}");
    }

    // 착지(물리 충돌 이벤트)
    void OnCollisionStay2D(Collision2D collision)
    {
        if (!isGround)
        {
            ChangeAnim(State.Run);
        }
        isGround = true;
    }

    void OnCollisionExit2D(Collision2D collision)
    {
        ChangeAnim(State.Jump);
        isGround = false;
    }

    // 장애물 터치(트리거 충돌 이벤트)
    void OnTriggerEnter2D(Collider2D collision)
    {
        rigid.simulated = false;
        ChangeAnim(State.Hit);
        onHit.Invoke();
    }

    // 애니메이션 변경
    void ChangeAnim(State state)
    {
        anim.SetInteger("State", (int)state);
    }
}

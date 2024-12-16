using UnityEngine;
using UnityEngine.Events; // UnityEvent�� ����ϱ� ���� �߰�
using System;
using System.Net;
using System.Net.Sockets;
using System.Text;
using System.Collections;

public class Dino : MonoBehaviour
{
    public enum State { Stand, Run, Jump, Hit }
    public float highJumpPower = 14f;  // ���� ����
    public float lowJumpPower = 11f;   // ���� ����
    public bool isGround;
    public UnityEvent onHit;

    private Rigidbody2D rigid;
    private Animator anim;

    private UDPReceiver udpReceiver; // UDPReceiver ����

    void Awake()
    {
        rigid = GetComponent<Rigidbody2D>();
        anim = GetComponent<Animator>();

        // UDPReceiver ������Ʈ ã��
        udpReceiver = FindObjectOfType<UDPReceiver>();
        if (udpReceiver == null)
        {
            Debug.LogError("UDPReceiver ��ũ��Ʈ�� ã�� �� �����ϴ�.");
        }
    }

    void Update()
    {
        if (!GameManager.isLive)
            return;

        if (udpReceiver != null)
        {
            // UDPReceiver���� ������ ���� ���� ���� ó��
            if (udpReceiver.receivedNumber == 3 && isGround) // ���� ����: ���� ����
            {
                Jump(highJumpPower);
                udpReceiver.receivedNumber = 0; // �� �ʱ�ȭ
            }
            else if (udpReceiver.receivedNumber == 4 && isGround) // �Ʒ��� ����: ���� ����
            {
                Jump(lowJumpPower);
                udpReceiver.receivedNumber = 0; // �� �ʱ�ȭ
            }
        }
    }

    private void Jump(float jumpPower)
    {
        rigid.AddForce(Vector2.up * jumpPower, ForceMode2D.Impulse);
        ChangeAnim(State.Jump);
        Debug.Log($"Jump with power: {jumpPower}");
    }

    // ����(���� �浹 �̺�Ʈ)
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

    // ��ֹ� ��ġ(Ʈ���� �浹 �̺�Ʈ)
    void OnTriggerEnter2D(Collider2D collision)
    {
        rigid.simulated = false;
        ChangeAnim(State.Hit);
        onHit.Invoke();
    }

    // �ִϸ��̼� ����
    void ChangeAnim(State state)
    {
        anim.SetInteger("State", (int)state);
    }
}

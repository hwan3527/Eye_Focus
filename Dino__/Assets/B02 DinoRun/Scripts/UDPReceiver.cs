using System;
using System.Net;
using System.Net.Sockets;
using System.Text;
using UnityEngine;
using System.Collections;

public class UDPReceiver : MonoBehaviour
{
    public int receivedNumber = 0; // 수신된 숫자
    private UdpClient udpClient;
    public int port = 5005; // Python과 동일한 포트
    private IPEndPoint endPoint;

    void Start()
    {
        udpClient = new UdpClient(port);
        endPoint = new IPEndPoint(IPAddress.Any, port);

        // Coroutine을 사용하여 0.3초마다 데이터 수신
        StartCoroutine(ReceiveDataCoroutine());
        Debug.Log("UDP Receiver started on port " + port);
    }

    private IEnumerator ReceiveDataCoroutine()
    {
        while (true)
        {
            if (udpClient.Available > 0)
            {
                byte[] data = udpClient.Receive(ref endPoint);
                string receivedData = Encoding.UTF8.GetString(data);
                if (int.TryParse(receivedData, out int number))
                {
                    receivedNumber = number; // 수신된 숫자 저장
                    Debug.Log("Received: " + receivedNumber);
                }
            }
            yield return new WaitForSeconds(0.3f); // 0.3초 대기
        }
    }

    private void OnDestroy()
    {
        udpClient.Close();
    }
}
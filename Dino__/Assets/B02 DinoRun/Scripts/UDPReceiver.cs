using System;
using System.Net;
using System.Net.Sockets;
using System.Text;
using UnityEngine;
using System.Collections;

public class UDPReceiver : MonoBehaviour
{
    public int receivedNumber = 0; // ���ŵ� ����
    private UdpClient udpClient;
    public int port = 5005; // Python�� ������ ��Ʈ
    private IPEndPoint endPoint;

    void Start()
    {
        udpClient = new UdpClient(port);
        endPoint = new IPEndPoint(IPAddress.Any, port);

        // Coroutine�� ����Ͽ� 0.3�ʸ��� ������ ����
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
                    receivedNumber = number; // ���ŵ� ���� ����
                    Debug.Log("Received: " + receivedNumber);
                }
            }
            yield return new WaitForSeconds(0.3f); // 0.3�� ���
        }
    }

    private void OnDestroy()
    {
        udpClient.Close();
    }
}
using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Scripting.APIUpdating;

public class BackGroundimageController : MonoBehaviour
{
    float height;
    float speed;
    BoxCollider2D boxcollider2D;
    // Start is called before the first frame update
    void Start()
    {
        boxcollider2D = GetComponent<BoxCollider2D>();
        height = boxcollider2D.size.y;
        speed = 3.0f;
    }

    // Update is called once per frame
    void Update()
    {
        Move();
        if (transform.position.y <= -height)
        {
            Reposition();
        } 
    }

    void Move()
    {
        transform.Translate(Vector3.down * speed * Time.deltaTime);
    }
    void Reposition()
    {
        Vector3 offset = new Vector3(0, height * 2, 0);
        transform.position = transform.position + offset;
    }
}

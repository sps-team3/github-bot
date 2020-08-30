curl 'localhost:8080/webhook/im' \
-H 'Content-Type: application/json; charset=utf-8' \
-H 'timestamp: 1577262236757' \
-H 'sign: xxxxxxxxxxxxx' \
-d '{
    "msgtype": "text", 
    "text": {
        "content": "config hzw649 my-portfolio 59b744fe68279fa715636ab5b9d351aa32bafe7cce761b4606e4fe5145977903"
    }, 
    "msgId": "XXXX", 
    "createAt": 1487561654123,
    "conversationType": "2", 
    "conversationId": "XXXX", 
    "conversationTitle": "TEST", 
    "senderId": "XXXX", 
    "senderNick": "TEST",
    "senderCorpId": "XXXX",
    "senderStaffId": "XXXX",
    "chatbotUserId":"XXXX",
    "atUsers":[
       {
         "dingtalkId":"XXXX",
         "staffId":"XXXX"
       }
    ]
}'

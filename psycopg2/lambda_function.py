import json
import boto3
import sys
import logging
import psycopg2

print('Lambda Handler for AppSyncLambdaFunction')

from psycopg2.db_util import make_conn, fetch_data, readRDS


def lambda_handler(event, context):
    print(event)
    response = ""
    query = event["info"]["fieldName"]

    if query == "getUser":
        result = {}
        id = event["arguments"]["id"]
        query_cmd = f"select * from \"users\" where userid = {id}"
        raw = readRDS(query_cmd)
        for line in raw:
            result['userId'] = line[0]
            result['name'] = line[1]
            result['age'] = line[2]
            result['email'] = line[3]

        return result

    elif query == "getOrder":
        result = {}
        orderId = event["arguments"]["orderId"]
        query_cmd = f"select * from \"orders\" where \"orderid\" = {orderId}"
        print(query_cmd)
        raw = readRDS(query_cmd)
        for line in raw:
            result['orderId'] = line[0]
            result['userId'] = line[1]
            result['orderAmount'] = line[2]
            result['orderDate'] = json.dumps(line[3], default=str)
        return result

    elif query == "getPayment":
        client = boto3.resource('dynamodb')
        table = client.Table('PaymentLogs')
        print(table.scan())
        result = table.get_item(Key={'paymentId': event["arguments"]["paymentId"]})
        return result

    elif query == "getAllOrders":
        result = []
        dict = {}
        query_cmd = f"select * from \"orders\" "
        print(query_cmd)
        raw = readRDS(query_cmd)
        for line in raw:
            dict['orderId'] = line[0]
            dict['userId'] = line[1]
            dict['orderAmount'] = line[2]
            dict['orderDate'] = line[3]
            result.append(dict)

        return result

    elif query == "getAllUserOrders":
        result = []
        dict = {}
        userId = event["arguments"]["userId"]
        query_cmd = f"select * from \"orders\"  where \"userid\"={userId};"
        print(query_cmd)
        raw = readRDS(query_cmd)
        for line in raw:
            dict['orderId'] = line[0]
            dict['userId'] = line[1]
            dict['orderAmount'] = line[2]
            dict['orderDate'] = line[3]
            result.append(dict)
        return result



    elif query == "addUser":

        userid = event["arguments"]["input"]["userId"]
        username = event["arguments"]["input"]["name"]
        userage = event["arguments"]["input"]["age"]
        useremail = event["arguments"]["input"]["email"]

        conn = make_conn()
        conn.autocommit = True

        cur = conn.cursor()
        query = f"INSERT INTO \"users\" (userId, name, age, email) VALUES ({userid},'{username}',{userage},'{useremail}')"
        cur.execute(query)

        cur.close
        conn.close

        return {
            'statusCode': 200,
            'data': json.dumps('Succesfully inserted user!')
        }

    elif query == "createOrder":

        orderid = event["arguments"]["input"]["orderId"]
        userid = event["arguments"]["input"]["userId"]
        orderdate = event["arguments"]["input"]["orderDate"]
        orderamount = event["arguments"]["input"]["orderAmount"]

        conn = make_conn()
        conn.autocommit = True

        cur = conn.cursor()
        query = f"INSERT INTO \"orders\"(\"orderid\", \"userid\", \"orderamount\", \"orderdate\") VALUES ({orderid}, {userid}, {orderamount}, '{orderdate}')"
        cur.execute(query)

        cur.close
        conn.close

        return {
            'statusCode': 200,
            'data': json.dumps('Succesfully inserted order!')
        }


    elif (query == "createPayment"):

        client = boto3.resource('dynamodb')
        table = client.Table('PaymentLogs')
        response = table.put_item(Item={
            'paymentId': event["arguments"]["input"]["paymentId"],
            'orderId': event["arguments"]["input"]["orderId"],
            'status': event["arguments"]["input"]["status"],
            'paymentDate': event["arguments"]["input"]["paymentDate"]})
        return response

    elif query == "deleteUser":

        id = event["arguments"]["userId"]
        conn = make_conn()
        conn.autocommit = True

        cur = conn.cursor()
        query = f"DELETE FROM \"users\" where \"userid\"={id};"
        cur.execute(query)

        cur.close
        conn.close

        return {
            'statusCode': 200,
            'data': json.dumps(f"Succesfully deleted userid {id}!")
        }

    elif query == "deleteOrders":
        orderId = event["arguments"]["orderId"]
        conn = make_conn()
        conn.autocommit = True

        cur = conn.cursor()
        query = f"DELETE FROM \"orders\" where \"orderid\"={orderId};"
        cur.execute(query)

        cur.close
        conn.close

        return {
            'statusCode': 200,
            'data': json.dumps(f"Succesfully deleted orderid {orderId}!")
        }

    elif query == "deletePayment":
        client = boto3.resource('dynamodb')
        table = client.Table('PaymentLogs')
        response = table.delete_item(Key={'paymentId': event["arguments"]["paymentId"]})
        return {
            'statusCode': 200,
            'data': json.dumps(f"Succesfully deleted paymentId record!")
        }

    else:
        return response




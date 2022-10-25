import boto3
import json
from datetime import datetime
from dateutil import tz
from urllib.parse import quote

def lambda_handler(event, context):
    client = boto3.client('sns')
    hanoiTZ = tz.gettz('Asia/Bangkok')
    timestamp = datetime.strptime(event['time'], "%Y-%m-%dT%H:%M:%SZ")
    localTimeStamp = timestamp.astimezone(hanoiTZ).strftime("%Y-%m-%d %H:%M:%S")

    detail = event['detail']
    metric = event['detail']['configuration']['metrics'][0]
    subject = "Alpha ALARM: \"" + detail['alarmName'] + "\" in Asia Pacific (Singapore)"
    message = "Alarm Details:"
    message = message + "\n- Name:                       " + detail['alarmName']
    message = message + "\n- Description:                " + detail['configuration']['description']
    message = message + "\n- State Change:               " + detail['previousState']['value'] + " -> " + detail['state']['value']
    message = message + "\n- Reason for State Change:    " + detail['state']['reason']
    message = message + "\n- Timestamp:                  " + localTimeStamp
    message = message + "\n- AWS Account:                " + event['account']
    message = message + "\n- Alarm Arn:                  " + event['resources'][0]
    message = message + "\n\nMonitored Metric:"
    message = message + "\n- MetricNamespace:            " + metric['metricStat']['metric']['namespace']
    message = message + "\n- MetricName:                 " + metric['metricStat']['metric']['name']
    message = message + "\n- InstanceId:                 " + metric['metricStat']['metric']['dimensions'].get('InstanceId', 'data missing')
    message = message + "\n- Period:                     " + str(metric['metricStat']['period'])
    message = message + "\n- Statistic:                  " + metric['metricStat']['stat']
    message = message + "\n- Unit:                       " + metric['metricStat'].get('unit', 'not specified')
    message = message + "\n\nView this alarm in the AWS Management Console:\n"
    url = 'https://' + event['region'] + '.console.aws.amazon.com/cloudwatch/deeplink.js?region=' + event['region'] + '#alarmsV2:alarm/' + quote(detail['alarmName'])
    message = message + url

    # response = client.publish(
    #     TargetArn="arn:aws:sns:us-east-1:269597175775:Khoi_Test_Topic",
    #     MessageStructure='text',
    #     Subject=subject,
    #     Message=message,
    # )

    # return response
    print(message)

f=open('./event.json')
event=json.load(f)
lambda_handler(event, '')
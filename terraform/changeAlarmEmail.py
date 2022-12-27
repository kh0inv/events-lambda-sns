import boto3
import os
from datetime import datetime
from dateutil import tz
from urllib.parse import quote

def lambda_handler(event, context):
  client = boto3.client('sns')
  hanoiTZ = tz.gettz('Asia/Bangkok')
  timestamp = datetime.strptime(event['time'], "%Y-%m-%dT%H:%M:%SZ")
  localTimeStamp = timestamp.astimezone(hanoiTZ).strftime("%Y-%m-%d %H:%M:%S")
  targetSNSTopicArn = os.environ.get('SNS_TOPIC_ARN')
  projectName = os.environ.get('PROJECT_NAME')
  region = os.environ.get('AWS_REGION')
  regionName = region
  if region == 'ap-southeast-1':
    regionName = 'Singapore'
  if region == 'us-east-1':
    regionName = 'N. Virginia'

  detail = event['detail']
  metric = event['detail']['configuration']['metrics'][0]
  subject = projectName.upper() + " Alarm: \"" + detail['alarmName'] + "\" in " + regionName
  message = "Alarm Details:"
  message = message + "\n- Name:                       " + detail['alarmName']
  if "description" in detail['configuration']:
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

  response = client.publish(
      TargetArn=targetSNSTopicArn,
      MessageStructure='text',
      Subject=subject,
      Message=message,
  )

  return response

import json
import boto3
import requests
from datetime import datetime
import pytz
import constant
def send_slack_message(slack_webhook_url, slack_message):
  print('>send_slack_message:slack_message:'+slack_message)
  slack_payload = {'text': slack_message}
  print('>send_slack_message:posting message to slack channel')
  response = requests.post(constant.slack_webhook_url, json.dumps(slack_payload))
  response_json = response.text  # convert to json for easy handling
  print('>send_slack_message:response after posting to slack:'+str(response_json))
def find_running_ec2instances():
  send_message_to_slack = 0
  global totalinstanceshutdown
  totalinstanceshutdown = 0
  notification_message = 'The following EC2 instance(s) are ShutDown: \n'
  IST = pytz.timezone('Asia/Kolkata')
  current_time = datetime.now(IST)
  total_running_ec2_instances = 0
  for region in constant.regions:
    client = boto3.client("ec2", region_name=region)
    running_ec2_instances = client.describe_instances(
        Filters=[{'Name': 'instance-state-name','Values': ['running']}]
    )
    for groups in running_ec2_instances['Reservations']:
        num_running_ec2_instances = len(groups['Instances'])
        if num_running_ec2_instances > 0:
            # there is at least one running instance in this region
            total_running_ec2_instances += num_running_ec2_instances
            va= groups['Instances']
            for i in va:
                if 'Tags' in i:
                    dict1 = {}
                    for tag in i['Tags']:
                        dict1[tag["Key"]] = tag["Value"]
                    if "SHUTDOWN" in dict1 and "TEAM_LOCATION" in dict1:
                        if dict1["SHUTDOWN"] == "DAILY" and dict1["PLATFORM_TYPE"] == "USHUR" and dict1["TEAM_LOCATION"] == "INDIA" and current_time.hour >= constant.indiastoptime:
                            send_message_to_slack = 1
                            if "POC" in dict1:
                                ec2_POC = dict1["POC"]
                            else:
                                ec2_POC = "No POC"
                            ec2_info = ', POC:' + ec2_POC
                            if "Name" in dict1:
                               ec2_instance_name = dict1["Name"]
                            else:
                                ec2_instance_name = "No Name"
                            ec2_info = ':point_right: Region:' + region + ', Name:' + ec2_instance_name + ec2_info
                            print('>find_running_ec2instances:running ec2 instance found:' + ' ' + str(ec2_info))
                            try:
                                client.stop_instances(InstanceIds=[str(i["InstanceId"])])
                                totalinstanceshutdown += 1
                                ec2_info = ec2_info + ", InstanceId: " + i["InstanceId"]
                            except:
                                print("No Instances to ShutDown")
                            notification_message += ec2_info + '\n'
                        elif dict1["SHUTDOWN"] == "DAILY" and dict1["PLATFORM_TYPE"] == "USHUR" and dict1["TEAM_LOCATION"] == "US" and current_time.hour >= constant.usstoptime:
                            send_message_to_slack = 1
                            if "POC" in dict1:
                                ec2_POC = dict1["POC"]
                            else:
                                ec2_POC = "No POC"
                            ec2_info = ', POC:' + ec2_POC
                            if "Name" in dict1:
                                ec2_instance_name = dict1["Name"]
                            else:
                                ec2_instance_name = "No Name"
                            ec2_info = ':point_right: Region:' + region + ', Name:' + ec2_instance_name + ec2_info
                            print('>find_running_ec2instances:running ec2 instance found:' + ' ' + str(ec2_info))
                            try:
                                client.stop_instances(InstanceIds=[str(i["InstanceId"])])
                                totalinstanceshutdown += 1
                                ec2_info = ec2_info + ", InstanceId: " + i["InstanceId"]
                            except:
                                print("No Instances to ShutDown")
                            notification_message += ec2_info + '\n'
                        if dict1["SHUTDOWN"] == "WEEKLY" and dict1["PLATFORM_TYPE"] == "USHUR" and dict1["TEAM_LOCATION"] == "INDIA" and current_time.hour >= constant.indiastoptime and current_time.strftime("%A") == constant.IndiaStopDay:
                            send_message_to_slack = 1
                            if "POC" in dict1:
                                ec2_POC = dict1["POC"]
                            else:
                                ec2_POC = "No POC"
                            ec2_info = ', POC:' + ec2_POC
                            if "Name" in dict1:
                               ec2_instance_name = dict1["Name"]
                            else:
                                ec2_instance_name = "No Name"
                            ec2_info = ':point_right: Region:' + region + ', Name:' + ec2_instance_name + ec2_info
                            print('>find_running_ec2instances:running ec2 instance found:' + ' ' + str(ec2_info))
                            try:
                                client.stop_instances(InstanceIds=[str(i["InstanceId"])])
                                totalinstanceshutdown += 1
                                ec2_info = ec2_info + ", InstanceId: " + i["InstanceId"]
                            except:
                                print("No Instances to ShutDown")
                            notification_message += ec2_info + '\n'
                        elif dict1["SHUTDOWN"] == "WEEKLY" and dict1["PLATFORM_TYPE"] == "USHUR" and dict1["TEAM_LOCATION"] == "US" and current_time.hour >= constant.usstoptime and current_time.strftime("%A") == constant.UsStopDay:
                            send_message_to_slack = 1
                            if "POC" in dict1:
                                ec2_POC = dict1["POC"]
                            else:
                                ec2_POC = "No POC"
                            ec2_info = ', POC:' + ec2_POC
                            if "Name" in dict1:
                                ec2_instance_name = dict1["Name"]
                            else:
                                ec2_instance_name = "No Name"
                            ec2_info = ':point_right: Region:' + region + ', Name:' + ec2_instance_name + ec2_info
                            print('>find_running_ec2instances:running ec2 instance found:' + ' ' + str(ec2_info))
                            try:
                                client.stop_instances(InstanceIds=[str(i["InstanceId"])])
                                totalinstanceshutdown += 1
                                ec2_info = ec2_info + ", InstanceId: " + i["InstanceId"]
                            except:
                                print("No Instances to ShutDown")
                            notification_message += ec2_info + '\n'
                    else:
                        print("values are not satisfying")
                else:
                    print("values are not satisfying")
        else:
            print("values are not satisfying")
  if test > 0:
      print("slck msg final", notification_message)
      send_slack_message(constant.slack_webhook_url, notification_message)
      print("Total Instances shutdown :", totalinstanceshutdown)
  else:
      print("Slack Message is not sent")
      print("Total Instances shutdown :", totalinstanceshutdown)
  return total_running_ec2_instances
def lambda_handler(event, context):
  num_running_instances = find_running_ec2instances()
  num_shutdown_instances = totalinstanceshutdown
  cloudwatch = boto3.client('cloudwatch')
  response = cloudwatch.put_metric_data(
      MetricData = [
            {
                'MetricName': 'DevInstanceShutDown',
                'Dimensions': [
                    {
                        'Name': 'DevInstanceShutDown',
                        'Value': 'InstanceCount'
                    },
                ],
                'Unit': 'None',
                'Value': num_shutdown_instances
            },
        ],
        Namespace = 'Instanceshutdown'
  )
  return {
      'statusCode': 200,
      'body': json.dumps('Number of EC2 instances currently running in all regions:' + str(num_running_instances))
  }

#Author Rohan G - stopping an ec2 instance because a Special_exemption tag is missing

import json
import boto3

ec2_client = boto3.client('ec2')
sns_client = boto3.client('sns')

def lambda_handler(event, context):
    #TODO IMPLEMENT
    ec2_instance_id=event['detail']['instance-id']
    
    response = ec2_client.describe_tags(
    Filters=[
        {
            'Name': 'resource-id',
            'Values': [ec2_instance_id]
        }
     ]
    )

    #print(response)         #lets print the response then we will see how to process the tags
    
    #alltags = response['Tags']
    
    flag='STOP'             #by default, you need to stop the instance, unless you find the tag called "Special"
    #print(alltags)
    for item in response['Tags']:
        print(item['Key'])
        if item['Key']=='Special_exemption':
            flag='DONT_STOP'
            break               #come out of the loop
    
    print(flag)
    
    if flag=='STOP':
    #stop ec2 and send SNS notification - else do nothing..we want the ec2 up and running
        response = ec2_client.stop_instances(InstanceIds=[ec2_instance_id]) 
        snsarn = 'arn:aws:sns:us-east-1:421588605339:ec2StopTopic:bc717947-1718-417d-84b0-1970351c2234'
        errorMsg = "EC2 " + ec2_instance_id + "Stopped"
        response = sns_client.publish(TopicArn=snsarn, Message=errorMsg, Subject="ec2 instance stopped because Special_exemption tag not present")
        

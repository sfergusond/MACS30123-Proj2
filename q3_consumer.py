import boto3, time, ast

kinesis = boto3.client('kinesis')
sns = boto3.client('sns')

# Create SNS topic
topic_arn = sns.create_topic(Name='macs30123')['TopicArn']
subscription = sns.subscribe(
	TopicArn=topic_arn,
	Protocol='email',
	Endpoint='csfergusondryden@uchicago.edu',
)
time.sleep(20) # give time to confirm email subscription before continuing

shards = kinesis.get_shard_iterator(
	StreamName='macs30123',
	ShardId='shardId-000000000000',
	ShardIteratorType='LATEST'
	)['ShardIterator']

while 1==1:
	out = kinesis.get_records(
		ShardIterator=shards,
		Limit=1
		)

	data = out['Records'][0]['Data']
	data = ast.literal_eval(data.decode('utf-8'))

	if data['PRICE'] < 3:
		event_time = data['EVENT_TIME']
		print(data)

		# Publish to SNS topic
		response = sns.publish(
			TopicArn=topic_arn,
			Message=f"{data['TICKER']} fell below $3 at {data['EVENT_TIME']}",
			Subject='MACS30123 Price Alert',
			)
		time.sleep(10) # Give email some time to send before deleting the topic

		# Delete Kinesis Stream
		kinesis.delete_stream(StreamName='macs30123')

		# Delete SNS topic
		sns.delete_topic(TopicArn=topic_arn)

		# Terminate instances
		ec2 = boto3.client('ec2')
		ec2.terminate_instances(InstanceIds=['i-0462064050c9416d3', 'i-0740a955833d3f2c5'])

	shards = out['NextShardIterator']
	time.sleep(.2)
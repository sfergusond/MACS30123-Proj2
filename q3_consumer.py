import boto3, time

kinesis = boto3.client('kinesis')

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

	print(out)

	shards = out['NextShardIterator']
	time.sleep(.2)
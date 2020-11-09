import random, datetime, json, boto3

def getReferrer():
	data = {}
	now = datetime.datetime.now()
	str_now = now.isoformat()
	data['EVENT_TIME'] = str_now
	data['TICKER'] = 'AAPL'
	price = random.random() * 100 # Assume price is in USD
	data['PRICE'] = round(price, 2)
	return data

# Create Kinesis stream
kinesis = boto3.client('kinesis')
kinesis.create_stream(
	StreamName='macs30123',
	ShardCount=1
)

while True:
	data = json.dumps(getReferrer())

	# Send data to the Kinesis stream
	kinesis.put_record(
		StreamName='macs30123',
		Data=data,
		PartitionKey='partitionkey'
		)
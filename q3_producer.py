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

kinesis = boto3.client('kinesis')

while True:
	data = json.dumps(getReferrer())

	# Send data to the Kinesis stream
	kinesis.put_record(
		StreamName='macs30123',
		Data=data,
		PartitionKey='partitionkey'
		)
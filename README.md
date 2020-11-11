## 1

### a) 

On a t2.micro EC2 instance, the serial version of the code took 149 seconds to run: 12 seconds for step 1, and 137 seconds for step 2. After parallelizing the code, the best result took 34 seconds to run, 7 seconds for step 1, and 27 seconds for step 2. Overall, I saw about a 4x speedup. The largest bottleneck I saw ocurred in step 1. I only noticed a 5 second speedup, so I'm assuming the lambda invocation overhead took a significant amount of time, upwards of 10 seconds. I tested different batch sizes for step 2 and noticed diminishing returns lower/higher than splitting the list of books into ten equal parts. Larger slices meant that each Lamdba task had to compute a lot more in parallel, while smaller slices meant that the parallel benefit became outweighed by the Lambda incovation overhead.

![serial_runtime](https://github.com/sfergusond/MACS30123-Proj2/blob/master/q1_runtime_serial.png)
![parallel_runtim](https://github.com/sfergusond/MACS30123-Proj2/blob/master/q1_runtimes.png)

### b) 

In this scenario, we aren't concerned with fault tolerance since we're only importing data into a locally stored file. We're also scraping and storing a relatively small amount of data, so it would likely be a waste of money to pay for a hosted database. If we were sharing the data publicly or scraping significantly more data, an AWS hosted solution would be appropriate. In this scenario, fault tolerance would be helpful given the greater strain (more people accessing the data and more jobs inserting data) on the database, and it would be much easier to allow the public to access the database.

## 2

The output for my mrjob implementation: 

[[13064, "the"], [8705, "and"], [7882, "of"], [7018, "a"], [6091, "to"], [4286, "in"], [3135, "is"], [2510, "her"], [2147, "that"], [1996, "with"]]

Runtime: 4.6 seconds

## 3

Note: instead of using Boto3 to create the EC2 instances and the Kinesis stream, I just made them manually on the AWS console. I had issues with the IAM permissions when trying to create those on Python. I was able to terminate/delete everything through Boto3.

![screenshot](https://github.com/sfergusond/MACS30123-Proj2/blob/master/q3_alert.png)

## 4

I would like to collect and analyze live Twitter data on the US election. Rather than focus on what's being said in the US, I'd like to examine how social media has reacted differently to the election around the world. I'd like to find out whether certain countries have a more positive or negative bent to Biden's presumed victory, or whether certain types of regimes have consitent social media content surrounding Trump's authoritarian tactics to delay the electoral process.

To accomplish this, I will use various resources in the AWS ecosystem. I'll use an EC2 instance to schedule a cluster of Lamdba tasks to scrape Twitter using pywren. Results will be sent through a Kinesis stream into an RDS database. To clean the data, I'll use AWS Translate. For the analysis portion, PySpark or mrjob would be used along with AWS Comprehend. 

Schedule:
-Week 1: Create Twitter API account and write prototype code to scrape relevant Twitter posts
-Week 2: Parallelize prototype code and begin ingesting data into an AWS RDS database by incorporating EC2, Lambda, and Kinesis 
-Week 3: Stop data ingestion after ~2 weeks of daily scraping, write prototype code for the data cleaning and analysis using Translate and Comprehend
-Week 4: Parallelize prototype code with PySpark or mrjob and conduct analysis on the whole body of data to find results


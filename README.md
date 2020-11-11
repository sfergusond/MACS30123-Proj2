## 1

### a) 

On a t2.micro EC2 instance, the serial version of the code took 149 seconds to run: 12 seconds for step 1, and 137 seconds for step 2. After parallelizing the code, the best result took 34 seconds to run, 7 seconds for step 1, and 27 seconds for step 2. Overall, I saw about a 4x speedup. The largest bottleneck I saw ocurred in step 1. I only noticed a 5 second speedup, so I'm assuming the lambda invocation overhead took a significant amount of time, upwards of 10 seconds. I tested different batch sizes for step 2 and noticed diminishing returns lower/higher than splitting the list of books into ten equal parts. Larger slices meant that each Lamdba task had to compute a lot more in parallel, while smaller slices meant that the parallel benefit became outweighed by the Lambda incovation overhead.

### b) 

## 2

The output for my mrjob implementation: 

[[13064, "the"], [8705, "and"], [7882, "of"], [7018, "a"], [6091, "to"], [4286, "in"], [3135, "is"], [2510, "her"], [2147, "that"], [1996, "with"]]

Runtime: 4.6 seconds

## 3

Note: instead of using Boto3 to create the EC2 instances and the Kinesis stream, I just made them manually on the AWS console. I had issues with the IAM permissions when trying to create those on Python. I was able to terminate/delete everything through Boto3.

![screenshot](https://github.com/sfergusond/MACS30123-Proj2/blob/master/q3_alert.png)


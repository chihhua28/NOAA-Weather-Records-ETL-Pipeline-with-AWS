### run ec2_producer_code on EC2
# ssh into EC2

chmod go-r <aws key pair location>
ssh -i <aws key pair location> <ec2 user name>@<ec2 public ip>

# install libraries
sudo yum install nano
sudo yum install python3
python3 -m pip install --user boto3
python3 -m pip install --user requests

# open nano file
nano
# copy ec2_producer_code.py and paste here
# Ctrl+O to save
# add file name "ec2_producer_code.py"
# Ctrl+X to exit

# run ec2_producer_code
python3 ec2_producer_code.py

# Sync Classcharts Homework with a Trello Board

## Installation

```
python setup.py install
```

## Configuration

To create configuration environment variables run `classcharts_trello_sync_configure`

The following envrionment variables are needed:

```sh
# Classcharts credentials
export CLASSCHARTS_USERNAME='[INSERT CLASSCHARTS USERNAME]'
export CLASSCHARTS_PASSWORD='[INSERT CLASSCHARTS PASSWORD]'

# The Trello API key and secret are available here: https://trello.com/app-key
export TRELLO_API_KEY='[INSERT TRELLO API KEY PASSWORD]'
export TRELLO_API_SECRET='[INSERT TRELLO API SECRET]'

# The below can be generated by running the `classcharts_trello_sync_configure`
export TRELLO_OAUTH_TOKEN='[INSERT TRELLO OAUTH TOKEN]'
export TRELLO_OAUTH_TOKEN_SECRET='[INSERT TRELLO OAUTH SECRET]'

# Students have the environment name STUDENT_xxx
# The format is Full Classcharts Name, Full Trello Name, Target Trello Board, Target Trello List, Number of minutes per slot
# eg:
export STUDENT_1='Jane Doe, Jane Doe, Jane, Inbox, 45'
export STUDENT_2='John Doe, Jonathan Doe, John, Inbox, 30'
```

## To Run

To synchronise data run the command `classcharts_trello_sync`

## To Deploy as AWS Lamba

### Prerequisites

* python3
* virtualenv (`pip install virtualenv`)
* awscli (`pip install awscli; aws configure`)
* AWS account with an IAM user

### Instalation

1. Create the deployment package with:

```sh
./scripts/build_lambda.sh
```

2. Create a basic role for the Lambda function allowing it to write logs to CloudWatch. Go to Lambda->Create Function->Create A Customer Role. Add a policy to allow it to write logs eg:

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "logs:CreateLogGroup",
                "logs:CreateLogStream",
                "logs:PutLogEvents"
            ],
            "Resource": "arn:aws:logs:*:*:*"
        }
    ]
}
```

3. Export this role as the CLASSCHARTS_LAMBDA_ROLE variable. For example:

```
export LAMBDA_ROLE_ENV=arn:aws:iam::xxxxxxxx:role/lambda_basic_execution
```

4. Create a group for the IAM user and add a policy that will allow the user to assign the above role and create lambda function:

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "SID1",
            "Effect": "Allow",
            "Action": "lambda:CreateFunction",
            "Resource": "*"
        },
        {
            "Sid": "SID2",
            "Effect": "Allow",
            "Action": "iam:PassRole",
            "Resource": "arn:...lambda_basic_execution"
        }
    ]
}
```

5. Run `./scripts/deploy_lambda.sh`

6. In the AWS Console under triggers add Cloudwatch Events and set up a Cron to trigger the Lambda periodically.

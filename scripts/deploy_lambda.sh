aws lambda create-function \
--region eu-west-1 \
--function-name classcharts \
--zip-file  fileb://dist/classcharts_lambda.zip \
--role $CLASSCHARTS_LAMBDA_ROLE \
--handler lambda.main \
--runtime python3.6 \
--timeout 180 \
--memory-size 128 \
--profile classcharts \
--environment Variables="{
    CLASSCHARTS_USERNAME='$CLASSCHARTS_USERNAME',
    CLASSCHARTS_PASSWORD='$CLASSCHARTS_PASSWORD',
    TRELLO_API_KEY='$TRELLO_API_KEY',
    TRELLO_API_SECRET='$TRELLO_API_SECRET',
    TRELLO_OAUTH_TOKEN='$TRELLO_OAUTH_TOKEN',
    TRELLO_OAUTH_TOKEN_SECRET='$TRELLO_OAUTH_TOKEN_SECRET',
    STUDENT_1='$STUDENT_1'
}"

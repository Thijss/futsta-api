# Note: This script assumes you have a lambda function on AWS with the same name as the current directory
# You can alter "${PWD##*/}" to a fixed name if this is not the case

# Zip
cd .venv/lib/python3.10/site-packages
zip -q -r ../../../../package.zip .
cd ../../../../
zip -q -r -g package.zip app

# Deploy
aws lambda update-function-code --function-name "${PWD##*/}" --zip-file fileb://package.zip

# Cleanup
rm package.zip

# automating-aws-with-python
Repository for the A Cloud Guru course 
*Automating AWS with Python*

## 01-webotron

Webotron is a script that will sync a local directory
to an s3 bucket, and optionally configure Route 53 
and cloudfront as well

### Features

Webotron currently has the fololowing features:

- List buckets
- List contents of a bucket
- Create and set up bucket
- Sync directory tree to a bucket
- Set AWS profile with --profile=<profileName>
- Configure route 53 domain

$ python webotron/webotron.py --profile=pythonAutomation find-cert kittentest.tokenring.net
{'CertificateArn': 'arn:aws:acm:us-east-1:325620063179:certificate/314d64ae-ee95-4e4f-b446-a6a7d7c413c3', 'DomainName': 'tokenring.net'}

Token@DESKTOP-6EL275N MINGW64 /c/tk_free_misc_notes/Python/AcloudGurus_code/code/automating-aws-with-python/01-webotron (master)
$ python webotron/webotron.py --profile=pythonAutomation find-cert tokenring.net
{'CertificateArn': 'arn:aws:acm:us-east-1:325620063179:certificate/314d64ae-ee95-4e4f-b446-a6a7d7c413c3', 'DomainName': 'tokenring.net'}


## 02-notifon
Notifon is a project to notify Slack users of changes to your AWS account using CloudWatch Events

### Features

Notifon currently has the following features:

- Send notifications to Slack when cloudwatch events happen

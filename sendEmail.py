import boto3

ses = boto3.client("ses")
s3 = boto3.resource('s3')

def handler(event, context):
    email = event['email']

    my_bucket = s3.Bucket('medicalreport')
    unsorted = []
    for file in my_bucket.objects.filter():
    unsorted.append(file)
    files = [obj.key for obj in sorted(unsorted, key=get_last_modified, reverse=True)][0:9]

    key = files[0]

    try:
        mail = ses.send_email(
            Source="netra.chandrasekhar@vitap.ac.in",
            Destination={
                'ToAddresses': email
           },
            Message={
                'Subject': {
                    'Data': "Emergency - Medical Report"
                },
                'Body': {
                    'Text': {
                        'Data': "https://medicalreport.s3.us-east-2.amazonaws.com/"+key
                    }
                }
            }
        )
    except BaseException as e:
        print(e)
        raise(e)

    return {"message": "Successfully executed"}
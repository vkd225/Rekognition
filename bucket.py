import boto3
s3 = boto3.resource('s3')

SRCBUCKET = "searchimagestricon"
TARGETBUCKET = "teargetimagestricon"
KEY_SOURCE = "s1.jpeg"

Target_List = []
for bucket in s3.buckets.all():
    source = (bucket.name)
    if source ==  'teargetimagestricon':
        for key in bucket.objects.all():
            out =  (key.key)
            Target_List.append(out)

length_target_list = len (Target_List)


for i in xrange(0, length_target_list):
    KEY_TARGET = str (Target_List[i])

def compare_faces(bucket, key, bucket_target, key_target, threshold=70, region="us-west-2"):
    rekognition = boto3.client("rekognition", region)
    response = rekognition.compare_faces(
	    SourceImage={
			"S3Object": {
				"Bucket": bucket,
				"Name": key,
			}
		},
		TargetImage={
			"S3Object": {
				"Bucket": bucket_target,
				"Name": key_target,
			}
		},
	    SimilarityThreshold=threshold,
	)
    return response['SourceImageFace'], response['FaceMatches']




for i in xrange(0, length_target_list):
    KEY_TARGET = str (Target_List[i])
    source_face, matches = compare_faces(SRCBUCKET, KEY_SOURCE, TARGETBUCKET, KEY_TARGET)
    match = len (matches)

    # the main source face
    #print "Source Face ({Confidence}%)".format(**source_face)

    if (match > 0):
        # one match for each target face
        for match in matches:
            print KEY_SOURCE + " matches " + KEY_TARGET + " with "
            print "  Similarity : {}%".format(match['Similarity'])
            # print "Target Face ({Confidence}%)".format(**match['Face'])


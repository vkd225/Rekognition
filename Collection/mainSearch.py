import boto3
s3 = boto3.resource('s3')

SOURCEBUCKET = "searchimagestricon"
COLLECTION = "TriconHeroesCollection"

KEY_SOURCE = raw_input("Enter Imagename: ")
s3.meta.client.upload_file(KEY_SOURCE, 'searchimagestricon', KEY_SOURCE)
print ("File Uploaded")


def search_faces_by_image(bucket, key, collection_id, threshold=80, region="us-west-2"):
	rekognition = boto3.client("rekognition", region)
	response = rekognition.search_faces_by_image(
		Image={
			"S3Object": {
				"Bucket": bucket,
				"Name": key,
			}
		},
		CollectionId=collection_id,
		FaceMatchThreshold=threshold,
	)
	return response['FaceMatches']

for record in search_faces_by_image(SOURCEBUCKET, KEY_SOURCE, COLLECTION):
	print len(record)
	face = record['Face']
	print len(face)
	print "Matches: {}".format(face['ExternalImageId']) + " with Similiraty: ({}%)".format(record['Similarity'])
	#print "  FaceId : {}".format(face['FaceId'])
	#print "  ImageId : {}".format(face['ExternalImageId'])



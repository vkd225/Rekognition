import boto3
s3 = boto3.resource('s3')

TARGETBUCKET = "targetimagestricon"
COLLECTION = "TriconHeroesCollection"

# Note: you have to create the collection first!
# rekognition.create_collection(CollectionId=COLLECTION)

# To create a collection "TriconHeroCollection" using awscli
# aws rekognition create-collection --collection-id TriconHeroesCollection
# aws:rekognition:us-west-2:979789329130:collection/TriconHeroesCollection	200


Target_List = []
for bucket in s3.buckets.all():
	target = (bucket.name)
	if target ==  'targetimagestricon':
		for key in bucket.objects.all():
			out =  (key.key)
			Target_List.append(out)
length_target_list = len (Target_List)


def index_faces(bucket, key, collection_id, image_id=None, attributes=(), region="us-west-2"):
	rekognition = boto3.client("rekognition", region)
	response = rekognition.index_faces(
		Image={
			"S3Object": {
				"Bucket": bucket,
				"Name": key,
			}
		},
		CollectionId=collection_id,
		ExternalImageId=image_id,
		DetectionAttributes=attributes,
	)
	return response['FaceRecords']


for i in range (0,length_target_list):
	KEY = Target_List[i]
	IMAGE_ID = KEY

	for record in index_faces(TARGETBUCKET, KEY, COLLECTION, IMAGE_ID):
		face = record['Face']
		print "ExternalImageId: {}".format(face['ExternalImageId']) + "     Confidence: {}%".format(face['Confidence'])
		# details = record['FaceDetail']
		# print "Confidence: {}%".format(face['Confidence'])
		# print "FaceId: {}".format(face['FaceId'])
		# print "ImageId: {}".format(face['ImageId'])

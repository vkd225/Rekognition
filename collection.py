# import boto3
#
# BUCKET = "teargetimagestricon"
# KEY = "amir.jpeg"
# IMAGE_ID = KEY  # S3 key as ImageId
# COLLECTION = "TriconHeroCollection"
#
# # Note: you have to create the collection first!
# # rekognition.create_collection(CollectionId=TRICONCOLLECTION)
# # aws rekognition create-collection --collection-id TriconHeroCollection
# # aws:rekognition:us-west-2:xxxxxxxxxxxxxxxxx:collection/TriconHeroCollection	200
#
#
#
#
#
#
# def index_faces(bucket, key, collection_id, image_id=None, attributes=(), region="us-west-2"):
# 	rekognition = boto3.client("rekognition", region)
# 	response = rekognition.index_faces(
# 		Image={
# 			"S3Object": {
# 				"Bucket": bucket,
# 				"Name": key,
# 			}
# 		},
# 		CollectionId=collection_id,
# 		ExternalImageId=image_id,
# 		DetectionAttributes=attributes,
# 	)
# 	return response['FaceRecords']
#
#
# for record in index_faces(BUCKET, KEY, COLLECTION, IMAGE_ID):
# 	face = record['Face']
# 	# details = record['FaceDetail']
# 	print "Face ({}%)".format(face['Confidence'])
# 	print "  FaceId: {}".format(face['FaceId'])
# 	print "  ImageId: {}".format(face['ImageId'])








import boto3

BUCKET = "searchimagestricon"
KEY = "s1.jpeg"

COLLECTION = "TriconHeroCollection"

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

for record in search_faces_by_image(BUCKET, KEY, COLLECTION):
	face = record['Face']
	print "Matched Face ({}%)".format(record['Similarity'])
	print "  FaceId : {}".format(face['FaceId'])
	print "  ImageId : {}".format(face['ExternalImageId'])


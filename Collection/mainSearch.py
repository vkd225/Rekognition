import boto3
s3 = boto3.resource('s3')

SOURCEBUCKET = "searchimagestricon"
COLLECTION = "TriconHeroesCollection"

# ------------------- Upload Source Image to the Source Bucket --------------------------------------

KEY_SOURCE = raw_input("Enter Imagename: ")
s3.meta.client.upload_file(KEY_SOURCE, 'searchimagestricon', KEY_SOURCE)
print ("File Uploaded")



# ----------------------- Search faces in the Collection ---------------------------------------------
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


# ---------------------------- Check the input if it is a face or not ----------------------------------
# Detect labels of the input image

def detect_labels(bucket, key, max_labels=10, min_confidence=90, region="us-west-2"):
	rekognition = boto3.client("rekognition", region)
	response = rekognition.detect_labels(
		Image={
			"S3Object": {
				"Bucket": bucket,
				"Name": key,
			}
		},
		MaxLabels=max_labels,
		MinConfidence=min_confidence,
	)
	return response['Labels']



# --------------------- Similarity with collection images. Confidence of the source image -------------------

for label in detect_labels(SOURCEBUCKET, KEY_SOURCE):
	# print "{Name} - {Confidence}%".format(**label)
	if "Person" in label.values():
		print "{Name} - {Confidence}%".format(**label)

		for record in search_faces_by_image(SOURCEBUCKET, KEY_SOURCE, COLLECTION):
			face = record['Face']
			print "Matches: {}".format(face['ExternalImageId']) + " with Similiraty: ({}%)".format(record['Similarity'])
			#print "  FaceId : {}".format(face['FaceId'])
			#print "  ImageId : {}".format(face['ExternalImageId'])


	else:
		print "{Name} - {Confidence}%".format(**label)

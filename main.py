import boto3
s3 = boto3.resource('s3')


SRCBUCKET = "searchimagestricon"
TARGETBUCKET = "teargetimagestricon"

FEATURES_BLACKLIST = ("Landmarks", "Emotions", "Pose", "Quality", "BoundingBox", "Confidence")


# ----------------------------- Load image from system and send it to S3 Bucket -----------------------

KEY_SOURCE = raw_input("Enter Fileneame: ")
s3.meta.client.upload_file(KEY_SOURCE, 'searchimagestricon', KEY_SOURCE)

print ("File Upload")


# Target Bucket
Target_List = []
for bucket in s3.buckets.all():
	source = (bucket.name)
	if source ==  'teargetimagestricon':
		for key in bucket.objects.all():
			out =  (key.key)
			Target_List.append(out)
length_target_list = len (Target_List)


# --------------------------------- Detect Facial Expressions ------------------------------------------

def detect_facial_expression(bucket, key, attributes=['ALL'], region="us-west-2"):
	rekognition = boto3.client("rekognition", region)
	response = rekognition.detect_faces(
		Image={
			"S3Object": {
				"Bucket": bucket,
				"Name": key,
			}
		},
		Attributes=attributes,
	)
	return response['FaceDetails']




# ------------------------------------------ Compare Faces----------------------------------------------

def compare_faces(bucket, key, bucket_target, key_target, threshold=80, region="us-west-2"):
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



# ---------------------------- Check the input if it is a face or not ----------------------------------
# Detect labels of the input image

def detect_labels(bucket, key, max_labels=10, min_confidence=95, region="us-west-2"):
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




# ----------------------------If Face, compare face with TargetBucket images-----------------------------------

for label in detect_labels(SRCBUCKET, KEY_SOURCE):
	# print "{Name} - {Confidence}%".format(**label)
	if "Person" in label.values():
		print "{Name} - {Confidence}%".format(**label)

		for i in xrange(0, length_target_list):
			KEY_TARGET = str (Target_List[i])
			source_face, matches = compare_faces(SRCBUCKET, KEY_SOURCE, TARGETBUCKET, KEY_TARGET)
			match = len (matches)

			# the main source face
			#print "Source Face ({Confidence}%)".format(**source_face)

			if (match > 0):
				# one match for each target face
				for match in matches:
					print KEY_SOURCE + " matches " + KEY_TARGET + " with " + "Similarity : {}%".format(match['Similarity'])

					# print "Target Face ({Confidence}%)".format(**match['Face'])


		for face in detect_facial_expression(SRCBUCKET, KEY_SOURCE):
			print "Face ({Confidence}%)".format(**face)




			#emotions
			no_emotions_detected = len(face['Emotions'])

			for i in range(0, no_emotions_detected):
				emotion = (face['Emotions'][i])
				if (emotion['Confidence'] > 85):
					print emotion['Type'], emotion['Confidence']



			# # facial features
			# for feature, data in face.iteritems():
			# 	if feature not in FEATURES_BLACKLIST:
			# 		# print "  {feature}({data[Value]}) : {data[Confidence]}%".format(feature=feature, data=data)
			# 		print data


	else:
		print "{Name} - {Confidence}%".format(**label)



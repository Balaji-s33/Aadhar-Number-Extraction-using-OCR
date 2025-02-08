import cv2,pytesseract,numpy as np,time,re
start_time=time.time()
def set_image_dpi(image):
	height,width=image.shape[:2]
	dpi=300
	return cv2.resize(image,None,fx=(dpi/70),fy=(dpi/70))
def correct_orientation(image):
	osd=pytesseract.image_to_osd(image)
	angle=int(re.search(r'Rotate: (\d+)',osd).group(1))
	return cv2.rotate(image,[cv2.ROTATE_90_CLOCKWISE,cv2.ROTATE_180,cv2.ROTATE_90_COUNTERCLOCKWISE][[90,180,270].index(angle)])if angle in[90,180,270]else image
image=cv2.imread('aadhar-card (1).jpg')
if image is None:
	print("Please provide a proper image.")
else:
	image=set_image_dpi(image)
	image=correct_orientation(image)
	gray=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
	detection_data=pytesseract.image_to_data(gray,output_type=pytesseract.Output.DICT)
	four_digit_numbers,bounding_boxes=[],[]
	for i in range(len(detection_data['text'])):
		text=detection_data['text'][i]
		x,y,w,h=detection_data['left'][i],detection_data['top'][i],detection_data['width'][i],detection_data['height'][i]
		if text.isdigit()and len(text)==4:
			four_digit_numbers.append(text)
			bounding_boxes.append((x,y,w,h))
	valid_sequences=[]
	for i in range(len(four_digit_numbers)-2):
		if i<len(four_digit_numbers)-3 and all(four_digit_numbers[j]!=four_digit_numbers[j+1]for j in range(i,i+3)):
			if four_digit_numbers[i+3]!=four_digit_numbers[i+2]:continue
			if four_digit_numbers[i+3]==four_digit_numbers[i+2]:continue
		if four_digit_numbers[i]!=four_digit_numbers[i+1]!=four_digit_numbers[i+2]:
			valid_sequences.append((four_digit_numbers[i],bounding_boxes[i],four_digit_numbers[i+1],bounding_boxes[i+1],four_digit_numbers[i+2],bounding_boxes[i+2]))
	if not valid_sequences:
		print("Please provide a proper image.")
	else:
		for seq in valid_sequences:
			combined_text=f"{seq[0]} {seq[2]} {seq[4]}"
			print("detected aadhar number:",combined_text)
			for box in[seq[1],seq[3],seq[5]]:
				x,y,w,h=box
				cv2.rectangle(image,(x,y),(x+w,y+h),(0,255,0),2)
		cv2.imwrite('new.jpg',image)
end_time=time.time()
print("Time taken:",end_time-start_time,"seconds")
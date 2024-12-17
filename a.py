import cv2

cap = cv2.VideoCapture("repo/bing.mp4") 

while(cap.isOpened()):
    ret, frame = cap.read()
    if not ret:
        break
    cv2.imshow('Video Player', frame)

    if cv2.waitKey(25) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
# import streamlit as st
# import cv2
# import face_recognition as frg
# import yaml 
# from utils import recognize, build_dataset
# # Path: code\app.py

# st.set_page_config(layout="wide")
# #Config
# cfg = yaml.load(open('config.yaml','r'),Loader=yaml.FullLoader)
# PICTURE_PROMPT = cfg['INFO']['PICTURE_PROMPT']
# WEBCAM_PROMPT = cfg['INFO']['WEBCAM_PROMPT']



# st.sidebar.title("Settings")



# #Create a menu bar
# # menu = ["Picture","Webcam"]
# menu = ["Webcam"]
# choice = st.sidebar.selectbox("Input type",menu)
# # Put slide to adjust tolerance
# TOLERANCE = st.sidebar.slider("Tolerance",0.0,1.0,0.5,0.01)
# st.sidebar.info("Tolerance is the threshold for face recognition. The lower the tolerance, the more strict the face recognition. The higher the tolerance, the more loose the face recognition.")

# #Infomation section 
# st.sidebar.title("Student Information")
# name_container = st.sidebar.empty()
# id_container = st.sidebar.empty()
# name_container.info('Name: Unnknown')
# id_container.success('ID: Unknown')

# st.title("Face Recognition App")
# st.write(WEBCAM_PROMPT)
# #Camera Settings
# cam = cv2.VideoCapture(0)
# cam.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
# cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
# FRAME_WINDOW = st.image([])
# # st.button('Login')
# # while True:
    
# #     ret, frame = cam.read()
# #     if not ret:
# #         st.error("Failed to capture frame from camera")
# #         st.info("Please turn off the other app that is using the camera and restart app")
# #         st.stop()
# #     image, name, id = recognize(frame,TOLERANCE=0.4)
# #     image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
# #     #Display name and ID of the person
    
# #     name_container.info(f"Name: {name}")
# #     id_container.success(f"ID: {id}")
# #     FRAME_WINDOW.image(image)
# #     if name!='Unknown':
# #         # st.success(name ,'Authenticated')
# #         st.success(name+' - Authenticated!', icon="✅")

# # Display live camera feed
# def live_feed():
#     ret, frame = cam.read()
#     if not ret:
#         st.error("Failed to capture frame from camera")
#         st.info("Please turn off any other apps using the camera and restart the app.")
#         return None
#     frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#     FRAME_WINDOW.image(frame_rgb, channels="RGB")
#     return frame

# # Start live feed
# captured_frame = None
# while cam.isOpened():
#     captured_frame = live_feed()
#     if captured_frame is None:
#         break
#     if st.button("Capture Image", key="capture_button"):
#         if captured_frame is not None:
#             cam.release()  # Stop the camera feed
#             image, name, id = recognize(captured_frame, TOLERANCE=0.4)
#             image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
#             name_container.info(f"Name: {name}")
#             id_container.success(f"ID: {id}")
#             FRAME_WINDOW.image(image, caption="Captured Image")
            
#             if name != "Unknown":
#                 FRAME_WINDOW.empty()  # Clear the live feed area
#                 st.success(f"{name} - Authenticated! ✅")
#             else:
#                 st.error("Authentication failed! User not found in the database.")
#         else:
#             st.error("Failed to capture frame from camera")
#             st.info("Please turn off any other apps using the camera and restart the app.")
#         break




import streamlit as st
import face_recognition
import numpy as np
from PIL import Image

# Load reference image and encode
REFERENCE_IMAGE_PATH = "romy.jpeg"  # Change this to your reference image path
reference_image = face_recognition.load_image_file(REFERENCE_IMAGE_PATH)
reference_encoding = face_recognition.face_encodings(reference_image)[0]

def authenticate_user(image):
    face_locations = face_recognition.face_locations(image)
    face_encodings = face_recognition.face_encodings(image, face_locations)
    
    for face_encoding in face_encodings:
        matches = face_recognition.compare_faces([reference_encoding], face_encoding)
        if True in matches:
            return True
    return False

def main():
    st.title("Facial Authentication App")
    st.write("Capture an image using your camera for authentication.")

    captured_image = st.camera_input("Take a Photo")
    
    if captured_image:
        image = Image.open(captured_image)
        image = np.array(image)  # Convert to NumPy array
        # st.image(image, caption="Captured Image", use_column_width=True)

        if authenticate_user(image):
            st.success("Authentication Successful!")
        else:
            st.error("Authentication Failed!")

if __name__ == "__main__":
    main()

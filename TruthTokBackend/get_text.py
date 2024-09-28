import pyktok as pyk
import speech_recognition as sr
from pydub import AudioSegment
import os
from imutils.object_detection import non_max_suppression
import numpy as np
import cv2
from download_reels import download
import pytesseract

def download_vid(link):
    if 'tiktok' in link: 
        pyk.specify_browser('chrome')
        pyk.save_tiktok(link, True, 'tiktok_video.mp4', 'chrome')
        return "tiktok_video.mp4"
    elif 'reel' in link:
        download(link, 'reel_video.mp4')
        return "reel_video.mp4"
    else:
        raise ValueError("Unsupported link format")

def get_audio(video):
    video = AudioSegment.from_file(video, format="mp4")
    audio = video.set_channels(1).set_frame_rate(16000).set_sample_width(2)
    audio.export("audio.wav", format="wav")

    recognizer = sr.Recognizer()

    with sr.AudioFile("audio.wav") as source:
        audio_text = recognizer.record(source)
    transcription_text = recognizer.recognize_google(audio_text, language='en-US')

    with open("transcription.txt", "w") as file:
        file.write(transcription_text)

    return transcription_text

net = cv2.dnn.readNet("frozen_east_text_detection.pb")

def detect_text(frame):
    newW, newH = (320, 320)
    rW, rH = frame.shape[1] / float(newW), frame.shape[0] / float(newH)
    frame_resized = cv2.resize(frame, (newW, newH))

    blob = cv2.dnn.blobFromImage(frame_resized, 1.0, (newW, newH), (123.68, 116.78, 103.94), swapRB=True, crop=False)
    net.setInput(blob)
    (scores, geometry) = net.forward(["feature_fusion/Conv_7/Sigmoid", "feature_fusion/concat_3"])
    
    (numRows, numCols) = scores.shape[2:4]
    rects = []
    confidences = []
    detected_text = ""

    for y in range(0, numRows):
        scoresData = scores[0, 0, y]
        xData0 = geometry[0, 0, y]
        xData1 = geometry[0, 1, y]
        xData2 = geometry[0, 2, y]
        xData3 = geometry[0, 3, y]
        anglesData = geometry[0, 4, y]

        for x in range(0, numCols):
            if scoresData[x] < 0.5:
                continue

            (offsetX, offsetY) = (x * 4.0, y * 4.0)
            angle = anglesData[x]
            cos = np.cos(angle)
            sin = np.sin(angle)
            h = xData0[x] + xData2[x]
            w = xData1[x] + xData3[x]
            endX = int(offsetX + (cos * xData1[x]) + (sin * xData2[x]))
            endY = int(offsetY - (sin * xData1[x]) + (cos * xData2[x]))
            startX = int(endX - w)
            startY = int(endY - h)

            rects.append((startX, startY, endX, endY))
            confidences.append(scoresData[x])

    boxes = non_max_suppression(np.array(rects), probs=confidences)

    for (startX, startY, endX, endY) in boxes:
        startX = int(startX * rW)
        startY = int(startY * rH)
        endX = int(endX * rW)
        endY = int(endY * rH)
        cv2.rectangle(frame, (startX, startY), (endX, endY), (0, 255, 0), 2)

        roi = frame[startY:endY, startX:endX]
        text = pytesseract.image_to_string(roi)
        detected_text += text + " "

    return frame, detected_text

def process_video(video_path):
    cap = cv2.VideoCapture(video_path)
    frames_processed = 0
    all_detected_text = ""

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
    
        if frames_processed % 100 == 0:
            frame, detected_text = detect_text(frame)
            all_detected_text += detected_text
            cv2.imshow("Text Detection", frame)
        
        frames_processed += 1

        if cv2.waitKey(1) == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()

    return all_detected_text
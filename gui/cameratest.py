from threading import Thread
import cv2, time

class VideoStreamWidget(object):
    def __init__(self):
        self.capture = cv2.VideoCapture('rtsp://Drimages:Satan666@192.168.0.172:554/live/ch1')
        # Start the thread to read frames from the video stream
        self.thread = Thread(target=self.update, args=())
        self.thread.daemon = True
        self.thread.start()

    def update(self):
        # Read the next frame from the stream in a different thread
        while True:
            if self.capture.isOpened():
                (self.status, self.frame) = self.capture.read()
##            time.sleep(.01)

    def show_frame(self):
        # Display frames in main program
        cv2.imshow('frame', self.frame)
        key = cv2.waitKey(1)
        if key == ord('q'):
            self.capture.release()
            cv2.destroyAllWindows()
            exit(1)

if __name__ == '__main__':
    video_stream_widget = VideoStreamWidget()
    while True:
        try:
            video_stream_widget.show_frame()
        except AttributeError:
            pass

##import cv2
##import numpy as np
#ffpyplayer for playing audio
##from ffpyplayer.player import MediaPlayer
##video_path='rtsp://Drimages:Satan666@192.168.0.172:554/live/ch1'
##def PlayAudio(video_path):
####    video=cv2.VideoCapture(video_path)
##    player = MediaPlayer(video_path)
##    while True:
####        grabbed, frame=video.read()
##        audio_frame, val = player.get_frame()
####        if not grabbed:
####            print("End of video")
####            break
####        if cv2.waitKey(28) & 0xFF == ord("q"):
####            break
####        cv2.imshow("Video", frame)
##        if val != 'eof' and audio_frame is not None:
##            #audio
##            img, t = audio_frame
####    video.release()
##    cv2.destroyAllWindows()
##PlayAudio(video_path)

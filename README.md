# Shru-The-Virtual-Sign-Language-Assistant

Uses Azure Cognitive Services to obtain the speech phrases from a video file. Maps the phrases to corresponding ASL representation from the ASL Mini Database. Stiches and lays the ASL video on top of the original video.

__Code Description__
1. _extract_audio(video,output)_: This function takes in a video file and extracts the corresponding audio file. The "ffmpeg" library is used for this conversion which converts in almost real time.
2. _speech_recognize_continuous_from_file()_: This function performs continuous speech recognition with input from an audio file. The Azure Speech SDK is employed for this purpose. Speech-to-text from the Speech SDk allows the conversion from an audio stream to text in real time.
3. The output text from the previous function are mapped to the videos in the database. And then finally, the videos are stitched together to provide a continuous and seamless experience. 

__Database Description__
The ASL_Mini_Database is database consisting of some phrases in American Sign Language (ASL). 

Provide Subscription Key and Region. Name the input video as 'Input.mp4'

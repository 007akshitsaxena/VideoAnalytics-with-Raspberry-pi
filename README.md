# AI powered automated attendance monitoring system
This project is an automated attendance monitoring system having a producer/consumer system architecture. First component(producer) is Raspberry pi (Raspberry pi 3 model B+) feeds video stream over the internet to the second core component(consumer) a web-server(Flask), which runs machine learning algorithms to process received video feeds and finally generate attendance sheet.

## About Web-Server
- For running `emloyee.py` as web service I used Flask microweb framework.
- A quick review of machine learning algorithms.
  - I have used face_recognition library (author: Adam Geitgey)
  - Pipeline of standard and Deep learning algorithms was designed in same order to solve face_recognition
    - Histogram of Oriented Gradients (HoG) : This algoritms is used to locate faces in whole image.
    - Facial Landmark estimation : To overcome the problem of different poses/posture of faces this algo marks 68 specific locations on every      face.
    - Convolutional Neural Network (CNN): This algorithms performs face encoding by generating embeddings(128-D feature matrix) for each face.
    - Support Vector Machine (SVM): This algorithm perform final classification task.
- If you want to try 
  - Make sure you are using python=3.3 or greater version and better to make separate virtual environment
  - Refer this link to install face_recognition library: https://github.com/ageitgey/face_recognition
  - Once done move inside your directory where you clone and run this on shell `pip install -r requirements.txt`
  - Web-server is ready to use.

[Interested in detail explanation of machine learning algorithms refer this.](https://medium.com/@ageitgey/machine-learning-is-fun-part-4-modern-face-recognition-with-deep-learning-c3cffc121d78)

## Headless raspberry pi setup
32 GB micro SD card flashed with Raspbian image. After flashing, SD card volume is partitioned into two volumes namely 
- boot
- Rootfs

### How to SSH and connect pi to wifi-router
If you are running headless pi(without any monitor & keyboard) then only follow this because by default SSH service is disabled in raspi. Move inside the boot volume of SD card 
- For ssh :
  - Create a blank file and save it by name `ssh` without any extension.
- For connection to wifi-router:
  - Create another blank file and save it by name `wpa_supplicant.conf` and open it and type below :
  
```
country=IN  # your two letter country code, IN is for India
update_Config = 1
ctrl_interface=/var/run/wpa_supplicant

network={
    ssid="your_Wifi_name"
    psk ="your_Wifi_password"
    key_mgmt=WPA-PSK
}
```

### Remote access to Raspi

- Dynamic Host Configuration Protocol service (DHCP) inbuilt in modern routers assign dynamic IP addresses to all network devices. Access your router configuration page and assign your raspi a static IP. 

- Do port forwarding for streaming over the internet.

```
#employee.py
video_capture = cv2.VideoCapture("http://pi:raspberry@static_IP_address:Port") #if you are in same network
video_capture = cv2.VideoCapture("http://pi:raspberry@public_IP_of_router:Port")  #if you are in different network

```


                                                 




    
    
    
    
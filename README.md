# Library Management System
Platform- python3 
hardware- 2 X Raspberry pie, camera
## File details:
In total 10 python files
- userLogin.py
- masterLib.py
- face_reco.py
- psql.py
- addBook.py
- borrowBook.py
- returnBook.py
- calender_event.py
- logout_client.py
- visualisation.py
## Libraries Used:
UI:flask,flask_bootstrap,flask_WTF,flask_table,zipfile,
facial recognition: imutils, face_recognition, argparse,pickle, time and cv2
masterlib: socket and json
calender_event:datetime, googleapiclient, httplib2 and oauth2client 
userlogin: sqlite3, passlib
Database: GCP(Gcloud)- postgres
documentation- Sphinx
HTML format documentation: Documentation/_build/html/index.html
## References:
GoogleAPi- https://developers.google.com/calendar/quickstart/python
face_recog : https://www.pyimagesearch.com/2018/06/18/face-recognition-with-opencv-python-and-deep-learning/
sphinx- http://www.sphinx-doc.org/en/master/
https://stackoverflow.com/questions/47376744/how-to-prevent-cached-response-flask-server-using-chrome
https://stackoverflow.com/questions/42214376/zip-single-file
https://flask-table.readthedocs.io/en/stable/#more-about-buttoncol
https://sweetcode.io/flask-python-3-mysql/
https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-xi-facelift
http://mattrichardson.com/Raspberry-Pi-Flask/
https://github.com/plumdog/flask_table/blob/master/examples/simple_app.py

## Group Members:
- Deepika Gill - s3698341
- Sanchit Sharma - s3695622
- Sarvatra Indoria - s3699505
- Yamin Huzaifa - s3667340

## Quickstart

-Install the required dependencies in master pi 
-Setup a GCloud account ,and setup database credentials 
-files on RP-pie userLogin.py & face_recognition
-remaining file need to be in master pi 
-launch masterlib.py in master-pi(intiate server listen)
-launch userLogin.py in client pi  


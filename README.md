**Whiteflycount API Sample**

----
This repository has files for the whiteflycount API. 
The API is python based using the Django Rest Framework



**Requirements**

*All requirements are included in requirements.txt file. Main requirements are:*
*  Django == 1.11.9
*  Pillow
*  Opencv-python
*  Scikit-learn
*  Scikit-image
*  Requests(for client.py only)


1.  **Installation**
    *  `pip install -r requirements.txt`(preferably in python3 virtual environment)
2.  **Running the API**
  
    *  python manage.py runserver 
        *(Runs on localhost:8000 by default. Can specify port by using runserver host:port e.g. localhost:5000)*
3.  **Running the client**
    *  Sample client written in python
    *  `python client.py   "path-to-image"    "url-to-post"`(e.g. `python client.py   test_images/image58.jpg  http://35.196.103.193/home/api2/`)
    *  sample server with browsable API is hosted at http://35.196.103.193/home/api2/ and sample images in test_images folder
    *  reults are stored in test_images folder with copy of annotated image
4.  **API Output**  
    *  Result is JSON with format and returns count and list coordinates of position whiteflies on the input image.
    *  `{\"Count\": \"4\", \"Detected_Boxes\": [[478, 347, 492, 361], [294, 364, 308, 378], [210, 472, 224, 486], [688, 588, 702, 602]]}`
    

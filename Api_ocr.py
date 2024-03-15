import requests
def fun():
    url = "https://demo.api4ai.cloud/ocr/v1/results?algo=simple-text"
    querystring = {"etype": "image"}


    image_path = r"D:\react_sql\output_path\img.png"
    with open(image_path, "rb") as image_file:
        image_data = image_file.read()

    payload = {"image": ("image.jpg", image_data)}

    headers = {
        "X-RapidAPI-Key": "d24645bdedmshc25dba0ff5b4c9ap13cd02jsn4f8d3704a2fc",
        "X-RapidAPI-Host": "ocr43.p.rapidapi.com"
    }

    response = requests.post(url, files=payload, headers=headers, params=querystring)

    if response.status_code == 200:
        result = response.json()
        # print(result)
        text = result['results'][0]['entities'][0]['objects'][0]['entities'][0]['text']
        print("Extracted Text:", text)

    else:
        print("Error:", response.status_code)

# config = {
#     "host": "localhost",
#     "user": "vaibhav",
#     "password": "vaibhav@123__",
#     "database": "vaibhav",
#     'auth_plugin':'mysql_native_password'
# }
    
    

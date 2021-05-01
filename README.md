# **Measure Visual Acuity API**
## Team SecureVision 

## Requirements
- Install all libraries mentioned in requirements.txt
 ```python
pip install -r requirements.txt
```
- Mongo-URI has to be provided for database connectivity.
- Initialize the variables sender_email, password and mongo_url with appropriate credentials.

## Usage
- The api takes in the following parameters - 'position', 'distance', 'dpi' and 'chart_type'.
- Based on the parameters, optotype corresponding to the position is returned with the specific size.
 ```python
python mva_api.py
```

## Screenshots
![Screenshot (237)](https://user-images.githubusercontent.com/62014238/116792635-86be9d00-aadf-11eb-964b-d432fabd1563.png)
![Screenshot (238)](https://user-images.githubusercontent.com/62014238/116792638-8c1be780-aadf-11eb-9107-060de5c41dbc.png)



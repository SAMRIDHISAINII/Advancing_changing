# Advancing_changing

 > AI-powered web application able to track changes in urban landscape

### Technologies

- Vue.js (frontend)
- Flask (backend)
- PyTorch (machine learning library)
- Unet++ (neural network)

### Structure
```Python
.
├── app
│   └── unet # UNET++ files
...
├── src      # Vue.js frontend
└── app.py   # Flask backend
...
```

### How to use

0. Install CUDA Toolkit and cudNN.

1. Set up your environment. I recommend you to use anaconda for it since we're doing some machine learning:
```bash
# create conda env with Python 3.7
$ conda create -n junctionx python=3.7

# activate it
$ conda activate junctionx

# install all dependencies
$ pip install -r requirements.txt
```

2. Install Node.JS modules:
```bash
$ npm install
```

3. Run backend:
```bash
$ python app.py
```
It is usually run on `http://127.0.0.1:5000/` (basically only needed for API)

4. Run frontend (you need second terminal):
```bash
$ npm run serve
```
It is usually run on `http://127.0.0.1:8080/` (open in your browser)

5. Upload pics to neural net and get results 
   
    5.1. Go to `Upload` page 
   
    5.2. Upload two pics of the size `650x650` before and after 

    5.3. Click `Upload` button
 
    5.4. Get result and download by clicking `Download` button


# Smart Home Energy Management System
*This is the final project for Principals Of Database System Fall 2023*  

## Designing Stage
This part includes need analysis, schema design, simulative data generation, and some query testings. Documentations can be found in [part1.pdf](./part1.pdf) 

## How To RUN

### 1. Clone And Run Frontend

First RUN [SHEMS Client](https://github.com/yangfan2001/shemsapp ) in Localhost using node.js in localhost

And then Clone This Repo

### 2. Create a Virtual Environment

```
cd SHEMS_server
python -m venv venv
```

### 3. Activate the Virtual Environment

Before working on your project, you need to activate the virtual environment.

For Windows:

```
bashCopy code
.\venv\Scripts\activate
```

For macOS/Linux:

```
bashCopy code
source venv/bin/activate
```

Once activated, your command line will usually show `(venv)` before the prompt, indicating that the virtual environment is active.

### 4. Install Dependencies

run:

```
pip install -r requirements.txt
```

### 5. Run Server

```
Python app.py
```


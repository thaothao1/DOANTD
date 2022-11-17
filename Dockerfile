# 
FROM python:3.9

# 
WORKDIR /web

# 
COPY ./requirements.txt ./requirements.txt

# 
RUN pip install --no-cache-dir --upgrade -r ./requirements.txt

# 
COPY ./web ./web

# 
CMD ["uvicorn", "web.main", "--host", "0.0.0.0", "--port", "80"]

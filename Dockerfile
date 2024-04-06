FROM amancevice/pandas:slim

RUN mkdir /backend
WORKDIR /backend

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
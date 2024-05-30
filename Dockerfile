FROM amancevice/pandas

RUN mkdir /backend
WORKDIR /backend

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
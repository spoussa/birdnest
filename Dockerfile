FROM python

WORKDIR /birdnest

# Copy the current directory contents into the container
COPY . /birdnest//

RUN apt-get update \
  && apt-get install -y --no-install-recommends \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*


ENV PYTHONUNBUFFERED=1


# Install any needed packages specified in requirements.txt
RUN pip3 install --requirement requirements.txt

# uWSGI will listen on this port
EXPOSE 8000

COPY ./entrypoint.sh /birdnest/

RUN chmod u+x entrypoint.sh


ENTRYPOINT ["./entrypoint.sh"]

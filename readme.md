# Remote Speed Test

This is a small utility that will sit on a random server and respond with the output of speedtest-cli on a request to 127.0.0.1:9002.

...mainly so I can test my wired speeds and maybe graph them somewhere.

## Running

Pick either method then access localhost or your server at port 9002. 

A lock file will be created preventing more than one test running at the same time. Hopefully it doesn't crash mid-run :^)

If it does, you can clear the lock file at `/tmp/speedtest.lock` or restart the docker container if you're using docker.

If either `bits` value, or `ping` return `-1.0` that means the value couldn't be parsed from the speed test results.

### With Docker Compose

```bash
docker-compose up -d --build
# And then you'll see something like this:
curl http://127.0.0.1:9002/
{"success":true,"download":{"bits":156463759.17167062,"megabits":156.4637591716706,"bytes":19557969.896458827,"megabytes":19.557969896458825},"upload":{"bits":184543743.55893108,"megabits":184.54374355893108,"bytes":23067967.944866385,"megabytes":23.067967944866385},"ping":6.522}
```

### Outside of Docker

You may want to use a virtualenv!

```bash
pip install -r requirements.txt
fastapi run main.py
# And then you'll see something like this:
curl http://127.0.0.1:9002/
{"success":true,"download":{"bits":156463759.17167062,"megabits":156.4637591716706,"bytes":19557969.896458827,"megabytes":19.557969896458825},"upload":{"bits":184543743.55893108,"megabits":184.54374355893108,"bytes":23067967.944866385,"megabytes":23.067967944866385},"ping":6.522}
```
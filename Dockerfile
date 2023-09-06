# using multi-stage: 2 build steps auto run in parallel

###############################################################################
# super lightweight webserver

FROM ubuntu:latest AS serverbuilder

WORKDIR /home

# assembler to binary
RUN apt update &&\
    apt install -y git make yasm as31 nasm binutils &&\
    git clone --depth=1 https://github.com/nemasu/asmttpd.git &&\
    cd asmttpd &&\
    make release

###############################################################################
# jekyll build

FROM ruby:latest AS pagebuilder

WORKDIR /home

# install deps (docker cache)
COPY Gemfile .
RUN bundle install

# build
COPY . .
RUN bundle exec jekyll build --baseurl ''

###############################################################################
# run

FROM scratch

LABEL name="Kinh nhật tụng"
LABEL description="Vietnamese Mahayana Buddhism rituals in multiple languages"
LABEL author="PTA"

COPY --from=serverbuilder /home/asmttpd/asmttpd /
COPY --from=pagebuilder /home/_site /web_root
# default dir name of asmttpd

# any port of choice, here python default port
EXPOSE 8000

CMD ["/asmttpd", "/web_root", "8000"]

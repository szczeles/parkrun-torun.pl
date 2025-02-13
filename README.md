# parkrun-torun.pl page

## Local run

```
$ sudo docker run -p 4000:4000 --rm -ti -v `pwd`:/srv/jekyll jekyll/jekyll:latest bash
```

Inside container:

```
chown jekyll.jekyll /usr/gem/cache/
bundle install
bundle exec jekyll serve --host=0.0.0.0 --watch --safe
```

# api

## How to update blog_infos
```bash
$ cd scraping/blog_info
$ bash execute_all.sh
```

### How to upload to server
In the case of the following server info.

- name: kokoichi
- local ip address: 192.168.x.y

```sh
$ scp -r imgs/nogizaka kokoichi@192.168.x.y:/var/www/html/imgs/blog/
```

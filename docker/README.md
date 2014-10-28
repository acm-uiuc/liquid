Running via Docker
=================

```
docker run -t -i \
  -v /path/lot/local/settings/folder:/config \
  -e LOCAL_SETTINGS=/config/local_settings.py \
  quay.io/acmuiuc/liquid
```

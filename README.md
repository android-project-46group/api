# Get information from website

[![License](https://img.shields.io/badge/license-MIT-blue)](./LICENSE)

[![](https://img.shields.io/badge/android-555.svg?logo=kotlin)](https://github.com/android-project-46group/android)
[![](https://img.shields.io/badge/server-555.svg?logo=go)](https://github.com/android-project-46group/api-server)
[![](https://img.shields.io/badge/crawler-555.svg?logo=python)](https://github.com/android-project-46group/api)
[![](https://img.shields.io/badge/ios-555.svg?logo=swift)](https://github.com/android-project-46group/ios)

## How to update blogs in postgreSQL

- Just run [night_batch.sh](./batch/night_batch.sh)

```bash
$ bash night_batch.sh
```

- The night_batch file are executed automatically at 12 and 18.
- You can update manually by accessing [this endpoint](https://kokoichi0206.mydns.jp/blog/update/) with correct queries.
  - [see this issue](https://github.com/android-project-46group/api/issues/9)

# manhuadb 漫画下载

## Usage

### Prepare

```shell
pip install -r requirements.txt
```

### Download

```shell
python manhuadb.py -t {series,book} -u [url] -p [path] 
```

#### Parameter explain

* -h, --help            show this help message and exit
* -t {series,book}, --type {series,book}
* -u URL, --url URL
* -p PATH, --path PATH default: current folder

The `series` url be like https://www.manhuadb.com/manhua/xxx,
and `book` url be like https://www.manhuadb.com/manhua/xxx/xxx_xxx.html

the `PATH` arg is optional

### TODO

- [ ] Retry after network error
- [ ] Solution for empty data page
- [x] Command for single page
- [ ] Support webp extension
- [x] Check integrity

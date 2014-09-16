# Usage

```
usage: gwmt-dl [-h] [-v] [-d]
[-S {top_queries,top_pages,TOP_QUERIES,TOP_PAGES}] -u USER
[-p PASSWORD] -w WEBSITE [-l LIMIT_ROWS]

optional arguments:
-h, --help            show this help message and exit
-v, --verbose
-d, --debug
-S/--selected {top_queries,top_pages,TOP_QUERIES,TOP_PAGES}
-u USER, --user USER
-p PASSWORD, --password PASSWORD
-w WEBSITE, --website WEBSITE
-l LIMIT_ROWS, --limit-rows LIMIT_ROWS
```

The default selected query type is `TOP_QUERIES`. So using the `-S` option may be mostly unnecessary for most people as top pages information can be gathered from Google Analytics with better information.

Note that the `--website`/`-w` argument can take just a domain name like `adomain.com` but this will make the script default to using `http://adomain.com` when `https://` may be desired. In the case of `https://` always specify the full website domain with protocol (e.g. `https://adomain.com`). In any case, do not forget the subdomain (`www.`).

The `--limit-rows`/`-l` argument takes in an integer to limit amount of rows returned, mostly useful when using the `TOP_QUERIES` functionality.

# Two-factor authentication

If you have two-factor authentication enabled in your account, be sure to visit the Google [App passwords](https://security.google.com/settings/security/apppasswords) page to set up a specific password for this script. You can even store it on your machine locally:

```
vim ~/.gwmt-dl-pass         # Paste password in, :wq
chmod 0400 ~/.gwmt-dl-pass  # For (hopefully obvious) security reasons
```

Then you can invoke like so: `gwmt-dl -u myname@gmail.com -p $(< ~/.gwmt-dl-pass) ...`.

Yes, you can do this with your regular password too. Part of the point here is to avoid shell history keeping your password.

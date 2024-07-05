# Board - web

### Vulnerability

TinyIB, przy tworzeniu postu, queryuje URL podany w `embed` polu.

```php
$data = url_get_contents(trim($_POST['embed']));
if (strlen($data) == 0) {
    fancyDie(__('Failed to download file at specified URL.'));
}
```

> https://gitlab.com/tslocum/tinyib/-/blob/master/imgboard.php#L377-380

### Solution

Wysłać własny URL w polu embed, dostać clearnet'owy adres IP.

```
$ curl "http://209.38.244.39/flag/"
Hello</br></br>ecsc24{GreetingsPeopleOfTheWorld-WeWereAnonymous}
```
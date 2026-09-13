# Installing Webfonts
Follow these simple Steps.

## 1.
Put `teko/` Folder into a Folder called `fonts/`.

## 2.
Put `teko.css` into your `css/` Folder.

## 3. (Optional)
You may adapt the `url('path')` in `teko.css` depends on your Website Filesystem.

## 4.
Import `teko.css` at the top of you main Stylesheet.

```
@import url('teko.css');
```

## 5.
You are now ready to use the following Rules in your CSS to specify each Font Style:
```
font-family: Teko-Light;
font-family: Teko-Regular;
font-family: Teko-Medium;
font-family: Teko-SemiBold;
font-family: Teko-Bold;
font-family: Teko-Variable;

```
## 6. (Optional)
Use `font-variation-settings` rule to controll axes of variable fonts:
wght 300.0

Available axes:
'wght' (range from 300.0 to 700.0


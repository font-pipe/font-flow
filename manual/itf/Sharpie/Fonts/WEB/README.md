# Installing Webfonts
Follow these simple Steps.

## 1.
Put `sharpie/` Folder into a Folder called `fonts/`.

## 2.
Put `sharpie.css` into your `css/` Folder.

## 3. (Optional)
You may adapt the `url('path')` in `sharpie.css` depends on your Website Filesystem.

## 4.
Import `sharpie.css` at the top of you main Stylesheet.

```
@import url('sharpie.css');
```

## 5.
You are now ready to use the following Rules in your CSS to specify each Font Style:
```
font-family: Sharpie-Light;
font-family: Sharpie-Regular;
font-family: Sharpie-Bold;
font-family: Sharpie-Extrabold;
font-family: Sharpie-Black;
font-family: Sharpie-Variable;

```
## 6. (Optional)
Use `font-variation-settings` rule to controll axes of variable fonts:
wght 900.0

Available axes:
'wght' (range from 300.0 to 900.0


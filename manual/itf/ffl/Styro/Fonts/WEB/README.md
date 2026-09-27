# Installing Webfonts
Follow these simple Steps.

## 1.
Put `styro/` Folder into a Folder called `fonts/`.

## 2.
Put `styro.css` into your `css/` Folder.

## 3. (Optional)
You may adapt the `url('path')` in `styro.css` depends on your Website Filesystem.

## 4.
Import `styro.css` at the top of you main Stylesheet.

```
@import url('styro.css');
```

## 5.
You are now ready to use the following Rules in your CSS to specify each Font Style:
```
font-family: Styro-Extralight;
font-family: Styro-Light;
font-family: Styro-Regular;
font-family: Styro-Medium;
font-family: Styro-Semibold;
font-family: Styro-Bold;
font-family: Styro-Extrabold;
font-family: Styro-Black;
font-family: Styro-Variable;

```
## 6. (Optional)
Use `font-variation-settings` rule to controll axes of variable fonts:
wght 900.0

Available axes:
'wght' (range from 200.0 to 900.0


# Installing Webfonts
Follow these simple Steps.

## 1.
Put `asap/` Folder into a Folder called `fonts/`.

## 2.
Put `asap.css` into your `css/` Folder.

## 3. (Optional)
You may adapt the `url('path')` in `asap.css` depends on your Website Filesystem.

## 4.
Import `asap.css` at the top of you main Stylesheet.

```
@import url('asap.css');
```

## 5.
You are now ready to use the following Rules in your CSS to specify each Font Style:
```
font-family: Asap-Regular;
font-family: Asap-Italic;
font-family: Asap-Medium;
font-family: Asap-MediumItalic;
font-family: Asap-SemiBold;
font-family: Asap-SemiBoldItalic;
font-family: Asap-Bold;
font-family: Asap-BoldItalic;
font-family: Asap-Variable;
font-family: Asap-VariableItalic;

```
## 6. (Optional)
Use `font-variation-settings` rule to controll axes of variable fonts:
wght 400.0

Available axes:
'wght' (range from 400.0 to 700.0


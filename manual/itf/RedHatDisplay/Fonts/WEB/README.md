# Installing Webfonts
Follow these simple Steps.

## 1.
Put `red-hat-display/` Folder into a Folder called `fonts/`.

## 2.
Put `red-hat-display.css` into your `css/` Folder.

## 3. (Optional)
You may adapt the `url('path')` in `red-hat-display.css` depends on your Website Filesystem.

## 4.
Import `red-hat-display.css` at the top of you main Stylesheet.

```
@import url('red-hat-display.css');
```

## 5.
You are now ready to use the following Rules in your CSS to specify each Font Style:
```
font-family: RedHatDisplay-Light;
font-family: RedHatDisplay-LightItalic;
font-family: RedHatDisplay-Regular;
font-family: RedHatDisplay-Italic;
font-family: RedHatDisplay-Medium;
font-family: RedHatDisplay-MediumItalic;
font-family: RedHatDisplay-SemiBold;
font-family: RedHatDisplay-SemiBoldItalic;
font-family: RedHatDisplay-Bold;
font-family: RedHatDisplay-BoldItalic;
font-family: RedHatDisplay-ExtraBold;
font-family: RedHatDisplay-ExtraBoldItalic;
font-family: RedHatDisplay-Black;
font-family: RedHatDisplay-BlackItalic;
font-family: RedHatDisplay-Variable;
font-family: RedHatDisplay-VariableItalic;

```
## 6. (Optional)
Use `font-variation-settings` rule to controll axes of variable fonts:
wght 400.0

Available axes:
'wght' (range from 300.0 to 900.0


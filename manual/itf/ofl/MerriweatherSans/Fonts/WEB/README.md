# Installing Webfonts
Follow these simple Steps.

## 1.
Put `merriweather-sans/` Folder into a Folder called `fonts/`.

## 2.
Put `merriweather-sans.css` into your `css/` Folder.

## 3. (Optional)
You may adapt the `url('path')` in `merriweather-sans.css` depends on your Website Filesystem.

## 4.
Import `merriweather-sans.css` at the top of you main Stylesheet.

```
@import url('merriweather-sans.css');
```

## 5.
You are now ready to use the following Rules in your CSS to specify each Font Style:
```
font-family: MerriweatherSans-Light;
font-family: MerriweatherSans-LightItalic;
font-family: MerriweatherSans-Regular;
font-family: MerriweatherSans-Italic;
font-family: MerriweatherSans-Medium;
font-family: MerriweatherSans-MediumItalic;
font-family: MerriweatherSans-SemiBold;
font-family: MerriweatherSans-SemiBoldItalic;
font-family: MerriweatherSans-Bold;
font-family: MerriweatherSans-BoldItalic;
font-family: MerriweatherSans-ExtraBold;
font-family: MerriweatherSans-ExtraBoldItalic;
font-family: MerriweatherSans-Variable;
font-family: MerriweatherSans-VariableItalic;

```
## 6. (Optional)
Use `font-variation-settings` rule to controll axes of variable fonts:
wght 300.0

Available axes:
'wght' (range from 300.0 to 800.0


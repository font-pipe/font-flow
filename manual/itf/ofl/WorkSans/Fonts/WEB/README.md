# Installing Webfonts
Follow these simple Steps.

## 1.
Put `work-sans/` Folder into a Folder called `fonts/`.

## 2.
Put `work-sans.css` into your `css/` Folder.

## 3. (Optional)
You may adapt the `url('path')` in `work-sans.css` depends on your Website Filesystem.

## 4.
Import `work-sans.css` at the top of you main Stylesheet.

```
@import url('work-sans.css');
```

## 5.
You are now ready to use the following Rules in your CSS to specify each Font Style:
```
font-family: WorkSans-Thin;
font-family: WorkSans-ThinItalic;
font-family: WorkSans-ExtraLight;
font-family: WorkSans-ExtraLightItalic;
font-family: WorkSans-Light;
font-family: WorkSans-LightItalic;
font-family: WorkSans-Regular;
font-family: WorkSans-Italic;
font-family: WorkSans-Medium;
font-family: WorkSans-MediumItalic;
font-family: WorkSans-SemiBold;
font-family: WorkSans-SemiBoldItalic;
font-family: WorkSans-Bold;
font-family: WorkSans-BoldItalic;
font-family: WorkSans-ExtraBold;
font-family: WorkSans-ExtraBoldItalic;
font-family: WorkSans-Black;
font-family: WorkSans-BlackItalic;
font-family: WorkSans-Variable;
font-family: WorkSans-VariableItalic;

```
## 6. (Optional)
Use `font-variation-settings` rule to controll axes of variable fonts:
wght 400.0

Available axes:
'wght' (range from 100.0 to 900.0


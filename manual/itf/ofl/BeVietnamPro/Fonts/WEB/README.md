# Installing Webfonts
Follow these simple Steps.

## 1.
Put `beVietnam-pro/` Folder into a Folder called `fonts/`.

## 2.
Put `beVietnam-pro.css` into your `css/` Folder.

## 3. (Optional)
You may adapt the `url('path')` in `beVietnam-pro.css` depends on your Website Filesystem.

## 4.
Import `beVietnam-pro.css` at the top of you main Stylesheet.

```
@import url('beVietnam-pro.css');
```

## 5.
You are now ready to use the following Rules in your CSS to specify each Font Style:
```
font-family: BeVietnamPro-Thin;
font-family: BeVietnamPro-ThinItalic;
font-family: BeVietnamPro-ExtraLight;
font-family: BeVietnamPro-ExtraLightItalic;
font-family: BeVietnamPro-Light;
font-family: BeVietnamPro-LightItalic;
font-family: BeVietnamPro-Regular;
font-family: BeVietnamPro-Italic;
font-family: BeVietnamPro-Medium;
font-family: BeVietnamPro-MediumItalic;
font-family: BeVietnamPro-SemiBold;
font-family: BeVietnamPro-SemiBoldItalic;
font-family: BeVietnamPro-Bold;
font-family: BeVietnamPro-BoldItalic;
font-family: BeVietnamPro-ExtraBold;
font-family: BeVietnamPro-ExtraBoldItalic;
font-family: BeVietnamPro-Black;
font-family: BeVietnamPro-BlackItalic;
font-family: BeVietnamPro-Variable;
font-family: BeVietnamPro-VariableItalic;

```
## 6. (Optional)
Use `font-variation-settings` rule to controll axes of variable fonts:
wght 100.0

Available axes:
'wght' (range from 100.0 to 900.0


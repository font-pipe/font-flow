# Installing Webfonts
Follow these simple Steps.

## 1.
Put `public-sans/` Folder into a Folder called `fonts/`.

## 2.
Put `public-sans.css` into your `css/` Folder.

## 3. (Optional)
You may adapt the `url('path')` in `public-sans.css` depends on your Website Filesystem.

## 4.
Import `public-sans.css` at the top of you main Stylesheet.

```
@import url('public-sans.css');
```

## 5.
You are now ready to use the following Rules in your CSS to specify each Font Style:
```
font-family: PublicSans-Thin;
font-family: PublicSans-ThinItalic;
font-family: PublicSans-ExtraLight;
font-family: PublicSans-ExtraLightItalic;
font-family: PublicSans-Light;
font-family: PublicSans-LightItalic;
font-family: PublicSans-Regular;
font-family: PublicSans-Italic;
font-family: PublicSans-Medium;
font-family: PublicSans-MediumItalic;
font-family: PublicSans-SemiBold;
font-family: PublicSans-SemiBoldItalic;
font-family: PublicSans-Bold;
font-family: PublicSans-BoldItalic;
font-family: PublicSans-ExtraBold;
font-family: PublicSans-ExtraBoldItalic;
font-family: PublicSans-Black;
font-family: PublicSans-BlackItalic;
font-family: PublicSans-Variable;
font-family: PublicSans-VariableItalic;

```
## 6. (Optional)
Use `font-variation-settings` rule to controll axes of variable fonts:
wght 100.0

Available axes:
'wght' (range from 100.0 to 900.0


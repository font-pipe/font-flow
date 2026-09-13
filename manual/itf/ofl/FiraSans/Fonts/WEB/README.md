# Installing Webfonts
Follow these simple Steps.

## 1.
Put `fira-sans/` Folder into a Folder called `fonts/`.

## 2.
Put `fira-sans.css` into your `css/` Folder.

## 3. (Optional)
You may adapt the `url('path')` in `fira-sans.css` depends on your Website Filesystem.

## 4.
Import `fira-sans.css` at the top of you main Stylesheet.

```
@import url('fira-sans.css');
```

## 5.
You are now ready to use the following Rules in your CSS to specify each Font Style:
```
font-family: FiraSans-Thin;
font-family: FiraSans-ThinItalic;
font-family: FiraSans-ExtraLight;
font-family: FiraSans-ExtraLightItalic;
font-family: FiraSans-Light;
font-family: FiraSans-LightItalic;
font-family: FiraSans-Regular;
font-family: FiraSans-Italic;
font-family: FiraSans-Medium;
font-family: FiraSans-MediumItalic;
font-family: FiraSans-SemiBold;
font-family: FiraSans-SemiBoldItalic;
font-family: FiraSans-Bold;
font-family: FiraSans-BoldItalic;
font-family: FiraSans-ExtraBold;
font-family: FiraSans-ExtraBoldItalic;
font-family: FiraSans-Black;
font-family: FiraSans-BlackItalic;
font-family: FiraSans-Variable;
font-family: FiraSans-VariableItalic;

```
## 6. (Optional)
Use `font-variation-settings` rule to controll axes of variable fonts:
wght 400.0wght 1.0

Available axes:
'wght' (range from 1.0 to 950.0'wght' (range from 1.0 to 925.0


# Installing Webfonts
Follow these simple Steps.

## 1.
Put `familjen-grotesk/` Folder into a Folder called `fonts/`.

## 2.
Put `familjen-grotesk.css` into your `css/` Folder.

## 3. (Optional)
You may adapt the `url('path')` in `familjen-grotesk.css` depends on your Website Filesystem.

## 4.
Import `familjen-grotesk.css` at the top of you main Stylesheet.

```
@import url('familjen-grotesk.css');
```

## 5.
You are now ready to use the following Rules in your CSS to specify each Font Style:
```
font-family: FamiljenGrotesk-Regular;
font-family: FamiljenGrotesk-Italic;
font-family: FamiljenGrotesk-Medium;
font-family: FamiljenGrotesk-MediumItalic;
font-family: FamiljenGrotesk-SemiBold;
font-family: FamiljenGrotesk-SemiBoldItalic;
font-family: FamiljenGrotesk-Bold;
font-family: FamiljenGrotesk-BoldItalic;
font-family: FamiljenGrotesk-Variable;
font-family: FamiljenGrotesk-VariableItalic;

```
## 6. (Optional)
Use `font-variation-settings` rule to controll axes of variable fonts:
wght 400.0

Available axes:
'wght' (range from 400.0 to 700.0


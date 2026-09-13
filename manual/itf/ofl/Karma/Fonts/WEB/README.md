# Installing Webfonts
Follow these simple Steps.

## 1.
Put `karma/` Folder into a Folder called `fonts/`.

## 2.
Put `karma.css` into your `css/` Folder.

## 3. (Optional)
You may adapt the `url('path')` in `karma.css` depends on your Website Filesystem.

## 4.
Import `karma.css` at the top of you main Stylesheet.

```
@import url('karma.css');
```

## 5.
You are now ready to use the following Rules in your CSS to specify each Font Style:
```
font-family: Karma-Light;
font-family: Karma-Regular;
font-family: Karma-Medium;
font-family: Karma-SemiBold;
font-family: Karma-Bold;
font-family: Karma-Variable;

```
## 6. (Optional)
Use `font-variation-settings` rule to controll axes of variable fonts:
wght 300.0

Available axes:
'wght' (range from 300.0 to 700.0


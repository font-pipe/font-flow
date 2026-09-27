# Installing Webfonts
Follow these simple Steps.

## 1.
Put `pilcrow-rounded/` Folder into a Folder called `fonts/`.

## 2.
Put `pilcrow-rounded.css` into your `css/` Folder.

## 3. (Optional)
You may adapt the `url('path')` in `pilcrow-rounded.css` depends on your Website Filesystem.

## 4.
Import `pilcrow-rounded.css` at the top of you main Stylesheet.

```
@import url('pilcrow-rounded.css');
```

## 5.
You are now ready to use the following Rules in your CSS to specify each Font Style:
```
font-family: PilcrowRounded-Regular;
font-family: PilcrowRounded-Medium;
font-family: PilcrowRounded-Semibold;
font-family: PilcrowRounded-Bold;
font-family: PilcrowRounded-Heavy;
font-family: PilcrowRounded-Variable;

```
## 6. (Optional)
Use `font-variation-settings` rule to controll axes of variable fonts:
wght 400.0

Available axes:
'wght' (range from 400.0 to 900.0


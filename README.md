# xml2svg

## Introduction
The xml2svg.py Python script converts Android VectorDrawable `.xml`
files to `.svg` files.

This repository was forked from
https://gitlab.com/Hyperion777/VectorDrawable2Svg to add handling of indirect
colour references (e.g. in color.xml files) since that repository did not seem
to be actively maintained (based on the unaddressed issues and merge/pull
requests there at the time).


## Usage
```shell
python3 xml2svg.py a.xml b.xml ...
```

```shell
./xml2svg.py --color-xml-file=path/to/color.xml a.xml b.xml ...
```

```shell
/path/to/xml2svg.py --viewbox-only a.xml b.xml ...
```

The output .svg files are written in the same directory as the .xml files
(currently by simply replacing .xml with .svg in the filename).


## Improvements
This Python script only supports some Android VectorDrawable attributes.

Suggestions (or merge requests) for improvement are welcome.


## See also

- [vd2svg](https://github.com/neworld/vd2svg) - written in Kotlin

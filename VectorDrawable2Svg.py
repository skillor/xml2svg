#!/usr/bin/env python3
"""
VectorDrawable2Svg
This script converts VectorDrawable .xml files to SVG files.
Initial author: Alessandro Lucchet
Modified by: Rohan Talip
"""

import argparse
from xml.dom.minidom import Document, parse
import traceback

color_map = {}


def read_color_xml(file_path):
    color_xml = parse(file_path)
    resource_node = color_xml.getElementsByTagName('resources')[0]
    for color_node in resource_node.getElementsByTagName('color'):
        name = color_node.attributes['name'].value
        value = color_node.firstChild.nodeValue
        if name in color_map:
            raise 'Color ' + name + ' already exists: ' + color_map[name]
        color_map[name] = value


def get_color(value, depth=1):
    prefix = '@color/'

    if value.startswith('#'):
        return value

    if depth >= 3:
        raise 'Depth is >= 3'

    if prefix not in value:
        raise '@color not found in ' + value

    name = value.split(prefix)[1]
    color = color_map.get(name)
    if not color:
        return value

    if prefix in color:
        return get_color(color, depth + 1)
    return color


# extracts all paths inside vd_container and add them into svg_container
def convert_paths(vd_container, svg_container, svg_xml):
    vd_paths = vd_container.getElementsByTagName('path')
    for vd_path in vd_paths:
        # only iterate in the first level
        if vd_path.parentNode == vd_container:
            svg_path = svg_xml.createElement('path')
            svg_path.attributes['d'] = vd_path.attributes[
                'android:pathData'].value

            if vd_path.hasAttribute('android:fillColor'):
                svg_path.attributes['fill'] = get_color(
                    vd_path.attributes['android:fillColor'].value)
            else:
                svg_path.attributes['fill'] = 'none'

            if vd_path.hasAttribute('android:strokeLineJoin'):
                svg_path.attributes['stroke-linejoin'] = vd_path.attributes[
                    'android:strokeLineJoin'].value
            if vd_path.hasAttribute('android:strokeLineCap'):
                svg_path.attributes['stroke-linecap'] = vd_path.attributes[
                    'android:strokeLineCap'].value
            if vd_path.hasAttribute('android:strokeMiterLimit'):
                svg_path.attributes['stroke-miterlimit'] = vd_path.attributes[
                    'android:strokeMiterLimit'].value
            if vd_path.hasAttribute('android:strokeWidth'):
                svg_path.attributes['stroke-width'] = vd_path.attributes[
                    'android:strokeWidth'].value
            if vd_path.hasAttribute('android:strokeColor'):
                svg_path.attributes['stroke'] = get_color(
                    vd_path.attributes['android:strokeColor'].value)

            svg_container.appendChild(svg_path)


# define the function which converts a vector drawable to a svg
def convert_vector_drawable(vd_file_path, viewbox_only):

    # create svg xml
    svg_xml = Document()
    svg_node = svg_xml.createElement('svg')
    svg_xml.appendChild(svg_node)

    # open vector drawable
    vd_xml = parse(vd_file_path)
    vd_node = vd_xml.getElementsByTagName('vector')[0]

    # setup basic svg info
    svg_node.attributes['xmlns'] = 'http://www.w3.org/2000/svg'
    if not viewbox_only:
        svg_node.attributes['width'] = vd_node.attributes[
            'android:viewportWidth'].value
        svg_node.attributes['height'] = vd_node.attributes[
            'android:viewportHeight'].value

    svg_node.attributes['viewBox'] = '0 0 {} {}'.format(
        vd_node.attributes['android:viewportWidth'].value,
        vd_node.attributes['android:viewportHeight'].value)

    # iterate through all groups
    vd_groups = vd_xml.getElementsByTagName('group')
    for vd_group in vd_groups:

        # create the group
        svg_group = svg_xml.createElement('g')

        # setup attributes of the group
        if vd_group.hasAttribute('android:translateX'):
            svg_group.attributes['transform'] = 'translate({},{})'.format(
                vd_group.attributes['android:translateX'].value,
                vd_group.attributes['android:translateY'].value)

        # iterate through all paths inside the group
        convert_paths(vd_group, svg_group, svg_xml)

        # append the group to the svg node
        svg_node.appendChild(svg_group)

    # iterate through all svg-level paths
    convert_paths(vd_node, svg_node, svg_xml)

    # write xml to file
    svg_file_path = vd_file_path.replace('.xml', '.svg')
    svg_xml.writexml(
        open(svg_file_path, 'w'), indent="", addindent="  ", newl='\n')


def main():
    parser = argparse.ArgumentParser(
        description="Convert VectorDrawable .xml files to .svg files.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="e.g. %(prog)s *.xml")

    parser.add_argument(
        "--color-xml-file", action="append", help="A color.xml file")
    parser.add_argument(
        "--viewbox-only",
        "--viewBox-only",
        help="Only add the viewBox attribute and not width or height",
        action="store_true")
    parser.add_argument("xml_files", nargs="+", metavar='xml-file')
    args = parser.parse_args()

    if args.color_xml_file:
        for color_xml_file in args.color_xml_file:
            read_color_xml(color_xml_file)

    for xml_file in args.xml_files:
        print("Converting", xml_file)
        try:
            convert_vector_drawable(xml_file, args.viewbox_only)
        except Exception:
            print("Failed to convert", xml_file)
            traceback.print_exc()


if __name__ == "__main__":
    main()

#!/bin/python3

import requests
import re
import argparse
from more_itertools import split_after


def download_gabc(chant_id):
    url = f"https://gregobase.selapa.net/download.php?id={chant_id}&format=gabc"
    response = requests.get(url)
    response.raise_for_status()
    if response.status_code != 200:
        raise Exception(f"HTTP request for GABC file returned unexpected status: {response.status_code}")
    return response.text.splitlines()

def split_header_and_content(gabc_lines):
    [header, content] = list(split_after(gabc_lines, lambda x: x == "%%"))
    return header, content


def make_header(old_header, chant_id, tone):
    return ( [f"% https://gregobase.selapa.net/chant.php?id={chant_id}"]
                + old_header[:-1]
                + [f"annotation:{tone};", "%%"] )

unicode_escapes = {
    "ae": "\u00e6",
    "Ae": "\u00c6",
    "AE": "\u00c6",
    "\u0153": "<sp>oe</sp>",
    "\u01fd": "<sp>'ae</sp>",
    "áe": "<sp>'ae</sp>",
    "\u2020": "+"
}

def escape_unicode_chars(content):
    return list([escape_unicode_chars_str(s) for s in content])

def escape_unicode_chars_str(s):
    if "oe" in s:
        print("Text contains sequence OE, can't tell if it should be joined")
    for (k, v) in unicode_escapes.items():
        s = s.replace(k, v)
    return s

def remove_episemas(content):
    return list([remove_episemas_str(s) for s in content])

def remove_episemas_str(s):
    return s.replace("'", "").replace("_", "")

INTONATION_REGEX_STR = r"\([cf]b?\d\).{2,}\*"
INTONATION_REGEX = re.compile(INTONATION_REGEX_STR)

def make_intonation_gabc(content):
    match = re.match(INTONATION_REGEX, content[0])
    if not match:
        raise Exception(f"Can't find intonation of antiphon: {content[0]}")
    return [match.group() + "*(::)", "%%TODO psalm verse"]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("chant_id")
    parser.add_argument("tone")
    parser.add_argument("output_name")
    parser.add_argument("-s", "--semidouble", action="store_true")
    parser.add_argument("-g", "--g-and-a", action="store_true")
    args = parser.parse_args()

    gabc_lines = download_gabc(args.chant_id)
    header, content = split_header_and_content(gabc_lines)
    new_header = make_header(header, args.chant_id, args.tone)
    # do this before unicode escapes
    # because it removes ' which is used in escapes
    new_content = content
    if args.g_and_a:
        new_content = remove_episemas(new_content)
    new_content = escape_unicode_chars(new_content)

    with open(f"{args.output_name}-antiphon.gabc", "w") as antiphon_out:
        antiphon_out.write("\n".join(new_header))
        antiphon_out.write("\n")
        antiphon_out.write("\n".join(new_content))

    if not args.semidouble:
        return

    intonation_content = make_intonation_gabc(new_content)
    with open(f"{args.output_name}-intonation.gabc", "w") as intonation_out:
        intonation_out.write("\n".join(new_header))
        intonation_out.write("\n")
        intonation_out.write("\n".join(intonation_content))

if __name__ == "__main__":
    main()

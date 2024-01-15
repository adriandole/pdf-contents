import argparse
import os
from dataclasses import dataclass
from typing import List

@dataclass
class Bookmark:
    title: str
    level: int
    page: int

class Metadata:
    def __init__(self, lines) -> None:
        self._lines = lines
        self._start = -1
        self._end = -1

    def to_file(self, fname):
        with open(fname, 'w') as f:
            f.writelines(self._lines)

    def locate_bookmarks(self):
        page_num_i = -1
        for i, l in enumerate(self._lines):
            if self._start == -1 and l.startswith('BookmarkBegin'):
                self._start = i
            if l.startswith('BookmarkPageNumber'):
                self._end = i
            if page_num_i == -1 and l.startswith('NumberOfPages'):
                page_num_i = i
        if self._start == -1:
            self._start = page_num_i + 1
            self._end = -1
        
    def erase_bookmarks(self):
        if self._start == -1:
            self.locate_bookmarks()
        if self._end != -1:
            del self._lines[self._start:self._end+1]

    def insert_bookmarks(self, bookmarks: List[Bookmark]):
        bookmarks.sort(key=lambda b: b.page, reverse=True)
        for b in bookmarks:
            self._lines.insert(self._start, f'BookmarkPageNumber: {b.page}\n')
            self._lines.insert(self._start, f'BookmarkLevel: {b.level}\n')
            self._lines.insert(self._start, f'BookmarkTitle: {b.title}\n')
            self._lines.insert(self._start, f'BookmarkBegin\n')

def parse_bookmarks(path, offset) -> List[Bookmark]:
    with open(path, 'r') as f:
        lines = f.readlines()

    bookmarks = []
    for ln in lines:
        l = ln.rstrip()
        b = Bookmark('', 0, 0)
        b.level = (len(l) - len(l.lstrip())) // 4 + 1
        ls = l.rsplit(maxsplit=1)
        b.page = int(ls[1]) + offset
        b.title = ls[0].strip()
        bookmarks.append(b)
    return bookmarks

def dump_data(book):
    dump_file = 'meta.txt'
    os.system(f'pdftk {book} dump_data output {dump_file}')
    with open(dump_file, 'r') as f:
        lines = f.readlines()
    m = Metadata(lines)
    os.remove(dump_file)
    return m

def update_data(book, m: Metadata, final):
    temp_meta_file = 'temp.txt'
    m.to_file(temp_meta_file)
    os.system(f'pdftk {book} update_info {temp_meta_file} output {final}')
    os.remove(temp_meta_file)

def write_new_contents(book, new_contents, offset, final_book='final.pdf'):
    m = dump_data(book)
    m.erase_bookmarks()
    bookmarks = parse_bookmarks(new_contents, offset)
    m.insert_bookmarks(bookmarks)
    update_data(book, m, final_book)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Adds table of contents to a PDF')
    parser.add_argument('book', type=str, help='PDF file to add contents to')
    parser.add_argument('contents', type=str, help='table of contents, see README for format')
    parser.add_argument('--offset', type=int, default=0, help='PDF page of numbered page 1')
    args = parser.parse_args()

    write_new_contents(args.book, args.contents, args.offset)
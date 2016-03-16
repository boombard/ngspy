import json
import re
from os import path
import os
import shutil
import click

class Renamer(object):

    def __init__(self, folder=None, interactive=False):
        self.set_folder(folder)
        self.file_descriptors = ['run', 'lane', 'direction']
        self.used_descriptors = []
        self.pattern = ''
        self.valid_files = []
        self.anomalies = []
        self.file_collection = {}

        default = 'run#lane_direction.fastq'
        if not interactive:
            # Set default template
            self.set_pattern(pattern=default, forward='1', reverse='2')
        self.set_template(template=default, forward='1', reverse='2')

    def set_folder(self, folder):
        assert path.isdir(folder), 'Please specify a valid folder'
        self.folder = folder

    def set_template(self, template, forward, reverse):
        self.template = template
        self.template_direction = {
            'forward': forward,
            'reverse': reverse
        }

    def set_pattern(self, pattern, forward, reverse):
        # TODO: add wildcard characters
        self.direction = {reverse: 'reverse', forward: 'forward'}

        # Set up the regex
        self.file_extension = path.splitext(pattern)[1]
        self.pattern = pattern[:]
        self.pattern = self.pattern.replace('.', '\.')

        for descriptor in self.file_descriptors:
            if descriptor in pattern:
                descriptor_pattern = descriptor.replace('{', '\{') \
                    .replace('}', '\}')
                self.pattern = self.pattern.replace(
                    descriptor, '(?P<%s>.+)' % descriptor_pattern)
                self.used_descriptors.append(descriptor)
        print('pattern: %s' % self.pattern)
        self.regex = re.compile(self.pattern)

    def get_file_meta(self, filename):
        m = self.regex.match(filename)
        if not m:
            print('%s cannot be parsed' % filename)
            self.anomalies.append(filename)
            return

        file_metadata = {'filename': filename}

        for descriptor in self.used_descriptors:
            match = m.group(descriptor)
            if not match:
                self.anomalies.append(filename)
                print('%s does not contain %s' % (filename, descriptor))
                return
            if descriptor == 'direction':
                if not self.direction.get(match):
                    self.anomalies.append(filename)
                    print('%s does not have a valid direction' % filename)
                    return
                file_metadata['direction'] = self.direction[match]
            else:
                file_metadata[descriptor] = match
        return file_metadata

    def get_new_name(self, filename):
        metadata = self.file_collection.get(filename)
        if not metadata:
            metadata = self.get_file_meta(filename)
        if not metadata:
            print('Could not find file metadata')
            return
        format_template = self.template[:]
        for descriptor in self.file_descriptors:
            format_template = format_template.replace(
                descriptor, '{' + descriptor + '}')

        new_filename = format_template.format(**metadata)
        new_filename = new_filename \
            .replace('forward', self.template_direction['forward']) \
            .replace('reverse', self.template_direction['reverse'])

        return new_filename

    def get_all_metadata(self):
        self.valid_files = []
        for filename in os.listdir(self.folder):
            metadata = self.get_file_meta(filename)
            if metadata:
                self.valid_files.append(filename)
                self.file_collection[filename] = metadata
                new_name = self.get_new_name(filename)
                self.file_collection[filename]['new_name'] = new_name
        with open('.file_metadata.json', 'w+') as outfile:
            json.dump(self.file_collection, outfile)
        print('Dumping metadata - ".file_metadata.json"')

        return self.file_collection

    def _rename_folder(self, mapping, folder, out=None):
        success_count = 0
        for filename in mapping.keys():
            new_name = mapping[filename]
            src = path.join(folder, filename)
            if out is not None:
                if not path.isdir(out):
                    os.makedirs(out)
                dest = path.join(out, new_name)
                shutil.copy(src, dest)
                success_count += 1
            else:
                dest = path.join(folder, new_name)
                shutil.move(src, dest)
                success_count += 1
        print('Successfully renamed %d files' % success_count)

    def rename_all(self, out=None):
        self.get_all_metadata()
        mapping = {old: self.file_collection[old]['new_name']
                   for old in self.file_collection.keys()}
        self._rename_folder(mapping, self.folder, out)

    def reverse_rename(self, metadata_json='.file_metadata.json',
                       target=None, out=None):
        assert path.isfile(metadata_json), 'Cannot find metadata json'
        with open(metadata_json) as mj:
            metadata = json.load(mj)
        if target is None:
            target = self.folder
        mapping = {metadata[old]['new_name']: old for old in metadata.keys()}
        self._rename_folder(mapping, target, out)

    def run(self):
        self.set_pattern()
        self.set_template()
        self.rename_all()


@click.command()
@click.argument('directory')
@click.option(
    '--pattern',
    prompt='What is the pattern of your files? e.g. run#lane.direction.fastq')
@click.option(
    '--pattern_forward',
    prompt='What represents forward in your files? e.g. "f" and "r"')
@click.option(
    '--pattern_reverse',
    prompt='What represents reverse in your files? e.g. "f" and "r"')
@click.option('--out',
              prompt='Destination folder? (Leave blank to move files in place)')
def run_renamer(directory, pattern, pattern_forward, pattern_reverse, out):
    ren = Renamer(directory, interactive=True)
    ren.set_pattern(pattern, pattern_forward, pattern_reverse)
    ren.get_all_metadata()
    if out == '':
        ren.rename_all(out=None)
    else:
        ren.rename_all(out)


if __name__ == '__main__':
    # ren = Renamer('../tests/rename_data')
    # ren.set_pattern(pattern='run.direction.lane.fq', forward='f', reverse='r')
    # ren.get_file_meta('test#f.1.fastq')
    # new_name = ren.get_new_name('test#f.1.fastq')
    # ren.rename_all(out='../tests/new_data')
    # ren.reverse_rename(target='../tests/new_data')
    # ren = Renamer(interactive=True)
    # ren.run()
    run_renamer()


from lxml.etree import ElementTree, tostring, Element, SubElement
import os
import sys
import time
import requests


class EnsemblQuery(object):

    def __init__(self, embl_organism):
        self.query = Element(
            'Query', virtualSchemaName='default', formatter='FASTA', header='0',
            uniqueRows='0', count='')
        self.doc = ElementTree(self.query)
        self.dataset = SubElement(
            self.query, 'Dataset', name=embl_organism, interace='default')
        # Default attributes
        self.add_attributes(['gene_exon_intron'])

    def add_attributes(self, attributes):
        if not isinstance(attributes, list):
            attributes = [attributes]
        for attribute in attributes:
            query_attribute = SubElement(self.dataset, 'Attribute',
                                         name=attribute)

    def add_filters(self, **filters):
        for key, value in filters.items():
            query_filter = SubElement(self.dataset, 'Filter',
                                      name=key, value=value)

    def getstring(self):
        string = tostring(
            self.doc, xml_declaration=True, doctype='<!DOCTYPE Query>',
            encoding='UTF-8').decode('utf-8')
        string = string.replace('\n', '')
        return string

    def download(self, file_path):
        r = requests.get('http://www.ensembl.org/biomart/martservice?query=' +
                         self.getstring(), stream=True)
        total = 0
        start = time.clock()
        with open(file_path, 'wb') as fp:
            try:
                for chunk in r.iter_content(chunk_size=1024):
                    fp.write(chunk)
                    fp.flush()
                    total += len(chunk)
                    total_time = time.clock() - start
                    avg_speed = total / 1000 / total_time
                    print('\r%.2f MB downloaded: Average speed %.2fkB/s' %
                          (total / 1e6, avg_speed), end='')
                    sys.stdout.flush()

                print('\nDownload finished in %ds' % (time.clock() - start))
            except KeyboardInterrupt:
                os.unlink(file_path)
                print('\nDownload cancelled.')


if __name__ == '__main__':
    query = EnsemblQuery('mmusculus_gene_ensembl')
    query.add_filters(chromosome_name='1')
    query.download('/Users/ge2/software/ngspy/store/test.txt')


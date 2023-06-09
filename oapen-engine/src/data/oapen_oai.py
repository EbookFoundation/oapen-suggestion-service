import datetime
import logging
from oaipmh.client import Client
from oaipmh.error import IdDoesNotExistError, NoRecordsMatchError
from oaipmh.metadata import MetadataReader, MetadataRegistry

OAPEN_OAIURL = 'https://library.oapen.org/oai/request'

logger = logging.getLogger(__name__)

oapen_reader = MetadataReader(
    fields={
        'title': ('textList', 'oai_dc:dc/datacite:title/text()'),
        'creator': ('textList', 'oai_dc:dc/datacite:creator/text()'),
        'subject': ('textList', 'oai_dc:dc/datacite:subject/text()'),
        'description': ('textList', 'oai_dc:dc/dc:description/text()'),
        'publisher': ('textList', 'oai_dc:dc/dc:publisher/text()'),
        'editor': ('textList', 'oai_dc:dc/datacite:contributor[@type="Editor"]/text()'),
        'date': ('textList', 'oai_dc:dc/datacite:date[@type="Issued"]/text()'),
        'timestamp': ('textList', 'oai_dc:dc/dc:date/text()'),
        'type': ('textList', 'oai_dc:dc/oaire:resourceType/text()'),
        'format': ('textList', 'oai_dc:dc/dc:format/text()'),
        'identifier': ('textList', 'oai_dc:dc/dc:identifier/text()'),
        'source': ('textList', 'oai_dc:dc/dc:source/text()'),
        'language': ('textList', 'oai_dc:dc/dc:language/text()'),
        'relation': ('textList', 'oai_dc:dc/dc:relation/text()'),
        'coverage': ('textList', 'oai_dc:dc/dc:coverage/text()'),
        'rights': ('textList', 'oai_dc:dc/oaire:licenseCondition/@uri'),
        'isbn': ('textList', 'oai_dc:dc/datacite:alternateIdentifier[@type="ISBN"]/text()'),
        'doi': ('textList', 'oai_dc:dc/datacite:alternateIdentifier[@type="DOI"]/text()'),
    },
    namespaces={
        'oai_dc': 'http://www.openarchives.org/OAI/2.0/oai_dc/',
        'dc' : 'http://purl.org/dc/elements/1.1/',
        'grantor': 'http://purl.org/dc/elements/1.1/',
        'publisher': 'http://purl.org/dc/elements/1.1/',
        'oapen': 'http://purl.org/dc/elements/1.1/',
        'oaire': 'https://raw.githubusercontent.com/rcic/openaire4/master/schemas/4.0/oaire.xsd',
        'datacite': 'https://schema.datacite.org/meta/kernel-4.1/metadata.xsd',
        'doc': 'http://www.lyncode.com/xoai'
    }
)

mdregistry = MetadataRegistry()
mdregistry.registerReader('oai_dc', oapen_reader)
oapen_client = Client(OAPEN_OAIURL, mdregistry)



def unlist(alist):
    if not alist:
        return None
    return alist[0]

def get_oapen_handles(from_date=None, until_date=None):
    if from_date == 'week':
        from_ = datetime.datetime.now() - datetime.timedelta(days=7)
    elif from_date:
        from_ = from_date
    else:
        from_ = datetime.datetime(2000, 1, 1)

    try:
        for record in oapen_client.listRecords(metadataPrefix='oai_dc', from_=from_,
                                              until=until_date):
            if not record[1]:
                # probably a deleted record
                continue
            item_type = unlist(record[1].getMap().get('type', None))
            ident = record[0].identifier()
            if ident.startswith('oai:library.oapen.org:'):
                handle = ident[22:]
                yield handle, item_type
    except NoRecordsMatchError:
        pass

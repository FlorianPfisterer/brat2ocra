from bratreader.repomodel import RepoModel
from brat2ocra.doc_converter import DocConverter
import argparse
import os
import json

def convert(brat_dir_path: str, output_dir_path: str):
    # load the brat repository
    repo = RepoModel(brat_dir_path)
    print('Loaded {} document(s) from {}'.format(len(repo.documents), brat_dir_path))

    for document_name in repo.documents:
        document = repo.documents[document_name]

        converter = DocConverter(document)
        sentences = converter.sentences

        with open(os.path.join(output_dir_path, '{}.json'.format(document_name)), 'x') as output_file:
            json.dump(list(map(lambda s: s.to_dict(), sentences)), output_file, indent=2)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--brat_dir_path', dest='brat_dir_path', required=True,
                        help='The path to the directory holding the brat files.')
    parser.add_argument('-o', '--output', dest='output_dir_path', required=True,
                        help='The path to the directory that will hold the resulting JSON files.')
    args = parser.parse_args()
    convert(args.brat_dir_path, args.output_dir_path)



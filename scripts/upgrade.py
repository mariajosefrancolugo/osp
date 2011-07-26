#!/usr/bin/env python

import logging
import optparse
import os
import re
import subprocess

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(message)s')

def call_command(command):
    process = subprocess.Popen(command.split(' '),
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
    return process.communicate()

if __name__ == '__main__':
    parser = optparse.OptionParser()
    parser.add_option('-f', '--from', dest='from_tag', action='store',
                      help='The current version of your OSP instance')
    parser.add_option('-t', '--to', dest='to_tag', action='store',
                      help='The version of OSP that you are upgrading to')
    parser.add_option('-p', '--path', dest='path', action='store',
                      help=('The path to your OSP instance'))
    options, args = parser.parse_args()

    # Check for existence of OSP directory and pull + update changes
    # instead of cloning, if possible

    logging.info('Cloning OSP repository')
    output, _ = call_command('hg clone http://osp.googlecode.com/hg/ osp')
    os.chdir('osp')

    if options.to_tag:
        to_version = options.to_tag
    else:
        logging.info('Determining the latest version of OSP')

        tags = open('.hgtags', 'r')
        lines = tags.readlines()
        tags.close()

        to_version = lines[-1].split(' ')[1]
        logging.info('Latest version: %s' % to_version)

    logging.info('Updating repository to the correct version of OSP')
    output, _ = call_command('hg update %s' % to_version)

    if options.from_tag:
        from_version = options.from_tag
    else:
        logging.info('Determining the current version of your OSP instance')

        if options.path:
            path = options.path
        else:
            logging.info('Determining the path to your OSP instance')
            try:
                import osp
            except ImportError:
                path = '/opt/django/osp'
                # Make sure this path exists
            else:
                path = os.path.dirname(os.path.realpath(osp.__file__))[:-4]

        setup = open('%s/setup.py' % path)
        # Make sure this file exists
        setup.close()

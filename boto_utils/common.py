import argparse
import os
import re

LINE_RE = re.compile(r'^\s*(.*?)=(.*?)\s*$')

def parse_aws_credentials_file(fp):
    """Return a dictionary containing aws_access_key_id and aws_secret_access_key, given a file to a credentials file
       in the format expected by AWS tools (as described at http://j.mp/qGGHNp).
      
      see http://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-started.html#cli-config-files
       
       This is a port of the Perl code in SES.pm, so should behave identically.
       
      Note: Only handles one AWS profile (ie 'default' credentials) other credential configs will fail 

       """
    
    result = {}

    for line in fp:

        line = line.strip()
        match = LINE_RE.match(line)
        print line

        if not line:
            continue
        if '[default]' in line:
            continue
        elif not match:
            raise ValueError, 'Cannot parse credentials file entry <%s>' % line
        elif match.group(1) == 'AWSAccessKeyId' or match.group(1) == 'aws_access_key_id':
            result['aws_access_key_id'] = match.group(2)
        elif match.group(1) == 'AWSSecretKey' or match.group(1) == 'aws_secret_access_key':
            result['aws_secret_access_key'] = match.group(2)
        else:
            raise ValueError, 'Unrecognized credential <%s>' % match.group(1)

    return result


def get_parser(regions=None, *args, **kwargs):
    """Returns an ArgumentParser preconfigured with global options."""
    parser = argparse.ArgumentParser(*args, **kwargs)
    parser.add_argument('-v', '--verbose', action='store_true', help='Output debugging information')
    parser.add_argument('-k', '--credentials-file',
        metavar='FILE',
        dest='credentials_file',
        type=argparse.FileType('r'),
        default=os.environ.get('AWS_CREDENTIALS_FILE', '/etc/aws-credentials.txt'),
        help='Path to your AWS credentials file (default: /etc/aws-credentials.txt)'
    )
    
    return parser

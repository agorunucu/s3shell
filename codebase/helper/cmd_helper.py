import argparse
import sys
import boto3
import global_vars


def parse():
    # Instantiate the parser
    parser = argparse.ArgumentParser(description='Command line for AWS S3')

    parser.add_argument('-a', '--access-key-id', type=str, help='Access key id of your account.')
    parser.add_argument('-s', '--secret-access-key', type=str, help='Secret access key of your account.')
    parser.add_argument('-r', '--region', type=str, help='Secret access key of your account.')
    parser.add_argument('-p', '--profile', type=str, help='The profile name you used in aws configure.')
    return parser, parser.parse_args()


def init_s3cli(parser, args):
    if ((args.access_key_id is None and args.secret_access_key is not None) or
        (args.access_key_id is not None and args.secret_access_key is None)) and \
            args.profile is None:
        print("You must set both access-key-id and secret-access-key!", file=sys.stderr)
        parser.print_help(sys.stderr)
        sys.exit(-1)

    if args.access_key_id is not None and args.profile is None and args.region is None:
        print("You must set region!", file=sys.stderr)
        parser.print_help(sys.stderr)
        sys.exit(-1)

    if (args.access_key_id is not None or args.secret_access_key is not None) and args.profile is not None:
        print("You must use only profile or (access-key-id and secret-access-key)!", file=sys.stderr)
        parser.print_help(sys.stderr)
        sys.exit(-1)

    if args.profile is not None:
        global_vars.current_profile = args.profile
        return __generate_boto3_with_profile(args.profile)
    elif args.access_key_id is not None or args.secret_access_key is not None:
        return __generate_boto3_with_keys(args.access_key_id, args.secret_access_key, args.region)
    # If none entered, then use default profile
    else:
        global_vars.current_profile = "default"
        return __generate_boto3_with_profile("default")


def __generate_boto3_with_profile(profile_name):
    session = boto3.Session(profile_name=profile_name)
    return session.client('s3')


def __generate_boto3_with_keys(access_key_id, secret_access_key, region):
    return boto3.client('s3',
                        aws_access_key_id=access_key_id,
                        aws_secret_access_key=secret_access_key,
                        region_name=region)

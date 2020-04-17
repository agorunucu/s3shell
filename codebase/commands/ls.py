import global_vars
from botocore.exceptions import ClientError


def dispatch(params):
    try:
        if global_vars.current_bucket is None:
            __list_buckets()
        else:
            __list_objects()
    except ClientError as ce:
        if "Access Denied" in str(ce):
            print("You dont have permission to list current path.  Run 'pwd' to find out where you are.")
        else:
            print(ce)


def __list_buckets():
    s3cli = global_vars.s3cli
    buckets = s3cli.list_buckets()
    bucket_count = len(buckets["Buckets"])
    print(f"total {bucket_count}")

    if bucket_count > 0:
        owner = buckets["Owner"]["DisplayName"]
        for bucket in buckets["Buckets"]:
            print(f"d  {owner}  {bucket['CreationDate']}  {bucket['Name']}")


def __list_objects():
    s3cli = global_vars.s3cli
    current_bucket = global_vars.current_bucket
    current_dir = global_vars.current_dir
    max_keys = 50  # TODO implement ENV
    current_min = 1

    if current_dir is None:
        list_response = s3cli.list_objects_v2(
            Bucket=current_bucket,
            MaxKeys=max_keys,
            Delimiter="/"
        )
    else:
        list_response = s3cli.list_objects_v2(
            Bucket=current_bucket,
            MaxKeys=max_keys,
            Prefix=current_dir + "/",
            Delimiter="/"
        )

    is_truncated = list_response['IsTruncated']
    key_count = list_response['KeyCount']

    if bool(is_truncated):
        print(f"total ?, showing {key_count}, range {current_min} - {current_min + key_count -1}")
    else:
        print(f"total {key_count}")

    if key_count == 0:
        return

    if 'Contents' in list_response:
        # These fields occurs in Contents field. It the field doesn't exists, then use default values.
        max_length_of_size_str = __get_max_length_of_str(list_response['Contents'], 'Size')
        max_length_of_owner_str = __get_max_length_of_str(list_response['Contents'], 'Owner', 'DisplayName',
                                                          default_min=len('unknown'))
        max_length_of_storage_str = __get_max_length_of_str(list_response['Contents'], 'StorageClass',
                                                            default_min=len("none"))
    else:
        max_length_of_size_str = 0
        max_length_of_owner_str = len('unknown')
        max_length_of_storage_str = len("none")

    if 'CommonPrefixes' in list_response:
        for common_prefix in list_response['CommonPrefixes']:
            if current_dir is None:
                object_name = common_prefix['Prefix']
            else:
                object_name = str(common_prefix['Prefix']).replace(current_dir+'/', '')

            if object_name.endswith('/'):
                object_name = object_name[:-1]

            # In some cases, users manually create a virtual dir.
            # So that, these dirs shown as object here.
            # To avoid list them within same dir, the following condition is used.
            if len(object_name) == 0:
                continue

            print("p "  # p for prefix
                  f"{'unknown'.rjust(max_length_of_owner_str, ' ')} "
                  f"{'none'.rjust(max_length_of_storage_str, ' ')}  "
                  f"{''.rjust(max_length_of_size_str, ' ')}  "
                  f"{''.rjust(25, ' ')}  "  # ex: 2016-07-02 01:25:16+00:00, 25 chars :)
                  f"{object_name}")

    if 'Contents' in list_response:
        for current_object in list_response['Contents']:
            if str(current_object['Key']).endswith('/'):
                object_type = 'd'
            else:
                object_type = 'o'

            if 'Owner' in current_object:
                owner = current_object['Owner']['DisplayName']
            else:
                owner = "unknown"

            # Remove current dir prefix from keys
            if current_dir is None:
                object_name = current_object['Key']
            else:
                object_name = str(current_object['Key']).replace(current_dir + '/', '')

            # In some cases, users manually create a virtual dir.
            # So that, these dirs shown as object here.
            # To avoid list them within same dir, the following condition is used.
            if len(object_name) == 0:
                continue

            print(f"{object_type} "
                  f"{owner.rjust(max_length_of_owner_str, ' ')} "
                  f"{str(current_object['StorageClass']).lower().rjust(max_length_of_storage_str, ' ')}  "
                  f"{str(current_object['Size']).rjust(max_length_of_size_str, ' ')}  "
                  f"{current_object['LastModified']}  "
                  f"{object_name}")


def __get_max_length_of_str(obj_array, key, second_key=None, default_min=0):
    min_val = default_min
    for obj in obj_array:
        if second_key is None:
            if key in obj:
                if len(str(obj[key])) > min_val:
                    min_val = len(str(obj[key]))
        else:
            if key in obj and second_key in obj[key]:
                if len(str(obj[key][second_key])) > min_val:
                    min_val = len(str(obj[key][second_key]))
    return min_val


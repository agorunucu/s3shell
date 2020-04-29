import global_vars

from botocore.exceptions import ClientError
from helper.path_helper import get_absolute_path, check_if_path_exists, calculate_relativity, \
    get_bucket_key_from_absolute_path


def dispatch(params):
    if not check_input(params):
        return

    stripped_path = str(params[0]).strip()

    if not stripped_path.startswith("/"):
        absolute_path = get_absolute_path(stripped_path)
    else:
        absolute_path = stripped_path

    calculated_absolute_path = calculate_relativity(absolute_path)
    bucket_name, object_key = get_bucket_key_from_absolute_path(calculated_absolute_path)

    # Check whether the full path exists or not
    is_exists, maybe_exception = check_if_path_exists(bucket_name, key=object_key)
    if is_exists:
        print(f"Directory is already exists. Dir: [{calculated_absolute_path}]")
        return None
    elif maybe_exception is not None and "access denied" in str(maybe_exception).lower():
        print(f"You dont have permission to access the path: [s3://{bucket_name}/{object_key}]")
        print(f"Exception: {str(maybe_exception)}")
        return None

    # If it comes here, then it means there is no path as entered, and user has access permission

    # If the bucket is successfully created at the command, but object key is not;
    # then we should rollback the bucket creation.
    # So, we should keep the state of bucket whether it created here or already exists
    is_bucket_created_now = False

    # Check whether the bucket exists
    is_bucket_exists, maybe_exception = check_if_path_exists(bucket_name)
    if is_bucket_exists is False and maybe_exception is not None and "not found" not in str(maybe_exception).lower():
        if "Access Denied" in str(maybe_exception):
            print(f"You dont have ListBucket permission for the bucket [s3://{bucket_name}]")
        print(f"Exception: {str(maybe_exception)}")
        return None
    elif is_bucket_exists is False:
        # Try to create bucket. If error occurs, then terminate the process.
        is_bucket_created, maybe_exception = __create_bucket(bucket_name)
        if not is_bucket_created:
            if "Access Denied" in str(maybe_exception):
                print(f"You dont have CreateBucket permission for the bucket [s3://{bucket_name}]")
            print(f"Exception: {str(maybe_exception)}")
            return None
        else:
            is_bucket_created_now = True

    # If it comes here, it means there is a bucket now.
    # Now we can check whether object creation is requested.
    if object_key is not None:
        is_object_created, maybe_exception = __create_dir(bucket_name, object_key)
        if not is_object_created:
            # An error occurred in object creation.
            if "Access Denied" in str(maybe_exception):
                print(f"You dont have PutObject permission on the bucket [s3://{bucket_name}]")
            print(f"Failed. Exception: {str(maybe_exception)}")
            # If the bucket also created here, we should now delete it.
            if is_bucket_created_now:
                is_bucket_deleted, maybe_exception = __delete_bucket(bucket_name)
                if not is_bucket_deleted:
                    # We needed to delete the bucket as rollback operation
                    # But it seems that we don't have DeleteBucket permission on the bucket
                    print("Rollback failed.")
                    print(f"The bucket [{bucket_name}] has been created at the beginning of the creation.")
                    print("But while object creation, an error happened. To make them as before,")
                    print("we tried to delete newly created bucket.")
                    print("It seems that the deletion process also encountered another exception:")
                    print(str(maybe_exception))
                    print("SUGGESTION: You can try to delete the bucket if you need to.")
                    print("SUGGESTION: You can check the permissions for S3 access.")


def check_input(params):
    if len(params) == 0:
        print(f"'mkdir' command takes at least one parameter.")
        return False
    return True


def __create_bucket(bucket_name):
    s3cli = global_vars.s3cli
    try:
        s3cli.create_bucket(Bucket=bucket_name,
                            CreateBucketConfiguration={
                                'LocationConstraint': global_vars.region
                            })
        return True, None
    except ClientError as ce:
        return False, ce


def __create_dir(bucket_name, object_key):
    if str(object_key).endswith('/'):
        temp_key = object_key
    else:
        temp_key = object_key + '/'

    s3cli = global_vars.s3cli
    try:
        s3cli.put_object(Bucket=bucket_name, Key=temp_key)
        return True, None
    except ClientError as ce:
        return False, ce


def __delete_bucket(bucket_name):
    s3cli = global_vars.s3cli
    try:
        s3cli.delete_bucket(Bucket=bucket_name)
        return True, None
    except ClientError as ce:
        return False, ce

# Shell for AWS S3
s3shell aims to create a simulated file system that uses s3 as the source. The commands used are similar to *nix terminal commands as far as possible.

### Currently supported commands
* [cd](#cd)
* [ls](#ls)
* [pwd](#pwd) 
* [printenv](#printenv)

### Future commands
* su
* stats
* mkdir
* cat
* set
* cp
* mv
* rm
* echo 
* history 

### How it works
The s3shell assumes buckets as directories under root `/`. The inner directories are keys of an object. When you execute a command, it makes boto3 calls to retrieve data and parse the result to show you in the view of the actual shell. You will be able to track your request counts by `stats` command at the future versions.   

For example, you have to buckets `test-bucket-1` and `test-bucket-2` and a file under `test-bucket-2` as the key `logs/latest/log1.csv`, the file structure is as follows;
```commandline
/test-bucket-1
/test-bucket-2/logs/latest/log1.csv
```
It also has environment variables by its own. You can print them out with [printenv](#printenv) command. It gets values from `codebase/environment/{profile}.yaml` file. You can add new ones by adding the file and restarting the shell. 
### How to run

1. Install the required libraries if not exists. These libraries could be found in [requirements](requirements.txt) file.
2. Run as `python3 s3shell` (You need to enter valid credentials here. See [Credentials](#credentials--security) section.)

### Credentials / Security
You need to enter aws access key id and aws security access key to use the shell. These values are not stored anywhere and only used in the session. There are two ways to enter values;
* Using `profile`. You can pass your aws cli profile names with `--profile` command. The shell will read credentials from `~/.aws` path. This is the recommended option. Example: `python3 s3shell --profile mytestawsprofile`
* Using `access-key-id` and `secret-access-key`. You can pass values directly. You need to enter `region` for this usage. This command could be visible in the `history` and cause expansion. Example: `python3 s3shell --access-key-id {your-access-key-id} --secret-access-key {your-secret-access-key} --region eu-west-1` 
### Commands and how to use them
#### cd
Changes directory. Works both absolute and relative paths. If you try to go non-exists or not-permitted dir, you get an error. Usage;
```commandline
> cd testdir
> cd /testrootdir/testdir
> cd test_dir/testdir2/../testdir3
> cd ..
> cd  # Goes root '/'
```

### ls
Lists current directory. If the current path is root `/`, lists buckets. Usage;
```commandline
> ls
```

### pwd
Shows current dir in both shell type and s3 type. Usage;
```commandline
> pwd
/bucket1/dir1
s3://bucket1/dir1
```

### printenv
Prints the current environment variables. Usage;
```commandline
> printenv
envvar1=value1
envvar2=value2
```
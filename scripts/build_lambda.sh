#!/bin/bash
lambda_name=classcharts_lambda

root_dir=`pwd`
build_dir=build/$lambda_name
dist_zip=$root_dir/dist/$lambda_name.zip

# Clean up
rm $dist_zip
rm -rf $build_dir

mkdir -p $build_dir/package

# Supporting packages
virtualenv $build_dir/env -p python3
source $build_dir/env/bin/activate
python setup.py install
deactivate

# TODO: Perhaps this copy can be avoided?
cp classcharts_trello_sync/__main__.py $build_dir/package/lambda.py
cp -r $build_dir/env/lib/python3.6/site-packages/* $build_dir/package

cd $build_dir/package
zip -r $dist_zip *

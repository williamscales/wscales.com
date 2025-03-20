#!/bin/bash
aws s3 sync ./build "s3://$1" --delete
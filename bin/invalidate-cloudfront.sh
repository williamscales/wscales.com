#!/bin/bash

aws cloudfront \
    create-invalidation \
    --distribution-id "$1" \
    --paths '/*'
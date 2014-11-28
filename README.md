wscales.com
===========

This is the source code for https://wscales.com/.

Dependencies
------------
Webapp dependencies are:
* Django 1.7.1 or newer
* Python 3.4 or newer

Ansible playbooks to build the Docker images and coordinate servers require the
following:
* Ansible 1.7.2 or newer
* Docker 1.3.1 or newer

Grunt
-----
To compile the custom bootstrap less files into css, you must install `grunt`
and its dependencies. To do so, run the following (in the project root):

```
$ npm install
```

which will pull in the dependencies. Then you can do something like

```
$ node_modules/grunt/bin/grunt.js bootstrap:compileLess
```

which will put the resulting css, js, and font files for bootstrap in
`wscales_com/zzw_theme_vertical/static/bootstrap/dist`. You can also run

```
$ node_modules/grunt/bin/grunt.js watch
```

to recompile the less files whenever any file in the directory
`wscales_com/zzw_theme_vertical/less` changes.

Ansible
-------
This project uses Ansible to build docker images and ...

## `images.yml`
Provides the `image_builder`

## `site.yml`
